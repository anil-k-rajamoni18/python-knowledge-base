# 🐍 Python Session Notes
### Topics: File Handling · Modules & Packages · Virtual Environments · Package Management · Logging · Mini Project

---

## 📁 1. File Handling with Python

File handling is the ability to create, read, update, and delete files using Python's built-in functions.

### 1.1 Opening Files — `open()`

```python
file = open("filename.txt", mode)
```

| Mode | Description |
|------|-------------|
| `'r'` | Read (default) — error if file doesn't exist |
| `'w'` | Write — creates or overwrites file |
| `'a'` | Append — adds to end of file |
| `'x'` | Create — error if file already exists |
| `'b'` | Binary mode (e.g., `'rb'`, `'wb'`) |
| `'+'` | Read + Write (e.g., `'r+'`) |

### 1.2 Reading Files

```python
# Method 1: read entire file as string
with open("notes.txt", "r") as f:
    content = f.read()

# Method 2: read line by line
with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())

# Method 3: readlines() → list of lines
with open("notes.txt", "r") as f:
    lines = f.readlines()
```

> ✅ Always use `with` statement — it automatically closes the file even if an exception occurs.

### 1.3 Writing Files

```python
# Write (overwrites existing content)
with open("output.txt", "w") as f:
    f.write("Hello, World!\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# Append (adds to existing content)
with open("output.txt", "a") as f:
    f.write("New line appended.\n")
```

### 1.4 Working with File Paths — `os` and `pathlib`

```python
import os

# Get current directory
print(os.getcwd())

# Join paths safely
path = os.path.join("folder", "subfolder", "file.txt")

# Check existence
os.path.exists(path)
os.path.isfile(path)
os.path.isdir(path)

# List directory
os.listdir(".")

# Create / remove directories
os.mkdir("new_folder")
os.makedirs("a/b/c", exist_ok=True)
os.remove("file.txt")
os.rmdir("empty_folder")
```

```python
from pathlib import Path

p = Path("folder/file.txt")
p.read_text()              # read content
p.write_text("Hello")     # write content
p.exists()                 # check existence
p.parent                   # parent directory
p.stem                     # filename without extension
p.suffix                   # extension (.txt)
list(Path(".").glob("*.py"))  # find all .py files
```

### 1.5 Working with CSV Files

```python
import csv

# Reading CSV
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])

# Writing CSV
data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
with open("output.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(data)
```

### 1.6 Working with JSON Files

```python
import json

# Reading JSON
with open("config.json", "r") as f:
    data = json.load(f)   # dict/list

# Writing JSON
with open("config.json", "w") as f:
    json.dump(data, f, indent=4)

# Convert to/from string
json_str = json.dumps(data)
data = json.loads(json_str)
```

### 1.7 Exception Handling in File Operations

```python
try:
    with open("missing.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found.")
except PermissionError:
    print("Permission denied.")
except IOError as e:
    print(f"IO Error: {e}")
```

---

## 📦 2. Modules and Packages

### 2.1 What is a Module?

A **module** is any `.py` file. It can contain functions, classes, and variables. Modules promote code reuse and organization.

```python
# math_utils.py
def add(a, b):
    return a + b

PI = 3.14159
```

```python
# main.py
import math_utils

print(math_utils.add(2, 3))
print(math_utils.PI)
```

### 2.2 Import Styles

```python
import math                        # import entire module
from math import sqrt, pi          # import specific names
from math import sqrt as sq        # alias
from math import *                 # import everything (⚠️ avoid in large projects)
```

### 2.3 The `__name__` Variable

```python
# script.py
def greet():
    print("Hello!")

if __name__ == "__main__":
    greet()   # only runs when script is executed directly
              # not when imported as a module
```

### 2.4 What is a Package?

A **package** is a directory containing an `__init__.py` file and multiple modules.

```
mypackage/
│── __init__.py
│── module_a.py
│── module_b.py
└── sub/
    ├── __init__.py
    └── helper.py
```

```python
# Importing from a package
from mypackage import module_a
from mypackage.sub.helper import some_function
```

### 2.5 `__init__.py`

Controls what gets exposed when the package is imported.

```python
# mypackage/__init__.py
from .module_a import add
from .module_b import subtract

__all__ = ["add", "subtract"]
```

### 2.6 Python Standard Library (Commonly Used)

| Module | Purpose |
|--------|---------|
| `os` | OS interactions, file paths |
| `sys` | System-level operations |
| `math` | Mathematical functions |
| `datetime` | Date and time handling |
| `random` | Random number generation |
| `json` | JSON encoding/decoding |
| `re` | Regular expressions |
| `collections` | Advanced data structures |
| `itertools` | Iteration tools |
| `functools` | Higher-order functions |
| `threading` | Multi-threading |
| `subprocess` | Run shell commands |

