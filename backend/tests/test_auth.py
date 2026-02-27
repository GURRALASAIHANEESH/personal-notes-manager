import pytest


class TestRegister:
    def test_register_success(self, client, db):
        res = client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "password": "Secure@123"
        })
        assert res.status_code == 201
        data = res.get_json()
        assert "access_token" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["role"] == "user"

    def test_register_duplicate_email(self, client, db, regular_user):
        res = client.post("/api/v1/auth/register", json={
            "email": "testuser@example.com",
            "password": "Secure@123"
        })
        assert res.status_code == 409
        assert "already registered" in res.get_json()["message"]

    def test_register_invalid_email(self, client, db):
        res = client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "password": "Secure@123"
        })
        assert res.status_code == 422

    def test_register_short_password(self, client, db):
        res = client.post("/api/v1/auth/register", json={
            "email": "short@example.com",
            "password": "123"
        })
        assert res.status_code == 422

    def test_register_missing_fields(self, client, db):
        res = client.post("/api/v1/auth/register", json={})
        assert res.status_code == 422


class TestLogin:
    def test_login_success(self, client, db, regular_user):
        res = client.post("/api/v1/auth/login", json={
            "email": "testuser@example.com",
            "password": "Test@1234"
        })
        assert res.status_code == 200
        assert "access_token" in res.get_json()

    def test_login_wrong_password(self, client, db, regular_user):
        res = client.post("/api/v1/auth/login", json={
            "email": "testuser@example.com",
            "password": "WrongPass"
        })
        assert res.status_code == 401

    def test_login_nonexistent_user(self, client, db):
        res = client.post("/api/v1/auth/login", json={
            "email": "ghost@example.com",
            "password": "NoUser@123"
        })
        assert res.status_code == 401

    def test_login_missing_fields(self, client, db):
        res = client.post("/api/v1/auth/login", json={"email": "x@x.com"})
        assert res.status_code == 422
