# 🐍 Python Full Stack — Day 4
---

## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, learners will be able to:
- Explain how Python's import system works and how `sys.path` controls module discovery
- Use all import styles correctly — `import`, `from...import`, relative, absolute — and know when to choose each
- Create and activate virtual environments and manage dependencies with `pip`
- Structure a Python project as a proper installable package with `setup.py` / `pyproject.toml`
- Avoid circular imports, namespace collisions, and environment pollution — the three most common project-level bugs

### 📋 Prerequisites (Days 1–3 Review)
- Python data types, variables, mutability (Day 1)
- Functions, scope, LEGB rule, closures (Day 2)
- Data structures — lists, dicts, sets, tuples (Day 3)
- Basic file system navigation (terminal: `cd`, `ls`/`dir`, `mkdir`)

### 🔗 Connection to the Full Stack Journey
- **Every Django project (Day 20+)** is a Python package — `settings.py`, `urls.py`, `views.py` are all modules inside a package
- **Virtual environments are non-negotiable** in professional Django/Flask development — every project gets its own env
- **`requirements.txt`** is how teams share dependency information — it's the first file a new developer installs from
- **`__init__.py`** controls what Django apps expose — understanding it prevents 80% of "ImportError" bugs
- **`pyproject.toml`** (Day 30+) is how you package and deploy Python applications

---

## 2. Concept Explanation

### 2.1 The Import System Deep Dive

**The "Why":** Python's import system is the mechanism that makes code reuse possible. Understanding it prevents the most frustrating class of bugs — `ModuleNotFoundError`, `ImportError`, and circular imports.

**What happens when you write `import math`?**

Python follows a precise lookup sequence:
1. **`sys.modules` cache** — checks if already imported (returns cached version instantly)
2. **Built-in modules** — checks C-extension built-ins (`sys`, `builtins`)
3. **`sys.path` directories** — searches each directory in order for a matching `.py` file or package folder

**Analogy:** Think of `sys.path` as Python's **library card catalog**. When you request a book (`import math`), the librarian first checks the "already borrowed" desk (`sys.modules`), then looks in the reference section (built-ins), then scans each shelf in the catalog order (`sys.path`).

```
import math  →  check sys.modules → check builtins → scan sys.path[0], [1], [2]...
```

**`sys.path` default contents (in order):**
1. The directory of the script being run (or `""` for interactive mode)
2. `PYTHONPATH` environment variable directories
3. Installation-dependent default (site-packages)

---

### 2.2 Import Styles

Python gives you several ways to import — each with a different trade-off between explicitness, namespace pollution, and readability.

| Style | Syntax | Brings into namespace |
|-------|--------|-----------------------|
| Module import | `import math` | `math` (access via `math.sqrt`) |
| Selective import | `from math import sqrt` | `sqrt` directly |
| Aliased import | `import numpy as np` | `np` |
| Wildcard import | `from math import *` | Everything in `__all__` |
| Relative import | `from . import utils` | `utils` (within package) |

**`__all__`** — a list variable in a module that explicitly defines what `from module import *` exports. It's also a signal to other developers about the module's public API.

---

### 2.3 Package Structure and `__init__.py`

**The "Why":** A **module** is a single `.py` file. A **package** is a directory containing an `__init__.py` file. The `__init__.py` file runs when the package is imported — it's the package's "constructor."

**What `__init__.py` can do:**
- Run initialization code
- Control the public API via `__all__`
- Re-export names for a cleaner import experience
- Set package-level metadata (`__version__`, `__author__`)

**Analogy:** If a package is a **department store**, `__init__.py` is the **welcome desk** — it decides what shoppers see when they walk in (public API), and it sets up the store before customers arrive (initialization).

---

### 2.4 Circular Imports

**The "Why":** Circular imports occur when Module A imports Module B, which imports Module A. Python partially initializes modules, so the circular reference catches one of them mid-initialization — leading to `ImportError` or `AttributeError`.

**Example:**
```
models.py imports from utils.py
utils.py imports from models.py  ← circular!
```

**Three ways to resolve:**
1. **Restructure** — move shared code to a third module neither imports from the other
2. **Import inside function** — defer the import until the function is called (lazy import)
3. **Import the module, not the name** — `import models` instead of `from models import MyClass`

---

### 2.5 `__name__ == "__main__"` Pattern

**The "Why":** Every Python file can be run two ways:
- **As a script:** `python myfile.py` → `__name__` is set to `"__main__"`
- **As a module:** `import myfile` → `__name__` is set to `"myfile"`

The `if __name__ == "__main__":` guard ensures that your script's entry-point code only runs when the file is executed directly — not when it's imported as a module.

**This is critical** for:
- Writing files that are both importable libraries AND runnable scripts
- Preventing test code from running when you import a module
- Organizing Django management commands and Flask dev servers

---

### 2.6 Virtual Environments

