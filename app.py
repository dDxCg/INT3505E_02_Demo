import json
from flask import Flask, jsonify, request, send_from_directory
from flask_migrate import Migrate
from flask_restx import Api
from config import Config
from db import db, mongo
from routes import all_namespaces
from extensions import cache, limiter
from flask_limiter.errors import RateLimitExceeded
from flask_cors import CORS
from pymongo.errors import ServerSelectionTimeoutError

from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import Histogram

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    cache.init_app(app)
    limiter.init_app(app)
    
    # mongo.init_app(app)
    # app.extensions["pymongo"] = mongo

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

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory('static', 'favicon.ico')

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

# --- Prometheus Metrics ---
    REQUEST_COUNT = Counter(
        "flask_requests_total",
        "Total HTTP requests",
        ["method", "endpoint"]
    )

    REQUEST_LATENCY = Histogram(
        "flask_request_latency_seconds",
        "HTTP request latency in seconds",
        ["endpoint"]
    )

    # --- Middleware for counting & latency ---
    @app.before_request
    def before_request():
        if request.path not in ["/metrics", "/favicon.ico"]:
            REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()
            request._prom_timer = REQUEST_LATENCY.labels(endpoint=request.path).time()
            request._prom_timer.__enter__()

    @app.after_request
    def after_request(response):
        if hasattr(request, "_prom_timer"):
            request._prom_timer.__exit__(None, None, None)
        return response


    # Metrics endpoint for Prometheus to scrape
    @app.route("/metrics")
    def metrics():
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
    
    # --- OpenAPI JSON endpoint ---
    @app.route("/swagger.yaml")
    def openapi_json():
        spec = api.__schema__

        # Save in same folder as app.py
        with open("swagger.yaml", "w") as f:
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

# --- Test function ---
# def test_mongo_connection(mongo_instance):
#     """
#     Test MongoDB connection and print the connected database name.
#     """
#     try:
#         # Ping server
#         pong = mongo_instance.cx.admin.command("ping")
#         print("✅ MongoDB server ping response:", pong)

#         # Check selected DB
#         if mongo_instance.db:
#             print("📘 Connected to database:", mongo_instance.db.name)
#         else:
#             print("❌ No database selected. Make sure your MONGO_URI includes a DB name.")

#     except ServerSelectionTimeoutError as e:
#         print(f"❌ MongoDB connection failed: {e}")

app = create_app()

if __name__ == "__main__":
    # test_mongo_connection(mongo)
    app.run(debug=True)
