# tests/test_auth.py
import json

def test_register_and_login(client):
    # register
    resp = client.post("/api/auth/register", json={
        "username":"alice", "email":"a@example.com", "password":"secret123"
    })
    assert resp.status_code == 201

    # register duplicate
    resp2 = client.post("/api/auth/register", json={
        "username":"alice", "email":"a@example.com", "password":"secret123"
    })
    assert resp2.status_code == 409

    # login
    resp = client.post("/api/auth/login", json={"username":"alice","password":"secret123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
