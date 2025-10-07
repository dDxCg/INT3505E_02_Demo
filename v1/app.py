from flask import Flask, request
from flask_restx import Api, Resource, fields

# mock database
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
]

app = Flask(__name__)
api = Api(app, title="Book API", description="Simple mock API for books")

ns = api.namespace("books", description="Book operations")

book_model = api.model("Book", {
    "title": fields.String(required=True, description="Book title"),
    "author": fields.String(required=True, description="Book author"),
})

@ns.route("/")
class BookList(Resource):
    @ns.marshal_list_with(book_model)
    def get(self):
        """Get all books"""
        return books

    @ns.expect(book_model)
    def post(self):
        """Add a new book"""
        data = request.json
        new_id = max(b["id"] for b in books) + 1 if books else 1
        new_book = {"id": new_id, **data}
        books.append(new_book)
        return new_book, 201


if __name__ == "__main__":
    app.run(debug=True)
