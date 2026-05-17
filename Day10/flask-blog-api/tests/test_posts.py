# tests/test_posts.py
def get_token(client):
    client.post("/api/auth/register", json={
        "username":"bob", "email":"b@example.com", "password":"secret123"
    })
    r = client.post("/api/auth/login", json={"username":"bob","password":"secret123"})
    return r.get_json()["access_token"]

def test_create_and_get_post(client):
    token = get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    # create
    resp = client.post("/api/posts/", json={"title":"My Post", "body":"Hello world"}, headers=headers)
    assert resp.status_code == 201
    post = resp.get_json()
    assert post["title"] == "My Post"

    # list
    resp = client.get("/api/posts/")
    assert resp.status_code == 200
    posts = resp.get_json()
    assert any(p["title"]=="My Post" for p in posts)
