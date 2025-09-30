from flask import Blueprint, request, jsonify
from services.book_service import BookService

books_bp = Blueprint("books", __name__, url_prefix="/books")

# --- Create Book ---
@books_bp.route("/", methods=["POST"])
def create_book():
    data = request.json
    book = BookService.create_book(data["title"], data["author"], data.get("year"))
    return jsonify({"id": book.id, "title": book.title, "author": book.author, "year": book.year})

# --- Public Search ---
@books_bp.route("/", methods=["GET"])
def search_books():
    title = request.args.get("title")
    author = request.args.get("author")

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

    return jsonify(result)

# --- Update Book ---
@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    book = BookService.update_book(book_id, data.get("title"), data.get("author"), data.get("year"))
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"id": book.id, "title": book.title, "author": book.author, "year": book.year})

# --- Delete Book ---
@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    success = BookService.delete_book(book_id)
    if not success:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"message": "Book deleted successfully"})

# --- Admin search ---
@books_bp.route("/admin", methods=["GET"])
def search_books_admin():
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
    return jsonify([{"id": b.id, "title": b.title, "author": b.author, "year": b.year} for b in books])

