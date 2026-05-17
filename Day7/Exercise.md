#  DAY 7 — REALTIME HANDS-ON QUESTIONS

---

## 🧩 SECTION 1 — Iterators & Generators

### 1️⃣ Build a Streaming File Reader (Log Processing)

Write a generator function:
- Reads a large log file (`server.log`) line by line
- Yields only lines containing "ERROR"
- Should not load the entire file into memory

**Usage Example:**

```python
for error in error_stream("server.log"):
    print(error)
```

---

### 2️⃣ Paginated API Generator (Industry API Calls)

Build a generator that:
- Calls a paginated API endpoint like:
  ```
  https://api.example.com/products?page=1
  ```
- Fetches page-by-page
- Yields results one product at a time
- Stops when API returns no more pages

---

### 3️⃣ Infinite Fibonacci Iterator

Create an Iterator class that generates Fibonacci numbers infinitely.

```python
fib = Fibonacci()
for i in fib:
    print(i)
```

Stop iteration only when user breaks.

---

### 4️⃣ CSV Chunk Reader (Data Engineering)

Create a generator that:
- Reads a CSV file in chunks of 100 rows
- Returns each chunk as a list of dictionaries
- Useful for ETL pipelines.

---

## 🧩 SECTION 2 — Decorators (with parameters)

### 5️⃣ Build a Retry Decorator

Create a decorator:
- Retries a function N times
- Waits x seconds between retries
- Logs all failed attempts

**Example:**

```python
@retry(times=3, delay=1)
def unstable_api_call():
    ...
```

---

### 6️⃣ Role-Based Access Decorator (Real Authentication Flow)

Create:

```python
@requires_role("admin")
def delete_user():
    ...
```

The decorator should:
- Check if current user has required role
- Raise custom `PermissionError` if not

---

### 7️⃣ Cache Decorator (Simple Memoization)

Implement:

```python
@cache
def expensive_operation(n):
    ...
```

**Requirements:**
- Cache results
- Return cached value on repeated calls
- Used in ML model predictions.

---

### 8️⃣ Timing Decorator with Threshold

Build:

```python
@time_warning(limit=2.0)
def process():
    ...
```

If execution > limit seconds → print warning.

Used in production KPI monitoring.

---

## 🧩 SECTION 3 — Context Managers

### 9️⃣ Database Transaction Context Manager

Simulate a DB transaction:

```python
with transaction():
    debit()
    credit()
```

**Inside:**
- If no exception → commit
- If exception → rollback
- Print steps for simulation.

---

### 🔟 Temporary Directory Context Manager (DevOps style)

Create:

```python
with temp_dir() as path:
    # create files inside temp dir
```

**Where `temp_dir()`:**
- Creates a temp folder
- Returns path
- Deletes folder automatically on exit

---

### 1️⃣1️⃣ Network Connection Context Manager

Simulate:

```python
with connection("api.server.com") as conn:
    conn.send("hello")
```

- On enter → print "Opening connection"
- On exit → print "Closing connection"

---

### 1️⃣2️⃣ Timer Context Manager for Code Blocks

**Usage:**

```python
with Timer("load-data"):
    load_data()
```

**Output:**

```
load-data executed in 0.345 seconds
```

---

## 🧩 SECTION 4 — Type Hints

### 1️⃣3️⃣ Strict Type Checking on Function Inputs

Write:

```python
def add_user(user: dict[str, str]) -> bool:
    ...
```

Then write test calls that intentionally violate type hints.
Run a static checker like `mypy` and observe errors.

---

### 1️⃣4️⃣ Type Alias for API Payload

Create:

```python
UserPayload = dict[str, str | int | bool]
```

Then build:

```python
def send_payload(data: UserPayload) -> None:
    ...
```

Call it with correct & incorrect types.

---

### 1️⃣5️⃣ Typed Dict for Employee Schema

Define:

```python
class Employee(TypedDict):
    id: int
    name: str
    salary: float
```

Write:

```python
def process_employee(emp: Employee):
    ...
```

Pass invalid data and test type safety.

---

## 🧩 SECTION 5 — Combined Real-Time Scenarios

These combine decorators + generators + context managers + logging + type hints — similar to real backend engineering tasks.

### 1️⃣6️⃣ Build a Performance Monitoring System (Mini Version of the Project)

Create:
- A decorator to measure execution time
- A context manager to measure block time
- Log results to `performance.log`
- Use type hints everywhere

**Test with:**

```python
@monitor
def process_data():
    ...

with monitor_block("training"):
    train_model()
```

---

### 1️⃣7️⃣ Data Pipeline Using Generators + Decorators

Build a pipeline:
- Generator → reads large CSV
- Decorator → logs time taken for each batch
- Decorator → retries failed batch
- Type hints for each step
- Context manager → open output file safely

---

### 1️⃣8️⃣ Web Scraper with Retry, Caching & Logging

Implement:
- retry decorator
- caching decorator
- context manager for saving results
- type hints
- generator yielding scraped items

---

### 1️⃣9️⃣ Automatic File Cleaner Tool

Create:
- Context manager → ensure folder exists and delete older files
- Generator → iterate over files
- Decorator → log files deleted
- Type hints throughout

---

### 2️⃣0️⃣ Multi-Layer Decorator Challenge

Apply multiple decorators:

```python
@retry(times=3)
@timeit
@logger(level="INFO")
def fetch_products():
    ...
```

**Test that:**
- Retry works
- Logging works
- Timer works
- Order of execution is correct