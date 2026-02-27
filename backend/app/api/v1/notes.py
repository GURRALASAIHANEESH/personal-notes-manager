from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import or_
from datetime import datetime, timezone
from ...extensions import db
from ...models.note import Note
from ...models.user import User
from ...schemas.note_schema import NoteCreateSchema, NoteUpdateSchema, validate_payload
from ...middleware.auth_middleware import jwt_required_custom

notes_bp = Blueprint("notes", __name__)
create_schema = NoteCreateSchema()
update_schema = NoteUpdateSchema()

@notes_bp.route("", methods=["POST"])
@jwt_required_custom
def create_note(current_user):
    data, errors = validate_payload(create_schema, request.get_json() or {})
    if errors:
        return jsonify({"code": 422, "message": "Validation failed", "errors": errors}), 422
    note = Note(user_id=current_user.id, title=data["title"].strip(),
                content=data["content"].strip(), is_private=data.get("is_private", True))
    note.set_tags(data.get("tags", []))
    db.session.add(note)
    db.session.commit()
    current_app.logger.info(f"Note created: id={note.id} by user={current_user.email}")
    return jsonify({"message": "Note created", "note": note.to_dict()}), 201

@notes_bp.route("", methods=["GET"])
@jwt_required_custom
def list_notes(current_user):
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 50)
    tag_filter = request.args.get("tag", "").strip().lower()
    search_query = request.args.get("q", "").strip()
    if current_user.role == "admin":
        query = Note.query
    else:
        query = Note.query.filter(or_(Note.user_id == current_user.id, Note.is_private == False))
    if tag_filter:
        query = query.filter(Note.tags.ilike(f"%{tag_filter}%"))
    if search_query:
        query = query.filter(or_(Note.title.ilike(f"%{search_query}%"), Note.content.ilike(f"%{search_query}%")))
    paginated = query.order_by(Note.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({"notes": [n.to_dict() for n in paginated.items],
                    "pagination": {"page": paginated.page, "per_page": paginated.per_page,
                                   "total": paginated.total, "pages": paginated.pages,
                                   "has_next": paginated.has_next, "has_prev": paginated.has_prev}}), 200

@notes_bp.route("/<int:note_id>", methods=["GET"])
@jwt_required_custom
def get_note(current_user, note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id and current_user.role != "admin" and note.is_private:
        return jsonify({"code": 403, "message": "Access denied"}), 403
    return jsonify({"note": note.to_dict()}), 200

@notes_bp.route("/<int:note_id>", methods=["PUT"])
@jwt_required_custom
def update_note(current_user, note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id and current_user.role != "admin":
        return jsonify({"code": 403, "message": "Access denied"}), 403
    data, errors = validate_payload(update_schema, request.get_json() or {})
    if errors:
        return jsonify({"code": 422, "message": "Validation failed", "errors": errors}), 422
    if "title" in data: note.title = data["title"].strip()
    if "content" in data: note.content = data["content"].strip()
    if "tags" in data: note.set_tags(data["tags"])
    if "is_private" in data: note.is_private = data["is_private"]
    note.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    current_app.logger.info(f"Note updated: id={note.id} by user={current_user.email}")
    return jsonify({"message": "Note updated", "note": note.to_dict()}), 200

@notes_bp.route("/<int:note_id>", methods=["DELETE"])
@jwt_required_custom
def delete_note(current_user, note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id and current_user.role != "admin":
        return jsonify({"code": 403, "message": "Access denied"}), 403
    db.session.delete(note)
    db.session.commit()
    current_app.logger.info(f"Note deleted: id={note_id} by user={current_user.email}")
    return jsonify({"message": "Note deleted"}), 200
