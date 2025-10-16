from models.book import Book
from db import db
from sqlalchemy.orm import joinedload

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
        query = Book.query.options(joinedload(Book.copies))
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        return query.all()

    @staticmethod
    def admin_search_books(id=None, title=None, author=None):
        query = Book.query.options(joinedload(Book.copies))

        if id is not None:
            query = query.filter(Book.id == id)
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))

        return query.all()
    
    @staticmethod
    def search_books_paginated(title=None, author=None, page=1, per_page=10):
        query = Book.query.options(joinedload(Book.copies))

        # Filter dynamically
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))

        # Get total count before slicing
        total = query.count()

        # Apply pagination (offset & limit)
        books = (
            query
            .order_by(Book.id)  # consistent order between pages
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        return books, total