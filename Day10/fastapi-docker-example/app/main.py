from fastapi import FastAPI

app = FastAPI()

users = [] 

@app.get("/")
def home():
    return {"message": "Hello, FastAPI running inside Docker 🚀!"}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}


@app.post("/user/")
def create_user(user: dict):
    users.append(user)
    return user

@app.get("/users/")
def list_users():
    return users


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    global users
    users = [user for user in users if user["id"] != user_id]
    return {"message": "User deleted"}

@app.put("/user/{user_id}")
def update_user(user_id: int, updated_user: dict):
    for index, user in enumerate(users):
        if user["id"] == user_id:
            users[index] = updated_user
            return updated_user
    return {"error": "User not found"}