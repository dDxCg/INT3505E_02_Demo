from flask import current_app, jsonify, request
from flask_restx import Namespace, Resource, fields
from flask import make_response
from services.user_service import UserService
from utils.v2.jwt_utils import create_access_token, create_refresh_token, revoke_all_user_refresh, now, auth_required
from db import REFRESH_STORE, ACCESS_JTI_BLACKLIST
from extensions import limiter
from config import Config

ACCESS_EXPIRE_MINUTES = Config.ACCESS_EXPIRE_MINUTES

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
            return {"msg": "username/password required"}, 400
        is_valid = UserService.verify_user(data["email"], data["password"])
        if not is_valid:
            return {"msg": "Invalid credentials"}, 401
        id = UserService.get_id(e)
        role = UserService.get_role(e)
        
        #basic scopes logics:
        scopes = ["read", "write"] if role == "admin" else ["read"]

        #gen access/refresh token
        access, jti = create_access_token(id, role, scopes)
        rtid = create_refresh_token(id)
        
        res = make_response({"msg": "success"}, 200)
        res.set_cookie(
            "refresh_token",    
            rtid,
            httponly=True,
            samesite="Lax",
            # secure=True,  #HTTPS
            expires=REFRESH_STORE[rtid]["exp"])
        res.set_cookie(
            "access_token",
            access,
            httponly=True,
            samesite="Lax",
            max_age=ACCESS_EXPIRE_MINUTES * 60,
            # secure=True,  #HTTPS
        )
        return res
    
@v6_auth_ns.route("/logout")
class Logout(Resource):
    @auth_required
    def post(self):
        user_id = request.user["id"]
        revoke_all_user_refresh(user_id)
        if request.user.get("jti"):
            ACCESS_JTI_BLACKLIST.add(request.user["jti"])

        res = make_response({"msg": "logged out"}, 200)
        res.set_cookie("access_token", "", expires=0)
        res.set_cookie("refresh_token", "", expires=0)
        return res

@v6_auth_ns.route("/refresh")
class Refresh(Resource):
    @v6_auth_ns.doc(
        responses={
            200: "Success",
            401: "Unauthorized / Invalid Token",
            429: "Rate limit exceeded"
        },
        description="Rotate refresh token and issue a new access token"
    )
    @limiter.limit("5 per 10 minutes")
    def post(self):
        rtid = request.cookies.get("refresh_token")
        if not rtid:
            return make_response({"msg": "no refresh token"}, 401)
        record = REFRESH_STORE.get(rtid)
        
        # print(rtid)
        # print(REFRESH_STORE)
        
        if not record:
            return make_response({"msg": "invalid refresh token"}, 401)
        # expired or already used/revoked => possible reuse -> revoke all
        if record["exp"] < now() or record["revoked"] or record["used"]:
            revoke_all_user_refresh(record["username"])
            return make_response({"msg": "refresh invalid or reused. re-login required"}, 401)

        # valid: rotate
        record["used"] = True
        record["revoked"] = True

        id = record["id"]
        user = UserService.get_by_id(id)
        role = user.role
        
        #basic scopes logics:
        scopes = ["read", "write"] if role == "admin" else ["read"]

        new_rtid = create_refresh_token(id)
        access, jti = create_access_token(id, role, scopes)
        res = make_response({"msg": "refresh"}, 200)
        res.set_cookie(
            "refresh_token", 
            new_rtid,
            httponly=True,
            samesite="Lax",
            # secure=True, #HTTPS
            expires=REFRESH_STORE[new_rtid]["exp"])
        res.set_cookie(
            "access_token",
            access,
            httponly=True,
            samesite="Lax",
            max_age=ACCESS_EXPIRE_MINUTES * 60,
            # secure=True,  #HTTPS
        )
        return res

@v6_auth_ns.route("/password")
class ResetPassword(Resource):
    @v6_auth_ns.expect(change_pass_model)
    @v6_auth_ns.response(401, "Invalid credentials")
    @auth_required
    def put(self):
        data = request.json
        id = request.user["id"]
        user = UserService.get_by_id(id)
        email = user.email
        new_password = data["password"]
        
        user = UserService.update_password(email, new_password)

        return {"msg": "Password changed"}