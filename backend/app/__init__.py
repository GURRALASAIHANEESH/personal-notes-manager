from flask import Flask, jsonify, request
from .config import get_config
from .extensions import db, migrate, jwt, bcrypt, cors, limiter
from .utils.logger import setup_logger


def create_app(config_override=None):
    app = Flask(__name__)

    cfg = config_override if config_override else get_config()
    app.config.from_object(cfg)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["FRONTEND_URL"]}})
    limiter.init_app(app)

    setup_logger(app)

    from .api.v1.auth import auth_bp
    from .api.v1.notes import notes_bp
    from .api.v1.ai import ai_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(notes_bp, url_prefix="/api/v1/notes")
    app.register_blueprint(ai_bp, url_prefix="/api/v1")

    @app.before_request
    def log_request():
        safe_headers = {k: v for k, v in request.headers if k != "Authorization"}
        app.logger.debug(f"-> {request.method} {request.path} | headers={safe_headers}")

    @app.after_request
    def log_response(response):
        app.logger.debug(f"<- {response.status_code} {request.method} {request.path}")
        return response

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"code": 400, "message": "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"code": 401, "message": "Unauthorized"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"code": 403, "message": "Forbidden"}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"code": 404, "message": "Resource not found"}), 404

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({"code": 422, "message": "Unprocessable entity"}), 422

    @app.errorhandler(429)
    def rate_limited(e):
        return jsonify({"code": 429, "message": "Too many requests"}), 429

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Internal error: {e}")
        return jsonify({"code": 500, "message": "Internal server error"}), 500

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_data):
        return jsonify({"code": 401, "message": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({"code": 401, "message": f"Invalid token: {reason}"}), 401

    @jwt.unauthorized_loader
    def missing_token(reason):
        return jsonify({"code": 401, "message": "Authorization token required"}), 401

    return app
