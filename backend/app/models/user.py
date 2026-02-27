from datetime import datetime, timezone
from ..extensions import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    notes = db.relationship("Note", backref="author", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "email": self.email, "role": self.role, "created_at": self.created_at.isoformat()}

    def __repr__(self):
        return f"<User {self.email}>"
