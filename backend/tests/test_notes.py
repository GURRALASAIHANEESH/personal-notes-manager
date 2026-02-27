import pytest


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


class TestCreateNote:
    def test_create_success(self, client, db, user_token):
        res = client.post("/api/v1/notes", json={
            "title": "My Note",
            "content": "Some content here.",
            "tags": ["flask", "python"],
            "is_private": True
        }, headers=auth_header(user_token))
        assert res.status_code == 201
        data = res.get_json()
        assert data["note"]["title"] == "My Note"
        assert "flask" in data["note"]["tags"]

    def test_create_no_auth(self, client, db):
        res = client.post("/api/v1/notes", json={"title": "X", "content": "Y"})
        assert res.status_code == 401

    def test_create_missing_title(self, client, db, user_token):
        res = client.post("/api/v1/notes", json={"content": "No title"},
                          headers=auth_header(user_token))
        assert res.status_code == 422


class TestListNotes:
    def test_list_own_notes(self, client, db, user_token, sample_note):
        res = client.get("/api/v1/notes", headers=auth_header(user_token))
        assert res.status_code == 200
        data = res.get_json()
        assert "notes" in data
        assert "pagination" in data

    def test_admin_sees_all(self, client, db, admin_token, sample_note):
        res = client.get("/api/v1/notes", headers=auth_header(admin_token))
        assert res.status_code == 200

    def test_search_by_query(self, client, db, user_token, sample_note):
        res = client.get("/api/v1/notes?q=Sample", headers=auth_header(user_token))
        assert res.status_code == 200
        notes = res.get_json()["notes"]
        assert any("Sample" in n["title"] for n in notes)

    def test_filter_by_tag(self, client, db, user_token, sample_note):
        res = client.get("/api/v1/notes?tag=test", headers=auth_header(user_token))
        assert res.status_code == 200

    def test_pagination(self, client, db, user_token, sample_note):
        res = client.get("/api/v1/notes?page=1&per_page=5", headers=auth_header(user_token))
        assert res.status_code == 200
        assert res.get_json()["pagination"]["per_page"] == 5


class TestNoteDetail:
    def test_get_own_note(self, client, db, user_token, sample_note):
        res = client.get(f"/api/v1/notes/{sample_note.id}", headers=auth_header(user_token))
        assert res.status_code == 200

    def test_get_private_note_other_user(self, client, db, admin_token, sample_note):
        # Admin can always view
        res = client.get(f"/api/v1/notes/{sample_note.id}", headers=auth_header(admin_token))
        assert res.status_code == 200

    def test_get_nonexistent_note(self, client, db, user_token):
        res = client.get("/api/v1/notes/99999", headers=auth_header(user_token))
        assert res.status_code == 404


class TestUpdateNote:
    def test_update_own_note(self, client, db, user_token, sample_note):
        res = client.put(f"/api/v1/notes/{sample_note.id}",
                         json={"title": "Updated Title"},
                         headers=auth_header(user_token))
        assert res.status_code == 200
        assert res.get_json()["note"]["title"] == "Updated Title"

    def test_update_other_user_note_forbidden(self, client, db, admin_token, sample_note):
        # Admin CAN update — test that non-owner regular user CANNOT
        from app.models.user import User
        from app.utils.password_helper import hash_password
        from app.utils.jwt_helper import generate_token
        other = User(email="other@x.com", password_hash=hash_password("Other@1234"), role="user")
        from app.extensions import db as _db
        _db.session.add(other)
        _db.session.commit()
        other_token = generate_token(other.id, other.role)
        res = client.put(f"/api/v1/notes/{sample_note.id}",
                         json={"title": "Hijack"},
                         headers=auth_header(other_token))
        assert res.status_code == 403


class TestDeleteNote:
    def test_delete_own_note(self, client, db, user_token, sample_note):
        res = client.delete(f"/api/v1/notes/{sample_note.id}",
                            headers=auth_header(user_token))
        assert res.status_code == 200

    def test_delete_nonexistent(self, client, db, user_token):
        res = client.delete("/api/v1/notes/99999", headers=auth_header(user_token))
        assert res.status_code == 404