**The "Why":** Without virtual environments, every Python project on your machine shares the same global `site-packages`. This leads to **dependency hell** — Project A needs Django 3.2, Project B needs Django 4.2, and they can't coexist globally.

**Virtual environment = an isolated Python installation** with its own `site-packages` directory, its own `pip`, and its own copy of Python.

**Analogy:** A virtual environment is like a **shipping container** for your project — everything it needs is packed inside, isolated from other containers, and consistent wherever it's deployed.

**Workflow:**
```
Create → Activate → Install → Work → Freeze → Deactivate
```

---

### 2.7 Package Distribution

**The "Why":** A properly structured package can be:
- Installed with `pip install .`
- Published to PyPI
- Shared across your team with consistent installation
- Used in CI/CD pipelines reliably

**`setup.py`** — the traditional packaging file (still widely used)
**`pyproject.toml`** — the modern standard (PEP 517/518), used by Poetry, Flit, and modern pip

**`src` layout pattern:** Placing your package inside a `src/` subdirectory prevents accidental imports of the local directory (instead of the installed package) during testing.

---

## 3. Syntax & Code Examples

### 3.1 Import Styles in Action

```python
# ── Style 1: Module import (most explicit, safest) ─────────────────────────
import math
import os
import sys

print(math.pi)              # 3.141592653589793
print(math.sqrt(16))        # 4.0
print(os.getcwd())          # current working directory

# ── Style 2: Selective import ──────────────────────────────────────────────
from math import sqrt, pi, ceil
from os.path import join, exists, dirname

print(sqrt(25))             # 5.0  — no 'math.' prefix needed
print(join("/home", "user", "docs"))    # /home/user/docs

# ── Style 3: Aliased import (standard for heavy-use libraries) ─────────────
import numpy as np          # industry convention
import pandas as pd         # industry convention
import datetime as dt

today = dt.date.today()

# ── Style 4: Wildcard (avoid in production code) ───────────────────────────
from math import *          # imports everything in math.__all__
# ❌ Now you don't know where 'sqrt' came from — bad for readability

# ── Style 5: Relative import (inside packages only) ───────────────────────
# In student_manager/operations.py:
# from . import models           # import sibling module
# from .models import Student    # import name from sibling module
# from .. import config          # import from parent package
```

---

### 3.2 Inspecting `sys.path` and `sys.modules`

```python
import sys

# See where Python looks for modules (in order)
print("sys.path entries:")
for i, path in enumerate(sys.path):
    print(f"  [{i}] {path}")

# Output (example):
# [0] /home/user/myproject        ← your script's directory (searched first!)
# [1] /usr/lib/python310.zip
# [2] /usr/lib/python3.10
# [3] /usr/local/lib/python3.10/dist-packages   ← site-packages

# Add a custom path at runtime (rarely needed, but useful to understand)
sys.path.insert(0, "/path/to/my/custom/libs")

# Inspect what's already imported
import math
print("math" in sys.modules)       # True
print(type(sys.modules["math"]))   # <class 'module'>

# See all currently imported modules
print(list(sys.modules.keys())[:10])
```

---

### 3.3 Building a Module with `__all__`

```python
# math_utils.py

"""Math utility functions for the student manager."""

__version__ = "1.0.0"
__author__ = "Your Name"

# __all__ defines the public API
# Only these names are exported by 'from math_utils import *'
__all__ = ["average", "percentage", "letter_grade"]

def average(scores: list[float]) -> float:
    """Calculate the arithmetic mean of a list of scores."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)

def percentage(score: float, total: float) -> float:
    """Convert raw score to percentage."""
    return (score / total) * 100

def letter_grade(avg: float) -> str:
    """Convert numeric average to letter grade."""
    if avg >= 90: return "A"
    if avg >= 80: return "B"
    if avg >= 70: return "C"
    if avg >= 60: return "D"
    return "F"

def _internal_helper():
    """Prefixed with _ — private by convention, not in __all__."""
    pass
```

```python
# main.py — importing from math_utils

import math_utils                      # imports the module object
print(math_utils.average([85, 90]))    # 87.5
print(math_utils.__version__)          # 1.0.0

from math_utils import average, letter_grade    # selective — explicit
print(average([70, 80, 90]))           # 80.0
print(letter_grade(80.0))             # B

from math_utils import *               # wildcard — gets only __all__ items
# average, percentage, letter_grade available
# _internal_helper NOT available (not in __all__)
```

---

### 3.4 The `__name__ == "__main__"` Pattern

