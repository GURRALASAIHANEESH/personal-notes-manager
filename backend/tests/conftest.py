import pytest
from app import create_app
from app.config import TestingConfig
from app.extensions import db as _db
from app.models.user import User
from app.models.note import Note
from app.utils.password_helper import hash_password
from app.utils.jwt_helper import generate_token


@pytest.fixture(scope="session")
def app():
    _app = create_app(config_override=TestingConfig)
    with _app.app_context():
        _db.create_all()
        yield _app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    """Wipe tables before every test for isolation."""
    with app.app_context():
        _db.session.remove()
        Note.query.delete()
        User.query.delete()
        _db.session.commit()
    yield
    with app.app_context():
        _db.session.remove()
        Note.query.delete()
        User.query.delete()
        _db.session.commit()


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db


@pytest.fixture
def regular_user(app):
    with app.app_context():
        user = User(
            email="testuser@example.com",
            password_hash=hash_password("Test@1234"),
            role="user",
        )
        _db.session.add(user)
        _db.session.commit()
        _db.session.refresh(user)
        return user


@pytest.fixture
def admin_user(app):
    with app.app_context():
        user = User(
            email="admin@example.com",
            password_hash=hash_password("Admin@1234"),
            role="admin",
        )
        _db.session.add(user)
        _db.session.commit()
        _db.session.refresh(user)
        return user


@pytest.fixture
def user_token(regular_user):
    return generate_token(regular_user.id, regular_user.role)


@pytest.fixture
def admin_token(admin_user):
    return generate_token(admin_user.id, admin_user.role)


@pytest.fixture
def sample_note(app, regular_user):
    with app.app_context():
        note = Note(
            user_id=regular_user.id,
            title="Sample Note",
            content="Sample content for testing.",
            is_private=True,
        )
        note.set_tags(["test", "sample"])
        _db.session.add(note)
        _db.session.commit()
        _db.session.refresh(note)
        return note
