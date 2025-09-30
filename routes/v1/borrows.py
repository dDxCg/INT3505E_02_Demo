from datetime import datetime
from flask import Blueprint, request, jsonify
from services.borrow_service import BorrowService

borrows_bp = Blueprint("borrows", __name__, url_prefix="/borrows")

# Borrow a book (by book_id)
@borrows_bp.route("/", methods=["POST"])
def borrow_book():
    user_id = request.args.get("user_id", type=int)
    book_id = request.args.get("book_id", type=int)
    if not user_id or not book_id:
        return jsonify({"error": "Missing user_id or book_id"}), 400

    borrow, error = BorrowService.borrow_copy(user_id, book_id)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "id": borrow.id,
        "user_id": borrow.user_id,
        "copy_id": borrow.copy_id,
        "borrow_date": borrow.borrow_date.isoformat(),
        "return_date": borrow.return_date.isoformat() if borrow.return_date else None
    })

# --- Return book ---
@borrows_bp.route("/<int:borrow_id>", methods=["PATCH"])
def return_borrow(borrow_id):
    borrow, error = BorrowService.return_copy(borrow_id)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "id": borrow.id,
        "user_id": borrow.user_id,
        "copy_id": borrow.copy_id,
        "borrow_date": borrow.borrow_date.isoformat(),
        "return_date": borrow.return_date.isoformat()
    })

# --- List all borrows ---
@borrows_bp.route("/", methods=["GET"])
def list_borrows():
    user_id = request.args.get("user_id", type=int)
    borrows = BorrowService.list_borrows(user_id)
    return jsonify([{
        "id": b.id,
        "user_id": b.user_id,
        "copy_id": b.copy_id,
        "borrow_date": b.borrow_date.isoformat(),
        "return_date": b.return_date.isoformat() if b.return_date else None
    } for b in borrows])

# --- Update borrow admin ---
@borrows_bp.route("/<int:borrow_id>", methods=["PUT"])
def admin_update_borrow(borrow_id):
    data = request.json or {}
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
        return jsonify({"error": "Borrow record or copy not found / invalid"}), 404

    return jsonify({
        "id": borrow.id,
        "user_id": borrow.user_id,
        "copy_id": borrow.copy_id,
        "borrow_date": borrow.borrow_date.isoformat(),
        "return_date": borrow.return_date.isoformat() if borrow.return_date else None
    })

# --- Delete borrows ---
@borrows_bp.route("/<int:borrow_id>", methods=["DELETE"])
def delete_borrow(borrow_id):
    success = BorrowService.delete_borrow(borrow_id)
    if not success:
        return jsonify({"error": "Borrow record not found"}), 404
    return jsonify({"message": "Borrow deleted successfully"})