from flask import Flask
from flask_migrate import Migrate
from config import Config
from db import db

# routes
from routes.v1.books import books_bp
from routes.v1.copies import copies_bp
from routes.v1.borrows import borrows_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init db + migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    # register blueprints
    app.register_blueprint(books_bp, url_prefix="/api/v1/books")
    app.register_blueprint(copies_bp, url_prefix="/api/v1/copies")
    app.register_blueprint(borrows_bp, url_prefix="/api/v1/borrows")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
