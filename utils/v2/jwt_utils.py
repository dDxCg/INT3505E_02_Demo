import jwt
import uuid
from datetime import datetime, timedelta
from flask import request, current_app, jsonify
from functools import wraps
from db import REFRESH_STORE, ACCESS_JTI_BLACKLIST

JWT_SECRET_KEY = current_app.config["JWT_SECRET_KEY"]
JWT_ALGO = current_app.config["JWT_ALGO"]
ACCESS_EXPIRE_MINUTES = current_app.config["ACCESS_EXPIRE_MINUTES"]
REFRESH_EXPIRE_DAYS = current_app.config["REFRESH_EXPIRE_DAYS"]

def now():
    return datetime.utcnow()

def create_access_token(id, role, scopes) -> str:
    jti = str(uuid.uuidv4())
    payload = {
        "id": id,
        "role": role,
        "scpoes": scopes,
        "jti": jti,
        "exp": int((now() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)).timestamp())
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGO)
    return token. jti

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
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"msg":"missing token"}), 401
        token = auth.split(" ",1)[1]
        try:
            payload = verify_access_token(token)
        except PermissionError as e:
            return jsonify({"msg": str(e)}), 401
        request.user = payload
        return f(*args, **kwargs)
    return wrapper