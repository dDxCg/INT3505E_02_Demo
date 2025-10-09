from flask import request, make_response, jsonify
from flask_restx import Namespace, Resource, fields
from services.book_service import BookService
import hashlib
from extensions import cache
from config import Config

v4_books_ns = Namespace("v4/books", description="Books operations")

book_model = v4_books_ns.model(
    "Book",
    {
        "title": fields.String(required=True, description="Book title"),
        "author": fields.String(required=True, description="Book author"),
        "year": fields.Integer(required=False, description="Publication year"),
    }
)


@v4_books_ns.route("/")
class BookList(Resource):
    @v4_books_ns.doc(
        responses={
            200: ("Success", book_model),
            304: "Not Modified"
        },
        headers={
            "ETag": "Current ETag of the resource",
            "Cache-Control": "Cache max-age in seconds",
            "X-Cache": "HIT or MISS",
            "X-Cache-Timeout": "Cache TTL in seconds"
        }
    )
    @v4_books_ns.param("title", "Filter by title")
    @v4_books_ns.param("author", "Filter by author")
    def get(self):
        title = request.args.get("title") or None
        author = request.args.get("author") or None

        cache_key = f"v4_books_{title}_{author}"
        cached_result = cache.get(cache_key)

        if cached_result:
            payload = cached_result
            cache_status = "HIT"
        else:
            # Fetch fresh data
            books = BookService.search_books(title=title, author=author)
            payload = []
            for b in books:
                available_copies = sum(1 for c in b.copies if c.status == "available")
                payload.append({
                    "id": b.id,
                    "title": b.title,
                    "author": b.author,
                    "year": b.year,
                    "available_copies": available_copies
                })
            # Store in cache
            cache.set(cache_key, payload)
            cache_status = "MISS"
        
        # Compute ETag based on payload content
        etag = hashlib.md5(str(payload).encode("utf-8")).hexdigest()

        # Check If-None-Match header from client
        if_none_match = request.headers.get("If-None-Match")
        if if_none_match == etag:
            response = make_response("", 304)  # Not Modified
            response.headers["ETag"] = etag
            response.headers["Cache-Control"] = f"max-age={Config.CACHE_DEFAULT_TIMEOUT}"
            response.headers["X-Cache"] = cache_status
            response.headers["X-Cache-Timeout"] = str(Config.CACHE_DEFAULT_TIMEOUT)
            return response

        # Return response with payload
        response = make_response(jsonify(payload), 200)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = f"max-age={Config.CACHE_DEFAULT_TIMEOUT}"
        response.headers["X-Cache"] = cache_status
        response.headers["X-Cache-Timeout"] = str(Config.CACHE_DEFAULT_TIMEOUT)
        return response