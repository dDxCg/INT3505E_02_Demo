import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from services.borrow_service import BorrowService

v3_admin_borrows_ns = Namespace("v3/admin/borrows", description="Admin borrows routes")

borrow_model = v3_admin_borrows_ns.model(
    "Borrow",
    {
        "user_id": fields.Integer(required=False, description="User ID"),
        "copy_id": fields.Integer(required=False, description="Copy ID"),
        "return_date": fields.String(required=False, description="Return date in ISO format")
    }
)

@v3_admin_borrows_ns.route("/<int:borrow_id>")
@v3_admin_borrows_ns.param("borrow_id", "Borrow record ID")
class BorrowDetail(Resource):
    @v3_admin_borrows_ns.expect(borrow_model)
    @v3_admin_borrows_ns.doc("admin_update_borrow")
    def put(self, borrow_id):
        """Admin update borrow record"""
        data = v3_admin_borrows_ns.payload or {}
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
            v3_admin_borrows_ns.abort(404, "Borrow record or copy not found / invalid")

        return {
            "id": borrow.id,
            "user_id": borrow.user_id,
            "copy_id": borrow.copy_id,
            "borrow_date": borrow.borrow_date.isoformat(),
            "return_date": borrow.return_date.isoformat() if borrow.return_date else None
        }

    @v3_admin_borrows_ns.doc("delete_borrow")
    def delete(self, borrow_id):
        """Delete a borrow record"""
        success = BorrowService.delete_borrow(borrow_id)
        if not success:
            v3_admin_borrows_ns.abort(404, "Borrow record not found")
        return {"message": "Borrow deleted successfully"}
    
    @v3_admin_borrows_ns.doc("return_borrow")
    def patch(self, borrow_id):
        """Return a borrowed copy"""
        borrow, error = BorrowService.return_copy(borrow_id)
        if error:
            v3_admin_borrows_ns.abort(400, error)

        return {
            "id": borrow.id,
            "user_id": borrow.user_id,
            "copy_id": borrow.copy_id,
            "borrow_date": borrow.borrow_date.isoformat(),
            "return_date": borrow.return_date.isoformat()
        }

