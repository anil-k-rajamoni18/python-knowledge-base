# 🎯 Python Full Stack — Day 4 Interview Preparation
# Topic: Modules, Packages & Virtual Environments

> **How to use this file:** Attempt each answer before reading. For senior roles, study the "Depth" sections and be ready to discuss real project scenarios. Questions are ordered by difficulty.

---

## 🟢 Beginner Level Questions

---

### Q1. What is the difference between a module and a package in Python?

**Answer:**
- **Module** — a single `.py` file containing Python code (functions, classes, variables)
- **Package** — a directory containing an `__init__.py` file and one or more modules

```
# Module — single file
math_utils.py         → import math_utils

# Package — directory with __init__.py
student_manager/
├── __init__.py       → import student_manager
├── models.py         → from student_manager import models
└── utils.py          → from student_manager.utils import helper
```

**Key distinction:** A package is a module that can contain other modules. The `__init__.py` is what makes a directory a package — without it, Python treats the directory as just a folder, not a package.

---

### Q2. What are the different ways to import in Python? When would you use each?

**Answer:**

```python
# 1. Import the whole module — most explicit, safest
import math
print(math.sqrt(16))        # access via module name

# 2. Import specific names — convenient for frequently used items
from math import sqrt, pi
print(sqrt(16))             # direct access

# 3. Import with alias — for long names or convention (numpy → np)
import numpy as np
import pandas as pd

# 4. Import with alias for a name
from datetime import datetime as dt

# 5. Wildcard — avoid in production (pollutes namespace)
from math import *

# 6. Relative import — inside packages only
from . import models            # sibling module
from .models import Student     # name from sibling
from .. import config           # parent package
```

**When to use which:**
- `import module` — default choice; clear origin of all names
- `from module import name` — when you use a name many times
- `import module as alias` — convention for heavy libraries (`np`, `pd`, `plt`)
- Relative imports — always inside a package; never in scripts

---

### Q3. What is `__name__ == "__main__"` and why is it important?

**Answer:**
Every Python module has a `__name__` attribute:
- When run **directly** as a script: `__name__` is `"__main__"`
- When **imported** by another module: `__name__` is the module's own name

```python
# student_utils.py
def calculate_average(scores):
    return sum(scores) / len(scores)

# This block ONLY runs when the file is executed directly
# It does NOT run when you do: import student_utils
if __name__ == "__main__":
    test_scores = [80, 90, 85]
    print(calculate_average(test_scores))   # 85.0
```

**Why it matters:**
- Lets you write files that are both **importable libraries** and **runnable scripts**
- Prevents test/demo code from running when another module imports your file
- Required pattern for Django's `manage.py`, Flask's `app.run()`, and all CLI tools

---

### Q4. What is a virtual environment and why do you need one?

**Answer:**
A virtual environment is an **isolated Python installation** with its own `site-packages` directory, its own `pip`, and (optionally) its own Python version.

**Why isolation matters:**
```
Without venv:                    With venv:
─────────────────────────────   ─────────────────────────────
Global Python                   projectA/venv/  → Django 3.2
├── Django 4.2                  projectB/venv/  → Django 4.2
├── requests 2.28               projectC/venv/  → Flask 2.3
└── ALL projects share this
    ← version conflicts!        ← each project isolated ✅
```

```bash
# Create
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Verify isolation
pip list    # only pip + setuptools (clean)

# Install
pip install django==4.2

# Freeze
pip freeze > requirements.txt

# Deactivate
deactivate
```

---

### Q5. What does `pip freeze > requirements.txt` do, and how do you use it?

**Answer:**
`pip freeze` outputs all currently installed packages with their **exact versions** in a format `pip install -r` can read.

```bash
# Capture current environment's dependencies
pip freeze > requirements.txt

# requirements.txt content:
Django==4.2.7
requests==2.31.0
psycopg2-binary==2.9.9

# Reproduce the exact same environment (teammate, CI/CD, deployment):
pip install -r requirements.txt
```

**Why exact versions matter in production:**
- Prevents "works on my machine" problems
- Ensures consistent behavior across dev, staging, and production
- Protects against breaking changes in minor/patch releases

**Best practice — separate dev and prod:**
```bash
pip install -r requirements.txt           # production dependencies only
pip install -r requirements-dev.txt       # adds pytest, black, mypy, etc.
```

---

### Q6. What is the purpose of `__init__.py`?

**Answer:**
`__init__.py` transforms a directory into a Python package and runs when the package is imported. It controls:

1. **Package initialization** — setup code that runs on import
2. **Public API definition** — what's exposed at the package level
3. **Re-exports** — convenience imports so users don't need deep paths

