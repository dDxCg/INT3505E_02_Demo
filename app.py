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

    # ----- V2 Public API -----
    api_v2 = Api(
        app,
        version="2.0",
        title="Library API v2",
        description="Public endpoints (no JWT)",
        doc="/docs/v2"  # Swagger UI for v2
    )
    api_v2.add_namespace(books_ns, path="/api/v2/books")
    api_v2.add_namespace(copies_ns, path="/api/v2/copies")
    api_v2.add_namespace(borrows_ns, path="/api/v2/borrows")

    # ----- V3 Secured API -----
    authorizations_v3 = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add 'Bearer <JWT>' to authorize"
        }
    }

    api_v3 = Api(
        app,
        version="3.0",
        title="Library API v3",
        description="JWT protected endpoints",
        doc="/docs/v3",
        authorizations=authorizations_v3
    )
    api_v3.add_namespace(v3_auth_ns, path="/api/v3/auth")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
