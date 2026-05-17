# DAY 7 — Advanced Python Concepts (In-Depth Notes)

---

## 🔥 1. Iterators & Generators (Memory-Efficient Programming)

### 🔸 1.1 What is an Iterator?
- In Python, an iterator is an object that allows you to traverse through elements of a collection one at a time, without needing to know how the collection is structured internally.

- It follows two main principles:
    - Iterables → Objects you can loop over (like list, tuple, string, dict, file, etc.)
    - Iterators → Objects that produce values one at a time using two methods:

- An iterable is like a book.
- An iterator is like a bookmark that tells you where you are while reading through the book.


An iterator is any object that implements:
- `__iter__()` → returns an iterator object (often itself)
- `__next__()` → returns the next value or raises `StopIteration`


**✔ Built-in examples of iterators: Example 1: Iterating a list manually** 
```python
numbers = [10, 20, 30]

it = iter(numbers)   # get iterator

print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30
print(next(it))  # error: StopIteration

```

**✔ Realtime Example 1: Reading data from a file**
- Files in Python are iterators.
- Because the file may be large — Python reads one line at a time, not all at once.

```python
file = open("data.txt")

for line in file:  # under the hood uses iterator
    print(line)
```

**✔ Realtime Example 2: Streaming sensor data (simulated)**
- Imagine you get temperature readings from a sensor:
```python
import time
import random

class Sensor:
    def __iter__(self):
        return self
    
    def __next__(self):
        temp = random.uniform(20, 30)
        time.sleep(1)   # fake delay
        return round(temp, 2)

sensor = Sensor()

for reading in sensor:
    print("Temperature:", reading)

```
- This continues indefinitely, producing data one at a time — perfect for an iterator.



**✔ Creating Your Own Iterator: Example: Countdown iterator**

```python
class CountDown:
    def __init__(self, start):
        self.num = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.num <= 0:
            raise StopIteration
        current = self.num
        self.num -= 1
        return current
```

**Use it:**

```python
for i in CountDown(5):
    print(i)
```

**✔ Realtime Example 3: Paginated API fetcher**
- Suppose you call an API that returns 10 items per page:
```python
class APIPaginator:
    def __init__(self, pages):
        self.page = 0
        self.pages = pages

    def __iter__(self):
        return self

    def __next__(self):
        if self.page >= self.pages:
            raise StopIteration
        self.page += 1
        return f"Fetched page {self.page}"

api_data = APIPaginator(3)

for page in api_data:
    print(page)
```

📌 **Where Iterators Are Used in Industry?**
- Pandas iterating over large datasets
- Streaming large files (logs, CSVs)
- Socket data streaming
- Real-time consumer apps (Kafka, RabbitMQ)

### 🔸 1.2 Generators: Iterators Made Easy

Generators allow you to write iterators without creating a class.

**Simple Generator**

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1
```

**Calling:**

```python
for i in countdown(5):
    print(i)
```

📌 **Why Generators Matter?**
- ✔ Use almost no memory
- ✔ Great for huge datasets
- ✔ Used in pipelines, ML data loaders
- ✔ Useful in real-time event streaming

### 🔸 1.3 Generator Expressions

```python
squares = (x*x for x in range(1_000_000))
```

Huge memory savings compared to a list comprehension.

**List vs Generator Memory Difference**

| Operation | Memory |
|-----------|--------|
| List `[x*x for x in range(1M)]` | ~8–10 MB |
| Generator `(x*x for x in range(1M))` | ~0 MB |

### 🔸 1.4 Use Case: Streaming File Reader

Real-world pipelines (ETL, Big Data):

```python
def read_logs(path):
    with open(path) as f:
        for line in f:
            yield line
```

---

## ⚡ 2. Decorators (with parameters)

Decorators allow you to add functionality to functions without modifying their code.

### 🔸 2.1 Basic Decorator

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

**Use:**

```python
@logger
def greet():
    print("Hello!")
