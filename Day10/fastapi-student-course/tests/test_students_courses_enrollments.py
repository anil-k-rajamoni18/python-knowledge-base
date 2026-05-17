import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_full_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 1) create user
        resp = await ac.post("/api/v1/users/", json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "alicepass"
        })
        assert resp.status_code == 200
        user = resp.json()

        # 2) login
        resp = await ac.post("/api/v1/auth/login", data={
            "username": "alice",
            "password": "alicepass"
        })
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3) create a student
        resp = await ac.post("/api/v1/students/", json={
            "full_name": "Alice Student",
            "email": "studentalice@example.com",
            "age": 21
        }, headers=headers)
        assert resp.status_code == 200
        student = resp.json()
        assert student["full_name"] == "Alice Student"

        # 4) create a course
        resp = await ac.post("/api/v1/courses/", json={
            "title": "Physics 101",
            "description": "Intro to Physics"
        }, headers=headers)
        assert resp.status_code == 200
        course = resp.json()
        assert course["title"] == "Physics 101"

        # 5) enroll student in course
        resp = await ac.post("/api/v1/enrollments/", json={
            "student_id": student["id"],
            "course_id": course["id"]
        }, headers=headers)
        assert resp.status_code == 200
        enrollment = resp.json()
        assert enrollment["student_id"] == student["id"]
        assert enrollment["course_id"] == course["id"]

        # 6) list enrollments
        resp = await ac.get("/api/v1/enrollments/", headers=headers)
        assert resp.status_code == 200
        enrollments = resp.json()
        assert isinstance(enrollments, list)
        assert any(e["id"] == enrollment["id"] for e in enrollments)
