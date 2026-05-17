# Student–Course Management System (Flask)

## 1. Project Title

**Student–Course Management System Using Flask**

---

## 2. Abstract

The Student–Course Management System is a web-based application built using the Flask framework to simplify the management of students, courses, and enrollments. It allows administrators to add and manage students and courses, while students can log in, view available courses, and enroll. The system aims to reduce paperwork, streamline academic record keeping, and provide a centralized dashboard for academic administration.

---

## 3. Introduction

Educational institutions manage large amounts of data related to students, courses, and their enrollments. Traditional paper-based approaches often lead to errors, inconsistency, and inefficiency.

This project introduces an online platform that automates:

- Student registration
- Course creation and management
- Enrollment process
- Real-time updates on academic data

Flask is chosen for its lightweight, modular, and efficient architecture for building scalable web applications.

---

## 4. Objectives

- Provide a centralized platform for managing students and courses
- Enable students to enroll in courses easily
- Allow administrators to perform CRUD operations
- Maintain accurate academic records
- Improve efficiency and reduce manual errors

---

## 5. Scope

The project is suitable for:

- Schools
- Colleges
- Online training institutes
- Any learning center requiring digital course/student management

**Functions include:**

- User authentication
- Admin dashboard
- Enrollments management
- Course lists
- Student lists

---

## 6. System Architecture

### Architecture Diagram (Conceptual)

```
                +------------------------+
                |        Browser         |
                | (User/Admin Interface) |
                +-----------+------------+
                            |
                            v
                +------------------------+
                |       Flask App        |
                |  Routing & Controllers |
                +-----------+------------+
                            |
               +------------+------------+
               |                         |
               v                         v
+---------------------------+   +---------------------------+
|   Business Logic Layer    |   | Authentication Middleware |
+---------------------------+   +---------------------------+
                            |
                            v
                +------------------------+
                |     Database Layer     |
                |     (SQLite/MySQL)     |
                +------------------------+
```

---

## 7. Functional Requirements

### Admin Features

- Login/Logout
- Add/Edit/Delete Students
- Add/Edit/Delete Courses
- View all enrollments
- Dashboard analytics

### Student Features

- Login/Logout
- View courses
- Enroll in a course
- View enrolled courses

---

## 8. Non-Functional Requirements

- **Security:** Password hashing using Werkzeug
- **Performance:** Fast CRUD operations
- **Usability:** Clean UI using Bootstrap
- **Scalability:** Supports migration to larger databases

---

## 9. Technology Stack

### Frontend

- HTML5
- CSS3
- Bootstrap
- JavaScript

### Backend

- Python 3.x
- Flask Framework
- Jinja2 Templates

### Database

- SQLite (for development)
- Can be upgraded to MySQL/PostgreSQL

### Tools

- Postman
- Git/GitHub
- VS Code or PyCharm

---

## 10. Database Design (ER Diagram Description)

### Entities

- Student
- Course
- Enrollment
- User (Admin/Student)

### Relationships

- A student can enroll in multiple courses
- A course can have multiple students
- Many-to-many relationship implemented through Enrollment table

---

## 11. Database Schema

### users table

| Column   | Type       | Description      |
|----------|------------|------------------|
| id       | Integer PK | User ID          |
| username | Text       | Login username   |
| password | Text       | Hashed password  |
| role     | Text       | admin/student    |

### students table

| Column     | Type       | Description        |
|------------|------------|--------------------|
| id         | Integer PK | Student ID         |
| name       | Text       | Student name       |
| email      | Text       | Unique email       |
| department | Text       | Student department |

### courses table

| Column      | Type       | Description         |
|-------------|------------|---------------------|
| id          | Integer PK | Course ID           |
| name        | Text       | Course title        |
| description | Text       | Course description  |

### enrollments table

| Column     | Type       | Description   |
|------------|------------|---------------|
| id         | Integer PK | Enrollment ID |
| student_id | Integer FK | Student       |
| course_id  | Integer FK | Course        |

---

## 12. Module Description

### 1. Authentication Module

- Login
- Logout
- Session handling
- Role-based access (admin/student)

### 2. Student Management Module

- Add, Edit, Delete students
- View all students

### 3. Course Management Module

- Add, Edit, Delete courses
- View list of courses

### 4. Enrollment Module

- Students enroll in courses
- Admin monitors enrollments
- Prevent duplicate enrollments

### 5. Dashboard Module

- Basic analytics
- Total students
- Total courses
- Total enrollments

---

## 13. System Workflow

### Admin Workflow

1. Admin logs in
2. Manages students
3. Manages courses
4. Views total enrollments
5. Logs out

### Student Workflow

1. Student logs in
2. Views available courses
3. Enrolls in chosen courses
4. Views enrollment list
5. Logs out

---

## 14. API Specifications

### 1. `/login` (POST)

- **Purpose:** Authenticate user
- **Params:** username, password

### 2. `/students` (GET)

- **Purpose:** List all students

### 3. `/add_student` (POST)

- **Purpose:** Create student record

### 4. `/courses` (GET)

- **Purpose:** List all courses

### 5. `/enroll` (POST)

- **Purpose:** Add new enrollment

---

## 15. User Interface (Screen Description)

### 1. Login Page

- Username & Password fields
- Role-based access

### 2. Admin Dashboard

Displays:
- Total Students
- Total Courses
- Total Enrollments

### 3. Student Management Page

- Table of students
- Edit/Delete buttons
- Add student form

### 4. Course Management Page

- Table of courses
- Edit/Delete buttons
- Add course form

### 5. Student Course Enrollment Page

- Course list
- Enroll button
- Displays enrolled courses

---

## 16. Testing

### Types of Tests

- Unit Testing
- Integration Testing
- UI Testing
- Database Testing

### Test Cases Include

- Login validation
- Duplicate student creation
- Course enrollment edge cases
- Viewing student lists
- Admin access control

---

## 17. Security Measures

- Password hashing
- Protected admin routes
- Input validation
- CSRF protection (Flask-WTF optional)

---

## 18. Future Enhancements

- Email/SMS notifications
- Payment integration for courses
- Attendance tracking
- Role upgrades (teacher, parent)
- Student performance analytics
- REST API for mobile app

---

## 19. Conclusion

The Student–Course Management System simplifies academic workflows and provides efficient digital management of students, courses, and enrollments. Built with Flask, the project is scalable, secure, and easily extensible to support future educational needs.

---

## 20. References

- Flask official documentation
- Bootstrap documentation
- SQLite documentation