---

## 🌐 3. Virtual Environments

### 3.1 Why Virtual Environments?

- Different projects may need different versions of the same library.
- Without virtual envs, packages installed globally can conflict.
- Virtual environments isolate each project's dependencies.

### 3.2 Creating and Using Virtual Environments

```bash
# Create a virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Deactivate
deactivate
```

After activation, your terminal prompt changes to show `(venv)`.

### 3.3 What's Inside `venv/`?

```
venv/
├── bin/          # Python interpreter & scripts (Linux/Mac)
├── Scripts/      # Python interpreter & scripts (Windows)
├── lib/          # Installed packages
└── pyvenv.cfg    # Config file
```

### 3.4 `.gitignore` for Virtual Envs

Always add `venv/` to `.gitignore`:
```
venv/
__pycache__/
*.pyc
.env
```

### 3.5 Alternative: `virtualenv`

```bash
pip install virtualenv
virtualenv myenv
source myenv/bin/activate
```

---

## 🛠️ 4. Package Management & Tools

### 4.1 `pip` — The Standard Package Manager

```bash
pip install requests              # install latest
pip install requests==2.28.0      # install specific version
pip install "requests>=2.25"      # version range
pip install -U requests           # upgrade
pip uninstall requests            # uninstall
pip list                          # list installed packages
pip show requests                 # info about a package
pip freeze                        # list installed with versions
```

### 4.2 `requirements.txt`

Used to share a project's dependencies.

```bash
# Generate
pip freeze > requirements.txt

# Install from file
pip install -r requirements.txt
```

Example `requirements.txt`:
```
requests==2.31.0
Flask==3.0.0
python-dotenv==1.0.0
```

### 4.3 `pyproject.toml` — Modern Standard

The modern replacement for `setup.py` and `requirements.txt`.

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "my-project"
version = "1.0.0"
dependencies = [
    "requests>=2.28",
    "Flask>=3.0",
]
```

### 4.4 `pipenv` — Pipfile-based Management

```bash
pip install pipenv
pipenv install requests       # adds to Pipfile
pipenv install --dev pytest   # dev dependency
pipenv shell                  # activate virtual env
pipenv run python app.py      # run without activating
pipenv lock                   # generate Pipfile.lock
```

### 4.5 `poetry` — Modern Dependency Management

```bash
pip install poetry
poetry new my-project         # create new project
poetry add requests           # add dependency
poetry add --group dev pytest # dev dependency
poetry install                # install all deps
poetry run python app.py      # run script
poetry build                  # build package
poetry publish                # publish to PyPI
```

### 4.6 `uv` — Ultra-Fast Package Manager (Modern)

```bash
pip install uv
uv venv                       # create virtual env
uv pip install requests       # install packages (10-100x faster)
uv pip freeze > requirements.txt
```

### 4.7 Comparison

| Tool | Config File | Speed | Use Case |
|------|------------|-------|----------|
| `pip` | `requirements.txt` | Normal | Simple projects |
| `pipenv` | `Pipfile` | Normal | App development |
| `poetry` | `pyproject.toml` | Normal | Libraries & Apps |
| `uv` | `pyproject.toml` | ⚡ Very fast | Modern projects |

---

## 📋 5. Logging with Python

### 5.1 Why Logging?

- `print()` is for development; logging is for production.
- Allows controlling output levels (DEBUG, INFO, WARNING, etc.).
- Can write to files, streams, external systems simultaneously.
- Can be turned on/off without changing code.

### 5.2 Logging Levels

| Level | Value | Use Case |
|-------|-------|----------|
| `DEBUG` | 10 | Detailed diagnostic info |
| `INFO` | 20 | Confirmation things are working |
| `WARNING` | 30 | Something unexpected (default level) |
| `ERROR` | 40 | Serious problem, function failed |
| `CRITICAL` | 50 | Severe error, program may crash |

### 5.3 Basic Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")
```

### 5.4 Logging to a File

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()   # also print to console
    ]
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

### 5.5 Custom Logger (Best Practice)

```python
import logging

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler("app.log")
        fh.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

# Usage
logger = get_logger(__name__)
logger.info("Server starting...")
logger.error("Database connection failed!")
```

### 5.6 Logging Exceptions

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Division error occurred")
    # logger.exception() automatically includes traceback
```

### 5.7 Logging with `logging.config`

```python
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "standard",
            "level": "WARNING"
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
```

### 5.8 Log Rotation

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=3               # keep last 3 files
)
```

---

