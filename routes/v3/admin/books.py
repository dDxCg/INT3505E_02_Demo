from flask import request
from flask_restx import Namespace, Resource, fields
from services.book_service import BookService

v3_admin_books_ns = Namespace("v3/admin/books", description="Admin books routes")

book_model = v3_admin_books_ns.model(
    "Book",
    {
        "title": fields.String(required=True, description="Book title"),
        "author": fields.String(required=True, description="Book author"),
        "year": fields.Integer(required=False, description="Publication year"),
    }
)

# --- Books admin endpoints ---
@v3_admin_books_ns.route("/<int:book_id>")
@v3_admin_books_ns.param("book_id", "The book identifier")
class BookDetail(Resource):
    @v3_admin_books_ns.expect(book_model)
    @v3_admin_books_ns.doc("update_book")
    def put(self, book_id):
        """Update a book"""
        data = v3_admin_books_ns.payload
        book = BookService.update_book(book_id, data.get("title"), data.get("author"), data.get("year"))
        if not book:
            v3_admin_books_ns.abort(404, "Book not found")
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        }

    @v3_admin_books_ns.doc("delete_book")
    def delete(self, book_id):
        """Delete a book"""
        success = BookService.delete_book(book_id)
        if not success:
            v3_admin_books_ns.abort(404, "Book not found")
        return {"message": "Book deleted successfully"}


@v3_admin_books_ns.route("/")
class BookAdmin(Resource):
    @v3_admin_books_ns.doc("search_books_admin")
    @v3_admin_books_ns.param("id", "Filter by book ID")
    @v3_admin_books_ns.param("title", "Filter by title")
    @v3_admin_books_ns.param("author", "Filter by author")
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

    @v3_admin_books_ns.expect(book_model)
    @v3_admin_books_ns.doc("create_book")
    def post(self):
        """Create a new book"""
        data = v3_admin_books_ns.payload
        book = BookService.create_book(data["title"], data["author"], data.get("year"))
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        }, 201