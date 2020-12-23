from models.db import db


class Books(db.Document):
    title = db.StringField()
    authors = db.ListField(db.StringField())
    publishedDate = db.IntField()
    isbn = db.StringField(primary_key=True)
    pageCount = db.IntField()
    thumbnail = db.StringField()
    language = db.StringField()

    @staticmethod
    def get_books_by_filters(title, author, from_date, to_date, language):
        try:
            return Books.objects(title__contains=title,
                                 __raw__={'authors': {'$regex': f'.*{author}.*'}},
                                 publishedDate__gte=int(from_date),
                                 publishedDate__lte=int(to_date),
                                 language__contains=language)
        except ValueError:
            return None

    @staticmethod
    def get_books_by_isbn(isbn):
        return Books.objects(isbn=isbn).first()

    @staticmethod
    def create_book(title, authors, published_date, isbn, page_count, thumbnail, language):
        Books(title=title, authors=authors, publishedDate=published_date, isbn=isbn, pageCount=page_count,
              thumbnail=thumbnail, language=language).save()

    @staticmethod
    def update_book(book, title=None, authors=None, published_date=None, page_count=None, thumbnail=None, language=None):
        book.title = title if title else book.title
        book.authors = authors if authors else book.authors
        book.publishedDate = published_date if published_date else book.publishedDate
        book.pageCount = page_count if page_count else book.pageCount
        book.thumbnail = thumbnail if thumbnail else book.thumbnail
        book.language = language if language else book.language
        book.save()