```

### 🔸 2.2 Decorator With Arguments (Advanced)

Three layers:
1. Decorator factory (accepts arguments)
2. Actual decorator
3. Wrapper function

**Example: parameterized logging decorator**

```python
def log(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"[{level}] Executing {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

**Use:**

```python
@log("INFO")
def process():
    print("Processing...")
```

### 🔸 2.3 Real-World Use Cases

| Area | Usage |
|------|-------|
| API security | `@authenticate`, `@rate_limit` |
| Performance monitoring | `@timeit` |
| Retry logic | `@retry(3)` |
| Caching | `@lru_cache` |
| Logging | `@log_event` |
| Validation | `@validate_input(type=str)` |

### 🔸 2.4 Timing Decorator (Industry)

```python
import time

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end-start:.4f} seconds")
        return result
    return wrapper
```

Used for profiling slow ML functions.

---

## 🧩 3. Context Managers (with block deep dive)

Context managers handle setup and cleanup automatically.

### 🔸 3.1 How Context Managers Work Internally

A context manager must implement:
- `__enter__()`
- `__exit__()`

**Example:**

```python
class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print("Opening file...")
        self.file = open(self.filename, "r")
        return self.file

    def __exit__(self, exc_type, exc, traceback):
        print("Closing file...")
        self.file.close()
```

**Use:**

```python
with FileManager("data.txt") as f:
    print(f.read())
```

### 🔸 3.2 Contextlib — Pythonic way

```python
from contextlib import contextmanager

@contextmanager
def open_file(name):
    f = open(name)
    try:
        yield f
    finally:
        f.close()
```

### 🔸 3.3 Real-World Uses of Context Managers

| Use Case | Description |
|----------|-------------|
| Database transactions | auto-commit/rollback |
| Lock acquisition | multithreading |
| Timer/scope logging | performance tracing |
| Temporary directories | safe cleanup |
| Resource pools | connections, files |

### 🔸 3.4 Example: Database Transaction Context Manager

```python
class Transaction:
    def __enter__(self):
        db.begin()
    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            db.rollback()
        else:
            db.commit()
```

---

## 🎯 4. Type Hints (Strong Typing for Python)

Introduced in Python 3.5+, widely used in:
- FastAPI
- ML pipelines
- Large codebases
- Production APIs

**Type hints help:**
- ✔ Boost autocomplete
- ✔ Detect bugs early
- ✔ Improve readability
- ✔ Enable static analysis (mypy, pyright)
- ✔ API contract enforcement

### 🔸 4.1 Basic Type Hints

```python
def greet(name: str) -> str:
    return f"Hello {name}"
```

### 🔸 4.2 Type hints for collections

```python
def average(values: list[int]) -> float:
    return sum(values) / len(values)
```

### 🔸 4.3 Optional & Union Types

```python
from typing import Optional

def load_user(id: int) -> Optional[dict]:
    ...
```

### 🔸 4.4 Custom Type Aliases

```python
User = dict[str, str]
```

### 🔸 4.5 Typed Dictionaries

```python
from typing import TypedDict

class Employee(TypedDict):
    name: str
    age: int
    email: str
```

### 🔸 4.6 Type Checking Tools

- mypy
- PyCharm type inspector
- VSCode Pyright
- pydantic (FastAPI)

### 🔸 4.7 Real Industry Example

FastAPI uses type hints to auto-generate:
- Validation
- Swagger documentation
- Serialization
- JSON schema

```python
def get_user(id: int) -> dict[str, str]:
    ...
```

---

## 💡 Mini Project — Performance Monitor Tool

You will combine:
- ✔ Decorators
- ✔ Context managers
- ✔ Logging
- ✔ Timing functions

**Features:**
- Measure execution time of any function
- Log results to a file
- Context manager to measure block execution
- Optional parameters for logging levels

### Core Components

#### 🔹 1. Timing Decorator

```python
def monitor(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        logging.info(f"{func.__name__} took {duration:.4f}s")
        return result
    return wrapper
```

#### 🔹 2. Timer Context Manager

```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        print(f"Block executed in {self.end - self.start:.4f}s")
```

#### 🔹 3. Example Use

```python
@monitor
def slow_function():
    time.sleep(1)

with Timer():
    slow_function()
```