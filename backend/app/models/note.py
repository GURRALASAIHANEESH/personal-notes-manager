from datetime import datetime, timezone
from ..extensions import db

class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500), nullable=True, default="")
    is_private = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def get_tags(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    def set_tags(self, tag_list):
        self.tags = ",".join([t.strip().lower() for t in tag_list if t.strip()])

    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "title": self.title, "content": self.content,
                "tags": self.get_tags(), "is_private": self.is_private,
                "created_at": self.created_at.isoformat(), "updated_at": self.updated_at.isoformat()}

    def __repr__(self):
        return f"<Note {self.id}: {self.title[:30]}>"
