# FastAPI Student-Course Management API

A production-ready **FastAPI** project that manages Users, Students, Courses, and Enrollments.  
Includes JWT authentication, async SQLAlchemy ORM, SQLite database, and auto-generated Swagger docs.

---

## 🚀 Features

- FastAPI + Async SQLAlchemy ORM
- User Authentication (JWT)
- CRUD for:
  - Users
  - Students
  - Courses
  - Enrollments
- Automatic API docs (Swagger / ReDoc)
- Dockerized deployment
- Environment-based configuration
- Initial superuser creation script

---

## 📦 Project Structure

```
fastapi-student-course/
├─ app/
│  ├─ main.py
│  ├─ api/
│  ├─ core/
│  ├─ db/
│  ├─ models/
│  ├─ schemas/
│  └─ crud/
├─ scripts/
│  └─ create_initial_data.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .env.example
└─ README.md
```

---
### DB Design

```sql
+----------------+          +----------------+          +----------------+
|     users      |          |    students    |          |     courses    |
|----------------|          |----------------|          |----------------|
| id (PK)        |1       1<| id (PK)        | 1     *< | id (PK)        |
| username       |          | full_name      |          | title          |
| email          |          | email          |          | description    |
| hashed_password|          | age            |          |                |
| is_active      |          | user_id (FK?)  |          |                |
| is_superuser   |          +----------------+          +----------------+
+----------------+
         \
          \ (optional link if Student has user account)
           \
            \
             * 
          +----------------+
          |  enrollments   |
          |----------------|
          | id (PK)        |
          | student_id (FK)| --> students.id
          | course_id (FK) | --> courses.id
          +----------------+
Unique constraint: (student_id, course_id)

```

---

## 🔧 Installation (Local Development)

### 1. Clone the repository

```bash
git clone <repository-url>
cd fastapi-student-course
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Start the application

```bash
uvicorn app.main:app --reload
```

### 6. Visit the documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🐳 Run with Docker

### Build and run containers

```bash
docker-compose up --build
```

### Stop containers

```bash
docker-compose down
```

### Access the application

- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

---

## 🛠 Initialize Database

Run the initial data creation script to set up the database and create a superuser:

```bash
python scripts/create_initial_data.py
```

This will:
- Create all database tables
- Generate an initial superuser account

---

## 🔒 Authentication

### Obtain a JWT token

Use the following endpoint to login and receive a JWT token:

```bash
POST /api/v1/auth/login
```

**Request Body:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

### Use the token in Swagger

1. Click the **Authorize** button in Swagger UI
2. Enter: `Bearer <your-token>`
3. Click **Authorize**

Now you can access protected endpoints!

---

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login and get JWT token |
| GET | `/api/v1/auth/me` | Get current user info |

### Students

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/students` | Get all students |
| GET | `/api/v1/students/{id}` | Get student by ID |
| POST | `/api/v1/students` | Create new student (Admin) |
| PUT | `/api/v1/students/{id}` | Update student (Admin) |
| DELETE | `/api/v1/students/{id}` | Delete student (Admin) |

### Courses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/courses` | Get all courses |
| GET | `/api/v1/courses/{id}` | Get course by ID |
| POST | `/api/v1/courses` | Create new course (Admin) |
| PUT | `/api/v1/courses/{id}` | Update course (Admin) |
| DELETE | `/api/v1/courses/{id}` | Delete course (Admin) |

### Enrollments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/enrollments` | Get all enrollments |
| POST | `/api/v1/enrollments` | Enroll student in course |
| DELETE | `/api/v1/enrollments/{id}` | Delete enrollment |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard/stats` | Get dashboard statistics |

---

## 🧪 Testing

### Run tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=app tests/
```

---

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Application
APP_NAME=Student-Course Management API
APP_VERSION=1.0.0
DEBUG=True

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database
DATABASE_URL=sqlite:///./student_course_management.db

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Default Admin
FIRST_SUPERUSER=admin
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin123
```

---

## 🚢 Production Deployment

### Using Gunicorn

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker in Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📝 Database Migrations (Alembic)

### Initialize Alembic

```bash
alembic init alembic
```

### Create a migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

---

# Branching Strategy

We follow a **Git flow inspired branching model** to manage development, testing, releases, and production deployments.

---

## 📌 Branches

| Branch | Purpose | Deployment Environment |
|--------|---------|------------------------|
| `dev` | Active development of new features and bug fixes | Development environment |
| `test` | Integration testing, QA, staging | Test/Staging environment |
| `release` | Pre-release branch; contains code ready for production verification | Pre-production / Release candidate environment |
| `main` / `prod` | Production-ready code | Production environment |

---

## 🔄 Workflow

### 1. Feature Development

Create a feature branch off `dev`:

```bash
git checkout dev
git checkout -b feature/awesome-feature
```

- Develop your feature
- Add tests
- Commit changes with meaningful messages
- Open a Pull Request to `dev`

---

### 2. Merge to `dev`

- All feature branches merge into `dev`
- Continuous Integration (CI) runs automated tests
- `dev` is continuously deployed to the **Development environment**

```bash
git checkout dev
git merge feature/awesome-feature
git push origin dev
```

---

### 3. Merge `dev` → `test`

- After features are stable in `dev`, merge into `test`
- QA team verifies changes in **Test/Staging environment**
- Bugs found in `test` are fixed back in `dev`

```bash
git checkout test
git merge dev
git push origin test
```

---

### 4. Merge `test` → `release`

- When QA passes, merge `test` into `release`
- This branch serves as a **release candidate** for production
- Minor adjustments or hotfixes can be applied here

```bash
git checkout release
git merge test
git push origin release
```

---

### 5. Merge `release` → `main` (Production)

- Once verified, merge `release` into `main` (or `prod`)
- Production deployment is triggered automatically via CI/CD
- Tag the release:

```bash
git checkout main
git merge release
git push origin main

# Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

---

### 6. Hotfixes

Hotfixes can be created from `main` for **urgent production fixes**:

```bash
# Create hotfix branch
git checkout main
git checkout -b hotfix/fix-urgent-bug

# Make fixes and commit
git add .
git commit -m "Fix urgent bug in production"

# Merge hotfix back to main
git checkout main
git merge hotfix/fix-urgent-bug
git push origin main

# Also merge to release
git checkout release
git merge hotfix/fix-urgent-bug
git push origin release

# And back to dev
git checkout dev
git merge hotfix/fix-urgent-bug
git push origin dev

# Tag the hotfix
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git push origin v1.0.1

# Delete hotfix branch
git branch -d hotfix/fix-urgent-bug
git push origin --delete hotfix/fix-urgent-bug
```

---

## 📊 Summary Diagram

```
feature/* → dev → test → release → main/prod
                           ↑
                      hotfix/*
```

**Flow Explanation:**

1. **Features** are developed in `feature/*` branches and merged to `dev`
2. **Development** code in `dev` is promoted to `test` for QA
3. **Tested** code in `test` moves to `release` as a candidate
4. **Release** candidates are deployed to `main/prod` for production
5. **Hotfixes** branch from `main` and merge back to all branches

---

## 🛡️ Branch Protection Rules

- All branches (`dev`, `test`, `release`, `main`) are **protected**
- Require **Pull Request reviews** before merging
- Require **status checks** to pass before merging
- Require **up-to-date** branches before merging
- **No direct commits** to protected branches

---

## 🚀 CI/CD Integration

CI/CD pipelines automatically deploy branches to corresponding environments:

| Branch | Trigger | Deployment Target | Actions |
|--------|---------|-------------------|---------|
| `dev` | Push / PR merge | Development | Run tests, build, deploy to dev |
| `test` | PR merge | Test/Staging | Run tests, build, deploy to staging |
| `release` | PR merge | Pre-production | Run tests, build, deploy to pre-prod |
| `main` | PR merge / Tag | Production | Run tests, build, deploy to production |

---

## 📋 Best Practices

### Commit Messages

Follow conventional commit format:

```
feat: add user authentication
fix: resolve login redirect issue
docs: update API documentation
test: add unit tests for enrollment service
chore: update dependencies
```

### Pull Request Guidelines

- **Title**: Clear and descriptive
- **Description**: What changes were made and why
- **Screenshots**: If UI changes are involved
- **Testing**: How to test the changes
- **Related Issues**: Link to related issues/tickets

### Code Review Checklist

- [ ] Code follows project style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact is acceptable
- [ ] Breaking changes are documented

---

## 🔖 Versioning

We follow [Semantic Versioning](https://semver.org/) (SemVer):

**MAJOR.MINOR.PATCH** (e.g., `v1.2.3`)

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Tagging

```bash
# Major release (breaking changes)
git tag -a v2.0.0 -m "Release v2.0.0 - Major update with breaking changes"

# Minor release (new features)
git tag -a v1.1.0 -m "Release v1.1.0 - Added new enrollment features"

# Patch release (bug fixes)
git tag -a v1.0.1 -m "Release v1.0.1 - Fixed authentication bug"

# Push tags
git push origin --tags
```

---

## 🚨 Emergency Procedures

### Rollback Production

If a critical issue is found in production:

1. **Immediate rollback** to previous stable tag:
   ```bash
   git checkout main
   git reset --hard v1.0.0  # Previous stable version
   git push origin main --force
   ```

2. **Create hotfix** branch to address the issue

3. **Follow hotfix workflow** to patch all branches

### Recovery from Failed Deployment

1. Check CI/CD logs for errors
2. Revert the problematic merge if needed
3. Fix issues in feature branch
4. Re-run the deployment pipeline

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Python-JOSE](https://python-jose.readthedocs.io/)

---

## 📞 Support

For support, email your.email@example.com or open an issue in the repository.

---

**Happy Coding! 🎉**