```python
# student_cli.py

"""
Student management CLI.
Can be imported as a module OR run directly as a script.
"""

import argparse
import sys


def add_student(name: str, grade: str) -> dict:
    """Create and return a student record."""
    return {"name": name, "grade": grade}


def list_students(students: list) -> None:
    """Print all students to stdout."""
    if not students:
        print("No students found.")
        return
    for i, s in enumerate(students, 1):
        print(f"  {i}. {s['name']} — Grade: {s['grade']}")


def parse_args():
    """Set up and return command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Student Management CLI",
        epilog="Example: python student_cli.py add --name Alice --grade A"
    )
    subparsers = parser.add_subparsers(dest="command")

    # 'add' subcommand
    add_parser = subparsers.add_parser("add", help="Add a new student")
    add_parser.add_argument("--name", required=True, help="Student name")
    add_parser.add_argument("--grade", default="N/A", help="Student grade")

    # 'list' subcommand
    subparsers.add_parser("list", help="List all students")

    return parser.parse_args()


# ── Entry point guard ──────────────────────────────────────────────────────
if __name__ == "__main__":
    # This block ONLY runs when executed directly:
    #   python student_cli.py add --name Alice --grade A
    # It does NOT run when imported:
    #   import student_cli  (only the functions are loaded)

    args = parse_args()
    students = []       # in real app, load from file/DB

    if args.command == "add":
        student = add_student(args.name, args.grade)
        students.append(student)
        print(f"✅ Added: {student}")
    elif args.command == "list":
        list_students(students)
    else:
        print("No command given. Use --help for usage.")
        sys.exit(1)
```

**Usage:**
```bash
python student_cli.py add --name Alice --grade A
# ✅ Added: {'name': 'Alice', 'grade': 'A'}

python student_cli.py list
# 1. Alice — Grade: A

python student_cli.py --help
```

---

### 3.5 Virtual Environments — Full Workflow

```bash
# ── Step 1: Create a virtual environment ──────────────────────────────────
python -m venv venv          # creates 'venv/' directory
# or with a specific Python version:
python3.11 -m venv venv

# ── Step 2: Activate ──────────────────────────────────────────────────────
# macOS / Linux:
source venv/bin/activate

# Windows (Command Prompt):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# After activation — prompt changes:
# (venv) user@machine:~/project$

# ── Step 3: Verify isolation ───────────────────────────────────────────────
which python          # → /path/to/project/venv/bin/python
pip list              # → only pip and setuptools (clean slate)

# ── Step 4: Install packages ───────────────────────────────────────────────
pip install requests
pip install django==4.2
pip install "django>=4.0,<5.0"      # version constraints

# ── Step 5: Freeze dependencies ────────────────────────────────────────────
pip freeze > requirements.txt       # capture exact versions
cat requirements.txt
# Django==4.2.7
# requests==2.31.0
# ...

# ── Step 6: Install from requirements (for teammates / CI) ────────────────
pip install -r requirements.txt

# ── Step 7: Deactivate ─────────────────────────────────────────────────────
deactivate

# ── Development vs Production dependencies ────────────────────────────────
# requirements.txt           — production (minimal)
# requirements-dev.txt       — includes testing, linting tools
pip install -r requirements.txt           # production
pip install -r requirements-dev.txt       # development

# ── Editable install (for packages you're developing) ─────────────────────
pip install -e .    # installs current directory as editable package
                    # changes to source are reflected immediately
```

---

### 3.6 Complete Package Structure

```
student_manager/                    ← project root (git repo)
│
├── src/                            ← src layout (modern best practice)
│   └── student_manager/            ← the actual package
│       ├── __init__.py             ← package entry point
│       ├── models.py               ← Student data models
│       ├── operations.py           ← CRUD operations
│       └── utils.py                ← shared utilities
│
├── tests/                          ← test suite
│   ├── __init__.py
│   ├── test_models.py
│   └── test_operations.py
│
├── .env                            ← environment variables (NOT in git)
├── .gitignore                      ← exclude venv/, __pycache__/, .env
├── README.md
├── requirements.txt                ← production deps
├── requirements-dev.txt            ← dev deps (pytest, black, mypy)
└── pyproject.toml                  ← modern packaging config
```

---

### 3.7 Package Files in Detail

```python
# src/student_manager/__init__.py

"""
Student Manager Package
=======================
A simple student record management system.

Usage:
    from student_manager import StudentManager
    from student_manager.models import Student
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "you@example.com"

# Re-export the most commonly used names for convenience
# Users can do: from student_manager import StudentManager
# instead of:   from student_manager.operations import StudentManager
from .operations import StudentManager
from .models import Student

__all__ = ["StudentManager", "Student"]
```

```python
# src/student_manager/models.py

"""Data models for the student manager."""

from collections import namedtuple
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Student:
    """Represents a student record."""
    name: str
    age: int
    grade: str = "N/A"
    scores: list[float] = field(default_factory=list)
    student_id: Optional[int] = None

    def average_score(self) -> float:
        if not self.scores:
            return 0.0
        return round(sum(self.scores) / len(self.scores), 1)

    def __repr__(self) -> str:
        return f"Student(name={self.name!r}, grade={self.grade!r}, avg={self.average_score()})"
```

