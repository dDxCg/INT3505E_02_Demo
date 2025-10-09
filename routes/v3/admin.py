from flask import request
from flask_restx import Namespace, Resource, fields
from services.book_service import BookService
from services.copy_service import CopyService
from services.borrow_service import BorrowService
from services.user_service import UserService

v3_admin_ns = Namespace("v3_admin", description="Admin routes")

user_model = v3_admin_ns("User", {
    "email": fields.String(required=True, description="Unique email"),
    "password": fields.String(required=True),
    "role": fields.String(description="user | admin")
})