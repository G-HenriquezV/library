"""
Manages Library and Book classes
"""
import json
from datetime import datetime, timedelta
from typing import Optional, Any, List
from uuid import uuid4


class Book:
    """
    Stores data and manages books
    """

    def __init__(self, title: str, author: str, bid: str = None, **kwargs: Any):
        """
        Initializes a book.

        :param title: Title of the book
        :param author: Author of the book
        :param bid: Optional. Unique book identifier, uses uuid4() if not set.
        :param kwargs: Additional optional book data like year, edition, isbn, etc.
        Can also be used CAREFULLY to set is_lent, current_user and return_date
        """
        self.title = title
        self.author = author
        self.bid = bid if bid is not None else str(uuid4())
        self.is_lent = False
        self.current_user = None  # String
        self.return_date = None  # Datetime object or None
        self.__dict__.update(kwargs)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def __repr__(self):
        return f"Book(<'{self.title}', '{self.author}', '{self.bid}'>)"

    # Should I really be using a static method?
    @staticmethod
    def from_dict(book_dict: dict, bid: str = None) -> 'Book':
        """
        Creates a Book type object using a dictionary

        :type book_dict: dict
        :param book_dict: Dictionary including all book data. 'title' and 'author' are required keys.
        :param bid: Optional. Book unique ID.
        :return: Book type object with the dictionary data on it
        """
        _book = Book(book_dict['title'], book_dict['author'], bid)
        for key, value in book_dict.items():
            if key in ['title', 'author']:
                continue
            if key == 'return_date':
                try:
                    _book.return_date = datetime.strptime(value, '%Y%m%d')
                except TypeError:  # Raised if there is no return date
                    _book.return_date = None
                continue
            _book.__dict__.update({key: value})
        return _book

    @property
    def days_until_return(self) -> Optional[timedelta]:
        """
        :return: Days until the expected return
        """
        if self.is_lent:
            return self.return_date - datetime.today()
        return None

    def to_dict(self) -> dict:
        """
        Returns a new dictionary object with all attributes, return_date as a string and no BID.
        Useful to save on a json file

        :return: Dictionary with attributes of the book class
        """
        book_dict = {}
        for key, value in self.__dict__.items():
            if key == 'bid':
                continue
            if key == 'return_date':
                try:
                    return_date = value.strftime('%Y%m%d')
                except AttributeError:  # When the return date is None you get an AttributeError
                    return_date = None
                book_dict.update({key: return_date})
                continue
            book_dict.update({key: value})
        return book_dict


class Library:
    """
    Manages every book inside the library
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.books = {}

    # Using a context manager might be overkill
    # However, could be used to create and restore a backup copy if any exception raises
    def __enter__(self):
        self.load()
        return self

    def __exit__(self, *args):
        self.save()

    def load(self) -> None:
        """
        Loads the library from the json file defined in the constructor (self.filename)
        """
        with open(self.filename, 'r', encoding='utf-8') as f:
            _books = json.load(f)
        for bid, book in _books.items():
            self.books.update({bid: Book.from_dict(book, bid)})

    def save(self) -> None:
        """
        Saves the library to the json file defined in the constructor (self.filename)
        """
        dict_to_save = {}
        for bid, book in self.books.items():
            dict_to_save.update({bid: book.to_dict()})
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(dict_to_save, f, ensure_ascii=False, indent=2)

    def search_title(self, search_string: str) -> List[Book]:
        """
        Searchs for a title in the book library

        :param search_string: Title to search
        :return: List of books with all the results. Empty list if there are no results.
        """
        search_string = search_string.lower()
        return [book for book in self.books.values() if search_string in book.title.lower()]

    def add_book(self, book: Book) -> None:
        """
        Adds a book to the library if it doesn't already exist

        :param book: Book-type object to add
        """
        if book in self.books.values():
            raise KeyError('Book already registered in the library')
        self.books.update({book.bid: book})

    def delete_book(self, book: Book, no_warn: bool = False) -> None:
        """
        Deletes book from the library.

        :param book: Book to delete
        :param no_warn: If KeyError exception should be raised if the book doesn't exist
        """
        if book not in self.books.values() and not no_warn:
            raise KeyError('Book is not registered in the library')
        self.books.pop(book.bid)

    def lend_book(self, book: Book, return_date: datetime, person: str) -> None:
        """
        Lends a book to a person

        :param book: Book to lend, must be in the library
        :param return_date: Expected return date
        :param person: Name of the person
        """
        if book not in self.books.values() or book.is_lent:
            raise KeyError('Book not lent or not registered in the library')
        book.is_lent = True
        book.return_date = return_date
        book.current_user = person

    def return_book(self, book: Book) -> None:
        """
        Sets the book as returned.

        :param book: Book to flag as returned
        """
        if book not in self.books.values() or not book.is_lent:
            raise KeyError('Book available to lent or not registered in the library')
        book.is_lent = False
        book.current_user = None
        book.return_date = None

    def print_all_books(self) -> None:
        """
        Prints every book in the library and its current status.
        """
        print(f'{"Book title":70} {"Author(s)":60} {"Availability":38}')
        print('-' * 168)
        for book in self.books.values():
            if book.is_lent:
                print(f'{book.title:70} {book.author:60} Returns on {book.return_date.strftime("%A %B %d %Y"):38}')
            else:
                print(f'{book.title:70} {book.author:60} {"Available":38}')

    def print_book_bid(self) -> None:
        """
        Prints every book BID
        """
        print(f'{"Book title":80} {"bid":38}')
        print('-' * 117)
        for book in self.books.values():
            print(f'{book.title:80} {book.bid:36}')