```python
# src/student_manager/utils.py

"""Shared utility functions — imported by both models.py and operations.py."""

def letter_grade(average: float) -> str:
    """Convert numeric average to letter grade."""
    if average >= 90: return "A"
    if average >= 80: return "B"
    if average >= 70: return "C"
    if average >= 60: return "D"
    return "F"

def validate_name(name: str) -> bool:
    """Return True if name is non-empty string."""
    return isinstance(name, str) and len(name.strip()) > 0

def format_student_row(student) -> str:
    """Format a student for tabular display."""
    return f"{student.student_id:>4} | {student.name:<20} | {student.grade:^5} | {student.average_score():>6.1f}"
```

```python
# src/student_manager/operations.py

"""CRUD operations on student records."""

from typing import Optional
from .models import Student      # relative import — sibling module
from .utils import letter_grade, validate_name   # relative import


class StudentManager:
    """Manages a collection of student records."""

    def __init__(self):
        self._students: dict[int, Student] = {}
        self._next_id: int = 1

    def add(self, name: str, age: int, scores: list[float] = None) -> Student:
        """Create and store a new student. Returns the created Student."""
        if not validate_name(name):
            raise ValueError(f"Invalid student name: {name!r}")

        scores = scores or []
        avg = sum(scores) / len(scores) if scores else 0.0
        grade = letter_grade(avg)

        student = Student(
            name=name,
            age=age,
            grade=grade,
            scores=scores,
            student_id=self._next_id
        )
        self._students[self._next_id] = student
        self._next_id += 1
        return student

    def get(self, student_id: int) -> Optional[Student]:
        """Return student by ID or None."""
        return self._students.get(student_id)

    def update_scores(self, student_id: int, scores: list[float]) -> bool:
        """Update scores and recalculate grade. Returns True if found."""
        student = self._students.get(student_id)
        if student is None:
            return False
        student.scores = scores
        avg = student.average_score()
        student.grade = letter_grade(avg)
        return True

    def delete(self, student_id: int) -> bool:
        """Delete student. Returns True if deleted."""
        return self._students.pop(student_id, None) is not None

    def list_all(self) -> list[Student]:
        """Return all students sorted by name."""
        return sorted(self._students.values(), key=lambda s: s.name)

    def __len__(self) -> int:
        return len(self._students)
```

```toml
# pyproject.toml — modern packaging configuration

[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "student-manager"
version = "0.1.0"
description = "A simple student record management system"
readme = "README.md"
requires-python = ">=3.10"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = []   # add third-party deps here

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "mypy>=1.0",
]

[tool.setuptools.packages.find]
where = ["src"]     # tells setuptools to look in src/

[project.scripts]
student-manager = "student_manager.cli:main"   # CLI entry point
```

---

### 3.8 Handling Circular Imports

```python
# ── Circular import problem ────────────────────────────────────────────────

# models.py (BAD version)
from operations import StudentManager   # imports operations

# operations.py (BAD version)
from models import Student              # imports models — CIRCULAR!
# When Python loads models.py, it starts loading operations.py,
# which needs models.py, which isn't fully loaded yet → ImportError

# ── Solution 1: Move shared code to utils.py (best) ───────────────────────
# models.py — imports only from utils (no circular dep)
from .utils import letter_grade

# operations.py — imports from models and utils (no circular dep)
from .models import Student
from .utils import letter_grade, validate_name

# ── Solution 2: Import inside the function (lazy import) ──────────────────
# models.py
def get_manager():
    from .operations import StudentManager  # imported only when called
    return StudentManager()

# ── Solution 3: Import module, not names ──────────────────────────────────
# Instead of: from operations import StudentManager (triggers full load)
# Use:        import operations (deferred; attributes accessed later)
import operations
manager = operations.StudentManager()
```

---

## 4. Common Mistakes & Gotchas

### ❌ Mistake 1: Naming Your File the Same as a Standard Library Module

```python
# ❌ Wrong — you created a file called 'math.py' in your project
# When you write: import math
# Python finds YOUR math.py first (it's in sys.path[0])!

# File: math.py (your file — accidentally named)
def sqrt(x):
    return x ** 0.5    # your version

# main.py
import math
print(math.pi)      # AttributeError: module 'math' has no attribute 'pi'
                    # Because Python imported YOUR math.py!

# ✅ Fix — never name files after built-in or stdlib modules
# Rename to: my_math.py, math_utils.py, custom_math.py
```

---

### ❌ Mistake 2: Forgetting to Activate the Virtual Environment

```bash
# ❌ Wrong — installing globally without activating venv
pip install django       # installs to GLOBAL Python! Pollutes system.

# ✅ Correct — always activate first
source venv/bin/activate    # (macOS/Linux)
pip install django           # now installs to venv only

# Quick check: is venv active?
which python    # should show path inside your project/venv/
# or check prompt — should show (venv) prefix
```

---

### ❌ Mistake 3: Using Relative Imports Outside a Package

