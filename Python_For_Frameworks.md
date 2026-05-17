# Python for Frameworks — In-Depth Learning Notes
> **Level:** Moderate → Advanced | **Focus:** Concepts every backend framework (Django, FastAPI, Flask) relies on

---

## Table of Contents

1. [Decorators — The Magic Behind Routes](#1-decorators)
2. [Context Managers — The `with` Statement](#2-context-managers)
3. [Generators & Iterators — Lazy Evaluation](#3-generators--iterators)
4. [Type Hints & Pydantic — FastAPI's Foundation](#4-type-hints--pydantic)
5. [Async / Await — Non-blocking I/O](#5-async--await)
6. [Metaclasses & Class-Based Views](#6-metaclasses--class-based-views)
7. [Descriptors — How ORM Fields Work](#7-descriptors)
8. [Dependency Injection Patterns](#8-dependency-injection)
9. [Middleware — Request/Response Pipeline](#9-middleware)
10. [Python's Import System & App Factory Pattern](#10-import-system--app-factory)
11. [Signals & Event Systems](#11-signals--event-systems)
12. [Concurrency Models — Threading vs Multiprocessing vs Async](#12-concurrency-models)

---

## 1. Decorators

Decorators are the **#1 pattern** frameworks use. Every `@app.route`, `@login_required`, `@cached_property` is a decorator.

### How Decorators Work — Step by Step

```python
# A decorator is simply a function that takes a function and returns a function.

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function runs")
        result = func(*args, **kwargs)     # call the original function
        print("After the function runs")
        return result
    return wrapper

@my_decorator                              # syntactic sugar for: greet = my_decorator(greet)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
# Output:
# Before the function runs
# Hello, Alice!
# After the function runs
```

### Preserving Metadata with `functools.wraps`

Without `wraps`, your decorated function loses its name and docstring — a common bug.

```python
import functools

def log_call(func):
    @functools.wraps(func)          # copies __name__, __doc__, __module__ etc.
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def add(a, b):
    """Adds two numbers."""
    return a + b

print(add.__name__)    # add  (NOT 'wrapper' — thanks to wraps)
print(add.__doc__)     # Adds two numbers.
```

### Decorator with Arguments (Decorator Factory)

This is how `@app.route("/home")` works — the decorator itself accepts arguments.

```python
def repeat(times):                        # outer function takes config
    def decorator(func):                  # middle function takes the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):     # inner function does the work
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(times=3)
def say_hi():
    print("Hi!")

say_hi()
# Hi!
# Hi!
# Hi!
```

### Class-Based Decorator

Used in Django's `@login_required` style decorators.

```python
class timer:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        import time
        self.calls += 1
        start = time.perf_counter()
        result = self.func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{self.func.__name__} took {elapsed:.4f}s (call #{self.calls})")
        return result

@timer
def slow_query():
    import time; time.sleep(0.1)

slow_query()   # slow_query took 0.1001s (call #1)
slow_query()   # slow_query took 0.1002s (call #2)
```

### Real-World: Building a Route Registry (Mini Flask)

```python
class MiniApp:
    def __init__(self):
        self.routes = {}

    def route(self, path, methods=("GET",)):
        def decorator(func):
            self.routes[path] = {"handler": func, "methods": methods}
            return func
        return decorator

    def dispatch(self, path, method="GET"):
        entry = self.routes.get(path)
        if not entry:
            return "404 Not Found"
        if method not in entry["methods"]:
            return "405 Method Not Allowed"
        return entry["handler"]()

app = MiniApp()

@app.route("/", methods=("GET",))
def index():
    return "Welcome to the homepage!"

@app.route("/submit", methods=("POST",))
def submit():
    return "Form submitted!"

print(app.dispatch("/"))               # Welcome to the homepage!
print(app.dispatch("/submit", "POST")) # Form submitted!
print(app.dispatch("/submit", "GET"))  # 405 Method Not Allowed
```

---

## 2. Context Managers

Frameworks use context managers for **database transactions**, **request lifecycle**, and **resource cleanup**.

### The Protocol: `__enter__` and `__exit__`

```python
class DatabaseTransaction:
    def __init__(self, connection):
        self.conn = connection

    def __enter__(self):
        print("BEGIN TRANSACTION")
        return self                        # the value bound to `as` variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:                       # an exception occurred
            print(f"ROLLBACK — Error: {exc_val}")
            return True                    # True = suppress the exception
        else:
            print("COMMIT")
        return False

class FakeConnection:
    pass

conn = FakeConnection()

with DatabaseTransaction(conn) as txn:
    print("Doing some DB work...")
    # raise ValueError("Something went wrong!")  # uncomment to test rollback

# Output:
# BEGIN TRANSACTION
# Doing some DB work...
# COMMIT
```

### Using `contextlib.contextmanager` — Generator Shortcut

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name):
    print(f"Acquiring {name}")
    try:
        yield name                        # code inside `with` runs here
    except Exception as e:
        print(f"Error with {name}: {e}")
    finally:
        print(f"Releasing {name}")        # always runs

with managed_resource("database connection") as resource:
    print(f"Using {resource}")

# Acquiring database connection
# Using database connection
# Releasing database connection
```

### Real-World: Request Context (like Flask's `g`)

```python
from contextlib import contextmanager
from threading import local

_local = local()                           # thread-local storage

@contextmanager
def request_context(user_id):
    _local.user_id = user_id
    _local.request_data = {}
    try:
        yield
    finally:
        del _local.user_id
        del _local.request_data

def get_current_user():
    return getattr(_local, "user_id", None)

with request_context(user_id=42):
    print(get_current_user())              # 42

print(get_current_user())                 # None — context is cleaned up
```

---

## 3. Generators & Iterators

Frameworks use generators for **streaming responses**, **paginated queries**, and **lazy data loading**.

### Iterator Protocol

```python
class CountUp:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self                       # object is its own iterator

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration           # signals end of iteration
        val = self.current
        self.current += 1
        return val

for n in CountUp(3):
    print(n)                              # 0, 1, 2
```

### Generator Functions — `yield`

```python
def stream_large_file(filepath, chunk_size=1024):
    """Read a large file in chunks — used in streaming HTTP responses."""
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk                   # pauses here, resumes on next()

# In a web framework:
# for chunk in stream_large_file("video.mp4"):
#     response.write(chunk)
```

### Generator Expressions

```python
# List comprehension — loads ALL into memory
squares_list = [x**2 for x in range(1_000_000)]   # 8 MB in memory

# Generator expression — lazy, computes one at a time
squares_gen = (x**2 for x in range(1_000_000))    # almost 0 memory

# Use sum() — it only needs one value at a time
total = sum(x**2 for x in range(1000))
```

### `yield from` — Delegating to Sub-generators

```python
def paginated_query(table, page_size=100):
    """Simulates DB query with pagination — real pattern in SQLAlchemy."""
    offset = 0
    while True:
        # Simulate fetching a page
        page = list(range(offset, offset + page_size))  # fake DB rows
        if not page:
            return
        yield from page                   # yield each item from the page
        offset += page_size
        if offset >= 300:                 # stop after 3 pages for demo
            return

count = sum(1 for _ in paginated_query("users"))
print(count)                             # 300
```

### `send()` — Two-Way Communication (used in async internals)

```python
def accumulator():
    total = 0
    while True:
        value = yield total              # yield sends total out, receives value in
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)                               # prime the generator (advance to first yield)
print(gen.send(10))                     # 10
print(gen.send(20))                     # 30
print(gen.send(5))                      # 35
```

---

## 4. Type Hints & Pydantic

**FastAPI is built entirely on type hints.** Understanding them is mandatory.

### Basic Type Hints

```python
from typing import Optional, List, Dict, Union, Tuple

def create_user(
    name: str,
    age: int,
    email: Optional[str] = None,         # can be str or None
    tags: List[str] = [],
    metadata: Dict[str, Union[str, int]] = {}
) -> Dict[str, object]:
    return {"name": name, "age": age}
```

### `TypeVar` and Generics

```python
from typing import TypeVar, Generic, List

T = TypeVar("T")

class Repository(Generic[T]):
    """Generic base — Django/SQLAlchemy-style."""
    def __init__(self):
        self._store: List[T] = []

    def save(self, item: T) -> T:
        self._store.append(item)
        return item

    def find_all(self) -> List[T]:
        return self._store

class User:
    def __init__(self, name: str):
        self.name = name

repo: Repository[User] = Repository()
repo.save(User("Alice"))
print(repo.find_all()[0].name)          # Alice — type checker knows this is User
```

### Pydantic — Data Validation (FastAPI's Core)

```python
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    age: int = Field(..., gt=0, lt=150)
    bio: Optional[str] = None

    @validator("email")
    def email_must_be_valid(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v.lower()                 # normalize to lowercase

    @validator("username")
    def username_alphanumeric(cls, v):
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric")
        return v

# Valid data
user = UserCreate(username="alice_99", email="Alice@Example.com", age=25)
print(user.email)                       # alice@example.com  (normalized)
print(user.dict())

# Invalid data — raises ValidationError
try:
    bad_user = UserCreate(username="a!", email="notanemail", age=-5)
except Exception as e:
    print(e)                            # detailed validation errors
```

### Pydantic for Config (like Django settings)

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str
    debug: bool = False
    allowed_hosts: List[str] = ["localhost"]

    class Config:
        env_file = ".env"               # reads from .env file automatically

# settings = Settings()
# print(settings.database_url)         # from env or default
```

---

## 5. Async / Await

FastAPI and modern Django rely on `asyncio`. This is the most important topic for modern backend work.

### The Event Loop Mental Model

```
Traditional (blocking):          Async (non-blocking):
  Request 1: [====DB====]          Request 1: [=wait=]   [=process=]
  Request 2:            [====DB====]    |       ↑
                                  Request 2: [=wait=][=process=]
                                              ↑
                                  While waiting → handle other requests!
```

### `async def` and `await`

```python
import asyncio

async def fetch_user(user_id: int) -> dict:
    """Simulates async DB call."""
    await asyncio.sleep(0.1)            # non-blocking wait (like awaiting DB/HTTP)
    return {"id": user_id, "name": f"User {user_id}"}

async def main():
    user = await fetch_user(1)         # suspend until result is ready
    print(user)

asyncio.run(main())                    # {"id": 1, "name": "User 1"}
```

### Running Tasks Concurrently with `gather`

```python
import asyncio
import time

async def slow_operation(name, delay):
    print(f"Starting {name}")
    await asyncio.sleep(delay)
    print(f"Done {name}")
    return f"{name} result"

async def sequential():
    start = time.time()
    r1 = await slow_operation("query1", 1)
    r2 = await slow_operation("query2", 1)
    print(f"Sequential: {time.time() - start:.2f}s")   # ~2.0s

async def concurrent():
    start = time.time()
    r1, r2 = await asyncio.gather(
        slow_operation("query1", 1),
        slow_operation("query2", 1)
    )
    print(f"Concurrent: {time.time() - start:.2f}s")   # ~1.0s

asyncio.run(concurrent())
```

### Async Context Managers & Iterators

```python
class AsyncDatabaseSession:
    async def __aenter__(self):
        print("Opening DB connection")
        await asyncio.sleep(0.01)       # simulate connection time
        return self

    async def __aexit__(self, *args):
        print("Closing DB connection")
        await asyncio.sleep(0.01)

    async def execute(self, query):
        await asyncio.sleep(0.01)
        return f"Results of: {query}"

async def get_users():
    async with AsyncDatabaseSession() as db:    # async context manager
        return await db.execute("SELECT * FROM users")

async def stream_rows():
    """Async generator — used for streaming DB rows."""
    for i in range(5):
        await asyncio.sleep(0.01)
        yield {"id": i, "value": i * 10}

async def main():
    result = await get_users()
    print(result)

    async for row in stream_rows():             # async for
        print(row)

asyncio.run(main())
```

### FastAPI-Style Async Endpoint

```python
from typing import List
import asyncio

# Simulating FastAPI without the framework
async def get_item(item_id: int) -> dict:
    await asyncio.sleep(0.05)               # simulated DB query
    return {"item_id": item_id, "name": f"Item {item_id}"}

async def get_items(limit: int = 10) -> List[dict]:
    tasks = [get_item(i) for i in range(limit)]
    return await asyncio.gather(*tasks)     # fetch all in parallel

async def main():
    items = await get_items(5)
    for item in items:
        print(item)

asyncio.run(main())
```

---

## 6. Metaclasses & Class-Based Views

Django's ORM `Model` and DRF's `Serializer` use **metaclasses** to work their magic.

### What is a Metaclass?

```
Normal class:   MyClass  is an instance of  type
Metaclass:      MyClass  is an instance of  MyMeta (which inherits from type)

type("MyClass", (Base,), {"attr": value})  ← type is itself a metaclass
```

### Custom Metaclass — Auto-registering Classes

```python
class PluginMeta(type):
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:                             # skip the base Plugin class itself
            mcs.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    def run(self): raise NotImplementedError

class AuthPlugin(Plugin):
    def run(self): return "Auth running"

class LogPlugin(Plugin):
    def run(self): return "Log running"

print(PluginMeta.registry)
# {'AuthPlugin': <class 'AuthPlugin'>, 'LogPlugin': <class 'LogPlugin'>}

for name, plugin_cls in PluginMeta.registry.items():
    print(plugin_cls().run())
```

### Django-Style Model Metaclass (Simplified)

```python
class FieldDescriptor:
    def __init__(self, name, field_type):
        self.name = name
        self.field_type = field_type

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.field_type):
            raise TypeError(f"{self.name} must be {self.field_type.__name__}")
        obj.__dict__[self.name] = value


class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        fields = {k: v for k, v in namespace.items() if isinstance(v, FieldDescriptor)}
        cls = super().__new__(mcs, name, bases, namespace)
        cls._fields = fields
        return cls

class Model(metaclass=ModelMeta):
    def save(self):
        print(f"Saving {self.__class__.__name__}: {self.__dict__}")

class CharField(FieldDescriptor):
    def __init__(self): super().__init__("", str)

class IntField(FieldDescriptor):
    def __init__(self): super().__init__("", int)


class User(Model):
    name = CharField()
    age = IntField()

u = User()
u.name = "Alice"
u.age = 30
u.save()                               # Saving User: {'name': 'Alice', 'age': 30}

try:
    u.age = "thirty"                   # TypeError: age must be int
except TypeError as e:
    print(e)
```

---

## 7. Descriptors

How Django ORM fields like `CharField`, `IntegerField` actually work under the hood.

### The Descriptor Protocol

```python
class Validator:
    """A descriptor that validates data type on assignment."""

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                          # accessed on class, not instance
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    def validate(self, value):
        pass                                     # override in subclasses

class StringField(Validator):
    def __init__(self, max_length=255):
        self.max_length = max_length

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        if len(value) > self.max_length:
            raise ValueError(f"{self.name} max length is {self.max_length}")

class PositiveInt(Validator):
    def validate(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{self.name} must be a positive integer")

class Product:
    title = StringField(max_length=100)
    price = PositiveInt()

    def __init__(self, title, price):
        self.title = title
        self.price = price

p = Product("Python Book", 49)
print(p.title, p.price)               # Python Book 49

try:
    p.price = -10                     # ValueError: price must be a positive integer
except ValueError as e:
    print(e)
```

### `__get__` — Cached Property (used in Django & Python stdlib)

```python
class cached_property:
    """Computes once, then caches on the instance — Django uses this."""

    def __init__(self, func):
        self.func = func
        self.attrname = None
        self.__doc__ = func.__doc__

    def __set_name__(self, owner, name):
        self.attrname = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.attrname not in obj.__dict__:
            obj.__dict__[self.attrname] = self.func(obj)   # compute and cache
        return obj.__dict__[self.attrname]

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @cached_property
    def area(self):
        import math
        print("Computing area...")       # only prints once!
        return math.pi * self.radius ** 2

c = Circle(5)
print(c.area)                           # Computing area... → 78.53...
print(c.area)                           # 78.53... (from cache, no recompute)
```

---

## 8. Dependency Injection

FastAPI has first-class DI. Understanding the pattern is key.

### Manual DI — Constructor Injection

```python
class Database:
    def query(self, sql): return f"DB result for: {sql}"

class Cache:
    def __init__(self):
        self._store = {}
    def get(self, key): return self._store.get(key)
    def set(self, key, value): self._store[key] = value

class UserService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db
        self.cache = cache               # dependencies injected, not created here

    def get_user(self, user_id: int):
        cached = self.cache.get(f"user:{user_id}")
        if cached:
            return cached
        user = self.db.query(f"SELECT * FROM users WHERE id={user_id}")
        self.cache.set(f"user:{user_id}", user)
        return user

# Wire up dependencies
db = Database()
cache = Cache()
service = UserService(db=db, cache=cache)   # inject!

print(service.get_user(1))             # DB result for: SELECT ...
print(service.get_user(1))             # returns from cache
```

### FastAPI-Style DI with Callables

```python
from functools import lru_cache
from typing import Generator

# Dependency functions — FastAPI calls these automatically
def get_db() -> Generator:
    """Provides a DB session per request."""
    db = {"connection": "open", "queries": []}
    try:
        yield db                         # FastAPI injects this into endpoints
    finally:
        db["connection"] = "closed"      # cleanup after request

@lru_cache                               # singleton — created once
def get_settings():
    return {"SECRET_KEY": "my-secret", "DEBUG": False}

# Simulating FastAPI endpoint behavior
def resolve_dependency(dep_func):
    """Mini dependency resolver."""
    import inspect
    gen = dep_func()
    if inspect.isgenerator(gen):
        return next(gen)
    return gen

db_session = resolve_dependency(get_db)
settings = get_settings()
print(db_session)                        # {'connection': 'open', 'queries': []}
print(settings)                          # {'SECRET_KEY': 'my-secret', ...}
```

---

## 9. Middleware

Middleware wraps every request/response — used for auth, logging, CORS, compression.

### WSGI Middleware (Flask/Django-style)

```python
class TimingMiddleware:
    """Wraps a WSGI app to add request timing."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        import time
        path = environ.get("PATH_INFO", "/")
        start = time.time()

        def custom_start_response(status, headers, exc_info=None):
            elapsed = time.time() - start
            headers.append(("X-Response-Time", f"{elapsed:.4f}s"))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

def simple_app(environ, start_response):
    """Minimal WSGI app."""
    status = "200 OK"
    headers = [("Content-Type", "text/plain")]
    start_response(status, headers)
    return [b"Hello, World!"]

# Wrap with middleware
app = TimingMiddleware(simple_app)
```

### ASGI Middleware (FastAPI/Starlette-style)

```python
import asyncio
from typing import Callable

class AuthMiddleware:
    """ASGI middleware that checks for auth token."""

    def __init__(self, app, secret_token: str):
        self.app = app
        self.secret_token = secret_token

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Extract headers
            headers = dict(scope.get("headers", []))
            token = headers.get(b"authorization", b"").decode()

            if token != f"Bearer {self.secret_token}":
                # Return 401 without calling the app
                await send({
                    "type": "http.response.start",
                    "status": 401,
                    "headers": [[b"content-type", b"text/plain"]],
                })
                await send({
                    "type": "http.response.body",
                    "body": b"Unauthorized",
                })
                return

        await self.app(scope, receive, send)  # pass to next layer
```

### Chaining Middleware

```python
class LoggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(f"→ {environ['REQUEST_METHOD']} {environ['PATH_INFO']}")
        result = self.app(environ, start_response)
        print(f"← Response sent")
        return result

# Stack middleware — innermost is called last (LIFO for wrapping)
app = simple_app
app = TimingMiddleware(app)         # layer 2
app = LoggingMiddleware(app)        # layer 1 (outermost — called first)
```

---

## 10. Import System & App Factory

Flask's `create_app()` and Django's `INSTALLED_APPS` — understanding `__init__.py` and imports.

### Python's Import System

```python
# When you write: import mypackage.models
# Python does:
# 1. Finds mypackage directory
# 2. Executes mypackage/__init__.py
# 3. Finds models.py inside
# 4. Executes models.py
# 5. Binds the name in sys.modules cache

import sys
print("django" in sys.modules)       # False if not imported yet
import django
print("django" in sys.modules)       # True — cached, won't re-execute
```

### App Factory Pattern (Flask-Style)

```python
# app/__init__.py
def create_app(config_name="development"):
    """Factory function — creates and configures a fresh app instance.
    
    Why? Testing! Each test gets a fresh app with test config.
    """
    configs = {
        "development": {"DEBUG": True,  "DB": "sqlite:///dev.db"},
        "testing":     {"DEBUG": False, "DB": "sqlite:///:memory:"},
        "production":  {"DEBUG": False, "DB": "postgresql://..."},
    }

    app = {"config": configs[config_name], "routes": {}, "extensions": {}}

    # Register blueprints / routers
    _register_routes(app)
    _init_extensions(app)

    return app

def _register_routes(app):
    app["routes"]["/health"] = lambda: {"status": "ok"}
    app["routes"]["/users"] = lambda: {"users": []}

def _init_extensions(app):
    app["extensions"]["db"] = f"DB connected to {app['config']['DB']}"

# Usage:
dev_app  = create_app("development")
test_app = create_app("testing")       # separate instance, separate DB

print(dev_app["extensions"]["db"])    # DB connected to sqlite:///dev.db
print(test_app["extensions"]["db"])   # DB connected to sqlite:///:memory:
```

### Lazy Imports for Performance

```python
# Heavy modules loaded only when needed (Django does this for ORM)
class LazyModule:
    def __init__(self, module_name):
        self._module_name = module_name
        self._module = None

    def __getattr__(self, name):
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

# json module loaded only on first attribute access
lazy_json = LazyModule("json")
# ... lots of code that might not use json ...
result = lazy_json.dumps({"key": "value"})  # imported here, not at startup
print(result)
```

---

## 11. Signals & Event Systems

Django's `post_save`, `pre_delete` signals — publisher/subscriber pattern.

```python
from collections import defaultdict
from typing import Callable, Any
import weakref

class Signal:
    """Django-style signal implementation."""

    def __init__(self):
        self._receivers: list = []

    def connect(self, receiver: Callable, sender=None):
        """Register a listener."""
        self._receivers.append((sender, receiver))

    def disconnect(self, receiver: Callable):
        self._receivers = [(s, r) for s, r in self._receivers if r != receiver]

    def send(self, sender, **kwargs) -> list:
        """Emit the signal — call all matching receivers."""
        responses = []
        for registered_sender, receiver in self._receivers:
            if registered_sender is None or registered_sender is sender:
                response = receiver(sender=sender, **kwargs)
                responses.append((receiver, response))
        return responses

# Define signals
post_save = Signal()
pre_delete = Signal()

# Receivers (like Django signal handlers)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        print(f"📧 Sending welcome email to {instance['email']}")

def invalidate_cache(sender, instance, **kwargs):
    print(f"🗑️  Cache invalidated for user {instance['id']}")

# Connect receivers
post_save.connect(send_welcome_email)
post_save.connect(invalidate_cache)

# Simulate model save
def save_user(user_data, created=False):
    print(f"Saving user {user_data['id']}...")
    post_save.send(sender="User", instance=user_data, created=created)

save_user({"id": 1, "email": "alice@example.com"}, created=True)
# Saving user 1...
# 📧 Sending welcome email to alice@example.com
# 🗑️  Cache invalidated for user 1
```

---

## 12. Concurrency Models

Choosing the right model is critical for backend performance.

```
CPU-bound work:   multiprocessing  ← parallel, separate memory
I/O-bound work:   asyncio          ← single thread, event loop  ← best for web
Mixed/legacy:     threading        ← limited by GIL for CPU tasks
```

### Threading — Good for I/O, Limited for CPU

```python
import threading
import time

results = {}
lock = threading.Lock()

def fetch_data(key, delay):
    time.sleep(delay)                  # simulates I/O (network, disk)
    with lock:                         # thread-safe write
        results[key] = f"data_{key}"

threads = [
    threading.Thread(target=fetch_data, args=(f"task_{i}", 0.5))
    for i in range(5)
]

start = time.time()
for t in threads: t.start()
for t in threads: t.join()            # wait for all threads
print(f"Done in {time.time()-start:.2f}s")   # ~0.5s (concurrent I/O)
print(results)
```

### Multiprocessing — True Parallelism for CPU

```python
from multiprocessing import Pool

def cpu_intensive(n):
    """Compute-heavy work — benefits from multiprocessing."""
    return sum(i**2 for i in range(n))

if __name__ == "__main__":            # REQUIRED guard for multiprocessing
    with Pool(processes=4) as pool:   # 4 worker processes
        results = pool.map(cpu_intensive, [10**5, 10**5, 10**5, 10**5])
    print(results)
```

### Asyncio — Best for Web Backends

```python
import asyncio
import aiohttp                        # pip install aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)   # all in parallel, one thread!

# asyncio.run(fetch_all(["https://api.example.com/users/1", ...]))
```

### Choosing the Right Model — Decision Table

| Scenario | Model | Why |
|---|---|---|
| HTTP API (FastAPI) | `asyncio` | Thousands of concurrent I/O-bound requests |
| Image processing | `multiprocessing` | CPU-bound, needs true parallelism |
| Background email sending | `threading` or `celery` | I/O-bound, or offload entirely |
| Django (traditional) | `threading` (WSGI) | Sync ORM, thread-per-request |
| Django (modern) | `asyncio` (ASGI) | Async views, channels |

---

## Quick Reference — Framework Concept Map

```
Flask / Django / FastAPI use:

Decorators          → @app.route, @login_required, @cached_property
Context Managers    → database transactions, request context, resource cleanup  
Generators          → streaming responses, paginated DB queries
Type Hints          → FastAPI request validation, auto-docs, editor support
Pydantic            → request body parsing, settings management (FastAPI)
Async/Await         → FastAPI endpoints, async Django views, aiohttp calls
Metaclasses         → Django Model, DRF Serializer auto-field detection
Descriptors         → ORM field validation, cached_property, lazy attributes
Dependency Injection→ FastAPI Depends(), service layer pattern
Middleware          → auth, CORS, rate limiting, request logging
App Factory         → create_app(), testable configurations
Signals             → Django post_save, pre_delete event hooks
Concurrency         → asyncio (FastAPI), threading (WSGI), workers (Gunicorn)
```

---

## Recommended Next Steps

1. **Build a mini-framework** — implement a router, middleware stack, and DI container from scratch
2. **Read FastAPI source** — `fastapi/routing.py` uses everything above
3. **Read Django ORM** — `django/db/models/base.py` for metaclass + descriptor patterns
4. **Practice async** — rewrite any sync code to async using `asyncio` + `aiohttp`
5. **Write tests** — pytest fixtures are context managers + generators in disguise

---

*Notes generated for moderate-to-advanced Python learners targeting backend frameworks.*
