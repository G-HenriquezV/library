"""
Manages all the books using the Shelf class
"""
from book import Book
from typing import List
from datetime import datetime
import json


class Shelf:
    """
    Manages every book in the collection
    """

    def __init__(self, filename):
        """
        Initalizes a shelf using a file with the records

        :param filename:  file with the book records
        """
        self.filename = filename
        self.records = self._read_file()
        self.book_list = self.import_books()

    def print_books(self):
        """
        Prints every book title in the shelf
        """
        for _book in self.book_list:
            print(_book.title, 'Available:', not book.is_lent)

    def import_books(self) -> List[Book]:
        """
        Reads the dict and creates a list with all the books
        """
        book_list = []
        for key in self.records:
            book_list.append(Book(self.records[key], key, self))
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
        book_list = []
        for _book in self.book_list:
            if search_string.lower() in _book.title.lower():
                book_list.append(_book)
        return book_list

    def first_search_result(self, search_string: str) -> Book:
        """
        Returns the first book with the string on its name

        :param search_string: Book title to search
        :return:
        """
        return self.book_search(search_string)[0]

    def _read_file(self) -> dict:
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_file(self) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    def get_book_with_bid(self, bid) -> Book:
        """
        Returns the book element with given bid

        :param bid:
        :return: Book with bid
        """
        for _book in self.book_list:
            if _book.bid == bid:
                return _book


if __name__ == '__main__':
    shelf = Shelf('books.json')
    date_example = datetime(2020, 5, 16)
    book = shelf.get_book_with_bid("b1")
    # book.lend('Katie', date_example)
    book.set_returned()
    print(book.return_date)