```python
# student_manager/__init__.py

__version__ = "1.0.0"

# Without this, users must write:
# from student_manager.operations import StudentManager
# With this, they can write:
# from student_manager import StudentManager
from .operations import StudentManager
from .models import Student

__all__ = ["StudentManager", "Student"]
```

**Note:** In Python 3.3+, a directory without `__init__.py` is a valid "namespace package" — but for regular packages with initialization, `__init__.py` is still required.

---

## 🟡 Intermediate Level Questions

---

### Q7. How does Python resolve the search path for modules? What is `sys.path`?

**Answer:**
When you `import something`, Python checks in this exact order:

1. **`sys.modules`** — if already imported, return the cached module immediately
2. **Built-in modules** — `sys`, `builtins`, etc. (compiled into CPython)
3. **`sys.path` directories** — scans each directory left to right for a matching file/package

```python
import sys

# See the search path
for path in sys.path:
    print(path)
# [0] = directory of the running script (or '' for interactive)
# [1] = PYTHONPATH env var entries
# [2+] = installation defaults (site-packages)

# This is why your script's directory is always found first
# — and why naming a file 'math.py' shadows the stdlib's math!
```

**Manipulation (rarely needed):**
```python
sys.path.insert(0, "/custom/path")     # add at front (highest priority)
sys.path.append("/another/path")       # add at back (lowest priority)
```

**Real-world implication:** The first entry in `sys.path` is your script's directory. This means local files shadow standard library modules if they share a name — a common gotcha.

---

### Q8. What is a circular import? How do you detect and fix it?

**Answer:**
A circular import occurs when Module A imports Module B, which imports Module A — creating a dependency cycle. Python partially initializes modules, so circular references catch one of them before it's fully defined.

```python
# ❌ Circular import example
# models.py
from operations import StudentManager   # triggers loading operations.py

# operations.py
from models import Student              # models.py isn't fully loaded yet!
# → ImportError: cannot import name 'Student' from partially initialized module 'models'
```

**Three fixes:**

```python
# ── Fix 1: Extract shared code to a third module (best long-term) ─────────
# utils.py — imported by both, imports neither
def validate_name(name): ...

# models.py — imports from utils only
from .utils import validate_name

# operations.py — imports from models and utils, not vice versa
from .models import Student
from .utils import validate_name

# ── Fix 2: Lazy import inside the function ────────────────────────────────
# models.py
def get_manager():
    from .operations import StudentManager  # deferred — no circular issue
    return StudentManager()

# ── Fix 3: Import the module, not the name ────────────────────────────────
# operations.py
import models                    # doesn't trigger full parse of models
student = models.Student(...)    # access attribute later
```

**How to detect:** Python's error message tells you exactly: `ImportError: cannot import name 'X' from partially initialized module 'Y' (most likely due to a circular import)`

---

### Q9. What is the difference between absolute and relative imports?

**Answer:**

**Absolute import** — uses the full dotted path from the top of the package tree. Works everywhere.

**Relative import** — uses `.` notation relative to the current module's position. Only works inside packages.

```python
# Package structure:
# student_manager/
# ├── __init__.py
# ├── models.py
# ├── operations.py
# └── utils/
#     ├── __init__.py
#     └── validators.py

# Inside operations.py:

# Absolute import — explicit, works if package is installed
from student_manager.models import Student
from student_manager.utils.validators import validate_name

# Relative import — concise, works when package moves/renames
from .models import Student             # sibling
from .utils.validators import validate_name    # sub-package
from ..config import DATABASE_URL       # parent package (if nested)
```

**When to use which:**
- **Absolute** — in scripts, top-level code, and when running as `__main__`
- **Relative** — inside packages, for intra-package imports
- **Never mix** — pick one style per project (most Django projects use absolute)

---

### Q10. What is `__all__` and how does it affect imports?

**Answer:**
`__all__` is a list variable in a module that explicitly declares its **public API** — the names exported by `from module import *`.

```python
# mymodule.py
__all__ = ["public_func", "PublicClass"]

def public_func():
    """Documented, intended for external use."""
    return "I'm public"

class PublicClass:
    pass

def _private_helper():
    """Prefixed with _, NOT in __all__ — internal use only."""
    pass

def also_private():
    """Not in __all__ — excluded from wildcard import."""
    pass
```

```python
# user code
from mymodule import *
# Only 'public_func' and 'PublicClass' are imported
# '_private_helper' and 'also_private' are NOT imported

# But explicit import still works regardless of __all__:
from mymodule import also_private   # this works!
```

