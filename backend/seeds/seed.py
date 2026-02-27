"""
Seed script — run with: python seeds/seed.py
Creates 1 admin, 2 regular users, and sample notes.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.note import Note
from app.utils.password_helper import hash_password

app = create_app()

def seed():
    with app.app_context():
        # Clear existing data (dev only)
        Note.query.delete()
        User.query.delete()
        db.session.commit()

        # Create admin
        admin = User(
            email="admin@notes.dev",
            password_hash=hash_password("Admin@1234"),
            role="admin",
        )

        # Create regular users
        alice = User(
            email="alice@notes.dev",
            password_hash=hash_password("Alice@1234"),
            role="user",
        )
        bob = User(
            email="bob@notes.dev",
            password_hash=hash_password("Bob@1234"),
            role="user",
        )

        db.session.add_all([admin, alice, bob])
        db.session.commit()

        # Create sample notes
        notes = [
            Note(user_id=alice.id, title="My First Note",
                 content="This is Alice's private note about her project ideas.",
                 is_private=True),
            Note(user_id=alice.id, title="Public Recipe",
                 content="Tomato pasta: boil pasta, add sauce, season well. Enjoy!",
                 is_private=False),
            Note(user_id=bob.id, title="Meeting Notes",
                 content="Discussed Q1 targets. Next meeting Friday 3pm.",
                 is_private=True),
            Note(user_id=bob.id, title="Travel Tips",
                 content="Pack light. Always carry a power bank. Book hotels early.",
                 is_private=False),
            Note(user_id=admin.id, title="System Config",
                 content="DB backup scheduled every Sunday 2AM. Monitor disk usage.",
                 is_private=True),
        ]

        for note in notes:
            note.set_tags(["sample", "seeded"])

        db.session.add_all(notes)
        db.session.commit()

        print("✅ Seed complete.")
        print(f"   admin@notes.dev     / Admin@1234")
        print(f"   alice@notes.dev     / Alice@1234")
        print(f"   bob@notes.dev       / Bob@1234")

if __name__ == "__main__":
    seed()