## 🚀 6. Mini Project: CSV Data Processing Tool with Logging

A command-line tool that reads a CSV file, filters/processes data, writes output, and logs all operations.

### Project Structure

```
csv_processor/
├── venv/
├── data/
│   └── students.csv
├── output/
├── logs/
├── processor/
│   ├── __init__.py
│   ├── reader.py
│   ├── filter.py
│   └── writer.py
├── logger_config.py
├── main.py
└── requirements.txt
```

### `logger_config.py`

```python
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(fmt)

        fh = RotatingFileHandler("logs/app.log", maxBytes=2_000_000, backupCount=3)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger
```

### `processor/reader.py`

```python
import csv
from logger_config import setup_logger

logger = setup_logger(__name__)

def read_csv(filepath: str) -> list[dict]:
    logger.info(f"Reading file: {filepath}")
    try:
        with open(filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            data = list(reader)
        logger.info(f"Successfully read {len(data)} records.")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error reading file: {e}")
        raise
```

### `processor/filter.py`

```python
from logger_config import setup_logger

logger = setup_logger(__name__)

def filter_by_score(data: list[dict], min_score: float) -> list[dict]:
    logger.info(f"Filtering records with score >= {min_score}")
    filtered = [
        row for row in data
        if float(row.get("score", 0)) >= min_score
    ]
    logger.info(f"{len(filtered)} records passed the filter (from {len(data)}).")
    return filtered
```

### `processor/writer.py`

```python
import csv
import os
from logger_config import setup_logger

logger = setup_logger(__name__)

def write_csv(data: list[dict], filepath: str) -> None:
    if not data:
        logger.warning("No data to write.")
        return

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    try:
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        logger.info(f"Written {len(data)} records to {filepath}")
    except Exception as e:
        logger.exception(f"Error writing file: {e}")
        raise
```

### `main.py`

```python
from processor.reader import read_csv
from processor.filter import filter_by_score
from processor.writer import write_csv
from logger_config import setup_logger
import json

logger = setup_logger("main")

def main():
    logger.info("=== CSV Processor Started ===")
    
    input_file = "data/students.csv"
    output_file = "output/filtered_students.csv"
    min_score = 70.0

    try:
        # Step 1: Read
        data = read_csv(input_file)

        # Step 2: Filter
        filtered = filter_by_score(data, min_score)

        # Step 3: Write
        write_csv(filtered, output_file)

        # Step 4: Summary
        summary = {
            "total_records": len(data),
            "passed": len(filtered),
            "failed": len(data) - len(filtered)
        }
        logger.info(f"Summary: {json.dumps(summary)}")
        print("\n✅ Processing complete!")
        print(f"   Total: {summary['total_records']} | Passed: {summary['passed']} | Failed: {summary['failed']}")

    except Exception as e:
        logger.critical(f"Processing failed: {e}")

if __name__ == "__main__":
    main()
```

### Sample `data/students.csv`

```csv
name,age,score,grade
Alice,20,85.5,A
Bob,22,62.0,C
Charlie,21,91.0,A+
Diana,23,45.5,F
Eve,20,78.0,B
Frank,22,55.0,D
Grace,21,88.0,A
```

### Setup and Run

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Install dependencies (none needed here — all stdlib!)
pip freeze > requirements.txt

# 3. Run
python main.py
```

### Expected Output

```
2024-01-15 10:30:00 | INFO     | main | === CSV Processor Started ===
2024-01-15 10:30:00 | INFO     | processor.reader | Reading file: data/students.csv
2024-01-15 10:30:00 | INFO     | processor.reader | Successfully read 7 records.
2024-01-15 10:30:00 | INFO     | processor.filter | Filtering records with score >= 70.0
2024-01-15 10:30:00 | INFO     | processor.filter | 4 records passed the filter (from 7).
2024-01-15 10:30:00 | INFO     | processor.writer | Written 4 records to output/filtered_students.csv
2024-01-15 10:30:00 | INFO     | main | Summary: {"total_records": 7, "passed": 4, "failed": 3}

✅ Processing complete!
   Total: 7 | Passed: 4 | Failed: 3
```

---

## 📝 Key Takeaways

| Topic | Key Point |
|-------|-----------|
| File Handling | Always use `with` statement; prefer `pathlib` for paths |
| Modules | Use `__name__ == "__main__"` guard for scripts |
| Packages | `__init__.py` controls public API of your package |
| Virtual Envs | One venv per project; always add `venv/` to `.gitignore` |
| Package Mgmt | Use `requirements.txt` for simple, `poetry`/`uv` for modern projects |
| Logging | Never use `print()` in production; use named loggers per module |

---