from flask import request
from flask_restx import Namespace, Resource, fields
from services.book_service import BookService

# Create Namespace
books_ns = Namespace("books", description="Books operations")

# Swagger model for creating/updating a book
book_model = books_ns.model(
    "Book",
    {
        "title": fields.String(required=True, description="Book title"),
        "author": fields.String(required=True, description="Book author"),
        "year": fields.Integer(required=False, description="Publication year"),
    }
)

# --- Public endpoints ---
@books_ns.route("/")
class BookList(Resource):
    @books_ns.doc("list_books")
    @books_ns.param("title", "Filter by title")
    @books_ns.param("author", "Filter by author")
    def get(self):
        """Search books (public)"""
        # use query params and convert empty strings to None
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

    @books_ns.expect(book_model)
    @books_ns.doc("create_book")
    def post(self):
        """Create a new book"""
        data = books_ns.payload
        book = BookService.create_book(data["title"], data["author"], data.get("year"))
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        }, 201


# --- Single book operations ---
@books_ns.route("/<int:book_id>")
@books_ns.param("book_id", "The book identifier")
class BookDetail(Resource):
    @books_ns.expect(book_model)
    @books_ns.doc("update_book")
    def put(self, book_id):
        """Update a book"""
        data = books_ns.payload
        book = BookService.update_book(book_id, data.get("title"), data.get("author"), data.get("year"))
        if not book:
            books_ns.abort(404, "Book not found")
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        }

    @books_ns.doc("delete_book")
    def delete(self, book_id):
        """Delete a book"""
        success = BookService.delete_book(book_id)
        if not success:
            books_ns.abort(404, "Book not found")
        return {"message": "Book deleted successfully"}


# --- Admin search ---
@books_ns.route("/admin")
class BookAdmin(Resource):
    @books_ns.doc("search_books_admin")
    @books_ns.param("id", "Filter by book ID")
    @books_ns.param("title", "Filter by title")
    @books_ns.param("author", "Filter by author")
    def get(self):
        """Search books (admin)"""
        from flask import request
        book_id = request.args.get("id")
        title = request.args.get("title")
        author = request.args.get("author")

        filters = {}
        if book_id:
            filters["id"] = int(book_id)
        if title:
            filters["title"] = title
        if author:
            filters["author"] = author

        books = BookService.admin_search_books(**filters)
        return [{"id": b.id, "title": b.title, "author": b.author, "year": b.year} for b in books]