**Two purposes of `__all__`:**
1. Controls wildcard import behavior
2. Serves as self-documenting API declaration — tells readers "these are the names I guarantee to maintain"

---

### Q11. What is `pip install -e .` and when would you use it?

**Answer:**
`pip install -e .` installs your package in **editable mode** (also called "development mode"). Instead of copying your code to `site-packages`, it creates a link — changes to your source files are immediately reflected without reinstalling.

```bash
# Regular install — copies to site-packages
pip install .
# Changing models.py requires pip install . again!

# Editable install — creates a link
pip install -e .
# Changing models.py is immediately reflected — no reinstall needed

# It creates a .egg-link file in site-packages pointing to your source
```

**When to use:**
- During active development of a package
- When running tests against your own package
- When multiple projects share a common internal library you're actively changing

**Requires** either `setup.py`, `setup.cfg`, or `pyproject.toml` with packaging metadata.

---

### Q12. What is the `src` layout pattern? Why is it recommended?

**Answer:**
The `src` layout places your package inside a `src/` subdirectory instead of the project root:

```
# Without src layout (common mistake)
myproject/
├── student_manager/      ← package lives at root
│   ├── __init__.py
│   └── models.py
├── tests/
└── setup.py

# With src layout (recommended)
myproject/
├── src/
│   └── student_manager/  ← package inside src/
│       ├── __init__.py
│       └── models.py
├── tests/
└── pyproject.toml
```

**Why `src` layout prevents a subtle bug:**

Without `src/`, when you run `python` from the project root, `student_manager/` is on `sys.path` because the current directory is on `sys.path[0]`. Your tests might import the local, un-installed version without realizing it — hiding packaging problems.

With `src/`, the package is NOT on `sys.path` unless explicitly installed (`pip install -e .`). Tests always run against the installed version, catching packaging mistakes early.

---

## 🔴 Advanced / Senior Level Questions

---

### Q13. How does Python's import caching (`sys.modules`) work, and when can it cause problems?

**Answer:**
`sys.modules` is a dictionary mapping module names to loaded module objects. It's checked first on every import — making repeated `import math` effectively free after the first call.

```python
import sys
import math

# First import — loads from disk
print("math" in sys.modules)   # True (after first import)

# Second import — returns cached version instantly
import math   # O(1) dict lookup — no disk access

# Inspecting the cache
print(type(sys.modules["math"]))    # <class 'module'>
print(sys.modules["math"].pi)       # 3.141592653589793

# Force reimport (rare — usually a bug signal)
import importlib
importlib.reload(math)
```

**When `sys.modules` causes problems:**

```python
# Problem 1: Stale module during testing
# If a module is imported, you modify it, and reimport — you get the old cached version!
# Solution: use importlib.reload() or restart the interpreter

# Problem 2: Mock patching order matters
# In tests, if a module is already in sys.modules when you patch it,
# the patch may not propagate to already-imported references

# Problem 3: Circular imports partially populate sys.modules
# Module A starts loading, is added to sys.modules partially,
# Module B imports A and gets the partial version
```

---

### Q14. Explain `pyproject.toml` and how it differs from `setup.py`.

**Answer:**
`setup.py` is the traditional packaging approach (Python 2 era). `pyproject.toml` is the modern standard introduced by PEP 517/518 — it's declarative, tool-agnostic, and supported by all modern build backends.

```python
# Old way — setup.py (imperative Python code)
from setuptools import setup, find_packages

setup(
    name="student-manager",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "dev": ["pytest", "black", "mypy"]
    },
    entry_points={
        "console_scripts": [
            "student-manager=student_manager.cli:main"
        ]
    }
)
```

```toml
# New way — pyproject.toml (declarative TOML)
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "student-manager"
version = "0.1.0"
description = "Student record management"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=7.0", "black>=23.0", "mypy>=1.0"]

[project.scripts]
student-manager = "student_manager.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

**Advantages of `pyproject.toml`:**
- Declarative — no arbitrary Python code during build
- Works with multiple backends (setuptools, poetry, flit, hatch)
- Consolidates all tool config (mypy, black, pytest) in one file
- Required by modern pip and all CI systems

---

### Q15. How would you handle different settings for development vs production using packages?

**Answer:**
The standard pattern (used by Django) is a settings package with a base module and environment-specific overrides:

```python
# myproject/settings/__init__.py
# Empty — just makes it a package

# myproject/settings/base.py — shared settings
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    "django.contrib.admin",
    "myapp.students",
]

# myproject/settings/development.py
from .base import *                     # inherit all base settings

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# myproject/settings/production.py
from .base import *
import os

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]   # must be set in environment
ALLOWED_HOSTS = [os.environ.get("DOMAIN", "")]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "localhost"),
    }
}
```

```bash
# Select settings module via environment variable
export DJANGO_SETTINGS_MODULE=myproject.settings.development
python manage.py runserver

