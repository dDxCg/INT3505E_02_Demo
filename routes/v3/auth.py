from flask import request
from flask_restx import Namespace, Resource, fields
from flask import current_app
from services.user_service import UserService
from utils.jwt_utils import generate_token
from utils.require_jwt import require_jwt

v3_auth_ns = Namespace("v3_auth", description="Authentication operations")

user_model = v3_auth_ns.model("UserRegister", {
    "email": fields.String(required=True, description="Unique email"),
    "password": fields.String(required=True)
})

token_model = v3_auth_ns.model("Token", {
    "access_token": fields.String(description="JWT access token")
})

change_pass_model = v3_auth_ns.model("ChangePassword", {
    "password": fields.String(required=True, description="New password"),
})

@v3_auth_ns.route("/register")
class Register(Resource):
    @v3_auth_ns.expect(user_model)
    @v3_auth_ns.response(201, "User created")
    def post(self):
        data = request.json
        user = UserService.create_user(data["email"], data["password"])
        return {"msg": "User created"}, 201

@v3_auth_ns.route("/login")
class Login(Resource):
    @v3_auth_ns.expect(user_model)
    @v3_auth_ns.marshal_with(token_model)
    @v3_auth_ns.response(401, "Invalid credentials")
    def post(self):
        data = request.json
        is_valid = UserService.verify_user(data["email"], data["password"])

        if not is_valid:
            return {"message": "Invalid credentials"}, 401
        
        role = UserService.get_role(data["email"])

        token = generate_token(data["email"], role)
        return {"access_token": token}

@v3_auth_ns.route("/password")
class ResetPassword(Resource):
    @v3_auth_ns.expect(change_pass_model)
    @v3_auth_ns.response(401, "Invalid credentials")
    @v3_auth_ns.doc(security="Bearer Auth")
    @require_jwt
    def post(self):
        data = request.json
        email = request.user["email"]
        new_password = data["password"]
        
        user = UserService.update_password(email, new_password)

        return {"msg": "Password changed"}
