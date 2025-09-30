from flask import Blueprint, request, jsonify
from services.copy_service import CopyService

copies_bp = Blueprint("copies", __name__, url_prefix="/copies")

# Create a new copy for a book
@copies_bp.route("/book/<int:book_id>", methods=["POST"])
def create_copy(book_id):
    status = request.args.get("status", "Available")
    copy = CopyService.create_copy(
        book_id=book_id,
        status=status
    )
    if not copy:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({
        "id": copy.id,
        "book_id": copy.book_id,
        "status": copy.status
    })

# Get all copies for a book
@copies_bp.route("/book/<int:book_id>", methods=["GET"])
def get_copies(book_id):
    copies = CopyService.get_copies_by_book(book_id)
    return jsonify([{"id": c.id, "book_id": c.book_id, "status": c.status} for c in copies])

# Update a copy
@copies_bp.route("/<int:copy_id>", methods=["PUT"])
def update_copy(copy_id):
    data = request.json
    copy = CopyService.update_copy(copy_id, status=data.get("status"))
    if not copy:
        return jsonify({"error": "Copy not found"}), 404
    return jsonify({"id": copy.id, "book_id": copy.book_id, "status": copy.status})

# Delete a copy
@copies_bp.route("/<int:copy_id>", methods=["DELETE"])
def delete_copy(copy_id):
    success = CopyService.delete_copy(copy_id)
    if not success:
        return jsonify({"error": "Copy not found"}), 404
    return jsonify({"message": "Copy deleted successfully"})