# Production
export DJANGO_SETTINGS_MODULE=myproject.settings.production
gunicorn myproject.wsgi
```

**The `.env` file pattern:**
```bash
# .env (not in git — in .gitignore)
SECRET_KEY=super-secret-key-here
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=mypassword

# config.py — loads .env into os.environ
from dotenv import load_dotenv
load_dotenv()   # reads .env file into environment
```

---

### Q16. How does `argparse` compare to `sys.argv` for CLI argument parsing?

**Answer:**
`sys.argv` is the raw list of command-line arguments. `argparse` provides a high-level framework for defining, parsing, and validating arguments with automatic `--help` generation.

```python
# ── sys.argv — raw, manual parsing ────────────────────────────────────────
import sys

# Running: python script.py Alice 25
args = sys.argv         # ['script.py', 'Alice', '25']
name = sys.argv[1]      # 'Alice'
age = int(sys.argv[2])  # 25 (must manually convert!)

# No validation, no --help, no error messages — everything manual

# ── argparse — structured, automatic ──────────────────────────────────────
import argparse

parser = argparse.ArgumentParser(description="Add a student")
parser.add_argument("--name", required=True, help="Student's name")
parser.add_argument("--age", type=int, required=True, help="Student's age")
parser.add_argument("--grade", default="N/A", choices=["A","B","C","D","F"])
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()
# Running: python script.py --name Alice --age 20 --grade A
# args.name = "Alice", args.age = 20, args.grade = "A", args.verbose = False

# Auto-generated --help:
# usage: script.py [-h] --name NAME --age AGE [--grade {A,B,C,D,F}] [--verbose]
```

**When to use `sys.argv`:** Never in production — only for understanding what `argparse` processes under the hood.

---

## 📝 Quick-Fire Answers

| Question | Answer |
|----------|--------|
| What does `python -m venv venv` create? | A virtual environment directory named `venv` |
| Where does `pip install` put packages? | Into the active environment's `site-packages` directory |
| What is `__pycache__`? | Directory containing compiled `.pyc` bytecode files — safe to delete |
| What's the first entry in `sys.path`? | The directory of the running script (or `''` for interactive mode) |
| How do you add a new entry point CLI command? | Add to `[project.scripts]` in `pyproject.toml` |
| Can you use relative imports in a script run with `python file.py`? | No — only inside installed packages |
| What does `importlib.reload(module)` do? | Re-executes the module code and updates the module object in `sys.modules` |
| What makes a directory a namespace package (no `__init__.py`)? | Python 3.3+ PEP 420 — allows packages without `__init__.py`, but no initialization code |
| What command installs a package in editable mode? | `pip install -e .` |
| Where should secrets like `SECRET_KEY` live? | Environment variables loaded from `.env` — never hardcoded or in git |
| What is the standard name for a virtual environment directory? | `venv` or `.venv` |
| What does `pip install -r requirements.txt` do? | Installs all packages listed in the requirements file |

---

## 🧠 Behavioral / Scenario Questions

### "How would you set up a new Python project from scratch?"

**Model answer structure:**
```
1. Create project directory and git init
2. Create virtual environment: python -m venv venv
3. Activate and confirm: source venv/bin/activate
4. Create pyproject.toml with project metadata
5. Create src/mypackage/__init__.py structure
6. Install development dependencies: pip install pytest black mypy
7. Create .gitignore (include venv/, .env, __pycache__)
8. Create requirements.txt and requirements-dev.txt
9. Write code with type hints
10. Run: pip install -e . for editable mode
```

### "You've cloned a colleague's Python project. What's the first thing you do?"

**Model answer:** "Read the README for Python version requirements. Create a virtual environment with that Python version (`python3.11 -m venv venv`). Activate it. Then `pip install -r requirements.txt` (and `requirements-dev.txt` if I'll be running tests). Check that `pip install -e .` works if it's a package. Finally, try to run the tests to confirm the environment is set up correctly."

### "A teammate reports an ImportError on their machine but not yours. How do you debug it?"

**Model answer:** "First check if they've activated their virtual environment — most common cause. Compare `pip list` outputs between machines. Check if the package name matches what's in `requirements.txt`. Look at `sys.path` on both machines. If the package is a local one, ensure `pip install -e .` has been run. Check Python version compatibility. If it's a circular import error, look at the traceback — Python will show the partially-initialized module."

---

*End of Day 4 Interview Prep — Day 5 will add: File I/O, Error Handling, Context Managers*
