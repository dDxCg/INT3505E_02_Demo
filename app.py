from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from db import db
from routes.v2.books import books_ns
from routes.v2.copies import copies_ns
from routes.v2.borrows import borrows_ns
from routes.v3.auth import v3_auth_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    authorizations_v3 = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Add 'Bearer <JWT>' here"
        }
    }

    api = Api(
        app,
        version="1.0",
        title="Library API",
        doc="/docs",  # only one Swagger UI
        authorizations=authorizations_v3
    )


    # ----- V2 namespaces (public) -----
    api.add_namespace(books_ns, path="/api/v2/books")
    api.add_namespace(copies_ns, path="/api/v2/copies")
    api.add_namespace(borrows_ns, path="/api/v2/borrows")

    # ----- V3 namespaces (JWT) -----
    api.add_namespace(v3_auth_ns, path="/api/v3/auth")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
