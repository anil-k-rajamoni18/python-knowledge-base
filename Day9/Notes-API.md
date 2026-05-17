# 🚀 DAY 9 — API & Web Development Concepts
---

## 📌 1. What is an API?

✔ **API** → Application Programming Interface

An API allows two software systems to communicate using predefined rules.

### ✔ Real-world analogies

**Restaurant waiter = API**
- Client gives order → Kitchen → Waiter returns food.

**ATM Machine = API**
- User requests money → Bank server → ATM returns cash.

---

## 📌 2. Types of APIs

### 1. Web APIs / HTTP APIs
Most common. Uses HTTP protocol.

### 2. REST APIs
Most popular style. Stateless, resource-based.

### 3. GraphQL
Flexible queries from the client.

### 4. SOAP
Old enterprise XML-based protocol.

### 5. gRPC
Used for microservices, extremely fast, uses Protocol Buffers.

---

## 📌 3. REST API — Core Concepts

**REST = Representational State Transfer**

A set of architectural constraints for designing scalable APIs.

### ⭐ REST Principles

- Client–Server separation
- Stateless
- Cacheable
- Layered system
- Uniform interface
- Resource-based
- HTTP methods define actions

---

## 📌 4. REST API Structure

```
BASE_URL/resource/{id}
```

**Examples:**
- `GET /users` → Get all users
- `GET /users/10` → Get one user
- `POST /users` → Create
- `PUT /users/10` → Full update
- `PATCH /users/10` → Partial update
- `DELETE /users/10` → Remove

---

## 📌 5. HTTP Basics (Important for API Developers)

### 5.1 HTTP Methods

| Method | Meaning | Example |
|--------|---------|---------|
| GET | Retrieve data | `/products` |
| POST | Create new record | `/users` |
| PUT | Replace full record | `/users/5` |
| PATCH | Update partial | `/users/5` |
| DELETE | Remove data | `/users/5` |

### 5.2 HTTP Status Codes

**2xx — Success**
- 200 OK
- 201 Created
- 204 No Content

**3xx — Redirect**
- 301 Moved Permanently

**4xx — Client Error**
- 400 Bad Request
- 401 Unauthorized (no/invalid token)
- 403 Forbidden (no permission)
- 404 Not Found
- 409 Conflict (duplicate entries)

**5xx — Server Error**
- 500 Internal Server Error
- 503 Service Unavailable

---

## 📌 6. HTTP Request Structure

```http
GET /users HTTP/1.1
Host: example.com
Authorization: Bearer <token>
User-Agent: Chrome
```

**Components:**
- ✔ Method
- ✔ URL
- ✔ Headers
- ✔ Body (for POST/PUT/PATCH)

---

