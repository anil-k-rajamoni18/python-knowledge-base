# 🚀 DAY 9 — API Development with FastAPI


## 📌 1. Introduction to FastAPI

FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+.

### ⭐ Why FastAPI is preferred in industry?

- 🚀 Extremely fast (built on ASGI + uvicorn)
- 🔍 Built-in automatic Swagger & Redoc documentation
- 🎯 Strong type hints → better code quality
- 🛡 Pydantic-based validation
- 🧩 Dependency Injection system
- 🔌 Async-ready (very important for high-scale systems)

**Used by:** Microsoft, Netflix, Uber, Explosion (spaCy), state agencies.

---

## 📌 2. Installing & Running FastAPI

### 2.1 Install FastAPI + uvicorn

```bash
pip install fastapi uvicorn
```

### 2.2 Create a Basic App

**main.py**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
```

### 2.3 Run the server

```bash
uvicorn main:app --reload
```

---

## 📌 3. FastAPI Auto-Documentation (Swagger + Redoc)

Once your server is running, open:

**Swagger UI**
👉 http://127.0.0.1:8000/docs

**Redoc**
👉 http://127.0.0.1:8000/redoc

FastAPI automatically generates:
- ✔ API endpoints
- ✔ Input/output models
- ✔ Validation messages

---

## 📌 4. Request/Response Models using Pydantic

Pydantic is used to define data schemas and perform validation.

### 4.1 Define a Pydantic Model

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
```

### 4.2 Use model in an API Endpoint

```python
@app.post("/users")
def create_user(user: User):
    return {"msg": "User created", "data": user}
```

FastAPI automatically:
- Validates name, age, email
- Shows it in API docs
- Returns JSON

### 4.3 Optional, Default Values, Field Validation

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)
    in_stock: bool = True
```

---

## 📌 5. API Routes — GET, POST, PUT, DELETE

### ⭐ 5.1 GET

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### ⭐ 5.2 POST

```python
@app.post("/items")
def create_item(item: dict):
    return item
```

### ⭐ 5.3 PUT (Update)

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "new_data": item}
```

### ⭐ 5.4 DELETE

```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"status": "deleted", "id": item_id}
```

---

## 📌 6. Query Parameters

```python
@app.get("/search")
def search(q: str = None, limit: int = 10):
    return {"query": q, "limit": limit}
```

---

## 📌 7. Path Parameters

```python
@app.get("/users/{id}")
def get_user(id: int):
    return {"id": id}
```

---

## 📌 8. Dependency Injection (FastAPI Core Feature)

Dependency Injection helps create:
- ✔ Reusable logic
- ✔ Shared resources (db, auth, logs)
- ✔ Cleaner code

### 8.1 Basic Dependency

```python
from fastapi import Depends

def get_token():
    return "12345"

@app.get("/secure")
def secure_data(token: str = Depends(get_token)):
    return {"token": token}
```

### 8.2 Database Connection as Dependency

```python
def get_db():
    db = sqlite3.connect("tasks.db")
    try:
        yield db
    finally:
        db.close()
```

---

## 📌 9. Using SQLite with FastAPI

### 9.1 Setup Database

```python
import sqlite3

def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
```

### 9.2 Initialize Table

```python
def create_table():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

create_table()
```

---

## 📌 10. CRUD with SQLite + FastAPI

### 10.1 Pydantic Model

```python
class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
```

### 10.2 Create Task

```python
@app.post("/tasks")
def create_task(task: Task, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
        (task.title, task.description, task.completed)
    )
    db.commit()
    return {"message": "Task created"}
```

### 10.3 Read All Tasks

```python
@app.get("/tasks")
def read_tasks(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()
```

### 10.4 Update Task

```python
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE tasks SET title=?, description=?, completed=? WHERE id=?",
        (task.title, task.description, task.completed, task_id)
    )
    db.commit()
    return {"message": "Task updated"}
```

### 10.5 Delete Task

```python
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    db.commit()
    return {"message": "Task deleted"}
```

---

## 📌 11. Automatic Validation Errors

FastAPI automatically returns:
- 422 errors for wrong body
- Type mismatches
- Missing required fields

**Example:**

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "missing"
    }
  ]
}
```

---

## 📌 12. Async API Endpoints (Advanced)

FastAPI supports async handlers:

```python
@app.get("/async")
async def async_route():
    return {"message": "async works"}
```

**Async is useful when:**
- Calling external APIs
- Doing I/O heavy operations
- Non-blocking server behavior is needed

---

## 📌 13. Folder Structure for Production

```
task_api/
│── main.py
│── models.py
│── schemas.py
│── database.py
│── routes/
│     └── tasks.py
│── tests/
│── requirements.txt
```

---

## 📌 14. Mini Project: Task Manager REST API

### Features:

- ✔ Create Task
- ✔ Update Task
- ✔ Delete Task
- ✔ Get One Task
- ✔ Get All Tasks
- ✔ Validation (Pydantic)
- ✔ SQLite storage
- ✔ Swagger documentation
- ✔ Proper folder structure
- ✔ Dependency injection
- ✔ Error handling

### Your Task Manager API should include:

- Unique task IDs
- Validation for title length
- Filtering tasks by status (completed=true)
- Bulk delete completed tasks
- Mark task as completed (PATCH method)
- Return proper HTTP statuses