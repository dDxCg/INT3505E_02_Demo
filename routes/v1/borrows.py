from flask_restx import Namespace, Resource, fields
from services.borrow_service import BorrowService
from datetime import datetime
from flask import request

# Namespace
borrows_ns = Namespace("borrows", description="Borrow operations")

# Swagger model for admin update or create borrow
borrow_model = borrows_ns.model(
    "Borrow",
    {
        "user_id": fields.Integer(required=False, description="User ID"),
        "copy_id": fields.Integer(required=False, description="Copy ID"),
        "return_date": fields.String(required=False, description="Return date in ISO format")
    }
)

# --- Borrow / List borrows ---
@borrows_ns.route("/")
class BorrowList(Resource):
    @borrows_ns.doc("list_borrows")
    @borrows_ns.param("user_id", "Filter by user ID")
    def get(self):
        """List borrows (optionally filtered by user)"""
        user_id = request.args.get("user_id", type=int)
        borrows = BorrowService.list_borrows(user_id)
        return [
            {
                "id": b.id,
                "user_id": b.user_id,
                "copy_id": b.copy_id,
                "borrow_date": b.borrow_date.isoformat(),
                "return_date": b.return_date.isoformat() if b.return_date else None
            } for b in borrows
        ]

    @borrows_ns.doc("borrow_book")
    @borrows_ns.param("user_id", "User ID", required=True)
    @borrows_ns.param("book_id", "Book ID", required=True)
    def post(self):
        """Borrow a book"""
        user_id = request.args.get("user_id", type=int)
        book_id = request.args.get("book_id", type=int)
        if not user_id or not book_id:
            borrows_ns.abort(400, "Missing user_id or book_id")

        borrow, error = BorrowService.borrow_copy(user_id, book_id)
        if error:
            borrows_ns.abort(400, error)

        return {
            "id": borrow.id,
            "user_id": borrow.user_id,
            "copy_id": borrow.copy_id,
            "borrow_date": borrow.borrow_date.isoformat(),
            "return_date": borrow.return_date.isoformat() if borrow.return_date else None
        }, 201


# --- Borrow detail operations ---
@borrows_ns.route("/<int:borrow_id>")
@borrows_ns.param("borrow_id", "Borrow record ID")
class BorrowDetail(Resource):
    @borrows_ns.doc("return_borrow")
    def patch(self, borrow_id):
        """Return a borrowed copy"""
        borrow, error = BorrowService.return_copy(borrow_id)
        if error:
            borrows_ns.abort(400, error)

        return {
            "id": borrow.id,
            "user_id": borrow.user_id,
            "copy_id": borrow.copy_id,
            "borrow_date": borrow.borrow_date.isoformat(),
            "return_date": borrow.return_date.isoformat()
        }

    @borrows_ns.expect(borrow_model)
    @borrows_ns.doc("admin_update_borrow")
    def put(self, borrow_id):
        """Admin update borrow record"""
        data = borrows_ns.payload or {}
        user_id = data.get("user_id")
        copy_id = data.get("copy_id")
        return_date_str = data.get("return_date")
        return_date = datetime.fromisoformat(return_date_str) if return_date_str else None

        borrow = BorrowService.admin_update_borrow(
            borrow_id,
            user_id=user_id,
            copy_id=copy_id,
            return_date=return_date
        )
        if not borrow:
            borrows_ns.abort(404, "Borrow record or copy not found / invalid")

        return {
            "id": borrow.id,
            "user_id": borrow.user_id,
            "copy_id": borrow.copy_id,
            "borrow_date": borrow.borrow_date.isoformat(),
            "return_date": borrow.return_date.isoformat() if borrow.return_date else None
        }

    @borrows_ns.doc("delete_borrow")
    def delete(self, borrow_id):
        """Delete a borrow record"""
        success = BorrowService.delete_borrow(borrow_id)
        if not success:
            borrows_ns.abort(404, "Borrow record not found")
        return {"message": "Borrow deleted successfully"}
