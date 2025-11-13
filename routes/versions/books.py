from flask import request, make_response, jsonify
import hashlib
from flask_restx import Namespace, Resource, fields
from services.book_service import BookService
from utils.v2.versioning import detect_version, add_sunset_headers
from extensions import cache
from config import Config

# Create Namespace
books_vers_ns = Namespace("/books", description="Books operations")

# Swagger model for creating/updating a book
book_model = books_vers_ns.model(
    "Book",
    {
        "title": fields.String(required=True, description="Book title"),
        "author": fields.String(required=True, description="Book author"),
        "year": fields.Integer(required=False, description="Publication year"),
    }
)

@books_vers_ns.route("")
class BookList(Resource):
    @books_vers_ns.doc("list_books")
    @books_vers_ns.param("title", "Filter by title")
    @books_vers_ns.param("author", "Filter by author")
    def get(self):
        """Search books (public)"""
        # use query params and convert empty strings to None
        title = request.args.get("title") or None
        author = request.args.get("author") or None
        version = detect_version()

        #caching
        if version == "v4":
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
                    available_copies = sum(1 for c in b.copies if c.status.lower() == "available")
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
                return add_sunset_headers(response, version)

            # Return response with payload
            response = make_response(jsonify(payload), 200)
            response.headers["ETag"] = etag
            response.headers["Cache-Control"] = f"max-age={Config.CACHE_DEFAULT_TIMEOUT}"
            response.headers["X-Cache"] = cache_status
            response.headers["X-Cache-Timeout"] = str(Config.CACHE_DEFAULT_TIMEOUT)
            return add_sunset_headers(response, version)
        #pagination
        elif version == "v5":
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 10, type=int)

            cache_key = f"v5_books_{title}_{author}_p{page}_pp{per_page}"
            cached_result = cache.get(cache_key)

            if cached_result:
                payload = cached_result
                cache_status = "HIT"
                print (cache_status)
            else:
                # Fetch fresh data
                books, total = BookService.search_books_paginated(
                    title=title,
                    author=author,
                    page=page,
                    per_page=per_page
                )
                payload = []
                for b in books:
                    available_copies = sum(1 for c in b.copies if c.status.lower() == "available")
                    payload.append({
                        "id": b.id,
                        "title": b.title,
                        "author": b.author,
                        "year": b.year,
                        "available_copies": available_copies
                    })

                result = {
                    "items": payload,
                    "total": total,
                    "page": page,
                    "per_page": per_page,
                    "pages": (total + per_page - 1) // per_page
                }
                # Store in cache
                cache.set(cache_key, result)
                payload = result
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
                return add_sunset_headers(response, version)

            # Return response with payload
            response = make_response(jsonify(payload), 200)
            response.headers["ETag"] = etag
            response.headers["Cache-Control"] = f"max-age={Config.CACHE_DEFAULT_TIMEOUT}"
            response.headers["X-Cache"] = cache_status
            response.headers["X-Cache-Timeout"] = str(Config.CACHE_DEFAULT_TIMEOUT)
            return add_sunset_headers(response, version)
        #fallback (default v1, v2, v3)
        else:
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

            response = make_response(jsonify(payload), 200)
            return add_sunset_headers(response, version)