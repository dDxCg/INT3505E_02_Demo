from flask_restx import Namespace, Resource, fields
from services.borrow_service import BorrowService
from flask import request
from utils.require_jwt import require_jwt

# Namespace
v3_borrows_ns = Namespace("v3/borrows", description="Borrow operations")

# Swagger model for admin update or create borrow
borrow_model = v3_borrows_ns.model(
    "Borrow",
    {
        "user_id": fields.Integer(required=False, description="User ID"),
        "copy_id": fields.Integer(required=False, description="Copy ID"),
        "return_date": fields.String(required=False, description="Return date in ISO format")
    }
)

@v3_borrows_ns.route("/")
class BorrowOperations(Resource):
    @v3_borrows_ns.doc("list_borrows")
    @v3_borrows_ns.doc(security="Bearer Auth")
    @require_jwt
    def get(self):
        """List borrows (optionally filtered by user)"""
        data = request.json
        user_id = data.user.id
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

    @v3_borrows_ns.doc("borrow_book")
    @v3_borrows_ns.doc(security="Bearer Auth")
    @v3_borrows_ns.param("book_id", "Book ID", required=True)
    @require_jwt
    def post(self):
        """Borrow a book"""
        body = request.json
        user_id = body.user.id
        book_id = request.args.get("book_id", type=int)
        if not user_id or not book_id:
            v3_borrows_ns.abort(400, "Missing user_id or book_id")

        borrow, error = BorrowService.borrow_copy(user_id, book_id)
        if error:
            v3_borrows_ns.abort(400, error)

        return {
            "id": borrow.id,
            "user_id": borrow.user_id,
            "copy_id": borrow.copy_id,
            "borrow_date": borrow.borrow_date.isoformat(),
            "return_date": borrow.return_date.isoformat() if borrow.return_date else None
        }, 201
    
    @v3_borrows_ns.doc("return_borrow")
    @v3_borrows_ns.doc(security="Bearer Auth")
    @require_jwt
    def patch(self, borrow_id):
        """Return a borrowed copy"""    
        data = request.json
        user_id = data.user.id

        is_valid = BorrowService.valid_user(borrow_id, user_id)
        if not is_valid:
            v3_borrows_ns.abort(400, error)
            
        borrow, error = BorrowService.return_copy(borrow_id)
        if error:
            v3_borrows_ns.abort(400, error)

        return {
            "id": borrow.id,
            "user_id": borrow.user_id,
            "copy_id": borrow.copy_id,
            "borrow_date": borrow.borrow_date.isoformat(),
            "return_date": borrow.return_date.isoformat()
        }