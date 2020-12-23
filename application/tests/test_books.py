import unittest
from models.books import Books
from tests.test_app import TestApp


class TestBooks(unittest.TestCase):

    def test_create_book(self):
        with TestApp() as testApp:
            Books.create_book('title', ['author'], '2020', '1234567890123', '123', 'thumbnail', 'en')
            self.assertEqual(len(Books.objects()), 1)

    def test_update_book(self):
        with TestApp() as testApp:
            Books.create_book('title', ['author'], '2020', '1234567890124', '123', 'thumbnail', 'en')
            book = Books.objects().first()
            Books.update_book(book, title='newTitle')
            self.assertEqual(len(Books.objects(title='newTitle')), 1)
            self.assertEqual(len(Books.objects(title='title')), 0)
