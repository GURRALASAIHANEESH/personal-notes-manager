"""
Integration test: Full register → login → create note → list → update → delete flow
Hits real test DB (SQLite in memory via TestingConfig).
"""


def test_full_notes_lifecycle(client, db):
    # 1. Register
    reg = client.post("/api/v1/auth/register", json={
        "email": "integration@example.com",
        "password": "Integrate@99"
    })
    assert reg.status_code == 201
    token = reg.get_json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Login with same credentials
    login = client.post("/api/v1/auth/login", json={
        "email": "integration@example.com",
        "password": "Integrate@99"
    })
    assert login.status_code == 200
    assert "access_token" in login.get_json()

    # 3. Create a note
    create = client.post("/api/v1/notes", json={
        "title": "Integration Test Note",
        "content": "Testing full lifecycle.",
        "tags": ["integration"],
        "is_private": False
    }, headers=headers)
    assert create.status_code == 201
    note_id = create.get_json()["note"]["id"]

    # 4. List notes — should include created note
    listing = client.get("/api/v1/notes", headers=headers)
    assert listing.status_code == 200
    ids = [n["id"] for n in listing.get_json()["notes"]]
    assert note_id in ids

    # 5. Get note detail
    detail = client.get(f"/api/v1/notes/{note_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.get_json()["note"]["title"] == "Integration Test Note"

    # 6. Update note
    update = client.put(f"/api/v1/notes/{note_id}",
                        json={"title": "Updated Integration Note"},
                        headers=headers)
    assert update.status_code == 200
    assert update.get_json()["note"]["title"] == "Updated Integration Note"

    # 7. Delete note
    delete = client.delete(f"/api/v1/notes/{note_id}", headers=headers)
    assert delete.status_code == 200

    # 8. Confirm deleted
    gone = client.get(f"/api/v1/notes/{note_id}", headers=headers)
    assert gone.status_code == 404
