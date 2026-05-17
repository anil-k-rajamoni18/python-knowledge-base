# 🚀 DAY 9 — Flask Framework (In-Depth Notes for API Development)

A complete, structured guide to Flask, Routing, Request Handling, Templating, Blueprints, Middleware, API development, and database integration.

---

## 📌 1. Introduction to Flask

✔ Flask is a lightweight, micro web framework for Python.

- Created by Armin Ronacher
- WSGI-based (Werkzeug), templating via Jinja2

### ✔ Key Features

- Minimal → Developer adds only needed components
- Flexible and unopinionated
- Easy to integrate with databases
- Excellent for small–medium applications, microservices, APIs

### ✔ When to choose Flask?

| Use Case | Choose Flask? |
|----------|---------------|
| Small app | ✔ Perfect |
| Rest API | ✔ Very common |
| Microservices | ✔ Excellent |
| Large MVC | ❌ FastAPI or Django better |

---

## 📌 2. Flask Architecture Overview

### ✔ Flask = Core + Extensions

**Core provides:**
- Routing
- Request/Response handling
- Templating
- Debug server

**Everything else (DB, Auth, Validation) is through extensions, e.g.:**
- `flask_sqlalchemy`
- `flask_marshmallow`
- `flask_login`
- `flask_restful`

---

## 📌 3. Installing Flask

```bash
pip install flask
```

Check version:

```python
import flask
print(flask.__version__)
```

---

## 📌 4. Basic Flask App

Create `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 📌 5. Application Factory Pattern (Professional Style)

Scalable Flask apps use factories:

```python
def create_app():
    app = Flask(__name__)
    
    @app.route("/")
    def home():
        return "Factory Pattern Works!"

    return app
```

Run with:

```python
app = create_app()
app.run()
```

---

## 📌 6. Flask Routing (URL Mapping)

**Basic route:**
```python
@app.route("/hello")
def hello():
    return "Hi!"
```

**Dynamic routes:**
```python
@app.route("/user/<username>")
def user(username):
    return f"Hello {username}"
```

**Type converters:**
```python
@app.route("/product/<int:id>")
def product(id):
    return f"Product ID = {id}"
```

**Allowed types:**
- `string`
- `int`
- `float`
- `path`
- `uuid`

---

## 📌 7. HTTP Methods in Flask

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Logged in"
    return "Login page"
```

---

## 📌 8. Handling Request Data

Import:

```python
from flask import request
```

**Query Parameters:**
```python
# /search?query=python
q = request.args.get("query")
```

**Form Data:**
```python
name = request.form.get("name")
```

**JSON Body:**
```python
data = request.get_json()
```

---

## 📌 9. Flask Response

```python
from flask import jsonify

return jsonify({"message": "success"})
```

**Explicit response:**
```python
return "Done", 201
```

**Headers:**
```python
return {"msg": "ok"}, 200, {"X-App": "Flask"}
```

---

## 📌 10. Flask Templates (Jinja2)

Flask uses Jinja2 for HTML templates.

**Folder:**
```
templates/
    index.html
```

**Example:**
```python
return render_template("index.html", name="John")
```

**HTML:**
```html
<h1>Hello {{ name }}</h1>
```

---

## 📌 11. Static Files

```
static/
   styles.css
   script.js
```

**Usage:**
```html
<link rel="stylesheet" href="/static/styles.css">
```

---

## 📌 12. URL Building

Use `url_for` instead of hardcoded URLs:

```python
url_for("home")
url_for("user", username="john")
```

---

## 📌 13. Flask Blueprints (Modular Architecture)

Used to split large applications.

**Example:**

**📁 auth/routes.py**

```python
from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login")
def login():
    return "Login Page"
```

**📁 app.py**

```python
app.register_blueprint(auth_bp, url_prefix="/auth")
```

**URL:**
```
/auth/login
```

---

## 📌 14. Flask Configuration Management

Ways to set config:

```python
app.config["DEBUG"] = True
```

Load from `config.py`

Environment variables:

```python
app.config.from_envvar("APP_CONFIG_FILE")
```

---

## 📌 15. Error Handling

Custom handler:

```python
@app.errorhandler(404)
def not_found(e):
    return {"error": "Not Found"}, 404
```

---

## 📌 16. Middleware in Flask (Before/After Request Hooks)

**Before request execution:**
```python
@app.before_request
def before():
    print("Request incoming...")
```

**After request:**
```python
@app.after_request
def after(response):
    print("Response leaving...")
    return response
```

**Used for:**
- ✔ Logging
- ✔ Authentication
- ✔ Performance tracking

---

## 📌 17. Flask Extensions (Industry-Standard)

### DB & ORM
- `flask_sqlalchemy`
- `flask_migrate`

### Validation
- `marshmallow`

### Auth
- `flask_jwt_extended`
- `flask_login`

### REST APIs
- `flask_restful`
- `flask_apispec`

---

## 📌 18. Database Integration — SQLite + SQLAlchemy

**Install:**
```bash
pip install flask_sqlalchemy
```

**Define Model:**
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
```

**Create DB:**
```python
db.create_all()
```

---

## 📌 19. CRUD Operations (ORM)

**Create:**
```python
s = Student(name="John")
db.session.add(s)
db.session.commit()
```

**Read:**
```python
Student.query.all()
```

**Update:**
```python
s = Student.query.get(1)
s.name = "Mike"
db.session.commit()
```

**Delete:**
```python
db.session.delete(s)
db.session.commit()
```

---

## 📌 20. API Development with Flask

Simple REST API:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

students = []

@app.get("/students")
def get_students():
    return jsonify(students)

@app.post("/students")
def add_student():
    data = request.get_json()
    students.append(data)
    return data, 201
```

---

## 📌 21. Using Marshmallow for Validation

```bash
pip install marshmallow
```

**Example:**

```python
from marshmallow import Schema, fields

class StudentSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)

schema = StudentSchema()
```

**Validate JSON:**

```python
data = schema.load(request.get_json())
```

---

## 📌 22. Flask-RESTful

```bash
pip install flask_restful
```

**Example:**

```python
from flask_restful import Resource, Api

api = Api(app)

class Hello(Resource):
    def get(self):
        return {"message": "hello"}

api.add_resource(Hello, "/hello")
```

---

## 📌 23. JWT Authentication in Flask

```bash
pip install flask_jwt_extended
```

**Usage:**

```python
from flask_jwt_extended import JWTManager

app.config["JWT_SECRET_KEY"] = "secret"
jwt = JWTManager(app)
```

---

## 📌 24. Production Deployment

Run using gunicorn:

```bash
gunicorn app:app -b 0.0.0.0:8000
```

**Recommended:**
- ✔ Nginx reverse proxy
- ✔ Docker container
- ✔ Load balancer

---

## 📌 25. Summary Checklist (What You Should Know)

You should now understand:

- ✔ Flask basics
- ✔ Routing
- ✔ GET/POST/PUT/DELETE
- ✔ Templates
- ✔ Blueprints
- ✔ Request/response
- ✔ Middleware
- ✔ SQLAlchemy
- ✔ REST APIs
- ✔ Marshmallow validation
- ✔ JWT Auth
- ✔ Deployment