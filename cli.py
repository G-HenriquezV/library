"""
Manages the command line interface
"""

import json
import os
from datetime import datetime
from typing import Optional

import click

from library import Library, Book


# noinspection PyMissingOrEmptyDocstring
@click.group()
def cli(): pass


def get_workinglib() -> Optional[str]:
    """
    Gets the current json books file, set in workinglibrary file.

    :return: The name of the current json file in use
    """
    try:
        with open('workinglibrary', 'r') as f:
            working_lib = f.read()
        return working_lib
    except FileNotFoundError:
        print('workinglibrary file not found')


@cli.command()
@click.argument('new_lib')
def change_workinglib(new_lib: str) -> None:
    """
    Changes the current working library file

    \b
    :param new_lib: New library json file to use
    """
    if not os.path.exists(new_lib):
        print(f'{new_lib} does not exist, creating empty json file')
        with open(new_lib, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=2)
    with open('workinglibrary', 'w') as f:
        f.write(new_lib)
        print(f'Working library has been changed to {new_lib}')


@cli.command()
@click.argument('book_name')
@click.argument('person')
@click.argument('return_date')
def lend_book(book_name: str, person: str, return_date: str) -> None:
    """
    Lends the fist book that matches given name to a person until a set date

    \b
    :param book_name: Book name to search
    :param person: Name of the person to lend the book
    :param return_date: Return date in YYYYMMDD format
    """
    try:
        return_date = datetime.strptime(return_date, '%Y%m%d')
    except ValueError:
        print('Error: Invalid date string. Use YYYYMMDD format.')
        exit()
    with Library(get_workinglib()) as library:
        book_name_search = library.search_title(book_name)
        if len(book_name_search) == 0:
            print('Book name not found!')
            exit()
        book = book_name_search[0]
        try:
            library.lend_book(book, return_date, person)
            print(f'{book} has been lent to {person.title()} until {return_date.strftime("%A %B %d %Y")}')
        except KeyError:
            print('Error: Book already lent')


@cli.command()
@click.argument('book_name')
def return_book(book_name: str) -> None:
    """
    Returns to the library the first book that matches book_name

    \b
    :param book_name: Name string of the book
    """
    with Library(get_workinglib()) as library:
        book_name_search = library.search_title(book_name)
        if len(book_name_search) == 0:
            print('Error: Book name not found!')
            exit()
        book = book_name_search[0]
        try:
            library.return_book(book)
            print(f'{book} has been returned')
        except KeyError:
            print(f'Error: {book} has not been lent')


@cli.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('title')
@click.argument('author')
@click.pass_context
def add_book(ctx, title, author):
    """
    Adds a book to the library. Additional arguments can be added as an option
    \b
    Example: add-book "Fahrenheit 491" "Ray Bradbury" --year 1953

    \b
    :param title: Title of the book
    :param author: Author of the book
    :param ctx: Context of the click command line
    """
    kwargs = {ctx.args[i][2:]: ctx.args[i+1] for i in range(0, len(ctx.args), 2)}
    _book = Book(title, author, **kwargs)
    with Library(get_workinglib()) as library:
        library.add_book(_book)
        print(f'{_book} has been added to the library with {_book.bid} as bid')


@cli.command()
@click.argument('book_name')
def delete_book(book_name: str) -> None:
    """
    Removes the first book that matches the book_name string from the library

    \b
    :param book_name: Name string of the book
    """
    with Library(get_workinglib()) as library:
        book_name_search = library.search_title(book_name)
        if len(book_name_search) == 0:
            print('Error: Book name not found!')
            exit()
        _book = book_name_search[0]
        library.delete_book(_book)
        print(f'{_book} has been removed from the library')


@cli.command()
def print_books() -> None:
    """
    Prints all the books in the current library
    """
    with Library(get_workinglib()) as library:
        library.print_all_books()


@cli.command()
def show_workinglib() -> None:
    """
    Prints the current working library file name
    """
    print(get_workinglib())


if __name__ == '__main__':
    cli()