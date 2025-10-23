import json
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from db import db
from routes import all_namespaces
from extensions import cache, limiter
from flask_limiter.errors import RateLimitExceeded

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cache.init_app(app)
    limiter.init_app(app)

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
        prefix="/api",
        authorizations=authorizations_v3
    )


    # Register all namespaces without specifying path
    for ns in all_namespaces:
        api.add_namespace(ns)

    # --- OpenAPI JSON endpoint ---
    @app.route("/openapi.json")
    def openapi_json():
        spec = api.__schema__

        # Save in same folder as app.py
        with open("openapi.json", "w") as f:
            json.dump(spec, f, indent=2)

        # Serve dynamically
        return jsonify(spec)
    
    # --- Rate Limit handler ---
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit_exceeded(e):
        return jsonify({
            "error": "rate_limit_exceeded",
            "message": "Too many requests.",
            "limit": str(e.description)
        }), 429

    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