```python
# ❌ Wrong — relative imports only work inside packages
# If you run:  python models.py  directly (as a script)
# Then models.py is __main__, not part of a package

# models.py
from .utils import helper    # ImportError: attempted relative import with no known parent package

# ✅ Correct — two options:

# Option A: Run the package, not the file
python -m student_manager.models    # runs as part of the package

# Option B: Use absolute imports when running as a script
# models.py
from student_manager.utils import helper    # absolute import — always works
```

---

### ❌ Mistake 4: Committing `venv/` or `.env` to Git

```bash
# ❌ Wrong — committing your virtual environment directory
git add venv/        # NEVER do this — venv/ is huge (~200MB) and machine-specific
git add .env         # NEVER do this — contains secret keys, DB passwords!

# ✅ Correct — add to .gitignore
# .gitignore
venv/
.env
__pycache__/
*.pyc
*.egg-info/
dist/
build/
.mypy_cache/

# ✅ Share dependencies via requirements.txt (generated, not the venv itself)
pip freeze > requirements.txt
git add requirements.txt    # this is fine to commit
```

---

### ❌ Mistake 5: Wildcard Imports in Production Code

```python
# ❌ Wrong — wildcard imports hide where names come from
from math import *
from os.path import *
from mymodule import *

sqrt(16)        # Which module? math? mymodule? Impossible to tell without checking.
join("/a", "b") # Which join? os.path? string? Ambiguous.

# ✅ Correct — explicit imports
from math import sqrt
from os.path import join

sqrt(16)        # Clearly from math
join("/a", "b") # Clearly from os.path

# Wildcard IS acceptable in:
# - __init__.py (re-exporting via __all__)
# - Interactive REPL sessions
# - Never in production module code
```

---

## 5. Hands-on Exercises

### 🧑‍🏫 Guided Exercise 1: Convert Student Manager into a Package

**Goal:** Take the student management code from Day 3 and restructure it as a proper Python package.

**Step 1: Create the directory structure**
```bash
mkdir -p student_manager/src/student_manager
mkdir -p student_manager/tests
touch student_manager/src/student_manager/__init__.py
touch student_manager/src/student_manager/models.py
touch student_manager/src/student_manager/operations.py
touch student_manager/src/student_manager/utils.py
touch student_manager/tests/__init__.py
touch student_manager/README.md
touch student_manager/requirements.txt
touch student_manager/pyproject.toml
cd student_manager
```

**Step 2: Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate    # (macOS/Linux)
# venv\Scripts\activate     # (Windows)
pip install -e .            # install package in editable mode
```

**Step 3: Populate the files**

Copy the `models.py`, `operations.py`, `utils.py`, and `__init__.py` content from Section 3.7 above into their respective files.

**Step 4: Test the imports work**
```python
# test_imports.py (run from project root)
from student_manager import StudentManager, Student

mgr = StudentManager()
alice = mgr.add("Alice", 20, [85, 92, 88])
print(alice)                    # Student(name='Alice', grade='B', avg=88.3)
print(len(mgr))                 # 1

bob = mgr.add("Bob", 22, [70, 65, 72])
print(mgr.list_all())           # [Student(Alice...), Student(Bob...)]
print(mgr.get(1))               # Student for Alice
print(mgr.update_scores(2, [80, 85, 82]))  # True
print(mgr.get(2).grade)        # B (updated!)
```

**Step 5: Verify different import styles all work**
```python
# Style 1: Import the package
import student_manager
print(student_manager.__version__)  # 0.1.0

# Style 2: From package import
from student_manager import StudentManager

# Style 3: From submodule import
from student_manager.models import Student
from student_manager.utils import letter_grade

print(letter_grade(87.5))   # B
```

---

### 🧑‍🏫 Guided Exercise 2: CLI Entry Point with argparse

**Goal:** Add a working CLI to the student manager package.

```python
# src/student_manager/cli.py

"""Command-line interface for Student Manager."""

import argparse
import sys
from . import StudentManager

# Module-level manager (in real app, would load from persistent storage)
manager = StudentManager()


def cmd_add(args: argparse.Namespace) -> None:
    """Handle 'add' subcommand."""
    scores = list(map(float, args.scores.split(","))) if args.scores else []
    student = manager.add(args.name, args.age, scores)
    print(f"✅ Added student: {student}")


def cmd_list(args: argparse.Namespace) -> None:
    """Handle 'list' subcommand."""
    students = manager.list_all()
    if not students:
        print("No students found.")
        return
    print(f"\n{'ID':>4} | {'Name':<20} | {'Grade':^5} | {'Avg':>6}")
    print("-" * 45)
    for s in students:
        from .utils import format_student_row
        print(format_student_row(s))


