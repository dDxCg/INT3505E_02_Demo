import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from services.copy_service import CopyService


v3_admin_copies_ns = Namespace("v3/admin/copies", description="Admin copies routes")


copy_model = v3_admin_copies_ns.model(
    "Copy",
    {
        "status": fields.String(required=False, description="Copy status", default="Available"),
    }
)
# --- Create / Get copies for a book ---
@v3_admin_copies_ns.route("/<int:book_id>")
@v3_admin_copies_ns.param("book_id", "The book ID")
class BookCopies(Resource):
    @v3_admin_copies_ns.doc("get_copies")
    def get(self, book_id):
        """Get all copies for a book"""
        copies = CopyService.get_copies_by_book(book_id)
        return [{"id": c.id, "book_id": c.book_id, "status": c.status} for c in copies]

    @v3_admin_copies_ns.expect(copy_model)
    @v3_admin_copies_ns.doc("create_copy")
    def post(self, book_id):
        """Create a new copy for a book"""
        data = v3_admin_copies_ns.payload or {}
        status = data.get("status", "Available")
        copy = CopyService.create_copy(book_id=book_id, status=status)
        if not copy:
            v3_admin_copies_ns.abort(404, "Book not found")
        return {"id": copy.id, "book_id": copy.book_id, "status": copy.status}, 201


# --- Update / Delete a copy ---
@v3_admin_copies_ns.route("/<int:copy_id>")
@v3_admin_copies_ns.param("copy_id", "The copy ID")
class CopyDetail(Resource):
    @v3_admin_copies_ns.expect(copy_model)
    @v3_admin_copies_ns.doc("update_copy")
    def put(self, copy_id):
        """Update a copy"""
        data = v3_admin_copies_ns.payload
        copy = CopyService.update_copy(copy_id, status=data.get("status"))
        if not copy:
            v3_admin_copies_ns.abort(404, "Copy not found")
        return {"id": copy.id, "book_id": copy.book_id, "status": copy.status}

    @v3_admin_copies_ns.doc("delete_copy")
    def delete(self, copy_id):
        """Delete a copy"""
        success = CopyService.delete_copy(copy_id)
        if not success:
            v3_admin_copies_ns.abort(404, "Copy not found")
        return {"message": "Copy deleted successfully"}
