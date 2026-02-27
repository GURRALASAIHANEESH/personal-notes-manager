from flask import Blueprint, jsonify, current_app
from ...models.note import Note
from ...middleware.auth_middleware import jwt_required_custom
from ...utils.ai_helper import summarize_note, suggest_tags

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/notes/<int:note_id>/summarize", methods=["POST"])
@jwt_required_custom
def summarize(current_user, note_id):
    note = Note.query.get_or_404(note_id)

    # Permission check — owner or admin only
    if note.user_id != current_user.id and current_user.role != "admin":
        return jsonify({"code": 403, "message": "Access denied"}), 403

    try:
        summary = summarize_note(note.title, note.content)
        current_app.logger.info(f"AI summary generated for note={note_id} by user={current_user.email}")
        return jsonify({"note_id": note_id, "summary": summary}), 200
    except Exception as e:
        current_app.logger.error(f"Groq summarize error: {e}")
        return jsonify({"code": 503, "message": "AI service unavailable"}), 503


@ai_bp.route("/notes/<int:note_id>/suggest-tags", methods=["POST"])
@jwt_required_custom
def suggest(current_user, note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id != current_user.id and current_user.role != "admin":
        return jsonify({"code": 403, "message": "Access denied"}), 403

    try:
        tags = suggest_tags(note.title, note.content)
        current_app.logger.info(f"AI tags suggested for note={note_id} by user={current_user.email}")
        return jsonify({"note_id": note_id, "suggested_tags": tags}), 200
    except Exception as e:
        current_app.logger.error(f"Groq suggest-tags error: {e}")
        return jsonify({"code": 503, "message": "AI service unavailable"}), 503


@ai_bp.route("/stats", methods=["GET"])
@jwt_required_custom
def stats(current_user):
    """Dashboard stats — admin sees all, user sees own."""
    from ...models.user import User
    from ...extensions import db
    from sqlalchemy import func

    if current_user.role == "admin":
        total_notes = Note.query.count()
        private_notes = Note.query.filter_by(is_private=True).count()
        public_notes = Note.query.filter_by(is_private=False).count()
        total_users = User.query.count()
    else:
        total_notes = Note.query.filter_by(user_id=current_user.id).count()
        private_notes = Note.query.filter_by(user_id=current_user.id, is_private=True).count()
        public_notes = Note.query.filter_by(user_id=current_user.id, is_private=False).count()
        total_users = None

    # Most used tags for this user
    notes = Note.query.filter_by(user_id=current_user.id).all()
    tag_counts = {}
    for note in notes:
        for tag in note.get_tags():
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    result = {
        "total_notes": total_notes,
        "private_notes": private_notes,
        "public_notes": public_notes,
        "top_tags": [{"tag": t, "count": c} for t, c in top_tags],
    }
    if total_users is not None:
        result["total_users"] = total_users

    return jsonify(result), 200