def cmd_delete(args: argparse.Namespace) -> None:
    """Handle 'delete' subcommand."""
    success = manager.delete(args.id)
    msg = f"✅ Deleted student {args.id}" if success else f"❌ Student {args.id} not found"
    print(msg)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="student-manager",
        description="Manage student records from the command line"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    p_add = subparsers.add_parser("add", help="Add a new student")
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--age", type=int, required=True)
    p_add.add_argument("--scores", help="Comma-separated scores e.g. 85,90,78")
    p_add.set_defaults(func=cmd_add)

    # list command
    p_list = subparsers.add_parser("list", help="List all students")
    p_list.set_defaults(func=cmd_list)

    # delete command
    p_del = subparsers.add_parser("delete", help="Delete a student by ID")
    p_del.add_argument("--id", type=int, required=True)
    p_del.set_defaults(func=cmd_delete)

    return parser


def main() -> None:
    """Package entry point."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
```

**Test it:**
```bash
python -m student_manager.cli add --name Alice --age 20 --scores 85,92,88
python -m student_manager.cli add --name Bob --age 22 --scores 70,65,72
python -m student_manager.cli list
python -m student_manager.cli delete --id 1
python -m student_manager.cli list
```

---

### 💻 Independent Practice 1: Multi-Environment Setup

**Task:** Set up two separate virtual environments for the same project and observe isolation.

```bash
# 1. Create project directory
mkdir env_experiment && cd env_experiment

# 2. Create two virtual environments
python -m venv env_dev
python -m venv env_prod

# 3. Install different packages in each
source env_dev/bin/activate
pip install requests==2.28.0    # older version for dev
pip freeze > requirements-dev.txt
deactivate

source env_prod/bin/activate
pip install requests==2.31.0    # newer version for prod
pip freeze > requirements-prod.txt
deactivate

# 4. Write a script that prints the requests version
# requests_version.py
import requests
print(f"requests version: {requests.__version__}")

# 5. Run with each environment and observe
source env_dev/bin/activate && python requests_version.py    # 2.28.0
source env_prod/bin/activate && python requests_version.py   # 2.31.0
```

**Questions to answer:**
```
1. Can env_dev "see" packages installed in env_prod? ______
2. Where does pip install packages inside the venv? ______
3. What does deactivate do to sys.path? ______
```

> **Hints:** Check `env_dev/lib/python3.x/site-packages/`. Use `python -c "import sys; print(sys.path)"` before and after activation.

---

### 💻 Independent Practice 2: Fix the Broken Package

**Task:** The following package has 3 bugs. Find and fix them all.

```
broken_package/
├── __init__.py
├── calculator.py
└── helpers.py
```

```python
# __init__.py  — Bug 1 is here
from calculator import add, subtract   # what's wrong with this import?
```

```python
# calculator.py — Bug 2 is here
import math.py  # what's wrong with this import?

from helpers import validate_number

def add(a, b):
    validate_number(a)
    validate_number(b)
    return a + b

def subtract(a, b):
    validate_number(a)
    validate_number(b)
    return a - b

if __name__ == "__main__":
    print(add(5, 3))
    print(subtract(10, 4))
```

```python
# helpers.py — Bug 3 is here
def validate_number(n):
    if not isinstance(n, (int, float)):
        raise TypeError(f"Expected number, got {type(n)}")

# This file was accidentally named 'random.py' in another version.
# Rename scenario: what would break if this file was named 'math.py'?
```

**Bug descriptions and fixes:**
```
Bug 1 (in __init__.py):  ___________________________________
Fix:                      ___________________________________

Bug 2 (in calculator.py): __________________________________
Fix:                       __________________________________

Bug 3 (describe the rename scenario): _______________________
Fix:                                   _______________________
```

---

### 🏆 Challenge Problem: Build a Plugin System

```python
"""
Build a simple plugin system using Python's import machinery.

Requirements:
1. A 'plugins/' directory containing separate .py files (each is a plugin)
2. A plugin loader that dynamically imports all .py files in the directory
3. Each plugin must expose: name, version, and a run() function
4. The main program discovers and runs all available plugins
5. New plugins can be added by just dropping a .py file in the directory

Structure:
    plugin_system/
    ├── main.py           ← discovers and runs plugins
    ├── plugin_loader.py  ← dynamic import logic
    └── plugins/
        ├── __init__.py
        ├── hello_plugin.py
        ├── math_plugin.py
        └── date_plugin.py
