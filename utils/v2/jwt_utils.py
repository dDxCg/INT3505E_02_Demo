import jwt
import uuid
from datetime import datetime, timedelta
from flask import make_response, request, current_app, jsonify
from functools import wraps
from db import REFRESH_STORE, ACCESS_JTI_BLACKLIST
from config import Config

JWT_SECRET_KEY = Config.JWT_SECRET_KEY
JWT_ALGO = Config.JWT_ALGO
ACCESS_EXPIRE_MINUTES = Config.ACCESS_EXPIRE_MINUTES
REFRESH_EXPIRE_DAYS = Config.REFRESH_EXPIRE_DAYS

def now():
    return datetime.utcnow()

def create_access_token(id, role, scopes) -> str:
    jti = str(uuid.uuid4())
    payload = {
        "id": id,
        "role": role,
        "scopes": scopes,
        "jti": jti,
        "exp": now() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGO)
    return token, jti

def create_refresh_token(id):
    rtid = str(uuid.uuid4())
    REFRESH_STORE[rtid] = {
        "id": id,
        "exp": now() + timedelta(days=REFRESH_EXPIRE_DAYS),
        "revoked": False,
        "used": False,
    }
    return rtid

def revoke_all_user_refresh(id):
    for k,v in REFRESH_STORE.items():
        if v["id"] == id:
            v["revoked"] = True

def verify_access_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGO])
    except jwt.ExpiredSignatureError:
        raise PermissionError("expired")
    except jwt.InvalidTokenError:
        raise PermissionError("invalid")
    if payload.get("jti") in ACCESS_JTI_BLACKLIST:
        raise PermissionError("revoked")
    return payload

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            return make_response(jsonify({"msg": "missing token"}), 401)
        # print(token)
        try:
            payload = verify_access_token(token)
        except PermissionError as e:
            return make_response(jsonify({"msg": str(e)}), 401)
        request.user = payload
        return f(*args, **kwargs)
    return wrapper