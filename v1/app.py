from flask import Flask, Response, send_from_directory
from flask_restx import Api, Resource, fields
import os

app = Flask(__name__)
api = Api(app)

# Mock database
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
]

ns = api.namespace("books")

book_model = api.model("Book", {
    "title": fields.String(required=True),
    "author": fields.String(required=True),
})

@ns.route("/")
class BookList(Resource):
    @ns.marshal_list_with(book_model)
    def get(self):
        return books

# Code-on-Demand endpoint
@app.route("/code")
def code_on_demand():
    js_code = """
    fetch('/books/')
      .then(r => r.json())
      .then(data => {
          const container = document.getElementById('books-container');
          if (!container) return;
          const ul = document.createElement('ul');
          data.forEach(b => {
              const li = document.createElement('li');
              li.textContent = `${b.title} by ${b.author}`;
              ul.appendChild(li);
          });
          container.appendChild(ul);
      })
      .catch(err => console.error(err));
    """
    return Response(js_code, mimetype="application/javascript")

# Serve the HTML file from same folder
@app.route("/index")
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")

if __name__ == "__main__":
    app.run(debug=True)
