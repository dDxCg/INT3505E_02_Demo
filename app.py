from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from db import db
from routes.v1.books import books_ns
from routes.v1.copies import copies_ns
from routes.v1.borrows import borrows_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    api = Api(app, version="1.0", title="Library API", doc="/docs")
    api.add_namespace(books_ns, path="/api/v1/books")
    api.add_namespace(copies_ns, path="/api/v1/copies")
    api.add_namespace(borrows_ns, path="/api/v1/borrows")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
