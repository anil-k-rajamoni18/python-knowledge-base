from fastapi import FastAPI
from models.user import User
app = FastAPI()

users = [] 

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return {"user_id": user, "data": users}
    return {"user_id": user_id, "data": {}}

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {"msg": "User created", "data": user}


@app.put("/users/{user_id}")
def update_user(user_id: int, inp_user: User):
    for user in users:
        if user["id"] == user_id:
            user['name'] = inp_user.name
            user['email'] = inp_user.email
            user['age'] = inp_user.age
            return {"msg": "updated user details", "data": users}
    return {"msg": f"user_id not found {user_id}"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user["id"] == user_id:
            users.pop(index)
            return {"mgs": f"user_id: {user_id} deleted"}
    return {"msg": f"user_id not found {user_id}"}
 

@app.get("/search")
def search(q: str = None, limit: int = 10):
    return {"query": q, "limit": limit}