"""

# plugin_loader.py
import importlib
import pkgutil
from types import ModuleType

def load_plugins(package_name: str) -> list[ModuleType]:
    """
    Dynamically discover and import all modules in a package.
    Returns list of imported plugin modules.
    """
    import importlib
    package = importlib.import_module(package_name)
    plugins = []

    for finder, name, ispkg in pkgutil.iter_modules(package.__path__):
        full_name = f"{package_name}.{name}"
        module = importlib.import_module(full_name)
        plugins.append(module)

    return plugins

def validate_plugin(module: ModuleType) -> bool:
    """Check if a module has the required plugin interface."""
    required = ["name", "version", "run"]
    return all(hasattr(module, attr) for attr in required)


# plugins/hello_plugin.py
name = "Hello Plugin"
version = "1.0.0"

def run(context: dict = None) -> str:
    return f"Hello from {name} v{version}!"


# plugins/math_plugin.py
import math as _math
name = "Math Plugin"
version = "1.0.0"

def run(context: dict = None) -> str:
    n = context.get("n", 16) if context else 16
    return f"sqrt({n}) = {_math.sqrt(n):.4f}"


# main.py
from plugin_loader import load_plugins, validate_plugin

def main():
    print("🔌 Plugin System Demo\n")
    plugins = load_plugins("plugins")

    valid = [p for p in plugins if validate_plugin(p)]
    invalid = [p.__name__ for p in plugins if not validate_plugin(p)]

    if invalid:
        print(f"⚠️  Skipped invalid plugins: {invalid}\n")

    context = {"n": 25}
    for plugin in valid:
        print(f"▶ Running: {plugin.name} v{plugin.version}")
        result = plugin.run(context)
        print(f"  Result: {result}\n")

if __name__ == "__main__":
    main()
```

---

## 6. Best Practices & Industry Standards

### Import Organization (PEP 8)

```python
# PEP 8 mandates this import order, separated by blank lines:

# 1. Standard library imports
import os
import sys
from pathlib import Path
from typing import Optional

# 2. Third-party imports
import django
import requests
from flask import Flask

# 3. Local application / package imports
from student_manager import StudentManager
from student_manager.models import Student
from student_manager.utils import letter_grade

# ✅ Use isort or black to auto-format import order
# pip install isort
# isort your_file.py
```

---

### Virtual Environment Hygiene

```bash
# ✅ Always use a venv — no exceptions
# ✅ Name it 'venv' (standard) or '.venv' (hidden, popular with modern tools)
# ✅ Always add it to .gitignore
# ✅ Document Python version in README or .python-version file

# .python-version (used by pyenv)
echo "3.11.0" > .python-version

# ✅ Separate dev and prod requirements
# requirements.txt       — production (minimal)
django==4.2.7
psycopg2==2.9.9

# requirements-dev.txt
-r requirements.txt          # includes production deps
pytest==7.4.0
black==23.10.0
mypy==1.6.0
isort==5.12.0
```

---

### Project Structure Guidelines

```
# ✅ Industry-standard Django project structure (preview)
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py          ← shared settings
│   │   ├── development.py   ← dev overrides
│   │   └── production.py    ← prod overrides
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   └── students/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       └── urls.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
└── venv/                    ← in .gitignore
```

---

### What Professionals Actually Do

```bash
# ✅ Use modern tools instead of bare venv + pip
pip install poetry           # dependency resolver + venv manager
poetry new myproject         # creates project with pyproject.toml
poetry add django            # adds and installs dep
poetry add --group dev pytest black  # dev deps

# ✅ Or use pipenv
pip install pipenv
pipenv install django
pipenv install --dev pytest

# ✅ Pin exact versions in production
pip freeze > requirements.txt    # captures exact versions

# ✅ Use .env for secrets, never hardcode
# .env
DATABASE_URL=postgresql://user:pass@localhost/mydb
SECRET_KEY=your-secret-key-here
DEBUG=False

# config.py
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-for-dev-only")
```

---

## 7. Real-World Application

### Django Project IS a Python Package

```python
# Every Django project is structured as a package
# manage.py uses __name__ == "__main__" pattern

# manage.py (Django's auto-generated file)
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django...") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

# Django's settings split (production pattern)
# settings/base.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# settings/development.py
from .base import *         # relative import — imports base settings
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# settings/production.py
from .base import *
import os
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']   # must be in environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
    }
}
```

### Flask Application Factory Pattern

```python
# factory pattern uses package structure + __init__.py
# myapp/__init__.py

from flask import Flask
from .config import Config
from .extensions import db, migrate

def create_app(config_class=Config) -> Flask:
    """Application factory — creates and configures the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (modular routes)
    from .students import bp as students_bp
    app.register_blueprint(students_bp, url_prefix='/students')

    return app

# run.py
from myapp import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

### 🔭 Connection to Upcoming Days
- **Day 5:** File I/O and error handling — uses module-level imports and `__name__` guard
- **Day 8:** Decorators — implemented as modules in a package; uses relative imports
- **Day 20:** Django setup — `django-admin startproject` generates a package; first command is `pip install django` in a venv
- **Day 30+:** Deployment — `requirements.txt` and `pyproject.toml` are what Docker and CI/CD use to install your app

---

## 8. Quick Revision Summary

### Key Terms

