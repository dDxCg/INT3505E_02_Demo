from functools import wraps
from flask import request
from utils.jwt_utils import decode_payload, extract_token_from_header

def require_jwt(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = extract_token_from_header()
        if not token:
            return {"message": "Missing or invalid token"}, 401
        
        payload = decode_payload(token)
        if not payload:
            return {"message": "Invalid or expired token"}, 401
        
        # attach payload (decoded JWT) to request
        request.user = payload
        return f(*args, **kwargs)
    return wrapper