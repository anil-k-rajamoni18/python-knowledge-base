# Flask Blog API - Complete Documentation

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Production-Grade Folder Structure](#-production-grade-folder-structure)
- [Quick Start Guide](#-quick-start-guide)
- [OpenAPI Documentation](#-openapi-documentation-swagger)
- [Testing](#-testing-with-pytest)
- [Deployment Guides](#-deployment-guides)
  - [Render.com](#-deployment-guide--rendercom)
  - [Railway.app](#-deployment-guide--railwayapp)
- [Deployment Notes](#-deployment-notes)
- [Notes & Next Steps](#-notes--next-steps)

---

## 🧩 Project Overview

This project is a full-scale backend application built using **Flask**, **JWT authentication**, **CORS**, **SQLAlchemy ORM**, and **SQLite/PostgreSQL**.

### Features

#### ✔ Users
* Signup / Login
* Profile
* Admin role

#### ✔ Posts
* Create, read, update, delete
* Pagination
* Author-only edit/delete

#### ✔ Comments
* Add comments under posts
* Delete own comments

#### ✔ Authentication
* JWT Access Tokens
* Protect routes
* Admin-only actions

#### ✔ Additional Features
* Background jobs
* Rate limiting
* Clean production folder structure
* Pytest testing
* Deployment to Render & Railway
* Optional Docker setup

---

## 🏗 Production-Grade Folder Structure

```
flask-blog-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── extensions.py
│   ├── auth/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── posts/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── comments/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── admin/
│   │   └── routes.py
│   └── utils.py
├── migrations/   # optional if using Flask-Migrate
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_posts.py
├── .env.example
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── README.md
```

---

## 🚀 Quick Start Guide

### Quick Run Instructions (Development)

#### 1. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# optionally edit .env
```

#### 2. Initialize DB & Run

```bash
export FLASK_APP=manage.py
flask run
# or
python manage.py
```

#### 3. Test the API

1. Use `POST /api/auth/register` to create a user
2. Then `/api/auth/login` to get JWT token
3. Use `/api/posts/` endpoints with the JWT token

---

## 📄 OpenAPI Documentation (Swagger)

Flask itself does not generate Swagger automatically, so here is a complete OpenAPI 3.0 spec you can include in a file `openapi.yaml` or `openapi.json`.

### Visualization Tools

You can use tools like:
- **Swagger UI**
- **Redoc**
- **Stoplight Studio**
- **Insomnia**
- **Hoppscotch**

### Full OpenAPI 3.0 Specification

```yaml
openapi: 3.0.0
info:
  title: Flask Blog API
  version: 1.0.0
  description: A lightweight blog API using Flask + JWT + SQLite.

servers:
  - url: http://localhost:5000/api

paths:

  /signup:
    post:
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username: { type: string }
                password: { type: string }
      responses:
        200:
          description: User created

  /login:
    post:
      summary: User login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username: { type: string }
                password: { type: string }
      responses:
        200:
          description: JWT generated
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token: { type: string }

  /posts:
    get:
      summary: Get all posts
      responses:
        200:
          description: List all posts
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Post'

    post:
      summary: Create a post
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PostCreate'
      responses:
        200:
          description: Post created

components:
  schemas:

    Post:
      type: object
      properties:
        id: { type: integer }
        title: { type: string }
        body: { type: string }

    PostCreate:
      type: object
      required: [title, body]
      properties:
        title: { type: string }
        body: { type: string }

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Adding Swagger UI to Flask

Install the required package:

```bash
pip install flask-swagger-ui
```

---

## 🧪 Testing with Pytest

### Run Tests

```bash
pytest -q
```

### Test Files Structure

- `tests/conftest.py` - Test configuration and fixtures
- `tests/test_auth.py` - Authentication tests
- `tests/test_posts.py` - Posts endpoint tests

---

## 🚀 Deployment Guides

Step-by-step instructions for deploying to **Render** and **Railway** (Both Included).

---

## 🟦 Deployment Guide — Render.com

### 1. Create Your Repository

Push the generated ZIP contents to GitHub:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your_repo_url>
git push -u origin main
```

### 2. Create a New Web Service

1. Go to: [https://dashboard.render.com](https://dashboard.render.com)
2. Click **New → Web Service**
3. Choose your repository

### 3. Configure Build Settings

| Setting | Value |
|---------|-------|
| Runtime | Python |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn run:app` |
| Environment | Python 3.10+ |

### 4. Add Environment Variables

Go to **Environment → Add Variable**:

```
JWT_SECRET_KEY = your-secret
```

**Optional:** If using a hosted PostgreSQL:

```
DATABASE_URL = postgresql://user:pass@host:port/dbname
```

### 5. Deploy

Click **Deploy** → Render builds + deploys automatically.

### ✨ Optional: Use Render PostgreSQL

1. Add **New → PostgreSQL**
2. Copy connection string
3. Replace:
   ```python
   sqlite:///blog.db
   ```
   with:
   ```python
   os.environ.get("DATABASE_URL")
   ```

---

## 🟩 Deployment Guide — Railway.app

Railway is even easier for Flask apps.

### 1. Upload Your GitHub Repo

1. Go to: [https://railway.app/dashboard](https://railway.app/dashboard)
2. Click: **New Project → Deploy from GitHub Repo**

### 2. Railway Auto-Detects Python

You will see:
```
✔ Detected: Python
✔ Installing dependencies
```

### 3. Add Environment Variables

Go to: **Variables → Add**

```
JWT_SECRET_KEY = your-secret
```

If using Railway PostgreSQL:

```
DATABASE_URL = <railway provided>
```

Railway automatically injects the connection URL when you create a PostgreSQL DB.

### 4. Add a Start Command

In **Service → Settings → Start Command**:

```bash
gunicorn run:app
```

### 5. Railway Provisions the Database

1. **Railway → New → PostgreSQL**
2. Use the variable:
   ```
   DATABASE_URL
   ```

No extra config needed.

### 6. Deploy

Hit **Deploy** and Railway does the rest.

---

## 📦 Deployment Notes

### General Deployment Considerations

- **Render / Railway**: Both support Docker. Build docker image and deploy container. For SQLite in production, switch to PostgreSQL and update `DATABASE_URL`. Use environment variables for secrets.

### Docker Deployment

```bash
docker-compose up --build
```

This will start `web` and `redis` services.

### Procfile (for Heroku/Render non-Docker)

```
web: gunicorn manage:app -b 0.0.0.0:$PORT
```

### Gunicorn Configuration

- Tune workers / threads per CPU for optimal performance
- Recommended: `workers = (2 * cpu_count) + 1`

### Database Migrations

To use real migrations in production, run:

```bash
flask db init
flask db migrate
flask db upgrade
```

Requires **Flask-Migrate** package.

---

## 📝 Notes & Next Steps

### Recommended Enhancements

1. **Add OpenAPI / Swagger** using `flask-apispec` or `flask-restx` for automatic docs.

2. **Replace SQLite with Postgres** in production by setting `DATABASE_URL`.

3. **Add email verification** and password reset endpoints.

4. **Add pagination metadata** (total pages, current page).

5. **Add caching** (Redis) and monitoring (Prometheus).

6. **Add CI** (GitHub Actions) for tests and deployment.

### Security Improvements

- Implement rate limiting on authentication endpoints
- Add CORS configuration for production
- Use strong JWT secret keys
- Implement refresh tokens
- Add input validation and sanitization

### Performance Optimizations

- Database indexing
- Query optimization
- Implement caching strategies
- Use connection pooling
- Add CDN for static assets

---

## 🔗 Useful Links

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

## 💡 Tips

- Make sure to create a `.env.example` file with all required environment variables (without actual values)
- Always use environment variables for sensitive data like `JWT_SECRET_KEY`
- Consider using `gunicorn` or `waitress` for production deployments instead of Flask's development server
- Test your API thoroughly before deploying to production
- Keep your dependencies up to date in `requirements.txt`
- Use version control (Git) for tracking changes
- Implement proper logging for debugging and monitoring