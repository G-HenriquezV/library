"""
Manages all the books using the Library class
"""
from typing import List
from datetime import datetime, timedelta
import json
from uuid import uuid1


"""
1. Make the changes the I've hinted at
2. Refactor as needed
    Changing class order
    More type hints
3. Add CLI using click
    Add a book to the library
    Delete a book from the library
    Lend a book
    Get a book returned
    Print list of book and the return date if lent out
"""



class Library:
    """
    Manages every book in the collection
    """

    def __init__(self, filename):
        """
        Initalizes a shelf using a file with the records

        :param filename:  file with the book records
        """
        self.filename = filename
        self.books = {} # key is id, value is book

    def print_books(self):
        """
        Prints every book title in the shelf
        """
        for _book in self.book_list:
            print(_book.title, 'Available:', not book.is_lent)

    def import_books(self) -> List['Book']:
        """
        Reads the dict and creates a list with all the books
        """
        book_list = []
        for key in self.records:
            book_list.append(Book(**self.records[key], key, self))
        return book_list

    def update_records(self, bid) -> None:
        """
        Rewrites the json file with the updated records
        """
        _book = self.get_book_with_bid(bid)
        self.records[bid]['is_lent'] = _book.is_lent
        self.records[bid]['current_user'] = _book.current_user
        try:
            self.records[bid]['return_date'] = _book.return_date.strftime('%Y%m%d')
        except AttributeError:  # When the return date is None you get an AttributeError
            self.records[bid]['return_date'] = None
        self._write_file()

    def book_search(self, search_string: str) -> List[Book]:
        """
        Looks for a book with a matching title

        :param search_string: Book title to search
        """
        search_string = search_string.lower()
        return [book for book in self.books.values() if search_string in book.title.lower()]

    # Change to public load and save methods
    def _read_file(self) -> dict:
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_file(self) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    def __getitem__(self, item):
        return self.books[item]

    def get_book_with_bid(self, bid) -> Book:
        """
        Returns the book element with given bid

        :param bid:
        :return: Book with bid
        """

        return self.books[bid]


# command_line()
if __name__ == '__main__':
    shelf = Library('books.json')
    date_example = datetime(2020, 5, 16)
    book = shelf.get_book_with_bid("b1")
    # book.lend('Katie', date_example)
    book.set_returned()
    print(book.return_date)


class Book:
    """
    Book class to manage them. Uses the Library class to manage records.
    """

    def __init__(
            self,
            title,
            author,
            bid=None,
            is_lent=False,
            current_user=None,
            return_date=None,
    ):
        """
        Initializes a book instance.

        :param book_dict: Dictionary including all the book data.
        :param shelf: Library where the book is located
        :param bid: Book ID
        """
        self.title = title
        self.author = author # make a string

        self.bid = bid if self.bid is not None else uuid1()
        self.is_lent = book_dict["is_lent"]
        self.current_user = book_dict["current_user"]
        try:
            self.return_date = datetime.strptime(book_dict["return_date"], '%Y%m%d')
        except TypeError:
            self.return_date = None

    def __str__(self):
        return f'{self.title} by {self.authors}'

    def __repr__(self):
        return f'Book(<{self.title}>)'

    # Return none instead of except
    @property
    def days_until_return(self) -> timedelta:
        """
        :return: Days until the expected return
        """
        if self.is_lent:
            return self.return_date - datetime.today()
        raise Exception('Book is currently on the shelf!')  # TODO: Check exception type

    # Move to library
    def lend(self, person_to_lend: str, lent_until: datetime):
        """
        Registers the book as lent to a person

        :param person_to_lend: Name of the person who currently has the book
        :param lent_until: Expected return date
        """
        if self.is_lent:
            raise Exception('Book not available!')
        self.is_lent = True
        self.current_user = person_to_lend
        self.return_date = lent_until
        self.shelf.update_records(self.bid)

    # Move to library
    def return_(self) -> None:
        """
        Registers the book as returned
        """
        if self.is_lent:
            self.is_lent = False
            self.current_user = None
            self.return_date = None
            self.shelf.update_records(self.bid)
        else:
            raise Exception('Book is currently on the shelf!')