## 📌 7. HTTP Response Structure

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "name": "John"
}
```

---

## 📌 8. Headers in APIs

**Common Request Headers:**
- `Authorization: Bearer <token>`
- `Content-Type: application/json`
- `Accept: application/json`
- `User-Agent: ...`

**Common Response Headers:**
- `Content-Type`
- `Cache-Control`
- `Set-Cookie`
- `Server`

---

## 📌 9. Authentication Mechanisms in APIs

### 1. API Key
Simple, used by external apps.

### 2. JWT (JSON Web Token)
Most common for modern applications.

### 3. OAuth2
Login with Google/Facebook systems.

### 4. Sessions + Cookies
Traditional web apps.

---

## 📌 10. API Security Essentials

**Mandatory:**
- ✔ Use HTTPS
- ✔ Validate all inputs
- ✔ Never expose credentials
- ✔ Use rate-limiting
- ✔ Use authentication/authorization
- ✔ Enable CORS carefully

**CORS Examples:**
```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST
```

---

## 📌 11. API Versioning

Always version APIs:
```
/api/v1/users
/api/v2/users
```

**Methods:**
- URL versioning → easiest
- Header versioning
- Query param versioning

---

## 📌 12. Request Validation

Every API must validate:
- ✔ Data types
- ✔ Required fields
- ✔ String length
- ✔ Format (email, phone, password strength)

FastAPI uses Pydantic for this.

---

## 📌 13. Pagination & Filtering

**Pagination Example:**
```
GET /products?page=2&limit=20
```

**Filtering:**
```
GET /employees?department=IT&city=London
```

**Sorting:**
```
GET /students?sort=name_desc
```

---

## 📌 14. Rate Limiting

Used to protect APIs from abuse:

**Examples:**
- 100 requests/minute
- 10 requests/second

**Tools:** Redis rate limiter, Cloudflare, FastAPI-Limiter.

---

## 📌 15. API Documentation Standards

**Tools:**
- ✔ OpenAPI
- ✔ Swagger UI
- ✔ Redoc
- ✔ Postman Collections

FastAPI auto-generates `/docs` & `/redoc`.

---

## 📌 16. Good API Response Structure

Always return consistent JSON:

```json
{
  "success": true,
  "data": {...},
  "error": null,
  "message": "User created successfully"
}
```

---

## 📌 17. Error Handling (Professional)

Example error response:

```json
{
  "success": false,
  "error": "ValidationError",
  "message": "Email is not valid"
}
```

---

## 📌 18. Idempotency (Important Interview Topic)

| Method | Idempotent? | Meaning |
|--------|-------------|---------|
| GET | Yes | Safe repeated |
| PUT | Yes | Overwrites same result |
| DELETE | Yes | Deleting twice same effect |
| POST | ❌ No | Creates new record each call |

**Example:**
- `PUT /users/10` → always predictable
- `POST /users` → not predictable

---

## 📌 19. API Testing Tools

### Manual Tools
- Postman
- Thunder Client
- Insomnia

### Automated Tools
- pytest
- locust
- unittest

---

## 📌 20. API Deployment Basics

To deploy FastAPI:

Use `uvicorn` + `gunicorn`

**Deploy on:**
- ✔ AWS EC2
- ✔ Render
- ✔ Railway
- ✔ Docker containers

**A typical production command:**
```bash
gunicorn main:app -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
```

---

## 📌 21. API Logging

Log every request:
- Endpoint accessed
- Method used
- Request body
- Response status
- Time taken

Helps with debugging and auditing.

---

## 📌 22. API Monitoring

**Tools:**
- Prometheus
- Grafana
- OpenTelemetry
- New Relic
- Datadog

**Track:**
- ✔ Latency
- ✔ Error rate
- ✔ Throughput (requests/sec)

---

## 📌 23. API Caching

Caching makes APIs faster.

**Types:**
- Client-side
- Server-side
- CDN caching

**Headers:**
```http
Cache-Control: max-age=3600
ETag: "xyz"
```

---

## 📌 24. API Best Practices (Very Important)

### ✔ Use nouns, not verbs
- ❌ `/createUser`
- ✔ `/users`

### ✔ Use plural names
- ❌ `/user`
- ✔ `/users`

### ✔ Return proper HTTP codes
### ✔ Validate input every time
### ✔ Avoid long nested routes
- ❌ `/api/v1/user/getUserDetails`
- ✔ `/api/v1/users/123/details`

---

## 📌 25. Summary — What You Should Understand by Day 9

You should now know:

### API Basics:
- ✔ HTTP request/response
- ✔ Methods & status codes
- ✔ Headers, cookies

### REST API Concepts:
- ✔ Resource-based URLs
- ✔ CRUD operations
- ✔ Versioning
- ✔ Pagination

### Security:
- ✔ JWT
- ✔ API Keys
- ✔ CORS

### Best Practices:
- ✔ Consistent responses
- ✔ Error handling
- ✔ Meaningful status codes
- ✔ Validation

### FastAPI-specific:
- ✔ Auto-docs
- ✔ Pydantic models
- ✔ Dependency injection
- ✔ SQLite integration
- ✔ Folder structure