from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from ..models.user import User
from ..extensions import db

def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = db.session.get(User, int(user_id))
        if not user:
            return jsonify({"code": 401, "message": "User no longer exists"}), 401
        return fn(current_user=user, *args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"code": 403, "message": "Admin access required"}), 403
        user_id = get_jwt_identity()
        user = db.session.get(User, int(user_id))
        if not user:
            return jsonify({"code": 401, "message": "User no longer exists"}), 401
        return fn(current_user=user, *args, **kwargs)
    return wrapper
