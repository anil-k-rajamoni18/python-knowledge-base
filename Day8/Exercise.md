# 🚀 DAY 8 — Real-Time Hands-On Practice Questions

---

## 🧩 SECTION 1 — SQLite Hands-On (File-Based DB)

### 1. Build a Student Marks Analyzer

Write Python code (SQLite + SQL queries) to:
- Create a table `marks(student_id, subject, score)`
- Insert marks for 5 students across 3 subjects
- Write SQL queries to:
  - Get average marks per student
  - Find the top scorer in Math
  - List all students failing (score < 40)

---

### 2. Inventory Manager

Create a CLI app that uses SQLite to:
- Add new items (name, category, quantity, price)
- Deduct stock while processing orders
- Generate low-stock alerts for items < 5
- Track total inventory value

---

### 3. Employee Attendance Tracker

Use SQLite + Python to:
- Record check-in/check-out times
- Calculate total hours worked per day
- Produce a weekly attendance summary
- Auto-generate a CSV report

---

## 🧩 SECTION 2 — PostgreSQL Hands-On (Production DB)

### 4. PostgreSQL: Build a Hotel Booking System (Without ORM)

Using `psycopg2`:

**Create tables:**
- `rooms(id, type, price, is_available)`
- `bookings(id, room_id, customer_name, start_date, end_date)`

**Write backend functions:**
- Get all available rooms
- Book a room
- Release room when booking ends
- Get total revenue for a date range

---

### 5. Employee Payroll System

In PostgreSQL:
- Create `employees` and `salaries` tables
- Insert sample data
- Write Python functions to:
  - Increase salary by 10% for all employees in a department
  - Get highest-paid employee
  - Generate monthly salary slip (returned as JSON)

---

### 6. Customer Segmentation Project

Using SQL queries:
- Query customers whose purchase value > 50,000
- Customers with no transactions in last 6 months
- Top 5 customers by lifetime value

Build an API-like Python function that returns results as dictionaries.

---

## 🧩 SECTION 3 — SQLAlchemy ORM Hands-On

### 7. Full ORM-Based Blog System

Using SQLAlchemy ORM:
- Define models: `User`, `Post`, `Comment`
- Create relationships
- Implement functions:
  - Add new post
  - Add comments to a post
  - Get all posts by a user
  - Delete a user → cascade delete posts + comments

---

### 8. ORM: Library Management System

**Tasks:**
- Model: `Book`, `Author`, `Loan`
- Add a validation rule:
  - Cannot loan a book if already loaned
- Find:
  - Most borrowed book
  - Author with highest number of books

---

### 9. Advanced SQLAlchemy Querying

Queries to write:
- Students with highest GPA
- Courses with no enrolled students
- Top 3 highest scoring students in a course

---

## 🧩 SECTION 4 — MongoDB Hands-On (Flexible DB)

### 10. Build a Movie Metadata System

Using `pymongo`:

**Insert movie documents with:**
- cast, director, rating, genres, year

**Query:**
- Movies with rating > 8
- All movies where "Tom Hanks" is in cast
- Count movies released after 2015
- Group by genre and count

---

### 11. Build an Activity Logging System

Insert user actions into a `logs` collection:

```json
{
  "user_id": 32,
  "action": "login",
  "timestamp": <datetime>,
  "device": "mobile"
}
```

**Tasks:**
- Get the last 10 actions by a user
- Find all users active in the last 24 hours
- Count total logins by device type
- Archive logs older than 30 days

---

### 12. E-Commerce Product Catalog

Collection: `products`

**Tasks:**
- Insert 20 products with attributes (dynamic fields allowed)
- Query:
  - Products with price between 500–1500
  - Products containing "Wireless" in title
  - Top 5 most viewed products
  - Update price for products in a category

---

## 🧩 SECTION 5 — MongoEngine (ODM) Hands-On

### 13. Create an Order Tracking System

**Define models:**
- `Order(id, customer_name, items, total, status, created_at)`
- `Item(name, quantity, price)`

**Tasks:**
- Insert an order with 3 items
- Update order status → shipped
- Compute total cost automatically
- Query all shipped orders

---

### 14. Build a Student Profile Database

**Model fields:**
- name
- age
- skills (list)
- scores (dict of subject → marks)

**Tasks:**
- Insert multiple students
- Query: Students who know Python AND scored > 80 in Math
- Add new skill to all students

---

## 🧩 SECTION 6 — Multi-Database Integration (Advanced Real-World)

### 15. Hybrid Analytics System (SQL + MongoDB)

**Use case:**
- SQL stores structured student records
- MongoDB stores click-stream data (behavioral logs)

**Tasks:**
- Fetch student profile from PostgreSQL
- Fetch browsing activity from MongoDB
- Build a combined report per student:
  - personal info
  - time spent on each page
  - most visited modules

---

### 16. Build a Unified Repository Layer (DAL)

**Write Python classes:**
- `SqlRepository`
- `MongoRepository`
- `HybridRepository`

**Features:**
- Common CRUD interface
- Hide DB-specific logic
- Return consistent formatted Python dictionaries

---

### 17. API Simulation: User Registration System

**Storage Rules:**
- PostgreSQL → user credentials
- MongoDB → user metadata + login logs

**Tasks:**
- Register new user
- Check if username already exists
- Log login event in MongoDB
- Fetch combined profile + activity report

---

## 🧩 SECTION 7 — Query Optimization & Indexing

### 18. PostgreSQL Optimization Task

Given slow queries:
- Add indexes
- Create materialized views
- Rewrite queries to improve speed

---

### 19. MongoDB Performance Optimization

**Tasks:**
- Create compound index on `(user_id, timestamp)`
- Analyze query performance with `.explain()`
- Compare performance before/after indexing

---

### 20. Build a Clean Folder Structure for Multi-DB App

Your directory should look like:

```
app/
├── db/
│   ├── sqlite_engine.py
│   ├── postgres_engine.py
│   ├── mongo_engine.py
│
├── models/
│   ├── orm_models.py
│   ├── mongo_models.py
│
├── crud/
│   ├── sql_crud.py
│   ├── mongo_crud.py
│
└── main.py
```