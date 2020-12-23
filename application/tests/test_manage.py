import unittest
from tests.test_app import TestApp
from models.books import Books


def post_add_book(client, title, author, date_published, isbn, page_count, thumbnail, language):
    return client.post('/add', follow_redirects=True, data={
        'title': title, 'author': author, 'publishedDate': date_published, 'isbn': isbn, 'pageCount': page_count,
        'thumbnail': thumbnail, 'language': language
    })


class TestManage(unittest.TestCase):

    def test_validation_form(self):
        with TestApp() as testApp:
            response = post_add_book(testApp.app, '', '', '', '', '', '', '')
            self.assertIn('Podaj tytuł'.encode('utf-8'), response.data)
            self.assertIn('Podaj prawidłowy rok publikacji'.encode('utf-8'), response.data)
            self.assertIn('Podaj poprawny numer ISBN 13'.encode('utf-8'), response.data)
            self.assertIn('Podaj prawidłowa liczbę stron'.encode('utf-8'), response.data)
            self.assertIn('Podaj prawidłowy adres URL'.encode('utf-8'), response.data)
            self.assertIn('Podaj poprawny numer ISBN 13'.encode('utf-8'), response.data)
            self.assertIn('Podaj prawidłowy język za pomocą kodu ISO 639-1'.encode('utf-8'), response.data)

    def test_adding_book(self):
        with TestApp() as testApp:
            post_add_book(testApp.app, 'title', 'author', '2020', '1234567890123', '123', 'https://facebook.com/', 'pl')
            self.assertEqual(len(Books.objects()), 1)

    def test_deleting_book(self):
        with TestApp() as testApp:
            isbn = '1234567890123'
            post_add_book(testApp.app, 'title', 'author', '2020', isbn, '123', 'https://facebook.com/', 'pl')
            self.assertEqual(len(Books.objects()), 1)
            testApp.app.post('/delete?isbn=' + isbn)
            self.assertEqual(len(Books.objects()), 0)

    def test_adding_by_keywords(self):
        with TestApp() as testApp:
            keyword = 'keyword'
            testApp.app.post('/addByKeywords', data={
                'keyword': keyword,
                'title': '',
                'author': '',
                'subject': '',
                'publisher': '',
                'isbn': '',
                'lccn': '',
                'oclc': '',
            })
            self.assertTrue(len(Books.objects()) > 0)



