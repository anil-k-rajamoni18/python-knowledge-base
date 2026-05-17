# 🚀 PostgreSQL + MongoDB Integration with Python

Using `psycopg2`, SQLAlchemy (PostgreSQL engine), `pymongo`, and MongoEngine.

These additions reflect how modern backend systems use:
- **PostgreSQL** for structured relational data
- **MongoDB** for dynamic or semi-structured data

---

## 🧩 1. PostgreSQL Integration with Python

PostgreSQL is widely used for:
- ✔ Production systems
- ✔ High-performance APIs
- ✔ Applications requiring strong data consistency
- ✔ Systems with complex queries

Python supports PostgreSQL through:
- `psycopg2` (low-level driver)
- SQLAlchemy + `psycopg2` (ORM)

### ⭐ 1.1 Installing PostgreSQL

Install PostgreSQL:
- **macOS** → Homebrew
- **Windows** → Installer
- **Linux** → apt/yum

Then create a database:

```sql
CREATE DATABASE school;
```

### ⭐ 1.2 psycopg2 Installation

```bash
pip install psycopg2 psycopg2-binary
```

### ⭐ 1.3 Connecting to PostgreSQL Using psycopg2

```python
import psycopg2

conn = psycopg2.connect(
    dbname="school",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
```

### ⭐ 1.4 Create Table in PostgreSQL

```python
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    grade VARCHAR(2)
)
""")
conn.commit()
```

### ⭐ 1.5 Insert Data

```python
cursor.execute(
    "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)",
    ("John", 20, "A")
)
conn.commit()
```

### ⭐ 1.6 Fetch Data

```python
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
print(rows)
```

### ⭐ 1.7 Update

```python
cursor.execute(
    "UPDATE students SET grade=%s WHERE id=%s",
    ("B", 1)
)
conn.commit()
```

### ⭐ 1.8 Delete

```python
cursor.execute("DELETE FROM students WHERE id=%s", (1,))
conn.commit()
```

### ⭐ 1.9 Closing PostgreSQL Connection

```python
cursor.close()
conn.close()
```

---

## 🧩 2. Using PostgreSQL with SQLAlchemy (ORM)

### ⭐ 2.1 Install Required Packages

```bash
pip install sqlalchemy psycopg2
```

### ⭐ 2.2 Create Engine

```python
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/school")
```

### ⭐ 2.3 Define Student Model (Same ORM as SQLite)

```python
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(String)

Base.metadata.create_all(engine)
```

Everything else (CRUD) is same as SQLite ORM.

---

## 🧩 3. MongoDB Integration with Python

MongoDB is ideal for:
- ✔ Logs
- ✔ Dynamic data (user preferences, product metadata)
- ✔ Schemaless storage
- ✔ Fast reads/writes
- ✔ Large-scale distributed systems

### ⭐ 3.1 Install MongoDB + Tools

MongoDB Community Edition or Atlas Cloud DB.

**Python Driver:**

```bash
pip install pymongo
```

### ⭐ 3.2 Connect to MongoDB (Local)

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["school"]
students = db["students"]
```

### ⭐ 3.3 Insert Document

```python
students.insert_one({
    "name": "Alice",
    "age": 22,
    "grade": "A",
    "skills": ["Python", "SQL"]
})
```

### ⭐ 3.4 Find Documents

**Find all:**

```python
for s in students.find():
    print(s)
```

**Filter:**

```python
students.find_one({"name": "Alice"})
```

### ⭐ 3.5 Update Document

```python
students.update_one(
    {"name": "Alice"},
    {"$set": {"grade": "B"}}
)
```

### ⭐ 3.6 Delete Document

```python
students.delete_one({"name": "Alice"})
```

### ⭐ 3.7 Query Operators (Very Important)

**Example:** find students with age > 20

```python
students.find({"age": {"$gt": 20}})
```

### ⭐ 3.8 Working with Arrays

```python
students.find({"skills": "Python"})
```

### ⭐ 3.9 Indexing in MongoDB

```python
students.create_index("name")
```

Indexes significantly speed up queries.

---

## 🧩 4. MongoEngine — ODM for MongoDB

- **ORM** = SQL (tables)
- **ODM** = MongoDB (documents)

**Install:**

```bash
pip install mongoengine
```

### ⭐ 4.1 Connect

```python
from mongoengine import connect

connect("school", host="localhost")
```

### ⭐ 4.2 Define Document Model

```python
from mongoengine import Document, StringField, IntField, ListField

class Student(Document):
    name = StringField()
    age = IntField()
    grade = StringField()
    skills = ListField(StringField())
```

### ⭐ 4.3 Insert Document

```python
s = Student(name="Bob", age=21, grade="A", skills=["Python"])
s.save()
```

### ⭐ 4.4 Query

```python
Student.objects(grade="A")
```

### ⭐ 4.5 Update

```python
Student.objects(name="Bob").update_one(set__grade="B")
```

### ⭐ 4.6 Delete

```python
Student.objects(name="Bob").delete()
```

---

## 🧩 5. When to Use What? (Real Industry Comparison)

| Task | PostgreSQL | MongoDB |
|------|------------|---------|
| Banking | ✔ Required | ❌ |
| Structured data | ✔ | ❌ |
| Flexible schema | ❌ | ✔ |
| Real-time analytics | ✔ | ✔ |
| Logs / telemetry | ❌ | ✔ |
| Highly relational data | ✔ | ❌ |
| IoT, events | ❌ | ✔ |

---

## 🧩 6. Add to Your Student Database Mini Project

Extend your project so that:
- ✔ Local SQLite = used by CLI App
- ✔ PostgreSQL = used in production mode
- ✔ MongoDB = used for logging or metadata

### Example Architecture

```
student_app/
│── database/
│     ├── sqlite_engine.py
│     ├── postgres_engine.py
│     ├── mongo_engine.py
│
│── orm_models.py
│── mongo_models.py
│── crud_sql.py
│── crud_mongo.py
│── main.py
```