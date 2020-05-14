"""
Book class definition
"""
from datetime import timedelta, datetime


class Book:
    """
    Book class to manage them. Uses the Shelf class to manage records.
    """

    def __init__(self, book_dict: dict, bid: str, shelf):
        """
        Initializes a book instance.

        :param book_dict: Dictionary including all the book data.
        :param shelf: Shelf where the book is located
        :param bid: Book ID
        """
        self.shelf = shelf
        self.bid = bid
        self.title = book_dict["title"]
        self.authors = book_dict["authors"]
        self.language = book_dict["language"]
        self.isbn10 = book_dict["isbn10"]
        self.isbn13 = book_dict["isbn13"]
        self.is_lent = book_dict["is_lent"]
        self.current_user = book_dict["current_user"]
        try:
            self.return_date = datetime.strptime(book_dict["return_date"], '%Y%m%d')
        except TypeError:
            self.return_date = None

    def __str__(self):
        return f'{self.title} by {self.authors}'

    def __repr__(self):
        return self.title

    @property
    def days_until_return(self) -> timedelta:
        """
        :return: Days until the expected return
        """
        if self.is_lent:
            return self.return_date - datetime.today()
        raise Exception('Book is currently on the shelf!')  # TODO: Check exception type

    def lend(self, person_to_lend: str, lent_until: datetime):
        """
        Registers the book as lent to a person

        :param person_to_lend: Name of the person who currently has the book
        :param lent_until: Expected return date
        """
        if self.is_lent is False:
            self.is_lent = True
            self.current_user = person_to_lend
            self.return_date = lent_until
            self.shelf.update_records(self.bid)
        else:
            raise Exception('Book not available!')

    def set_returned(self) -> None:
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

    def change_return_date(self, new_date: datetime) -> None:
        """
        Changes de return date of the book

        :param new_date:
        """
        # TODO
        raise NotImplementedError
