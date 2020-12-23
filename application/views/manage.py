from flask import render_template, Blueprint, request, redirect
from models.books import Books
import requests
from urllib.parse import quote
from wtforms import Form, StringField, validators

manage = Blueprint('manage', __name__, template_folder='templates')


class AddFromApiForm(Form):
    keyword = StringField('Słowo kluczowe', [validators.DataRequired(message='Podaj słowo kluczowe')])
    title = StringField('Tytuł')
    author = StringField('Autor')
    subject = StringField('Kategoria')
    publisher = StringField('Wydawnictwo')
    isbn = StringField('ISBN')
    lccn = StringField('LCCN')
    oclc = StringField('OCLC')


class AddManual(Form):
    title = StringField('Tytuł', [validators.DataRequired(message='Podaj tytuł')])
    author = StringField('Autor')
    publishedDate = StringField('Data publikacji',
                                [validators.Regexp(r'^\d{4}$', message='Podaj prawidłowy rok publikacji')])
    isbn = StringField('ISBN 13', [validators.Regexp(r'^\d{13}$', message='Podaj poprawny numer ISBN 13')])
    pageCount = StringField('Liczba stron', [validators.Regexp(r'^(\d+)$', message='Podaj prawidłowa liczbę stron')])
    thumbnail = StringField('Okładka', [validators.URL(message='Podaj prawidłowy adres URL')])
    language = StringField('Język publikacji',
                           [validators.Regexp('^[a-z]{2}$', message='Podaj prawidłowy język za pomocą kodu ISO 639-1')])


@manage.route('/add', methods=['GET', 'POST'])
def add_book():
    form = AddManual(request.form)
    if request.method == 'POST' and form.validate():
        Books.create_book(request.form['title'], request.form['author'].split(', '), request.form['publishedDate'],
                          request.form['isbn'], request.form['pageCount'], request.form['thumbnail'],
                          request.form['language'])
        return redirect('/')
    return render_template('manage.html', form=form)


@manage.route('/edit', methods=['GET', 'POST'])
def edit_book():
    form = AddManual(request.form)
    if request.method == 'POST':
        if form.validate():
            book = Books.get_books_by_isbn(request.args['isbn'])
            Books.update_book(book, request.form['title'], request.form['author'].split(', '),
                              request.form['publishedDate'],
                              request.form['pageCount'], request.form['thumbnail'], request.form['language'])
            return redirect('/')
    else:
        book = Books.get_books_by_isbn(request.args['isbn'])
        form.title.data = book.title
        form.author.data = ', '.join(book.authors)
        form.isbn.data = book.isbn
        form.publishedDate.data = book.publishedDate
        form.pageCount.data = book.pageCount
        form.thumbnail.data = book.thumbnail
        form.language.data = book.language

    return render_template('manage.html', form=form, edit=True)


@manage.route('/delete', methods=['GET', 'POST'])
def delete_book():
    if request.method == 'POST':
        Books.get_books_by_isbn(request.args['isbn']).delete()
        return redirect('/')

    return render_template('delete.html')


def get_isbn13(book):
    if 'industryIdentifiers' in book:
        for identifier in book['industryIdentifiers']:
            if identifier['type'] == 'ISBN_13':
                return identifier['identifier']


def get_published_date(book):
    if 'publishedDate' in book:
        return book['publishedDate'][:4]
    return None


def get_image_links(book):
    if 'imageLinks' in book:
        if 'thumbnail' in book['imageLinks']:
            return book['imageLinks']['thumbnail']
    return None


def get_authors(book):
    if 'authors' in book:
        return book['authors']
    return None


def get_page_count(book):
    if 'pageCount' in book:
        return book['pageCount']
    return None


def prepare_url(args, start_index, max_results=40):
    url = 'https://www.googleapis.com/books/v1/volumes?q='
    if args['keyword']:
        url += quote(args['keyword'])
    if args['title']:
        url += '+intitle=' + quote(args['title'])
    if args['author']:
        url += '+inauthor=' + quote(args['author'])
    if args['publisher']:
        url += '+inpublisher=' + quote(args['publisher'])
    if args['subject']:
        url += '+subject=' + quote(args['subject'])
    if args['isbn']:
        url += '+isbn=' + quote(args['isbn'])
    if args['lccn']:
        url += '+lccn=' + quote(args['lccn'])
    if args['oclc']:
        url += '+oclc=' + quote(args['oclc'])
    url += '&max-results=' + str(max_results)
    if start_index:
        url += '&startIndex=' + str(start_index)
    return url


def add_books_from_google_api(args, start_index):
    url = prepare_url(args, start_index)
    response = requests.get(url).json()
    if 'items' in response:
        for book in response['items']:
            book_details = book['volumeInfo']
            if get_isbn13(book_details):
                Books.create_book(book_details['title'], get_authors(book_details),
                                  get_published_date(book_details),
                                  get_isbn13(book_details),
                                  get_page_count(book_details),
                                  get_image_links(book_details), book_details['language'])
    if start_index + 40 < response['totalItems']:
        add_books_from_google_api(args, start_index + 40)


@manage.route('/addByKeywords', methods=['GET', 'POST'])
def add_book_api():
    form = AddFromApiForm(request.form)
    if request.method == 'POST' and form.validate():
        add_books_from_google_api(request.form, 0)
        return redirect('/')
    return render_template('addFromApi.html', form=form)
