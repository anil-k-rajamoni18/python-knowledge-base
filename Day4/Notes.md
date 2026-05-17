# 🐍 DAY 4 — Functions, Functional Tools & Error Handling
---

## 📌 Table of Contents

1. [Functions — The Building Blocks](#functions)
2. [Argument Types — Deep Dive](#arguments)
3. [Return Values](#return-values)
4. [Scope & Closures](#scope-closures)
5. [Decorators](#decorators)
6. [Lambda, Map, Filter, Reduce](#functional-tools)
7. [Error Handling — try/except/else/finally](#error-handling)
8. [Exception Hierarchy](#exception-hierarchy)
9. [Custom Exceptions](#custom-exceptions)
10. [Hands-On Exercises](#exercises)
11. [Mini Project — Contact Book CLI](#mini-project)

---

## 🗺️ Big Picture — Day 4 at a Glance

```
┌─────────────────────────────────────────────────────────────────┐
│                    DAY 4 CONCEPT MAP                            │
│                                                                 │
│  FUNCTIONS                                                      │
│  ├── def, return, docstrings                                    │
│  ├── Argument types: positional, keyword, default, *args, **kw  │
│  ├── Scope: local → enclosing → global → built-in (LEGB)        │
│  ├── Closures — functions that remember their environment       │
│  └── Decorators — wrap functions with extra behavior            │
│                                                                 │
│  FUNCTIONAL TOOLS                                               │
│  ├── lambda  — one-liner anonymous functions                    │
│  ├── map()   — transform every item                             │
│  ├── filter()— keep items matching a condition                  │
│  └── reduce()— collapse to a single value                       │
│                                                                 │
│  ERROR HANDLING                                                 │
│  ├── try / except / else / finally                              │
│  ├── Built-in exception types                                   │
│  ├── raise — signal errors explicitly                           │
│  └── Custom exceptions — domain-specific errors                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🟦 1. Functions — The Building Blocks {#functions}

### What is a Function?

A function is a named, reusable block of code that performs a specific task. You define it once and call it as many times as needed. Think of it like a recipe — write it once, cook it whenever you want.

```python
def greet():
    print("Hello!")

greet()   # Hello!
```

### Why Functions Matter in Real Software

Functions are not just a convenience — they're the foundation of good software design:

```
Without functions            With functions
──────────────────────────   ──────────────────────────────────
Copy-paste everywhere        Write once, call anywhere
Hard to test in isolation    Each function testable independently
One change = many fixes      One change = fixed everywhere
300-line main script         Modular, readable, maintainable
```

### Anatomy of a Well-Written Function

```python
def calculate_discount(price: float, discount_pct: float = 10.0) -> float:
    """
    Calculate the discounted price.

    Args:
        price (float): Original price in INR.
        discount_pct (float): Discount percentage (default 10%).

    Returns:
        float: Price after discount.

    Raises:
        ValueError: If price or discount_pct is negative.
    """
    if price < 0 or discount_pct < 0:
        raise ValueError("Price and discount must be non-negative")
    return price * (1 - discount_pct / 100)

# Usage
final_price = calculate_discount(2000, 15)  # 1700.0
```

Good functions have:
- A clear, verb-based name (`calculate_`, `fetch_`, `validate_`, `parse_`)
- A docstring
- Type hints (optional but very useful in teams)
- One single responsibility
- Predictable return behavior

---

## 🟦 2. Argument Types — Deep Dive {#arguments}

Python gives you four ways to pass data into functions. Understanding when to use each is essential.

### 1. Positional Arguments

The order you pass them in is what determines which parameter receives which value.

```python
def register_user(name, email, age):
    print(f"Registering {name}, {email}, age {age}")

register_user("Priya", "priya@example.com", 27)  # order matters!
```

### 2. Keyword Arguments

You name the parameters explicitly. Order no longer matters. Very readable for functions with many parameters.

```python
register_user(age=27, name="Priya", email="priya@example.com")  # same result
```

> **Industry Tip:** When calling functions with 3+ parameters, prefer keyword arguments. `create_order(user_id, True, False, 5)` is a mystery — `create_order(user_id, is_priority=True, notify=False, quantity=5)` is self-documenting.

### 3. Default Arguments

Parameters with a pre-set value if the caller doesn't provide one.

```python
def send_email(to, subject, cc=None, bcc=None, priority="normal"):
    print(f"Sending to {to} | Priority: {priority}")

send_email("ravi@company.com", "Meeting Tomorrow")   # cc, bcc, priority use defaults
send_email("ceo@company.com", "Urgent", priority="high")
```

> **Critical Gotcha — Mutable Default Arguments:**

```python
# WRONG — the list is shared across ALL calls
def add_item(item, cart=[]):
    cart.append(item)
    return cart

add_item("apple")   # ["apple"]
add_item("banana")  # ["apple", "banana"]  😱 not a fresh cart!

# CORRECT — use None as default, create fresh list inside
def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart
```

This is one of the most common Python bugs in production. Never use mutable objects (lists, dicts) as default argument values.

### 4. `*args` — Variable Positional Arguments

Use when you don't know how many positional arguments will be passed. `args` becomes a **tuple** inside the function.

```python
def total(*nums):
    return sum(nums)

total(1, 2, 3)           # 6
total(10, 20, 30, 40)    # 100

# Real example — logging with variable context
def log(level, *messages):
    for msg in messages:
        print(f"[{level}] {msg}")

log("ERROR", "DB connection failed", "Retry 1 failed", "Retry 2 failed")
```

### 5. `**kwargs` — Variable Keyword Arguments

Use when you don't know how many named arguments will be passed. `kwargs` becomes a **dict** inside the function.

```python
def create_profile(**info):
    for key, val in info.items():
        print(f"  {key}: {val}")

create_profile(name="Anil", city="Hyderabad", role="Backend Dev", yoe=4)
```

**Real-world: Flexible API wrapper**

```python
def api_request(endpoint, method="GET", **options):
    """
    options can include: headers, timeout, params, json, auth
    """
    import requests
    return requests.request(method, endpoint, **options)

api_request("/users", headers={"Auth": "Bearer xyz"}, timeout=5)
```

### Combining All Argument Types

The order must always follow this rule:

```
def func(positional, default=val, *args, **kwargs)
         ──────────  ────────────  ─────  ────────
         required    optional      extra  extra
         first       after req.    pos    named
```

```python
def build_query(table, limit=10, *filters, **options):
    print(f"Table: {table}, Limit: {limit}")
    print(f"Filters: {filters}")
    print(f"Options: {options}")

build_query("users", 20, "active=True", "age>18", order="desc", format="json")
```

---

## 🟦 3. Return Values {#return-values}

### Single Value

```python
def square(n):
    return n * n
```

### Multiple Values (returned as a tuple)

```python
def get_stats(nums):
    return min(nums), max(nums), sum(nums) / len(nums)

lo, hi, avg = get_stats([10, 20, 30, 40])
# lo=10, hi=40, avg=25.0
```

### Returning None

If a function has no `return` statement (or just `return`), it returns `None`. Forgetting this causes `NoneType` errors:

```python
def add_to_list(lst, item):
    lst.append(item)
    # no return — implicitly returns None

result = add_to_list([1, 2], 3)
print(result)   # None  ← common surprise
```

### Returning a Dictionary (Clean API Pattern)

For functions that produce multiple named results, a dict is often more readable than a tuple:

```python
def analyze(data):
    return {
        "count":  len(data),
        "mean":   sum(data) / len(data),
        "min":    min(data),
        "max":    max(data),
    }

stats = analyze([10, 30, 20, 50])
print(stats["mean"])   # 27.5
```

---

## 🟦 4. Scope & Closures {#scope-closures}

### The LEGB Rule

Python resolves variable names using the LEGB lookup order:

```
┌─────────────────────────────────────────────────────┐
│                   LEGB Rule                         │
│                                                     │
│  L → Local       — inside the current function      │
│  E → Enclosing   — outer function (for closures)    │
│  G → Global      — module-level variables           │
│  B → Built-in    — Python's builtins (len, print…)  │
│                                                     │
│  Python searches L first, then E, then G, then B    │
└─────────────────────────────────────────────────────┘
```

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)   # "local"  — finds L first

    inner()
    print(x)       # "enclosing"

outer()
print(x)           # "global"
```

### `global` and `nonlocal`

```python
counter = 0

def increment():
    global counter     # explicitly modify the global variable
    counter += 1

# nonlocal — modify enclosing scope variable
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

c = make_counter()
c()   # 1
c()   # 2
c()   # 3
```

### Closures — Functions That Remember

A closure is a function that captures variables from its enclosing scope, even after the outer function has finished executing. This is powerful and used widely in real code.

```python
def make_multiplier(factor):
    def multiply(n):
        return n * factor    # "factor" is captured from outer scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

double(5)    # 10
triple(5)    # 15

# Real use: configurable tax calculator
def tax_calculator(rate):
    def calculate(amount):
        return amount * (1 + rate / 100)
    return calculate

gst_18 = tax_calculator(18)
gst_5  = tax_calculator(5)

gst_18(1000)   # 1180.0
gst_5(1000)    # 1050.0
```

---

## 🟦 5. Decorators {#decorators}

Decorators are one of Python's most elegant features. They let you wrap a function with additional behavior — without modifying the function itself.

### The Core Idea

```
Normal call:   function(args)
Decorated:     wrapper → function(args) → wrapper
```

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function runs")
        result = func(*args, **kwargs)
        print("After the function runs")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("Priya")
# Before the function runs
# Hello, Priya!
# After the function runs
```

### Real-World Decorator Examples

**1. Timing a function (performance monitoring)**

```python
import time
import functools

def timer(func):
    @functools.wraps(func)    # preserves original function name/docstring
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)
        end    = time.time()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def load_data(filepath):
    # simulate slow operation
    time.sleep(0.5)
    return [1, 2, 3]

load_data("data.csv")
# load_data took 0.5003s
```

**2. Authentication check (used in every web framework)**

```python
def require_auth(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.get("token"):
            return {"error": "Unauthorized", "code": 401}
        return func(request, *args, **kwargs)
    return wrapper

@require_auth
def get_profile(request):
    return {"name": "Anil", "role": "admin"}
```

**3. Retry logic (very common in microservices)**

```python
def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
            raise Exception(f"All {times} attempts failed")
        return wrapper
    return decorator

@retry(times=3)
def call_external_api(url):
    # might fail due to network issues
    import requests
    return requests.get(url, timeout=2).json()
```

> **Observation:** Django, Flask, FastAPI — all use decorators extensively. `@app.route("/")`, `@login_required`, `@cache_page` are all decorators under the hood. Understanding how they work makes you a better framework user.

---

## 🟩 6. Lambda, Map, Filter, Reduce {#functional-tools}

These tools come from the functional programming paradigm and help you write concise, expressive data transformation pipelines.

### Lambda Functions

Anonymous (nameless) functions defined in a single expression.

```python
# Syntax: lambda parameters: expression

square  = lambda x: x ** 2
add     = lambda a, b: a + b
greet   = lambda name: f"Hello, {name}!"

square(5)       # 25
add(3, 4)       # 7
```

**Where lambdas shine — as inline arguments:**

```python
employees = [
    {"name": "Ravi",  "salary": 85000},
    {"name": "Priya", "salary": 72000},
    {"name": "Kiran", "salary": 91000},
]

# Sort by salary descending
sorted_emp = sorted(employees, key=lambda e: e["salary"], reverse=True)

# Sort strings by length
words = ["banana", "fig", "apple", "kiwi"]
sorted(words, key=lambda w: len(w))   # ["fig", "kiwi", "apple", "banana"]
```

**When NOT to use lambda:**

```python
# Bad — hard to read, hard to test
process = lambda x: x.strip().lower().replace(" ", "_")

# Good — give it a name, add a docstring
def slugify(text):
    """Convert text to a URL-safe slug."""
    return text.strip().lower().replace(" ", "_")
```

### map() — Apply a Function to Every Item

`map(function, iterable)` → returns a lazy iterator (wrap with `list()` to materialize).

```python
nums    = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))   # [2,4,6,8,10]

# With a regular function
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

temps_c = [0, 20, 37, 100]
temps_f = list(map(celsius_to_fahrenheit, temps_c))
# [32.0, 68.0, 98.6, 212.0]
```

**Industry Examples:**

```python
# Clean API price strings → floats
raw_prices    = ["199.99", "450.00", "89.5"]
clean_prices  = list(map(float, raw_prices))

# Extract a field from a list of dicts
users = [{"name": "Ravi"}, {"name": "Priya"}, {"name": "Kiran"}]
names = list(map(lambda u: u["name"], users))

# Hash passwords (never store plaintext!)
import hashlib
passwords    = ["secret123", "admin@456"]
hashed_pwds  = list(map(lambda p: hashlib.sha256(p.encode()).hexdigest(), passwords))
```

### filter() — Keep Items That Match a Condition

`filter(function, iterable)` → returns a lazy iterator of items where the function returns `True`.

```python
nums  = [1, 2, 3, 4, 5, 6, 7, 8]
evens = list(filter(lambda x: x % 2 == 0, nums))   # [2,4,6,8]

# filter with None removes falsy values
mixed  = [0, 1, "", "hello", None, [], [1,2], False, True]
truthy = list(filter(None, mixed))
# [1, "hello", [1,2], True]
```

**Industry Examples:**

```python
# Filter failed API requests
responses  = [{"status": 200}, {"status": 500}, {"status": 200}, {"status": 404}]
failures   = list(filter(lambda r: r["status"] >= 400, responses))

# Active users only
users       = [{"name": "Ravi", "active": True}, {"name": "Priya", "active": False}]
active      = list(filter(lambda u: u["active"], users))

# Only ERROR-level log lines
log_lines   = open("app.log").readlines()
error_lines = list(filter(lambda l: "ERROR" in l, log_lines))
```

### reduce() — Collapse a Sequence to One Value

```python
from functools import reduce
```

`reduce(function, iterable, initial)` applies the function cumulatively:

```
[1, 2, 3, 4]  →  ((1+2)+3)+4  →  10
```

```python
from functools import reduce

nums  = [1, 2, 3, 4, 5]
total = reduce(lambda a, b: a + b, nums)          # 15
product = reduce(lambda a, b: a * b, nums)        # 120

# With initial value
total_with_offset = reduce(lambda a, b: a + b, nums, 100)  # 115
```

**Industry Examples:**

```python
# Total file sizes in a download queue
files      = [{"name": "a.zip", "size": 450}, {"name": "b.iso", "size": 3200}]
total_size = reduce(lambda acc, f: acc + f["size"], files, 0)
# 3650 MB

# Merge multiple dicts
configs = [{"host": "localhost"}, {"port": 5432}, {"db": "myapp"}]
merged  = reduce(lambda a, b: {**a, **b}, configs)
# {"host":"localhost", "port":5432, "db":"myapp"}

# Max without using max()
largest = reduce(lambda a, b: a if a > b else b, [3, 1, 7, 2, 5])
# 7
```

### map/filter vs List Comprehensions — When to Use Which

```
Prefer comprehensions when:              Prefer map/filter when:
────────────────────────────────────     ──────────────────────────────────
Simple, readable transformations         Passing an already-named function
You want the result immediately          Composing functional pipelines
Filtering AND transforming at once       Working with itertools chains
Team is Python-native                    Performance-sensitive large datasets
```

```python
# These are equivalent — comprehension is often cleaner for simple cases
doubled_evens_comp = [x*2 for x in nums if x % 2 == 0]
doubled_evens_func = list(map(lambda x: x*2, filter(lambda x: x%2==0, nums)))
```

---

## 🟥 7. Error Handling — try/except/else/finally {#error-handling}

### Why It Matters

Production software faces an unpredictable world — network failures, bad user input, missing files, corrupted data. Error handling is what separates scripts from software.

```
Without error handling          With error handling
────────────────────────────    ──────────────────────────────────
App crashes on bad input        Gracefully handles the issue
User sees raw stack trace       User sees a friendly message
Data gets corrupted mid-write   Cleanup runs via finally
Entire pipeline fails           Log the error, continue or retry
```

### Full Structure

```python
try:
    # Code that might fail
    result = risky_operation()

except SpecificError as e:
    # Handle a known error type
    print(f"Specific error: {e}")

except (TypeError, ValueError) as e:
    # Handle multiple error types in one block
    print(f"Type/Value error: {e}")

except Exception as e:
    # Catch-all for unexpected errors (use sparingly!)
    print(f"Unexpected: {e}")

else:
    # Runs ONLY if no exception occurred
    print("Everything went fine!")

finally:
    # ALWAYS runs — cleanup code goes here
    print("Cleaning up...")
```

### The `else` Block — Often Forgotten

The `else` block runs only when no exception was raised. It's the "happy path" confirmation:

```python
try:
    data = json.loads(raw_input)
except json.JSONDecodeError:
    print("Invalid JSON")
else:
    # We KNOW data is valid here — no need to check again
    process(data)
finally:
    log_attempt()   # always log
```

### The `finally` Block — Always Runs

`finally` runs regardless of whether an exception occurred. Use it for cleanup:

```python
db_connection = None
try:
    db_connection = connect_to_db()
    results = db_connection.query("SELECT * FROM users")
except DatabaseError as e:
    print(f"DB error: {e}")
finally:
    if db_connection:
        db_connection.close()   # always close the connection
```

### `raise` — Signalling Errors Explicitly

You can raise exceptions intentionally to signal that something went wrong:

```python
def get_user(user_id):
    if not isinstance(user_id, int):
        raise TypeError(f"user_id must be int, got {type(user_id).__name__}")
    if user_id <= 0:
        raise ValueError(f"user_id must be positive, got {user_id}")
    return db.fetch(user_id)

# Re-raise after logging
try:
    result = risky_call()
except Exception as e:
    logger.error(f"Failed: {e}")
    raise     # re-raises the same exception — preserves stack trace
```

### Real-Time Industry Examples

**1. API Request Wrapper**

```python
import requests

def fetch_data(url, retries=3):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()   # raises HTTPError for 4xx/5xx
            return response.json()
        except requests.Timeout:
            print(f"Timeout on attempt {attempt}")
        except requests.HTTPError as e:
            print(f"HTTP error: {e.response.status_code}")
            break   # don't retry on client errors
        except requests.ConnectionError:
            print(f"Connection failed, attempt {attempt}/{retries}")
    return None
```

**2. File Reading with Fallback**

```python
import json

def load_config(path="config.json"):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found at {path}, using defaults")
        return {"host": "localhost", "port": 8000}
    except json.JSONDecodeError as e:
        print(f"Malformed JSON in {path}: {e}")
        raise   # this one we want to propagate — bad config is serious
```

**3. Database Transaction**

```python
def transfer_funds(from_id, to_id, amount):
    conn = get_db_connection()
    try:
        conn.begin()
        debit(conn, from_id, amount)
        credit(conn, to_id, amount)
        conn.commit()
        print(f"Transferred ₹{amount} successfully")
    except InsufficientFundsError:
        conn.rollback()
        raise   # let caller handle this
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Transfer failed: {e}") from e
    finally:
        conn.close()
```

**4. ML Pipeline with Graceful Degradation**

```python
def preprocess_batch(batch):
    clean = []
    for i, record in enumerate(batch):
        try:
            clean.append(normalize(record))
        except (ValueError, KeyError) as e:
            print(f"Skipping record {i}: {e}")
            continue   # skip bad records, process the rest
    return clean
```

### Observations Worth Remembering

- Catch **specific** exceptions, not bare `except:` — it swallows `KeyboardInterrupt`, `SystemExit`, and other critical signals.
- `except Exception as e` is acceptable as a catch-all but should always log `e`.
- `raise` without arguments (inside an except block) re-raises the original exception with the original traceback — always prefer this over `raise e`.
- `with` statements (context managers) are often the cleaner alternative to `try/finally` for resource cleanup.

---

## 🟥 8. Exception Hierarchy {#exception-hierarchy}

Python's exceptions form a class hierarchy. Catching a parent catches all its children:

```
BaseException
├── SystemExit               ← sys.exit() raises this
├── KeyboardInterrupt        ← Ctrl+C raises this
└── Exception                ← almost everything else
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError       ← list[99] when list has 3 items
    │   └── KeyError         ← dict["missing_key"]
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── TimeoutError
    ├── TypeError            ← "hello" + 5
    ├── ValueError           ← int("abc")
    ├── AttributeError       ← None.upper()
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── RuntimeError
    └── StopIteration        ← internal to iterators
```

**Practical note:** Catch `LookupError` to handle both `IndexError` and `KeyError` in one block. Catch `OSError` to handle most file/network errors.

```python
try:
    val = data[key]
except LookupError:
    val = default_value
```

---

## 🟪 9. Custom Exceptions {#custom-exceptions}

When built-in exceptions don't convey enough meaning about a business-level failure, you create your own.

### Basic Custom Exception

```python
class InvalidAgeError(Exception):
    pass

def register(age):
    if age < 18:
        raise InvalidAgeError(f"Minimum age is 18, got {age}")
```

### Custom Exception with Extra Attributes

```python
class APIError(Exception):
    """Raised when an API call fails."""
    def __init__(self, message, status_code=None, endpoint=None):
        super().__init__(message)
        self.status_code = status_code
        self.endpoint    = endpoint

    def __str__(self):
        return f"[{self.status_code}] {super().__str__()} ({self.endpoint})"

# Usage
try:
    raise APIError("User not found", status_code=404, endpoint="/api/users/99")
except APIError as e:
    print(e)               # [404] User not found (/api/users/99)
    print(e.status_code)   # 404
```

### Exception Hierarchy for a Domain

A well-structured app defines a hierarchy so callers can catch at different levels of granularity:

```python
# Base exception for the whole app
class AppError(Exception):
    pass

# Domain-specific exceptions
class AuthError(AppError):
    pass

class DatabaseError(AppError):
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field = field
        super().__init__(f"Validation failed on '{field}': {message}")

# Usage
def validate_email(email):
    if "@" not in email:
        raise ValidationError("email", f"'{email}' is not a valid email address")

try:
    validate_email("not-an-email")
except ValidationError as e:
    print(f"Field: {e.field}, Error: {e}")
except AppError as e:
    print(f"App-level error: {e}")
```

### When to Create Custom Exceptions

```
Create custom exceptions when:
✔ A built-in exception doesn't describe the problem precisely enough
✔ You want to attach extra data (status code, field name, context)
✔ Callers need to distinguish your errors from unrelated errors
✔ You're building a library or API that others will use
✔ You have business rules that can be violated (age, balance, permissions)
```

---

## 🧪 10. Hands-On Exercises {#exercises}

### Exercise 1: Higher-Order Functions

```python
def apply_twice(func, value):
    """Apply func to value, then apply func to the result."""
    return func(func(value))

apply_twice(lambda x: x + 3, 5)    # (5+3)+3 = 11
apply_twice(lambda x: x * 2, 3)    # (3*2)*2 = 12

# Extension: apply n times
def apply_n_times(func, value, n):
    for _ in range(n):
        value = func(value)
    return value

apply_n_times(lambda x: x + 1, 0, 5)   # 5
```

### Exercise 2: Names to Uppercase (map + lambda)

```python
names     = ["alice", "bob", "charlie", "diana"]
uppercased = list(map(lambda n: n.upper(), names))
# ["ALICE", "BOB", "CHARLIE", "DIANA"]

# With title case and stripping whitespace
raw_names = ["  alice", "BOB  ", " charlie "]
cleaned   = list(map(lambda n: n.strip().title(), raw_names))
# ["Alice", "Bob", "Charlie"]
```

### Exercise 3: Filter Even Numbers

```python
nums  = list(range(1, 21))
evens = list(filter(lambda x: x % 2 == 0, nums))
# [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# Also filter a list of dicts
students = [
    {"name": "Ravi",  "score": 82},
    {"name": "Priya", "score": 45},
    {"name": "Kiran", "score": 91},
    {"name": "Meera", "score": 55},
]
passed = list(filter(lambda s: s["score"] >= 60, students))
# [{"name":"Ravi","score":82}, {"name":"Kiran","score":91}]
```

### Exercise 4: Safe Division Function

```python
def safe_div(a, b):
    """
    Divide a by b safely.
    Returns the result or an error string.
    """
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError as e:
        return f"Error: Invalid types — {e}"

print(safe_div(10, 2))     # 5.0
print(safe_div(10, 0))     # Error: Cannot divide by zero
print(safe_div(10, "x"))   # Error: Invalid types — ...
```

### Exercise 5: Error-Safe Input Loop

```python
def get_valid_age():
    while True:
        try:
            age = int(input("Enter your age: "))
            if age < 0 or age > 150:
                raise ValueError("Age must be between 0 and 150")
            return age
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

# Enhanced version with max attempts
def get_integer_input(prompt, min_val=None, max_val=None, max_tries=3):
    for attempt in range(1, max_tries + 1):
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                raise ValueError(f"Must be ≥ {min_val}")
            if max_val is not None and val > max_val:
                raise ValueError(f"Must be ≤ {max_val}")
            return val
        except ValueError as e:
            print(f"Attempt {attempt}/{max_tries}: {e}")
    raise RuntimeError("Max input attempts exceeded")
```

### Exercise 6: Custom WeakPasswordError

```python
class WeakPasswordError(Exception):
    def __init__(self, reasons):
        self.reasons = reasons
        super().__init__("Password is too weak: " + "; ".join(reasons))

def validate_password(password):
    reasons = []

    if len(password) < 8:
        reasons.append("must be at least 8 characters")
    if not any(c.isupper() for c in password):
        reasons.append("must contain at least one uppercase letter")
    if not any(c.islower() for c in password):
        reasons.append("must contain at least one lowercase letter")
    if not any(c.isdigit() for c in password):
        reasons.append("must contain at least one digit")
    if not any(c in "!@#$%^&*" for c in password):
        reasons.append("must contain a special character (!@#$%^&*)")

    if reasons:
        raise WeakPasswordError(reasons)

    return True

# Test
try:
    validate_password("hello")
except WeakPasswordError as e:
    print(e)
    # Password is too weak: must be at least 8 characters;
    #   must contain at least one uppercase letter; ...
```

### Exercise 7 (New): Pipeline using map + filter + reduce

```python
from functools import reduce

orders = [
    {"id": 1, "amount": 1500, "status": "completed"},
    {"id": 2, "amount":  800, "status": "cancelled"},
    {"id": 3, "amount": 3200, "status": "completed"},
    {"id": 4, "amount":  200, "status": "completed"},
]

# Total revenue from completed orders only
revenue = reduce(
    lambda acc, amt: acc + amt,
    map(
        lambda o: o["amount"],
        filter(lambda o: o["status"] == "completed", orders)
    ),
    0
)
print(f"Total Revenue: ₹{revenue}")   # ₹4900
```

### Exercise 8 (New): Decorator — Validate Function Inputs

```python
import functools

def validate_positive(*param_names):
    """Decorator that ensures specified parameters are positive numbers."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            sig    = inspect.signature(func)
            params = list(sig.parameters.keys())
            for i, val in enumerate(args):
                if i < len(params) and params[i] in param_names:
                    if not isinstance(val, (int, float)) or val <= 0:
                        raise ValueError(f"'{params[i]}' must be a positive number, got {val}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_positive("price", "quantity")
def create_order(price, quantity, discount=0):
    return price * quantity * (1 - discount / 100)

create_order(100, 5)        # 500
create_order(-100, 5)       # ValueError: 'price' must be a positive number
```

---

## 🧩 11. Mini Project — Contact Book CLI {#mini-project}

This project ties together functions, error handling, custom exceptions, and file I/O. Build it piece by piece.

### Project Structure

```
contact_book/
├── contacts.json        ← persistent data store
├── models.py            ← Contact class + validation
├── storage.py           ← load/save functions
├── operations.py        ← add/search/delete/edit
└── main.py              ← CLI menu loop
```

### Custom Exceptions

```python
# models.py

class ContactError(Exception):
    """Base exception for contact book errors."""
    pass

class DuplicateContactError(ContactError):
    def __init__(self, name):
        super().__init__(f"Contact '{name}' already exists")

class ContactNotFoundError(ContactError):
    def __init__(self, query):
        super().__init__(f"No contact found matching '{query}'")

class InvalidPhoneError(ContactError):
    def __init__(self, phone):
        super().__init__(f"'{phone}' is not a valid phone number (10 digits required)")

class InvalidEmailError(ContactError):
    def __init__(self, email):
        super().__init__(f"'{email}' is not a valid email address")
```

### Validation Functions

```python
import re

def validate_phone(phone):
    if not re.fullmatch(r"\d{10}", phone.replace(" ", "").replace("-", "")):
        raise InvalidPhoneError(phone)
    return True

def validate_email(email):
    pattern = r"^[\w.\-+]+@[\w\-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise InvalidEmailError(email)
    return True
```

### Storage Functions

```python
# storage.py
import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    """Load contacts from JSON file. Creates file if missing."""
    try:
        with open(CONTACTS_FILE) as f:
            return json.load(f).get("contacts", [])
    except FileNotFoundError:
        save_contacts([])   # create empty file
        return []
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Contacts file is corrupted: {e}")

def save_contacts(contacts):
    """Save contacts list to JSON file."""
    try:
        with open(CONTACTS_FILE, "w") as f:
            json.dump({"contacts": contacts}, f, indent=2)
    except PermissionError:
        raise RuntimeError("Cannot write to contacts file — check permissions")
```

### Core Operations

```python
# operations.py

def add_contact(contacts, name, phone, email):
    # Check for duplicates
    if any(c["name"].lower() == name.lower() for c in contacts):
        raise DuplicateContactError(name)

    validate_phone(phone)
    validate_email(email)

    contacts.append({"name": name, "phone": phone, "email": email})
    return contacts

def search_contact(contacts, query):
    query = query.lower()
    results = [c for c in contacts
               if query in c["name"].lower() or query in c["email"].lower()]
    if not results:
        raise ContactNotFoundError(query)
    return results

def delete_contact(contacts, name):
    original_len = len(contacts)
    contacts = [c for c in contacts if c["name"].lower() != name.lower()]
    if len(contacts) == original_len:
        raise ContactNotFoundError(name)
    return contacts

def edit_contact(contacts, name, **updates):
    for contact in contacts:
        if contact["name"].lower() == name.lower():
            if "phone" in updates:
                validate_phone(updates["phone"])
                contact["phone"] = updates["phone"]
            if "email" in updates:
                validate_email(updates["email"])
                contact["email"] = updates["email"]
            return contacts
    raise ContactNotFoundError(name)
```

### CLI Menu

```python
# main.py

def main():
    contacts = load_contacts()
    print("📒 Contact Book — Type 'help' for commands\n")

    while True:
        try:
            cmd = input(">> ").strip().lower()

            if cmd == "help":
                print("Commands: add | search | delete | list | edit | export | quit")

            elif cmd == "list":
                if not contacts:
                    print("No contacts yet.")
                for c in contacts:
                    print(f"  {c['name']:<20} {c['phone']:<15} {c['email']}")

            elif cmd == "add":
                name  = input("Name:  ")
                phone = input("Phone: ")
                email = input("Email: ")
                contacts = add_contact(contacts, name, phone, email)
                save_contacts(contacts)
                print(f"✅ Added {name}")

            elif cmd == "search":
                query   = input("Search: ")
                results = search_contact(contacts, query)
                for c in results:
                    print(f"  {c}")

            elif cmd == "delete":
                name     = input("Name to delete: ")
                contacts = delete_contact(contacts, name)
                save_contacts(contacts)
                print(f"✅ Deleted {name}")

            elif cmd in ("quit", "exit"):
                print("Goodbye!")
                break

            else:
                print("Unknown command. Type 'help'.")

        except ContactError as e:
            print(f"⚠️  {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
```

### Optional Enhancements

```python
# Export to CSV
import csv

def export_to_csv(contacts, filename="contacts.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "phone", "email"])
        writer.writeheader()
        writer.writerows(contacts)
    print(f"Exported {len(contacts)} contacts to {filename}")

# Import from CSV
def import_from_csv(contacts, filename="import.csv"):
    imported = 0
    skipped  = 0
    with open(filename) as f:
        for row in csv.DictReader(f):
            try:
                contacts = add_contact(contacts, row["name"], row["phone"], row["email"])
                imported += 1
            except ContactError as e:
                print(f"Skipped: {e}")
                skipped += 1
    print(f"Imported {imported}, skipped {skipped}")
    return contacts
```

### Concepts Used — Breakdown

```
┌──────────────────────────┬────────────────────────────────────────────┐
│ Concept                  │ Where Used                                 │
├──────────────────────────┼────────────────────────────────────────────┤
│ Functions                │ Every operation: add, search, delete, edit │
│ *args / **kwargs         │ edit_contact(**updates)                    │
│ Default arguments        │ load_contacts(), fetch_data(retries=3)     │
│ Lambda + filter          │ search_contact, list comprehensions        │
│ try/except/else/finally  │ load_contacts, save_contacts, main loop    │
│ Custom exceptions        │ Full hierarchy: ContactError and children  │
│ raise                    │ validate_phone, validate_email, operations │
│ File I/O with context mgr│ open() with with statement                 │
│ JSON                     │ load_contacts, save_contacts               │
│ Regex                    │ validate_email, validate_phone             │
└──────────────────────────┴────────────────────────────────────────────┘
```

---

## 📝 Quick Recap Cheatsheet

```
FUNCTIONS
  def name(pos, kw=default, *args, **kwargs): ...
  return val1, val2     ← returns tuple
  LEGB: Local → Enclosing → Global → Built-in

CLOSURES & DECORATORS
  Closure: inner function captures outer variable
  Decorator: @wrapper wraps function with extra behavior
  Always use @functools.wraps(func) inside decorators

FUNCTIONAL TOOLS
  lambda x: expr          ← anonymous, one-liner
  map(fn, iter)           ← transform every item → lazy iterator
  filter(fn, iter)        ← keep matching items → lazy iterator
  reduce(fn, iter, init)  ← collapse to one value (from functools)

ERROR HANDLING
  try / except / else / finally
  Catch SPECIFIC exceptions, not bare except:
  raise                   ← re-raise in except block (preserves trace)
  raise SomeError("msg")  ← raise new error
  finally                 ← always runs, use for cleanup

CUSTOM EXCEPTIONS
  class MyError(Exception): pass
  class DetailedError(Exception):
      def __init__(self, field, msg):
          self.field = field
          super().__init__(msg)

GOLDEN RULES
  ✔ One function = one responsibility
  ✔ Name functions with verbs: get_, create_, validate_, parse_
  ✔ Never use mutable defaults: def f(x, lst=None) not def f(x, lst=[])
  ✔ Always close resources — use with statements
  ✔ Catch specific errors; log before re-raising
  ✔ Custom exceptions make APIs self-documenting
```

---

*Day 4 Notes — Functions, Functional Tools & Error Handling | Consolidated & Expanded*
