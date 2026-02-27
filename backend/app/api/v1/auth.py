from flask import Blueprint, request, jsonify, current_app
from ...extensions import db, limiter
from ...models.user import User
from ...schemas.auth_schema import RegisterSchema, LoginSchema, validate_payload
from ...utils.password_helper import hash_password, check_password
from ...utils.jwt_helper import generate_token

auth_bp = Blueprint("auth", __name__)
register_schema = RegisterSchema()
login_schema = LoginSchema()

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("10 per minute")
def register():
    data, errors = validate_payload(register_schema, request.get_json() or {})
    if errors:
        return jsonify({"code": 422, "message": "Validation failed", "errors": errors}), 422
    if User.query.filter_by(email=data["email"].lower()).first():
        return jsonify({"code": 409, "message": "Email already registered"}), 409
    user = User(email=data["email"].lower(), password_hash=hash_password(data["password"]), role="user")
    db.session.add(user)
    db.session.commit()
    current_app.logger.info(f"New user registered: {user.email} (id={user.id})")
    token = generate_token(user.id, user.role)
    return jsonify({"message": "Registration successful", "access_token": token, "user": user.to_dict()}), 201

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("20 per minute")
def login():
    data, errors = validate_payload(login_schema, request.get_json() or {})
    if errors:
        return jsonify({"code": 422, "message": "Validation failed", "errors": errors}), 422
    user = User.query.filter_by(email=data["email"].lower()).first()
    if not user or not check_password(data["password"], user.password_hash):
        current_app.logger.warning(f"Failed login attempt for: {data['email']}")
        return jsonify({"code": 401, "message": "Invalid email or password"}), 401
    current_app.logger.info(f"User logged in: {user.email} (id={user.id})")
    token = generate_token(user.id, user.role)
    return jsonify({"message": "Login successful", "access_token": token, "user": user.to_dict()}), 200
