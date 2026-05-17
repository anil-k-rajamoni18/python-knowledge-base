import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login(monkeypatch):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create user
        resp = await ac.post("/api/v1/users/", json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "testuser"
        assert "id" in data

        # Login
        resp = await ac.post("/api/v1/auth/login", data={
            "username": "testuser",
            "password": "testpassword"
        })
        assert resp.status_code == 200
        token_data = resp.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
