# DAY 6 — Files, Modules, Virtual Environments



---

## 🧩 1. Working With Files in Python (Text, Binary, CSV, JSON)

Files are central to most software systems. Applications read logs, store user data, write reports, sync with APIs, and much more.

Python provides a unified way to work with files using the built-in `open()` function.

### 🔸 1.1 File Opening Modes

| Mode | Meaning | Used For |
|------|---------|----------|
| `"r"` | Read only (default) | Reading config files, templates |
| `"w"` | Write (overwrite) | Creating new logs/reports |
| `"a"` | Append | Adding new data to existing files |
| `"x"` | Exclusive create | Creating config file if not exist |
| `"rb"`/`"wb"` | Binary read/write | Images, PDFs, Excel |
| `"r+"` | Read + Write | Updating values inside a file |

### 🔸 1.2 Safe File Handling: with open()

Industry standard — ensures file automatically closes.

```python
with open("data.txt", "r") as file:
    content = file.read()
```

**Why "with" is used:**
- ✔ Auto closes file
- ✔ Prevents resource leaks
- ✔ Safe even with exceptions
- ✔ Best practice in all production systems

### 🔸 1.3 File Reading Methods

| Method | Explanation |
|--------|-------------|
| `.read()` | Reads entire file as string |
| `.readline()` | Reads one line |
| `.readlines()` | Returns list of all lines |
| Looping | Best for large files |

**Example:** Processing 100MB server logs efficiently:

```python
with open("server.log") as file:
    for line in file:
        if "ERROR" in line:
            print(line)
```

### 🔸 1.4 File Writing

```python
with open("output.txt", "w") as f:
    f.write("Hello World\n")
    f.write("Writing multiple lines")
```

⚠️ **Common Pitfall:** Using `"w"` will erase entire file — use `"a"` to append.

---

## 🧩 2. Working with CSV Files (Industry-Relevant)

**CSV is used in:**
- HR employee lists
- Sales reports
- Data engineering pipelines
- Export/import from Excel
- ETL jobs

Python's `csv` module handles all edge cases.

### 🔸 2.1 Reading CSV

```python
import csv

with open("employees.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["email"])
```

- ✔ `DictReader` converts each row → Python dictionary
- ✔ Avoids index confusion
- ✔ Industry standard approach

### 🔸 2.2 Writing CSV

```python
import csv

data = [
    {"name": "Amit", "age": 28},
    {"name": "Sara", "age": 31}
]

with open("output.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(data)
```

---

## 🧩 3. JSON — The Most Important Format in APIs

**JSON is used everywhere:**
- REST APIs
- Databases like MongoDB
- Storing configs
- Python-to-JavaScript communication

### 🔸 3.1 Reading JSON

```python
import json

with open("config.json") as f:
    config = json.load(f)
print(config)
```

### 🔸 3.2 Writing JSON

```python
import json

data = {"name": "Rahul", "skills": ["Python", "AWS"]}

with open("user.json", "w") as f:
    json.dump(data, f, indent=4)
```

- ✔ `indent=4` → readable
- ✔ Standard for API payloads

---

## 🧩 4. Sending HTTP Requests Using Python (requests Library)

**Used for:**
- Consuming APIs
- Automation scripts
- Microservices communication
- Data fetching
- Health monitoring tools

### 🔸 4.1 GET Request

```python
import requests

response = requests.get("https://api.github.com/users/octocat")
data = response.json()
print(data["login"])
```

### 🔸 4.2 POST Request

```python
payload = {"name": "John", "job": "Developer"}
response = requests.post("https://httpbin.org/post", json=payload)
print(response.json())
```

---

## 🧩 5. Modules & Packages

**Why we use them?**
- ✔ Keep code organized
- ✔ Break big systems into smaller reusable components
- ✔ Improve testing
- ✔ Avoid duplication
- ✔ Enable team collaboration

### 🔸 5.1 Creating a Module

**File:** `math_utils.py`

```python
def add(a, b):
    return a + b
```

**Use it:**

```python
import math_utils
print(math_utils.add(3, 5))
```

### 🔸 5.2 Creating a Package

**Folder structure:**

```
mypackage/
    __init__.py
    utils.py
    helpers.py
```

**Import:**

```python
from mypackage.utils import greet
```

### 🔸 5.3 Why __init__.py is important?

- Marks folder as a Python package
- Helps Python locate modules
- Can export selected functions

---

## 🧩 6. Virtual Environments (venv)

Virtual environments isolate dependencies.

**Why necessary?**

Imagine:
- Project A needs Django 3.2
- Project B needs Django 4.0

Without venv, both would clash → system breaks.

### 🔸 6.1 Creating a venv

```bash
python -m venv venv
```

### 🔸 6.2 Activating

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 🔸 6.3 Installing Packages

```bash
pip install requests
pip install flask
```

### 🔸 6.4 Saving Dependencies

```bash
pip freeze > requirements.txt
```

### 🔸 6.5 Installing from requirements

```bash
pip install -r requirements.txt
```

This is how teams share consistent environments.

---

## 🧩 7. Logging in Python (Industry Essential)

Logging is more important than print statements.

**Used in:**
- Microservices
- APIs
- Background jobs
- Monitoring failures
- Debugging production issues

### 🔸 7.1 Basic Logging Setup

```python
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("App started")
logging.error("Something went wrong")
```

### 🔸 7.2 Logging Levels

| Level | Meaning |
|-------|---------|
| DEBUG | Developer-level info |
| INFO | General events |
| WARNING | Something unusual |
| ERROR | Error happened but app continues |
| CRITICAL | System crash likely |

### 🔸 7.3 Real Example: Logging Login Attempts

```python
def login(username):
    logging.info(f"Login attempt by {username}")
    if username != "admin":
        logging.warning("Invalid login")
```

---

## 🧩 Mini Project (In-Depth)

### ✅ File-Based Todo Manager (JSON + Logs)

**Features:**
- Add task
- Delete task
- Mark complete
- Save everything in `todo.json`
- Log each action

**Architecture:**

```
todo_app/
│
├── todo.json
├── app.log
├── todo_manager.py
└── utils.py
```

**Sample Code: Saving Tasks**

```python
import json

def save_tasks(tasks):
    with open("todo.json", "w") as f:
        json.dump(tasks, f, indent=4)
```

**Logging integration:**

```python
import logging

logging.basicConfig(filename="app.log", level=logging.INFO)

def add_task(task):
    logging.info(f"Task added: {task}")
```

This project simulates how real backend systems store data on disk before moving to full database solutions.