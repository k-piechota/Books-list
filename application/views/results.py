from flask import render_template, Response, Blueprint, request
from models.books import Books

results = Blueprint('results', __name__, template_folder='templates')


def get_books(args):
    title = args.get('title') or ''
    author = args.get('author') or ''
    from_date = args.get('from') or '0'
    to_date = args.get('to') or '9999'
    language = args.get('language') or ''
    return Books.get_books_by_filters(title, author, from_date, to_date, language)


@results.route('/')
def show_results():
    return render_template('results.html')


@results.route('/api')
def api():
    books = get_books(request.args)
    json_books = books.to_json().replace('_id', 'isbn') if books else None
    return Response(json_books, mimetype='application/json')
