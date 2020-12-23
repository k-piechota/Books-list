import unittest
from models.books import Books
from tests.test_app import TestApp
from views import results


class TestResults(unittest.TestCase):

    def createSomeBooks(self):
        Books.create_book('title', ['author'], '2020', '1234567890123', '123', 'thumbnail', 'en')
        Books.create_book('title1', ['author1'], '2019', '1234567890124', '123', 'thumbnail', 'pl')
        Books.create_book('title2', ['author2'], '2018', '1234567890125', '123', 'thumbnail', 'es')

    def test_empty_filters(self):
        with TestApp():
            self.createSomeBooks()
            self.assertEqual(len(results.get_books({})), 3)

    def test_title_contains(self):
        with TestApp():
            self.createSomeBooks()
            self.assertEqual(len(results.get_books({'title': 'title'})), 3)
            self.assertEqual(len(results.get_books({'title': 'title2'})), 1)

    def test_authors_contains(self):
        with TestApp():
            self.createSomeBooks()
            self.assertEqual(len(results.get_books({'author': 'author'})), 3)
            self.assertEqual(len(results.get_books({'author': 'author2'})), 1)

    def test_filter_by_date_published(self):
        with TestApp():
            self.createSomeBooks()
            self.assertEqual(len(results.get_books({'from': '2019'})), 2)
            self.assertEqual(len(results.get_books({'from': '2019', 'to': '2019'})), 1)

    def test_filter_by_language(self):
        with TestApp():
            self.createSomeBooks()
            self.assertEqual(len(results.get_books({'language': 'en'})), 1)
