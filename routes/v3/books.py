from flask import request
from flask_restx import Namespace, Resource, fields
from services.book_service import BookService

v3_books_ns = Namespace("v3/books", description="Books operations")

book_model = v3_books_ns.model(
    "Book",
    {
        "title": fields.String(required=True, description="Book title"),
        "author": fields.String(required=True, description="Book author"),
        "year": fields.Integer(required=False, description="Publication year"),
    }
)


@v3_books_ns.route("/")
class BookList(Resource):
    @v3_books_ns.doc("list_books")
    @v3_books_ns.param("title", "Filter by title")
    @v3_books_ns.param("author", "Filter by author")
    def get(self):
        title = request.args.get("title") or None
        author = request.args.get("author") or None

        books = BookService.search_books(title=title, author=author)

        result = []
        for b in books:
            available_copies = sum(1 for c in b.copies if c.status == "available")
            result.append({
                "id": b.id,
                "title": b.title,
                "author": b.author,
                "year": b.year,
                "available_copies": available_copies
            })
        return result
