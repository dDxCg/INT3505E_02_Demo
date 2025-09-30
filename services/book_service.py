from models.book import Book
from db import db

class BookService:
    @staticmethod
    def create_book(title: str, author: str, year: int = None) -> Book:
        book = Book(title=title, author=author, year=year)
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def get_book(book_id: int) -> Book | None:
        return Book.query.get(book_id)

    @staticmethod
    def update_book(book_id: int, title: str = None, author: str = None, year: int = None) -> Book | None:
        book = Book.query.get(book_id)
        if not book:
            return None
        if title:
            book.title = title
        if author:
            book.author = author
        if year is not None:
            book.year = year
        db.session.commit()
        return book

    @staticmethod
    def delete_book(book_id: int) -> bool:
        book = Book.query.get(book_id)
        if not book:
            return False
        db.session.delete(book)
        db.session.commit()
        return True

    @staticmethod
    def search_books(title=None, author=None):
        query = Book.query
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        return query.all()

    @staticmethod
    def admin_search_books(id=None, title=None, author=None):
        query = Book.query

        if id is not None:
            query = query.filter(Book.id == id)
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))

        return query.all()