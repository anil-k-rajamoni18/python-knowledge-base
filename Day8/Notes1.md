# 🚀 DAY 8 — Working with Databases (SQL & ORM)

Covers SQL concepts, SQLite fundamentals, SQLAlchemy ORM, workflows used in backend engineering, APIs, data engineering, and automation systems.

---

## 📌 1. INTRODUCTION TO DATABASES

A database is a structured storage system used to store, manage, and manipulate data.

Python commonly uses:

| Type | Examples | Notes |
|------|----------|-------|
| Relational (SQL) | SQLite, PostgreSQL, MySQL | Structured, uses tables |
| NoSQL | MongoDB, Redis | Flexible schemas |

For this module, we focus on:
- ✔ SQL
- ✔ SQLite
- ✔ SQLAlchemy ORM

---

## 🧩 2. Relational Database Concepts

### 2.1 Tables, Rows, Columns

- **Table** = like a spreadsheet
- **Row** = a record
- **Column** = field/attribute
- **Primary Key** = unique ID (e.g., `id`)
- **Foreign Key** = reference to another table

---

## 🧩 3. SQL BASICS — CRUD OPERATIONS

**CRUD = Create, Read, Update, Delete**

These are the core operations for any backend system.

### 3.1 CREATE — Insert Data

```sql
INSERT INTO students (name, age, grade)
VALUES ('Alice', 22, 'A');
```

### 3.2 READ — Select Data

```sql
SELECT name, grade FROM students;
```

**Filtering:**

```sql
SELECT * FROM students WHERE grade = 'A';
```

**Sorting:**

```sql
SELECT * FROM students ORDER BY age DESC;
```

### 3.3 UPDATE — Modify Data

```sql
UPDATE students
SET grade = 'B'
WHERE name = 'Alice';
```

### 3.4 DELETE — Remove Data

```sql
DELETE FROM students WHERE age < 20;
```

---

## 🧩 4. SQL JOINS (Must-Know for Real Projects)

Joins combine data from multiple tables.

### Example Tables

**students**
- id
- name
- course_id

**courses**
- id
- course_name
- student_id

### 4.1 INNER JOIN

Only records that exist in BOTH tables.

```sql
SELECT students.name, courses.course_name
FROM students
INNER JOIN courses
ON students.id = courses.student_id;
```

### 4.2 LEFT JOIN

All records from left table + matching right.

```sql
SELECT students.name, courses.course_name
FROM students
LEFT JOIN courses
ON students.id = courses.student_id;
```

### 4.3 RIGHT JOIN

(Available in PostgreSQL, NOT in SQLite)

### 4.4 FULL OUTER JOIN

All rows from both tables.
(SQLite doesn't support natively)

---

## 🧩 5. Working With SQLite (Python Built-In DB)

SQLite is:
- Serverless
- File-based (`.db` file)
- Fast for development/testing

Python module:

```python
import sqlite3
```

### 5.1 Connecting to Database

```python
conn = sqlite3.connect("school.db")
cursor = conn.cursor()
```

### 5.2 Creating a Table

```python
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    grade TEXT
)
""")
conn.commit()
```

### 5.3 Insert Data

```python
cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
               ("Alice", 22, "A"))
```

### 5.4 Fetch Data

```python
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)
```

### 5.5 Update

```python
cursor.execute("UPDATE students SET grade = ? WHERE id = ?", ("B", 1))
```

### 5.6 Delete

```python
cursor.execute("DELETE FROM students WHERE id = ?", (1,))
```

---

## 🧩 6. SQLAlchemy ORM — Industry Standard ORM

**ORM = Object Relational Mapping**

Maps Python classes → database tables
Maps Python objects → rows

Like:

| SQL Table | Python ORM |
|-----------|------------|
| students | Student class |
| row | Student object |

### 6.1 Install SQLAlchemy

```bash
pip install sqlalchemy
```

### 6.2 Create Engine

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///school.db")
```

### 6.3 ORM Base + Session

```python
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
```

---

## 🧩 7. Defining ORM Models

Define a Student table:

```python
from sqlalchemy import Column, Integer, String

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(String)

    def __repr__(self):
        return f"<Student(name={self.name}, grade={self.grade})>"
```

Create tables:

```python
Base.metadata.create_all(engine)
```

---

## 🧩 8. CRUD Using SQLAlchemy

### 8.1 CREATE (Insert)

```python
student = Student(name="Alice", age=22, grade="A")
session.add(student)
session.commit()
```

### 8.2 READ (Query)

```python
students = session.query(Student).all()
```

**Filtering:**

```python
session.query(Student).filter_by(grade="A").all()
```

### 8.3 UPDATE

```python
student = session.query(Student).filter_by(name="Alice").first()
student.grade = "B"
session.commit()
```

### 8.4 DELETE

```python
session.delete(student)
session.commit()
```

---

## 🧩 9. SQLAlchemy Relationships (Many-to-One, One-to-Many)

**Example:**
- Each student enrolled in one course
- A course has many students

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    course_name = Column(String)
    students = relationship("Student", back_populates="course")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="students")
```

---

## 🧩 10. Hands-On Exercises (Detailed)

### 1️⃣ CRUD operations in SQLite

Write Python scripts to:
- Create tables
- Insert multiple students
- Update grades
- Delete students
- Fetch with filters

### 2️⃣ ORM Models + Queries

**Tasks:**

Build Student and Course ORM classes

Insert 10 students, 3 courses

**Query:**
- All A-grade students
- Students in a specific course
- Youngest student
- Update a student's course

---

## 🧩 11. Mini Project — Student Database App (ORM Driven)

A complete CLI application that performs:
- ✔ Add Student
- ✔ List Students
- ✔ Update Student Info
- ✔ Delete Student
- ✔ Search by:
  - name
  - grade
  - course
- ✔ ORM + SQLite
- ✔ Clean folder structure
- ✔ DB auto-created
- ✔ Includes `requirements.txt`

### Structure:

```
student_app/
│── main.py
│── models.py
│── database.py
│── crud.py
│── school.db
```

### 🎯 Features to Include

- SQLAlchemy ORM
- CRUD operations
- Validation
- Search functionality
- Menu-driven CLI
- Pretty output
- Error handling