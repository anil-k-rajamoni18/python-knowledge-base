# 🐍 Python — Day 6 Notes

---

## Table of Contents

1. [How Files Work in an OS — The Mental Model](#1-how-files-work-in-an-os--the-mental-model)
2. [Working with Text Files](#2-working-with-text-files)
3. [Binary Files](#3-binary-files)
4. [Working with CSV Files](#4-working-with-csv-files)
5. [JSON — The API Data Format](#5-json--the-api-data-format)
6. [File System Operations with `os` and `pathlib`](#6-file-system-operations-with-os-and-pathlib)
7. [Sending HTTP Requests](#7-sending-http-requests)
8. [Modules — How Python's Import System Works](#8-modules--how-pythons-import-system-works)
9. [Packages and the `__init__.py` File](#9-packages-and-the-__init__py-file)
10. [Standard Library — The Hidden Goldmine](#10-standard-library--the-hidden-goldmine)
11. [Virtual Environments — Deep Dive](#11-virtual-environments--deep-dive)
12. [Logging — The Production Standard](#12-logging--the-production-standard)
13. [Hands-On Exercises (All Coded)](#13-hands-on-exercises-all-coded)
14. [Mini Project — File-Based Todo Manager (Full Implementation)](#14-mini-project--file-based-todo-manager-full-implementation)

---

## 1. How Files Work in an OS — The Mental Model

Before writing a single line of file code, it helps to understand what actually happens when a program opens a file.

```
YOUR PYTHON PROGRAM
       │
       │  open("data.txt", "r")
       ▼
OPERATING SYSTEM KERNEL
  ├── Checks file permissions
  ├── Locates file on disk (via filesystem)
  ├── Creates a FILE DESCRIPTOR (a small integer, e.g. 3)
  ├── Allocates a BUFFER in RAM
  └── Returns a FILE OBJECT to your program

YOUR PYTHON PROGRAM
  ├── Reads/writes via the FILE OBJECT
  └── Data flows through the buffer (not directly to/from disk)

When you close() or the with-block exits:
  ├── Buffer is FLUSHED to disk
  ├── File descriptor is released
  └── OS resources are freed
```

This explains several things:
- Why you **must** close files — unclosed files keep OS file descriptors occupied (limited resource)
- Why `with open()` is essential — it guarantees the close even if an exception happens
- Why writes sometimes don't appear immediately — they're buffered; `flush()` forces them to disk

### File Paths

```python
# Absolute path — starts from root
"/home/anil/projects/sprox/config.json"     # Linux/Mac
"C:\\Users\\Anil\\projects\\sprox\\data.csv" # Windows

# Relative path — relative to where the script runs
"config.json"            # same directory
"../data/config.json"    # one level up, then data/
"data/config.json"       # subdirectory

# Best practice — use pathlib (cross-platform)
from pathlib import Path
base = Path(__file__).parent         # directory of the current script
config_path = base / "config.json"   # OS-aware path joining
```

---

## 2. Working with Text Files

### File Opening Modes — Complete Reference

| Mode | Read | Write | Creates? | Truncates? | Position |
|------|------|-------|----------|------------|----------|
| `"r"` | ✅ | ❌ | ❌ | ❌ | Start |
| `"w"` | ❌ | ✅ | ✅ | ✅ Yes | Start |
| `"a"` | ❌ | ✅ | ✅ | ❌ | End |
| `"x"` | ❌ | ✅ | ✅ (fails if exists) | ❌ | Start |
| `"r+"` | ✅ | ✅ | ❌ | ❌ | Start |
| `"w+"` | ✅ | ✅ | ✅ | ✅ Yes | Start |
| `"a+"` | ✅ | ✅ | ✅ | ❌ | End |
| `"rb"`, `"wb"`, `"ab"` | binary | binary | same as above | — | — |

> **Real-world rule:** Use `"w"` only when you want to overwrite completely (e.g. writing a fresh report). Use `"a"` for log files. Use `"r"` for reading config. Use `"x"` to safely create a file that must not already exist (prevents accidental overwrites).

### The `with` Statement — Context Manager

```python
# ❌ Risky — if an exception occurs before close(), file stays open
f = open("data.txt", "r")
content = f.read()
f.close()   # might never reach this line

# ✅ Always use with — guarantees close() even if exception occurs
with open("data.txt", "r") as f:
    content = f.read()
# file is closed here automatically — no matter what happened inside
```

`with` works via Python's **context manager protocol** (`__enter__` and `__exit__` methods). The file object implements this — `__exit__` calls `close()` for you.

### Reading Methods Compared

```python
with open("server.log", "r", encoding="utf-8") as f:

    # .read() — entire file as one string (avoid for large files)
    content = f.read()

    # .read(n) — read exactly n characters
    chunk = f.read(1024)

    # .readline() — one line including \n
    line = f.readline()

    # .readlines() — all lines as a list
    lines = f.readlines()   # ["line1\n", "line2\n", ...]

    # Iterating (best for large files — memory efficient)
    for line in f:          # reads one line at a time, not all into RAM
        process(line.strip())
```

**Real-world rule:** Never use `.read()` or `.readlines()` on log files or data files that could be large (100MB+). Always iterate line by line.

### Writing Files

```python
# Write (overwrites if file exists)
with open("report.txt", "w", encoding="utf-8") as f:
    f.write("Sales Report — May 2026\n")
    f.write("=" * 40 + "\n")

    # writelines — writes list of strings (no automatic newlines!)
    lines = ["Item 1: ₹500\n", "Item 2: ₹1200\n"]
    f.writelines(lines)

# Append — adds to end without erasing
with open("app.log", "a", encoding="utf-8") as f:
    f.write("2026-05-12 10:30:00 INFO Server started\n")
```

### Real-World Examples

**Processing server logs (streaming, memory-safe):**
```python
from datetime import datetime

error_count = 0
error_lines = []

with open("server.log", "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, start=1):
        if "ERROR" in line or "CRITICAL" in line:
            error_count += 1
            error_lines.append(f"Line {line_num}: {line.strip()}")

# Write error summary
with open("error_report.txt", "w") as out:
    out.write(f"Error Report — Generated {datetime.now()}\n")
    out.write(f"Total errors found: {error_count}\n\n")
    out.writelines(line + "\n" for line in error_lines)

print(f"Found {error_count} errors. Report saved.")
```

**Config file read/write:**
```python
def read_config(path):
    """Read key=value config file into a dict."""
    config = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):   # skip blank/comments
                continue
            key, _, value = line.partition("=")
            config[key.strip()] = value.strip()
    return config

def write_config(path, config):
    """Write dict back to key=value config file."""
    with open(path, "w") as f:
        for key, value in config.items():
            f.write(f"{key} = {value}\n")

# Usage
config = read_config("app.conf")
config["debug"] = "false"
write_config("app.conf", config)
```

### File Pointer and `seek()`

```python
with open("data.txt", "r+") as f:
    content = f.read()
    print(f.tell())         # current position (end of file)

    f.seek(0)               # go back to start
    f.write("UPDATED\n")    # overwrite from the beginning

    f.seek(0, 2)            # seek to end (0 bytes from end)
    f.write("appended\n")
```

---

## 3. Binary Files

Not all files are text. Images, PDFs, Excel files, pickled Python objects, and compiled code are binary.

```python
# Reading a binary file
with open("image.png", "rb") as f:
    header = f.read(8)   # read first 8 bytes
    print(header.hex())  # PNG files start with 89504e470d0a1a0a

# Copying a binary file
with open("source.jpg", "rb") as src, open("copy.jpg", "wb") as dst:
    while chunk := src.read(65536):   # 64KB chunks
        dst.write(chunk)

# Pickling Python objects (serialization)
import pickle

data = {"model": "GPT", "accuracy": 0.94, "params": [1.2, 0.8, 3.1]}

# Save to disk
with open("model_meta.pkl", "wb") as f:
    pickle.dump(data, f)

# Load from disk
with open("model_meta.pkl", "rb") as f:
    loaded = pickle.load(f)

print(loaded)   # {"model": "GPT", "accuracy": 0.94, ...}
```

> **Security Warning:** Never unpickle data from untrusted sources. Pickle can execute arbitrary code on load. Use JSON for external data exchange.

---

## 4. Working with CSV Files

CSV (Comma-Separated Values) is the most common format for tabular data exchange — HR systems, finance reports, data exports, ETL pipelines.

### Why Use the `csv` Module Instead of `split(",")`?

Raw splitting breaks on commas inside quoted fields:
```
"Smith, John",28,"Engineer, Senior"
```
`"Engineer, Senior".split(",")` gives `["Engineer", " Senior"]` — wrong. The `csv` module handles quoting, escaping, and newlines inside fields correctly.

### Reading CSV

```python
import csv

# Basic reader — rows as lists
with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)    # skip header row
    for row in reader:
        print(row)            # ["Anil", "28", "Engineering"]

# DictReader — rows as dicts (preferred in production)
with open("employees.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # row is {"name": "Anil", "age": "28", "dept": "Engineering"}
        name = row["name"]
        age  = int(row["age"])   # remember: values are strings
        print(f"{name}, age {age}")
```

### Writing CSV

```python
import csv

employees = [
    {"name": "Anil",  "age": 28, "dept": "Engineering", "salary": 85000},
    {"name": "Sara",  "age": 26, "dept": "HR",          "salary": 62000},
    {"name": "Ravi",  "age": 31, "dept": "Finance",     "salary": 74000},
]

with open("employees_export.csv", "w", newline="", encoding="utf-8") as f:
    # newline="" is important on Windows — prevents extra blank rows
    writer = csv.DictWriter(f, fieldnames=["name", "age", "dept", "salary"])
    writer.writeheader()
    writer.writerows(employees)

print("CSV written.")
```

### Real-World — ETL Pipeline (Extract, Transform, Load)

```python
import csv
from datetime import datetime

def process_sales_csv(input_path, output_path):
    """
    Read raw sales data, clean it, add computed columns, write output.
    Typical ETL preprocessing step.
    """
    processed = []
    errors = []

    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_num, row in enumerate(reader, start=2):   # start=2 (header is 1)
            try:
                amount = float(row["amount"])
                gst    = amount * 0.18
                total  = amount + gst

                processed.append({
                    "order_id":   row["order_id"],
                    "customer":   row["customer"].strip().title(),
                    "amount":     round(amount, 2),
                    "gst":        round(gst, 2),
                    "total":      round(total, 2),
                    "processed_at": datetime.now().isoformat()
                })
            except (ValueError, KeyError) as e:
                errors.append(f"Line {line_num}: {e}")

    # Write processed data
    if processed:
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=processed[0].keys())
            writer.writeheader()
            writer.writerows(processed)

    return len(processed), errors

count, errors = process_sales_csv("raw_sales.csv", "clean_sales.csv")
print(f"Processed {count} rows. Errors: {len(errors)}")
for err in errors:
    print(f"  ⚠ {err}")
```

---

## 5. JSON — The API Data Format

JSON (JavaScript Object Notation) is the lingua franca of web APIs. REST APIs, configuration files, NoSQL databases, and inter-service communication all use JSON.

### Python ↔ JSON Mapping

```
Python           JSON
──────────────────────
dict         →   object  {}
list         →   array   []
str          →   string  ""
int, float   →   number
True/False   →   true/false
None         →   null
```

### Reading JSON

```python
import json

# From file
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)          # file → dict

# From string (e.g. API response body)
json_string = '{"name": "Anil", "role": "admin", "active": true}'
data = json.loads(json_string)     # string → dict
print(data["name"])                # "Anil"
print(data["active"])              # True (Python bool, not string)
```

### Writing JSON

```python
import json

payload = {
    "user_id": 1042,
    "name": "Anil Rajamoni",
    "skills": ["Python", "FastAPI", "Kubernetes"],
    "metadata": {"joined": "2024-01-15", "verified": True}
}

# To file
with open("user.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=4, ensure_ascii=False)
    #                     ↑          ↑
    #                  readable   supports unicode (₹, é, etc.)

# To string (e.g. for API response body or logging)
json_string = json.dumps(payload, indent=2)
print(json_string)
```

### Handling Non-Serializable Types

Python's `json` module can only serialize basic types. Custom types need a handler:

```python
import json
from datetime import datetime, date
from decimal import Decimal

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

data = {
    "created_at": datetime.now(),
    "price": Decimal("1299.99"),
    "tags": {"python", "backend"}
}

print(json.dumps(data, cls=CustomEncoder, indent=2))
```

### Real-World — Config-Driven Application

```python
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "app": {"name": "sproxhrms", "version": "1.0.0", "debug": False},
    "database": {"host": "localhost", "port": 5432, "name": "sprox"},
    "cache": {"ttl": 300, "max_size": 1000}
}

def load_config(config_path="config.json"):
    path = Path(config_path)
    if not path.exists():
        print("Config not found. Using defaults.")
        with open(config_path, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

    with open(config_path, "r") as f:
        user_config = json.load(f)

    # Deep merge: user config overrides defaults
    merged = DEFAULT_CONFIG.copy()
    for section, values in user_config.items():
        if section in merged and isinstance(merged[section], dict):
            merged[section].update(values)
        else:
            merged[section] = values

    return merged

config = load_config()
print(f"Running {config['app']['name']} v{config['app']['version']}")
print(f"DB: {config['database']['host']}:{config['database']['port']}")
```

---

## 6. File System Operations with `os` and `pathlib`

### `pathlib` — The Modern Way (Python 3.4+)

`pathlib` provides an object-oriented interface to the file system. It's cross-platform (works on Windows, Linux, Mac without changing `/` to `\\`).

```python
from pathlib import Path

# Create paths
home    = Path.home()                    # /home/anil
cwd     = Path.cwd()                     # current working directory
script  = Path(__file__)                 # path of current script
data    = Path("data") / "reports" / "2026.csv"   # path joining with /

# Path information
print(data.name)        # "2026.csv"
print(data.stem)        # "2026"
print(data.suffix)      # ".csv"
print(data.parent)      # data/reports
print(data.is_absolute())

# Checks
data.exists()
data.is_file()
data.is_dir()

# Create directories
Path("logs/2026/05").mkdir(parents=True, exist_ok=True)
# parents=True creates intermediate dirs
# exist_ok=True doesn't raise error if already exists

# List files
for f in Path("data").iterdir():
    print(f)

# Glob — find files by pattern
for py_file in Path(".").glob("**/*.py"):   # recursive
    print(py_file)

for csv_file in Path("reports").glob("*.csv"):
    print(csv_file)

# Read and write directly (small files)
content = Path("config.txt").read_text(encoding="utf-8")
Path("output.txt").write_text("Hello World", encoding="utf-8")
```

### `os` Module — Lower-Level Operations

```python
import os

os.getcwd()                           # current working directory
os.chdir("/home/anil/project")        # change directory
os.listdir(".")                       # list directory contents
os.makedirs("a/b/c", exist_ok=True)  # create nested dirs
os.remove("temp.txt")                 # delete file
os.rmdir("empty_dir")                 # delete empty directory
os.rename("old.txt", "new.txt")       # rename/move
os.path.exists("file.txt")           # check if exists
os.path.join("data", "file.csv")     # OS-aware path join

# Environment variables
db_pass = os.environ.get("DB_PASSWORD", "fallback_default")
# Never hardcode secrets — read from environment
```

### Real-World — Organizing Files by Date

```python
from pathlib import Path
from datetime import datetime
import shutil

def organize_logs(source_dir: str, archive_dir: str):
    """Move log files into year/month subdirectories based on modification date."""
    source = Path(source_dir)
    archive = Path(archive_dir)

    moved = 0
    for log_file in source.glob("*.log"):
        mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
        dest_dir = archive / str(mtime.year) / f"{mtime.month:02d}"
        dest_dir.mkdir(parents=True, exist_ok=True)

        shutil.move(str(log_file), dest_dir / log_file.name)
        moved += 1

    print(f"Organized {moved} log files.")

organize_logs("logs/raw", "logs/archive")
```

---

## 7. Sending HTTP Requests

The `requests` library is the standard way to consume REST APIs in Python. It abstracts the complexity of HTTP into a clean, intuitive interface.

```bash
pip install requests
```

### Core Request Types

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# ── GET ────────────────────────────────────────────────────────────────────
response = requests.get(f"{BASE_URL}/users/1")
print(response.status_code)    # 200
print(response.headers["Content-Type"])
data = response.json()         # parses JSON body → dict
print(data["name"])

# With query parameters
params = {"_limit": 5, "_page": 1}
response = requests.get(f"{BASE_URL}/posts", params=params)
# Equivalent URL: /posts?_limit=5&_page=1

# ── POST ───────────────────────────────────────────────────────────────────
payload = {"title": "New Post", "body": "Content here", "userId": 1}
response = requests.post(
    f"{BASE_URL}/posts",
    json=payload,                          # auto-sets Content-Type: application/json
    headers={"Authorization": "Bearer token123"}
)
print(response.status_code)   # 201 Created
print(response.json())

# ── PUT (full update) ───────────────────────────────────────────────────────
response = requests.put(
    f"{BASE_URL}/posts/1",
    json={"title": "Updated", "body": "New content", "userId": 1}
)

# ── PATCH (partial update) ─────────────────────────────────────────────────
response = requests.patch(f"{BASE_URL}/posts/1", json={"title": "Patched"})

# ── DELETE ─────────────────────────────────────────────────────────────────
response = requests.delete(f"{BASE_URL}/posts/1")
print(response.status_code)   # 200 or 204
```

### Production-Grade Request Handling

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session(retries=3, backoff=0.5, timeout=10):
    """Create a requests session with retry logic and timeout."""
    session = requests.Session()

    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff,          # waits: 0.5, 1.0, 2.0 seconds
        status_forcelist=[429, 500, 502, 503, 504],   # retry on these codes
        allowed_methods=["GET", "POST"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # Set default timeout on all requests
    session.request = lambda method, url, **kwargs: \
        requests.Session.request(session, method, url, timeout=timeout, **kwargs)

    return session

# Usage
session = create_session()

try:
    response = session.get("https://api.example.com/users")
    response.raise_for_status()   # raises HTTPError for 4xx/5xx
    users = response.json()

except requests.exceptions.ConnectionError:
    print("Network error — check internet connection")
except requests.exceptions.Timeout:
    print("Request timed out — server too slow")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code} — {e.response.text}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### Real-World — Fetching and Saving API Data

```python
import requests
import json
from pathlib import Path
from datetime import datetime

def fetch_and_cache(url: str, cache_file: str, max_age_hours=1):
    """Fetch from API, cache locally, return cached if fresh."""
    cache_path = Path(cache_file)

    # Check if cache is fresh
    if cache_path.exists():
        age = datetime.now().timestamp() - cache_path.stat().st_mtime
        if age < max_age_hours * 3600:
            print(f"Using cached data ({age/60:.1f} min old)")
            return json.loads(cache_path.read_text())

    # Fetch fresh data
    print("Fetching fresh data from API...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Save to cache
    cache_path.write_text(json.dumps(data, indent=2))
    print(f"Data cached to {cache_file}")
    return data

users = fetch_and_cache(
    "https://jsonplaceholder.typicode.com/users",
    "cache/users.json"
)
for user in users[:3]:
    print(f"  {user['name']} — {user['email']}")
```

---

## 8. Modules — How Python's Import System Works

### What Is a Module?

Any `.py` file is a module. When you write `import math`, Python finds `math.py` (or its compiled equivalent) and runs it. Everything defined at the top level of that file becomes available as attributes of the module object.

### How Python Finds Modules — `sys.path`

```python
import sys
print(sys.path)
```

Python searches for modules in this order:
1. The directory of the script being run
2. Directories in the `PYTHONPATH` environment variable
3. Standard library directories
4. Site-packages (where `pip install` puts things)

```
import requests
         │
         ▼
sys.path search order:
  1. Current script's directory → not found
  2. PYTHONPATH dirs            → not found
  3. Standard library           → not found
  4. site-packages/requests/    → FOUND ✅
```

### Import Styles — Comparison

```python
# 1. Import module — access via module name (safest, most explicit)
import math
print(math.sqrt(16))
print(math.pi)

# 2. Import specific names — faster access, but pollutes namespace
from math import sqrt, pi, ceil
print(sqrt(16))

# 3. Import with alias — for long names or common conventions
import numpy as np             # standard in data science
import pandas as pd            # standard in data engineering
from datetime import datetime as dt

# 4. Import all — avoid in production code (pollutes namespace, hard to trace)
from math import *             # ❌ not recommended

# 5. Conditional import — handle optional dependencies gracefully
try:
    import ujson as json       # faster JSON library
except ImportError:
    import json                # fallback to stdlib
```

### Creating Your Own Module

**`file: math_utils.py`**
```python
"""Utility functions for mathematical operations."""

PI = 3.14159265358979

def circle_area(radius: float) -> float:
    """Calculate area of a circle."""
    return PI * radius ** 2

def circle_perimeter(radius: float) -> float:
    """Calculate perimeter of a circle."""
    return 2 * PI * radius

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def primes_up_to(limit: int) -> list:
    """Return all primes up to limit using Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]

# This block only runs when the file is executed directly
# NOT when it's imported as a module
if __name__ == "__main__":
    print(f"Area of circle r=5: {circle_area(5):.2f}")
    print(f"Primes up to 30: {primes_up_to(30)}")
```

**Using the module:**
```python
import math_utils as mu

print(mu.circle_area(7))
print(mu.is_prime(17))     # True
print(mu.is_prime(18))     # False
```

### The `__name__ == "__main__"` Pattern

```python
# In mymodule.py:
def helper():
    return "help"

def main():
    print("Running as a script")

if __name__ == "__main__":
    main()
    # This block only executes when you run: python mymodule.py
    # It does NOT execute when another file does: import mymodule
```

This is the standard way to make a file both importable as a library and runnable as a standalone script. Every well-written Python module has this.

---

## 9. Packages and the `__init__.py` File

### What Is a Package?

A package is a directory containing Python modules and a special `__init__.py` file. It lets you organize related modules into a namespace hierarchy.

```
sprox_utils/              ← package (directory)
│
├── __init__.py           ← marks this as a package; runs on import
├── db.py                 ← sprox_utils.db
├── auth.py               ← sprox_utils.auth
├── validators.py         ← sprox_utils.validators
│
└── api/                  ← sub-package
    ├── __init__.py
    ├── routes.py         ← sprox_utils.api.routes
    └── middleware.py     ← sprox_utils.api.middleware
```

### `__init__.py` — What It Does

```python
# sprox_utils/__init__.py

# 1. Can be empty — just marks directory as package

# 2. Can import things to simplify the public API
from .db import connect, disconnect
from .auth import verify_token, hash_password
from .validators import validate_email, validate_phone

__version__ = "1.0.0"
__author__ = "Anil Rajamoni"

# Now users can do:
#   from sprox_utils import connect  (instead of from sprox_utils.db import connect)
#   import sprox_utils; sprox_utils.verify_token(...)
```

### Import Styles for Packages

```python
# Absolute imports (recommended)
from sprox_utils.db import connect
from sprox_utils.api.routes import router

# Relative imports (inside the package itself)
# In sprox_utils/auth.py:
from .db import connect          # sibling module
from ..config import settings    # parent package module
```

### Real-World Package Structure

```
sproxhrms/
│
├── main.py                  ← entry point
├── requirements.txt
├── .env
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── database.py
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── tenant.py
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   └── tenant_service.py
│
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── users.py
│   └── middleware/
│       ├── __init__.py
│       └── auth_middleware.py
│
└── utils/
    ├── __init__.py
    ├── validators.py
    └── helpers.py
```

---

## 10. Standard Library — The Hidden Goldmine

Python's standard library has batteries included. Before installing a third-party package, check if the stdlib already has it.

```python
# os — operating system interface
import os
os.environ.get("SECRET_KEY")
os.getpid()                    # current process ID

# pathlib — file system paths
from pathlib import Path

# datetime — dates and times
from datetime import datetime, date, timedelta
now   = datetime.now()
today = date.today()
week_ago = now - timedelta(weeks=1)
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

# collections — specialized containers
from collections import defaultdict, Counter, OrderedDict, deque, namedtuple

# itertools — efficient iteration tools
import itertools
list(itertools.chain([1,2], [3,4], [5]))       # [1,2,3,4,5]
list(itertools.combinations("ABCD", 2))        # all 2-item combos
list(itertools.product([0,1], repeat=3))       # all binary 3-tuples

# functools — higher-order functions
from functools import lru_cache, partial, reduce

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

# re — regular expressions
import re
email_pattern = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]+$")
is_valid = bool(email_pattern.match("anil@company.com"))

# random — random number generation
import random
random.choice(["red", "green", "blue"])
random.randint(1, 100)
random.sample(range(100), 10)      # 10 unique random numbers
random.shuffle(my_list)            # shuffle in place

# hashlib — cryptographic hashing
import hashlib
h = hashlib.sha256("password123".encode()).hexdigest()

# uuid — unique IDs
import uuid
user_id = str(uuid.uuid4())   # "f47ac10b-58cc-4372-a567-0e02b2c3d479"

# argparse — CLI argument parsing
import argparse
parser = argparse.ArgumentParser(description="My Tool")
parser.add_argument("--input",  required=True)
parser.add_argument("--output", default="output.csv")
args = parser.parse_args()
```

---

## 11. Virtual Environments — Deep Dive

### The Problem They Solve

```
WITHOUT VIRTUAL ENVIRONMENTS:
──────────────────────────────────────────────────────────
Global Python installation
├── requests 2.28
├── flask 2.0          ← Project A needs this
├── flask 3.0          ← Project B needs this ← CONFLICT!
└── numpy 1.24

This is impossible. Only one version can be installed globally.
```

```
WITH VIRTUAL ENVIRONMENTS:
──────────────────────────────────────────────────────────
project_a/
└── venv/
    └── site-packages/
        ├── flask 2.0
        └── requests 2.28

project_b/
└── venv/
    └── site-packages/
        ├── flask 3.0
        └── requests 2.31

Each project has its own isolated sandbox. No conflicts.
```

### How venv Works Internally

```python
python -m venv venv
```

This creates:
```
venv/
├── bin/ (or Scripts/ on Windows)
│   ├── python        ← symlink to system Python
│   ├── pip           ← isolated pip
│   └── activate      ← shell script to activate
│
├── lib/
│   └── python3.11/
│       └── site-packages/   ← all installed packages go here
│
└── pyvenv.cfg        ← config: which Python, include-system-site-packages
```

When you activate, your shell's `PATH` is modified to find the venv's `bin/` first — so `python` and `pip` refer to the venv versions.

### Complete Workflow

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate.bat         # Windows CMD
venv\Scripts\Activate.ps1         # Windows PowerShell

# Verify you're in the venv
which python          # should show venv path
python --version

# 3. Install packages (isolated to this venv)
pip install fastapi uvicorn sqlalchemy pydantic

# 4. Save dependencies
pip freeze > requirements.txt

# contents of requirements.txt:
# anyio==3.7.1
# fastapi==0.110.0
# pydantic==2.6.3
# ...

# 5. Deactivate when done
deactivate

# 6. Recreate (when another developer clones the repo)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### `.gitignore` for Python Projects

```
# .gitignore
venv/
__pycache__/
*.pyc
*.pyo
.env
*.log
.DS_Store
```

Never commit the `venv/` folder. Commit only `requirements.txt`. Team members create their own venv from it.

### `uv` — The Modern Fast Alternative (2024+)

`uv` is a Rust-based Python package manager that's 10–100x faster than pip:

```bash
pip install uv

# Create venv
uv venv

# Install packages (much faster)
uv pip install fastapi uvicorn sqlalchemy

# Sync from requirements.txt
uv pip sync requirements.txt
```

---

## 12. Logging — The Production Standard

### Why Not `print()`?

```python
# print() issues in production:
print("User logged in")           # no timestamp
print("Error: connection failed") # no severity level
print("DB query took 2.1s")       # goes to stdout only, not to a file
                                  # can't be turned off without changing code
                                  # no caller information

# logging gives you:
# 2026-05-12 10:30:45,123 - INFO  - auth.py:42 - User 1042 logged in
# 2026-05-12 10:30:46,890 - ERROR - db.py:108 - Connection refused: localhost:5432
```

### Logging Levels and When to Use Them

```
LEVEL       VALUE   WHEN TO USE
──────────────────────────────────────────────────────────────────────
DEBUG       10      Detailed diagnostic info. Only in development.
                    e.g. "Query executed: SELECT * FROM users WHERE id=1"

INFO        20      Normal application events. Healthy milestones.
                    e.g. "Server started on port 8000"
                    e.g. "User 1042 logged in successfully"

WARNING     30      Something unexpected but not an error. App still works.
                    e.g. "Retry attempt 2/3 for API call"
                    e.g. "Config key 'timeout' not found, using default"

ERROR       40      An error occurred. Specific operation failed.
                    e.g. "DB query failed: connection timeout"
                    e.g. "Payment charge failed for order #5042"

CRITICAL    50      Severe error. System may stop working.
                    e.g. "Database unreachable after 3 retries — shutting down"
```

### Basic Setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)-8s — %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()    # also print to console
    ]
)

logger = logging.getLogger(__name__)
# __name__ is the module name — e.g. "sproxhrms.services.auth_service"
# This creates a logger hierarchy, not a flat global logger

logger.debug("Starting configuration load")
logger.info("Application started successfully")
logger.warning("Cache size approaching limit: 950/1000")
logger.error("Failed to send email to user@example.com")
logger.critical("Redis connection lost — caching disabled")
```

### Production Logging Setup — Structured Logging

Modern production systems use structured (JSON) logging so that log aggregators (Datadog, ELK Stack, Loki) can parse and query logs efficiently.

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Format log records as JSON for structured logging."""

    def format(self, record):
        log_entry = {
            "timestamp":  datetime.utcnow().isoformat() + "Z",
            "level":      record.levelname,
            "logger":     record.name,
            "message":    record.getMessage(),
            "module":     record.module,
            "function":   record.funcName,
            "line":       record.lineno,
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)

def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)

    return logger

# Usage
logger = setup_logger("sproxhrms.auth")
logger.info("Login successful", extra={"user_id": 1042, "ip": "192.168.1.1"})
```

### Logging Context — Tracking Requests

In a web application, you want every log line for a given request to share a common request ID:

```python
import logging
import uuid

class RequestLogger:
    """Add request context to all log calls."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.request_id = str(uuid.uuid4())[:8]

    def _prefix(self, msg):
        return f"[req:{self.request_id}] {msg}"

    def info(self, msg, *args, **kwargs):
        self.logger.info(self._prefix(msg), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(self._prefix(msg), *args, **kwargs)

# In your request handler
base_logger = logging.getLogger("sproxhrms.api")

def handle_login(username: str):
    log = RequestLogger(base_logger)
    log.info(f"Login attempt for user: {username}")
    # ... do login logic
    log.info("Login successful")
    # All lines share the same [req:abc12345] prefix
```

### Logging Best Practices

```python
# ✅ Use lazy string formatting — don't format if log level disabled
logger.debug("Processing record: %s", record)     # only formats if DEBUG enabled
# ❌ Avoids:
logger.debug(f"Processing record: {record}")       # always formats, even if disabled

# ✅ Log exceptions with traceback
try:
    risky_operation()
except Exception as e:
    logger.exception("Operation failed")           # logs message + full traceback
    # or
    logger.error("Operation failed", exc_info=True)

# ✅ Separate loggers per module — don't use root logger
logger = logging.getLogger(__name__)   # one per file

# ❌ Never log sensitive information
logger.info(f"User password: {password}")          # security violation!
logger.info(f"Auth token: {token}")                # security violation!
# ✅ Log safely
logger.info(f"Login attempt for user: {username}")
```

---

## 13. Hands-On Exercises (All Coded)

### Exercise 1 — Log File Parser

```python
from pathlib import Path
from collections import Counter
import re

def parse_log_file(path: str):
    """Parse a log file and produce a summary report."""
    log_path = Path(path)
    if not log_path.exists():
        print(f"File not found: {path}")
        return

    level_counts = Counter()
    errors = []
    total_lines = 0
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) — (\w+) — (.+)")

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            total_lines += 1
            match = pattern.search(line)
            if match:
                timestamp, level, message = match.groups()
                level_counts[level] += 1
                if level in ("ERROR", "CRITICAL"):
                    errors.append(f"[{timestamp}] {message}")

    print(f"\n{'='*50}")
    print(f"  LOG ANALYSIS: {path}")
    print(f"{'='*50}")
    print(f"  Total lines: {total_lines}")
    for level, count in sorted(level_counts.items()):
        print(f"  {level:<10}: {count}")

    if errors:
        print(f"\n  Recent Errors:")
        for err in errors[-5:]:    # last 5 errors
            print(f"    ⚠ {err}")

parse_log_file("app.log")
```

### Exercise 2 — JSON Config Manager

```python
import json
from pathlib import Path

class ConfigManager:
    """Load, update, and save JSON configuration files."""

    def __init__(self, config_path: str):
        self.path = Path(config_path)
        self.config = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            with open(self.path, "r") as f:
                return json.load(f)
        return {}

    def get(self, key: str, default=None):
        """Get value using dot-notation key: 'database.host'"""
        keys = key.split(".")
        val  = self.config
        for k in keys:
            if not isinstance(val, dict):
                return default
            val = val.get(k, default)
        return val

    def set(self, key: str, value):
        """Set value using dot-notation key."""
        keys = key.split(".")
        d    = self.config
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.config, f, indent=4)

    def __repr__(self):
        return json.dumps(self.config, indent=2)

# Usage
cfg = ConfigManager("config/app.json")
cfg.set("database.host", "localhost")
cfg.set("database.port", 5432)
cfg.set("app.debug", True)
cfg.save()

print(cfg.get("database.host"))   # "localhost"
print(cfg.get("app.debug"))       # True
print(cfg.get("missing.key", "default"))  # "default"
```

### Exercise 3 — CSV Report Generator

```python
import csv
import json
from datetime import datetime
from pathlib import Path

def generate_sales_report(data_file: str, report_file: str):
    """Read sales JSON, compute stats, write CSV report."""
    # Read raw data
    with open(data_file, "r") as f:
        sales = json.load(f)

    # Compute per-region totals
    region_totals = {}
    for sale in sales:
        region = sale["region"]
        amount = sale["amount"]
        if region not in region_totals:
            region_totals[region] = {"sales": 0, "total": 0.0}
        region_totals[region]["sales"] += 1
        region_totals[region]["total"] += amount

    # Write report
    with open(report_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["region", "total_sales", "revenue", "avg_order"])
        writer.writeheader()
        for region, data in sorted(region_totals.items()):
            writer.writerow({
                "region":      region,
                "total_sales": data["sales"],
                "revenue":     round(data["total"], 2),
                "avg_order":   round(data["total"] / data["sales"], 2)
            })

    print(f"Report saved: {report_file}")

# Create sample data and run
sample_data = [
    {"region": "South", "amount": 15000, "date": "2026-05-01"},
    {"region": "North", "amount": 22000, "date": "2026-05-01"},
    {"region": "South", "amount": 18500, "date": "2026-05-02"},
    {"region": "East",  "amount": 9000,  "date": "2026-05-02"},
    {"region": "North", "amount": 31000, "date": "2026-05-03"},
]

with open("sales.json", "w") as f:
    json.dump(sample_data, f)

generate_sales_report("sales.json", "sales_report.csv")
```

### Exercise 4 — HTTP Data Fetcher with Caching

```python
import requests
import json
from pathlib import Path
from datetime import datetime

def fetch_github_repos(username: str, cache_hours: int = 1) -> list:
    """Fetch public repos for a GitHub user, with local caching."""
    cache_path = Path(f"cache/{username}_repos.json")
    cache_path.parent.mkdir(exist_ok=True)

    # Check cache freshness
    if cache_path.exists():
        age = (datetime.now().timestamp() - cache_path.stat().st_mtime) / 3600
        if age < cache_hours:
            print(f"Using cache ({age:.1f}h old)")
            return json.loads(cache_path.read_text())

    # Fetch from API
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        repos = resp.json()
        # Save to cache
        cache_path.write_text(json.dumps(repos, indent=2))
        return repos
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        if cache_path.exists():
            print("Falling back to stale cache")
            return json.loads(cache_path.read_text())
        return []

repos = fetch_github_repos("torvalds")
for r in sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:5]:
    print(f"⭐ {r.get('stargazers_count', 0):>6}  {r['name']}")
```

---

## 14. Mini Project — File-Based Todo Manager (Full Implementation)

A complete CLI todo app using JSON for persistence, logging for audit trail, and `pathlib` for file handling. This mirrors how real backend systems work before a database is introduced.

```python
"""
todo_app/
├── todo_manager.py    ← this file
├── todo.json          ← data store (auto-created)
└── todo.log           ← audit log (auto-created)
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path

# ─── Config ──────────────────────────────────────────────────────────────────
DATA_FILE = Path("todo.json")
LOG_FILE  = Path("todo.log")

# ─── Logging Setup ───────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("todo_app")

# ─── Data Layer ──────────────────────────────────────────────────────────────
def load_tasks() -> list:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks: list):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

# ─── Business Logic ──────────────────────────────────────────────────────────
def add_task(title: str, priority: str = "medium") -> dict:
    tasks = load_tasks()
    task = {
        "id":         str(uuid.uuid4())[:8],
        "title":      title.strip(),
        "priority":   priority.lower(),
        "done":       False,
        "created_at": datetime.now().isoformat(),
        "done_at":    None
    }
    tasks.append(task)
    save_tasks(tasks)
    logger.info(f"Task added: [{task['id']}] {task['title']} (priority: {priority})")
    return task

def complete_task(task_id: str) -> bool:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"Task {task_id} is already done.")
                return False
            task["done"]    = True
            task["done_at"] = datetime.now().isoformat()
            save_tasks(tasks)
            logger.info(f"Task completed: [{task_id}] {task['title']}")
            return True
    print(f"Task {task_id} not found.")
    return False

def delete_task(task_id: str) -> bool:
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == original_count:
        print(f"Task {task_id} not found.")
        return False
    save_tasks(tasks)
    logger.info(f"Task deleted: {task_id}")
    return True

def list_tasks(filter_by: str = "all") -> list:
    tasks = load_tasks()
    if filter_by == "pending":
        return [t for t in tasks if not t["done"]]
    elif filter_by == "done":
        return [t for t in tasks if t["done"]]
    return tasks

def get_stats() -> dict:
    tasks = load_tasks()
    total    = len(tasks)
    done     = sum(1 for t in tasks if t["done"])
    pending  = total - done
    by_prio  = {}
    for t in tasks:
        by_prio[t["priority"]] = by_prio.get(t["priority"], 0) + 1
    return {"total": total, "done": done, "pending": pending, "by_priority": by_prio}

# ─── Display ─────────────────────────────────────────────────────────────────
PRIORITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🟢"}

def display_tasks(tasks: list):
    if not tasks:
        print("  No tasks found.")
        return
    print(f"\n  {'ID':<10} {'Status':<8} {'P':<4} {'Title'}")
    print("  " + "-" * 55)
    for t in tasks:
        status = "✅ Done" if t["done"] else "⏳ Pending"
        icon   = PRIORITY_ICON.get(t["priority"], "⚪")
        print(f"  {t['id']:<10} {status:<14} {icon}  {t['title']}")

# ─── CLI Interface ────────────────────────────────────────────────────────────
def show_menu():
    print("\n" + "═" * 40)
    print("        📝 TODO MANAGER")
    print("═" * 40)
    print("  1. View all tasks")
    print("  2. View pending tasks")
    print("  3. View completed tasks")
    print("  4. Add a task")
    print("  5. Complete a task")
    print("  6. Delete a task")
    print("  7. View statistics")
    print("  8. Exit")
    print("═" * 40)

def main():
    logger.info("Todo Manager started")
    print("Welcome to Todo Manager!")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_tasks(list_tasks("all"))

        elif choice == "2":
            display_tasks(list_tasks("pending"))

        elif choice == "3":
            display_tasks(list_tasks("done"))

        elif choice == "4":
            title = input("Task title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue
            print("Priority: high / medium / low (default: medium)")
            priority = input("Priority: ").strip().lower() or "medium"
            if priority not in ("high", "medium", "low"):
                priority = "medium"
            task = add_task(title, priority)
            print(f"✅ Task added: [{task['id']}] {task['title']}")

        elif choice == "5":
            task_id = input("Enter task ID to complete: ").strip()
            if complete_task(task_id):
                print(f"✅ Task {task_id} marked as done.")

        elif choice == "6":
            task_id = input("Enter task ID to delete: ").strip()
            confirm = input(f"Delete task {task_id}? (yes/no): ").strip().lower()
            if confirm == "yes" and delete_task(task_id):
                print(f"🗑️  Task {task_id} deleted.")

        elif choice == "7":
            stats = get_stats()
            print(f"\n  Total tasks:   {stats['total']}")
            print(f"  Completed:     {stats['done']}")
            print(f"  Pending:       {stats['pending']}")
            print(f"  By priority:   {stats['by_priority']}")
            if stats["total"] > 0:
                pct = stats["done"] / stats["total"] * 100
                bar = "█" * int(pct // 5) + "░" * (20 - int(pct // 5))
                print(f"  Progress:      [{bar}] {pct:.1f}%")

        elif choice == "8":
            logger.info("Todo Manager exited")
            print("Goodbye! 👋")
            break

        else:
            print("Invalid option. Choose 1–8.")

if __name__ == "__main__":
    main()
```

---

## Quick Reference — Day 6 Cheat Sheet

```
FILE MODES:
  "r"  → read only          "w"  → write (overwrites)
  "a"  → append             "x"  → create new (fails if exists)
  "r+" → read + write       "rb" → binary read

FILE READING:
  .read()       → full file as string (small files only)
  .readline()   → one line
  .readlines()  → list of all lines
  for line in f → streaming (best for large files)

JSON:
  json.load(f)      → file → dict
  json.loads(s)     → string → dict
  json.dump(d, f)   → dict → file
  json.dumps(d)     → dict → string

CSV:
  csv.reader(f)          → rows as lists
  csv.DictReader(f)      → rows as dicts (use this)
  csv.DictWriter(f, fieldnames=[...])  → write dicts

IMPORTS:
  import module            → access via module.name
  from module import name  → direct access
  import module as alias   → shorter name

VIRTUAL ENV:
  python -m venv venv      → create
  source venv/bin/activate → activate (Mac/Linux)
  pip install package      → install
  pip freeze > req.txt     → save deps
  pip install -r req.txt   → restore deps

LOGGING LEVELS (low → high):
  DEBUG → INFO → WARNING → ERROR → CRITICAL
```

| Tool | Use Case |
|------|----------|
| `open()` with `with` | All file I/O |
| `pathlib.Path` | File paths, directory ops |
| `csv.DictReader/Writer` | CSV files |
| `json.load/dump` | JSON files and API data |
| `requests` | HTTP API calls |
| `logging` | Production-grade output (not print) |
| `venv` | Dependency isolation |
| `__init__.py` | Package definition |
| `if __name__ == "__main__":` | Importable + runnable module |

---
