from flask import request
from flask_restx import Namespace, Resource, fields
from bson import ObjectId
# from flask import current_app
from db import mongo


v7_book_ns = Namespace("v7/books", description="Book CRUD operations")

# --- Models ---
book_model = v7_book_ns.model("Book", {
    "title": fields.String(required=True, description="Book title"),
    "author": fields.String(required=True, description="Author name"),
    "year": fields.Integer(description="Publication year"),
    "genre": fields.String(description="Genre"),
})

book_response = v7_book_ns.model("BookResponse", {
    "id": fields.String(description="Book ID"),
    "title": fields.String(description="Book title"),
    "author": fields.String(description="Author name"),
    "year": fields.Integer(description="Publication year"),
    "genre": fields.String(description="Genre"),
})

# --- Helper ---
def serialize_book(book):
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "year": book.get("year"),
        "genre": book.get("genre"),
    }

def get_books_collection():
    # mongo = current_app.extensions['pymongo']
    return mongo.db.books

# --- Routes ---
@v7_book_ns.route("/")
class BookList(Resource):
    @v7_book_ns.doc(params={
        "title": "Search by book title",
        "author": "Search by author name",
        "year": "Filter by publication year",
        "genre": "Filter by genre"
    })
    @v7_book_ns.marshal_list_with(book_response)
    def get(self):
        """Get all books or search by query parameters"""
        query = {}

        # collect filters from query string (?title=abc&author=xyz)
        title = request.args.get("title")
        author = request.args.get("author")
        year = request.args.get("year")
        genre = request.args.get("genre")

        if title:
            query["title"] = {"$regex": title, "$options": "i"}  # case-insensitive search
        if author:
            query["author"] = {"$regex": author, "$options": "i"}
        if year:
            query["year"] = int(year)
        if genre:
            query["genre"] = {"$regex": genre, "$options": "i"}

        books = get_books_collection().find(query)
        return [serialize_book(b) for b in books], 200

    @v7_book_ns.expect(book_model)
    @v7_book_ns.response(201, "Book created")
    def post(self):
        """Add a new book"""
        data = request.get_json()
        result = get_books_collection().insert_one(data)
        return {"id": str(result.inserted_id), "message": "Book created"}, 201


@v7_book_ns.route("/<string:id>")
@v7_book_ns.param("id", "Book ID")
class Book(Resource):
    @v7_book_ns.marshal_with(book_response)
    @v7_book_ns.response(404, "Book not found")
    def get(self, id):
        """Get a single book by ID"""
        book = get_books_collection().find_one({"_id": ObjectId(id)})
        if not book:
            v7_book_ns.abort(404, "Book not found")
        return serialize_book(book), 200

    @v7_book_ns.expect(book_model)
    @v7_book_ns.response(200, "Book updated")
    def put(self, id):
        """Update a book"""
        data = request.get_json()
        result = get_books_collection().update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count == 0:
            v7_book_ns.abort(404, "Book not found")
        return {"message": "Book updated"}, 200

    @v7_book_ns.response(200, "Book deleted")
    def delete(self, id):
        """Delete a book"""
        result = get_books_collection().delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            v7_book_ns.abort(404, "Book not found")
        return {"message": "Book deleted"}, 200
