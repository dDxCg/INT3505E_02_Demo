from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask import current_app
from services.user_service import UserService
from utils.v2.jwt_utils import create_access_token, create_refresh_token, revoke_all_user_refresh, now, auth_required
from db import REFRESH_STORE, ACCESS_JTI_BLACKLIST
from extensions import limiter

ACCESS_EXPIRE_MINUTES = current_app.config["ACCESS_EXPIRE_MINUTES"]

v6_auth_ns = Namespace("v6/auth", description="Authentication operations")

user_model = v6_auth_ns.model("UserRegister", {
    "email": fields.String(required=True, description="Unique email"),
    "password": fields.String(required=True)
})

change_pass_model = v6_auth_ns.model("ChangePassword", {
    "password": fields.String(required=True, description="New password"),
})


@v6_auth_ns.route("/register")
class Register(Resource):
    @v6_auth_ns.expect(user_model)
    @v6_auth_ns.response(201, "User created")
    def post(self):
        data = request.json
        user = UserService.create_user(data["email"], data["password"])
        return {"msg": "User created"}, 201
    
@v6_auth_ns.route("/login")
class Login(Resource):
    @v6_auth_ns.expect(user_model)
    @v6_auth_ns.doc(
        responses={
            401: "Invalid credentials",
            400: "username/password required"
        }
    )
    def post(self):
        data = request.json
        e = data["email"]
        p = data["password"]
        if not e or not p:
            return jsonify({"msg":"username/password required"}), 400
        is_valid = UserService.verify_user(data["email"], data["password"])
        if is_valid:
            return jsonify({"msg":"Invalid credentials"}), 401
        id = UserService.get_id(e)
        role = UserService.get_role(e)
        
        #basic scopes logics:
        if role == "admin":
            scopes = ["read", "write"]
        else:
            scopes = ["read"]

        #gen access/refresh token
        access, jti = create_access_token(id, role, scopes)
        rtid = create_access_token(id)

        
        res = jsonify({"access_token": access, "expires_in": ACCESS_EXPIRE_MINUTES*60})
        res.set_cookie("refresh_token", rtid,
                        httponly=True,
                        samesite="Lax",
                        # secure=True,  #HTTPS
                        expires=REFRESH_STORE[rtid]["exp"])
        return res
    
@v6_auth_ns.route("/logout")
class Logout(Resource):
    @v6_auth_ns.response(204, "logged out")
    def post(self):
        id = request.user["id"]
        revoke_all_user_refresh(id)
        
        if request.user.get("jti"):
            ACCESS_JTI_BLACKLIST.add(request.user["jti"])

        res = jsonify({"msg":"logged out"}), 204
        res.set_cookie("refresh_token","",expires=0)
        return res

@v6_auth_ns("/refresh")
class Refresh(Resource):
    @limiter.limit("5 per 10 minutes")
    def post(self):
        rtid = request.cookies.get("refresh_token")
        if not rtid:
            return jsonify({"msg":"no refresh token"}), 401
        record = REFRESH_STORE.get(rtid)
        if not record:
            return jsonify({"msg":"invalid refresh token"}), 401
        # expired or already used/revoked => possible reuse -> revoke all
        if record["expires_at"] < now() or record["revoked"] or record["used"]:
            revoke_all_user_refresh(record["username"])
            return jsonify({"msg":"refresh invalid or reused. re-login required"}), 401

        # valid: rotate
        record["used"] = True
        record["revoked"] = True

        id = record["id"]
        user = UserService.get_by_id(id)
        role = user["role"]
        
        #basic scopes logics:
        if role == "admin":
            scopes = ["read", "write"]
        else:
            scopes = ["read"]

        new_rtid = create_refresh_token(id)
        access, jti = create_access_token(id, role, user["scopes"])
        res = jsonify({"access_token": access, "expires_in": ACCESS_EXPIRE_MINUTES*60})
        res.set_cookie("refresh_token", new_rtid,
                        httponly=True,
                        samesite="Lax",
                        # secure=True, #HTTPS
                        expires=REFRESH_STORE[new_rtid]["exp"])
        return res

@v6_auth_ns.route("/password")
class ResetPassword(Resource):
    @v6_auth_ns.expect(change_pass_model)
    @v6_auth_ns.response(401, "Invalid credentials")
    @v6_auth_ns.doc(security="Bearer Auth")
    @auth_required
    def put(self):
        data = request.json
        email = request.user["email"]
        new_password = data["password"]
        
        user = UserService.update_password(email, new_password)

        return {"msg": "Password changed"}