| Term | One-line Definition |
|------|---------------------|
| Module | A single `.py` file that can be imported |
| Package | A directory with `__init__.py` that groups related modules |
| `sys.path` | Ordered list of directories Python searches for modules |
| `sys.modules` | Cache of already-imported modules — checked first on every import |
| `__init__.py` | Runs when a package is imported; defines the package's public API |
| `__all__` | List in a module defining what `from module import *` exports |
| `__name__` | `"__main__"` when run as script; module name when imported |
| Absolute import | Full dotted path: `from student_manager.models import Student` |
| Relative import | Dot notation: `from .models import Student` (only inside packages) |
| Virtual environment | Isolated Python installation with its own packages |
| `pip freeze` | Outputs installed packages with exact versions |
| `requirements.txt` | Text file listing project dependencies for `pip install -r` |
| Editable install | `pip install -e .` — installs package so source changes are live |
| `pyproject.toml` | Modern packaging config file (PEP 517/518) |
| Circular import | Module A imports B which imports A — causes `ImportError` |
| Lazy import | Deferring an import to inside a function — avoids circular deps |

---

### Core Syntax Cheat Sheet

```python
# ── Import styles ──────────────────────────────────────────────────────────
import module
from module import name
from module import name as alias
import module as alias
from package.submodule import name
from . import sibling_module          # relative (inside package)
from .sibling import name             # relative selective

# ── Controlling exports ────────────────────────────────────────────────────
__all__ = ["PublicClass", "public_func"]   # in your module

# ── Entry point guard ──────────────────────────────────────────────────────
if __name__ == "__main__":
    main()

# ── sys.path inspection ────────────────────────────────────────────────────
import sys
print(sys.path)
sys.path.insert(0, "/custom/path")

# ── Virtual environment (shell commands) ───────────────────────────────────
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
pip install package
pip freeze > requirements.txt
pip install -r requirements.txt
pip install -e .                # editable install
deactivate

# ── argparse skeleton ──────────────────────────────────────────────────────
import argparse
parser = argparse.ArgumentParser(description="...")
parser.add_argument("--name", required=True)
parser.add_argument("--count", type=int, default=1)
args = parser.parse_args()
print(args.name, args.count)
```

---

### 5 MCQ Recap Questions

**Q1.** What is the correct order Python searches for a module named `mymodule`?
- A) Built-ins → `sys.path` → `sys.modules`
- **B) `sys.modules` cache → Built-ins → `sys.path` directories** ✅
- C) `sys.path` → Built-ins → `sys.modules`
- D) Current directory → Built-ins → `sys.modules`

**Q2.** When does `if __name__ == "__main__":` evaluate to `True`?
- A) Always
- B) When the file is imported as a module
- **C) When the file is run directly as a script** ✅
- D) When the file is inside a package

**Q3.** What is the correct way to create an empty set of virtual environment files to exclude from git?
- A) Delete the `venv/` directory after every session
- B) Add `venv/` to `requirements.txt`
- **C) Add `venv/` to `.gitignore`** ✅
- D) Use `pip uninstall -r requirements.txt`

**Q4.** Which import style is the safest and most explicit?
- A) `from math import *`
- B) `from . import *`
- **C) `import math` and use `math.sqrt()`** ✅
- D) `import math as m` (aliased)

**Q5.** What is the purpose of `__init__.py` in a package directory?
- A) It speeds up module imports
- B) It defines `sys.path` for the package
- **C) It runs when the package is imported and controls the package's public API** ✅
- D) It is required for Python to recognize `.py` files

---

## 9. Instructor Notes

### 📌 Anticipated Student Questions

| Question | Suggested Answer |
|----------|-----------------|
| "Can I use a venv inside another venv?" | Technically yes, but never do it. Always deactivate before creating a new one. |
| "What's the difference between `pip install` and `pip install -e .`?" | Regular install copies the package to site-packages. Editable install (`-e`) creates a link — changes to your source are immediately reflected without reinstalling. |
| "Why does `from . import module` fail when I run the file directly?" | Relative imports require the file to be part of a package. Run with `python -m package.module` or use absolute imports. |
| "What is `__pycache__` and can I delete it?" | Python's cached bytecode folder. Safe to delete — Python recreates it. Should be in `.gitignore`. |
| "What's the difference between `setup.py` and `pyproject.toml`?" | `setup.py` is the old way (still works). `pyproject.toml` is the modern PEP 517/518 standard — all new projects should use it. |
| "Is `pipenv` better than `venv`?" | `pipenv` and `poetry` add dependency resolution on top of venv. Fine for most projects. Teams often standardize on one tool. The concepts are the same. |
| "Can two projects share a venv?" | Technically yes, but it defeats the purpose. Each project must have its own venv. |


---

### 📚 Resources & Further Reading

- [Python Docs — The Import System](https://docs.python.org/3/reference/import.html)
- [Python Docs — `venv`](https://docs.python.org/3/library/venv.html)
- [Python Docs — `argparse`](https://docs.python.org/3/library/argparse.html)
- [PEP 8 — Import style guidelines](https://peps.python.org/pep-0008/#imports)
- [PEP 517 / 518 — `pyproject.toml`](https://peps.python.org/pep-0517/)
- [Real Python — Python Import System](https://realpython.com/python-import/)
- [Real Python — Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)
- [Poetry — modern dependency management](https://python-poetry.org/)
