# 💪 Python Full Stack — Day 4 Exercise & Practice File
# Topic: Modules, Packages & Virtual Environments

> **Instructions:** Work through sections in order. Predict outputs before running. Attempt every problem genuinely before checking the answer key. Many exercises require your terminal alongside your editor.

---

## 📋 Setup Check

```python
# Run this in Python to confirm your environment
import sys
import os

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Working directory: {os.getcwd()}")

print("\nsys.path entries:")
for i, p in enumerate(sys.path):
    print(f"  [{i}] {p or '(empty string = current dir)' }")
```

---

## Section A — Predict the Output (No Running Allowed!)

### A1. `__name__` Behavior

```python
# file: predictor.py
print(f"__name__ is: {__name__}")

def greet():
    return "Hello from predictor!"

if __name__ == "__main__":
    print("Running as script!")
    print(greet())
```

**Scenario 1:** You run `python predictor.py` directly.
```
Prediction: ______________________________
             ______________________________
```

**Scenario 2:** In another file, you write `import predictor`.
```
Prediction: ______________________________
```

**Scenario 3:** In another file, you write `from predictor import greet`.
```
Prediction: ______________________________
```

---

### A2. Import and `sys.modules`

```python
import sys
import math
import math    # imported again
import math    # imported again

print(id(sys.modules["math"]) == id(math))   # Line 1
print(sys.modules["math"] is math)            # Line 2

import os
print("json" in sys.modules)                  # Line 3 — json not yet imported
import json
print("json" in sys.modules)                  # Line 4 — json now imported
```

**Predictions:**
```
Line 1: ___
Line 2: ___
Line 3: ___
Line 4: ___
```

---

### A3. `__all__` Behavior

```python
# mymodule.py
__all__ = ["alpha", "beta"]

alpha = 1
beta = 2
gamma = 3
_delta = 4

def public_func(): return "public"
def _private_func(): return "private"
```

```python
# main.py
from mymodule import *

print(alpha)            # Line 1
print(beta)             # Line 2
# print(gamma)          # Line 3 — will this work?
# print(_delta)         # Line 4 — will this work?
```

**Predictions:**
```
Line 1: ___
Line 2: ___
Line 3 (if uncommented): ___ (NameError or value?)
Line 4 (if uncommented): ___ (NameError or value?)
```

---

### A4. Package Import Chain

```python
# Assume this package structure exists:
# mypackage/
# ├── __init__.py  →  from .core import Helper; __version__ = "2.0"
# ├── core.py      →  class Helper: def run(self): return "running"
# └── utils.py     →  def fmt(x): return f"[{x}]"

import mypackage

print(mypackage.__version__)            # Line 1
print(type(mypackage.Helper))          # Line 2

from mypackage import Helper
h = Helper()
print(h.run())                          # Line 3

from mypackage.utils import fmt
print(fmt("hello"))                     # Line 4
```

**Predictions:**
```
Line 1: ___
Line 2: ___
Line 3: ___
Line 4: ___
```

---

### A5. Import Style Differences

```python
# What is in the namespace after each import?

# Case 1
import os
# What name(s) are added to local namespace? ______

# Case 2
from os import getcwd, listdir
# What name(s) are added to local namespace? ______

# Case 3
import os.path
# What name(s) are added to local namespace? ______

# Case 4
from os.path import join as path_join
# What name(s) are added to local namespace? ______
```

---

## Section B — Fill in the Blanks

### B1. Complete the `__init__.py`

```python
# student_manager/__init__.py

# 1. Set the version
______ = "1.0.0"

# 2. Set the author
______ = "Your Name"

# 3. Re-export StudentManager from operations submodule
from .______ import StudentManager

# 4. Re-export Student from models submodule
from .models import ______

# 5. Define the public API
______ = ["StudentManager", "Student"]
```

---

### B2. Complete the Import Statements

```python
# In student_manager/operations.py

# 1. Import Student from the sibling models module (relative)
from ______ import Student

# 2. Import letter_grade and validate_name from sibling utils (relative)
from .______ import letter_grade, validate_name

# 3. Import the entire models module (relative)
from ______ import models

# 4. Import from parent package's config (relative, going up one level)
from ______ import config

# 5. Import Student using absolute path (works anywhere)
from student_manager.______ import Student
```

---

### B3. Complete the argparse Setup

```python
import argparse

parser = argparse.ArgumentParser(
    description="Student Grade Calculator",
    ______ = "Example: python calc.py --scores 80,90,85 --name Alice"
)

# Required string argument
parser.add_argument("------", required=______, help="Student name")

# Optional integer with default
parser.add_argument("--age", type=______, default=18)

# Comma-separated scores
parser.add_argument("--scores", help="Comma-separated scores")

# Boolean flag (True if present, False if absent)
parser.add_argument("--verbose", action="______", help="Verbose output")

# Choices restricted argument
parser.add_argument("--format", choices=["text", "json", "csv"], default="text")

args = parser.______()  # parse the command line

# Access parsed values
print(args.name)
print(args.age)
print(args.verbose)    # True or False
scores = list(map(float, args.scores.split(","))) if args.scores else []
```

---

### B4. Virtual Environment Shell Commands

Fill in the correct commands:

```bash
# 1. Create a virtual environment named 'venv'
python -m ______ venv

# 2. Activate on macOS/Linux
______ venv/bin/activate

# 3. Activate on Windows (PowerShell)
venv\Scripts\______

# 4. Verify the active Python is inside venv
______ python

# 5. Install a specific version of Django
pip install ______

# 6. Install from requirements file
pip install ______ requirements.txt

# 7. Capture current environment to requirements file
pip ______ > requirements.txt

# 8. Install current package in editable mode
pip install ______ .

# 9. Deactivate
______
```

---

## Section C — Debugging Exercises

### C1. The Shadow Module Bug

```
Project structure:
myproject/
├── math.py         ← you created this
└── calculator.py
```

```python
# calculator.py
import math

def circle_area(radius: float) -> float:
    return math.pi * radius ** 2

print(circle_area(5))   # AttributeError: module 'math' has no attribute 'pi'
```

**Explain why this crashes:**
```
______________________________________________
______________________________________________
```

**Fix it (two approaches):**
```
Fix 1 (rename the file): ____________________
Fix 2 (modify sys.path to skip local dir):
import sys
____________________
import math
```

---

### C2. The Missing `__init__.py`

```
Directory structure:
utilities/
├── string_utils.py
└── number_utils.py
```

```python
# app.py
from utilities import string_utils   # ModuleNotFoundError
```

**Why does this fail?**
```
______________________________________________
```

**Fix it:**
```bash
# What file needs to be created, and where?
touch ______________________
```

---

### C3. The Circular Import

```python
# users.py
from permissions import get_permissions

class User:
    def __init__(self, name):
        self.name = name
        self.permissions = get_permissions(self)

# permissions.py
from users import User      # ← circular!

PERMISSION_MAP = {
    "admin": ["read", "write", "delete"],
    "user": ["read"],
}

def get_permissions(user: User) -> list:
    return PERMISSION_MAP.get(user.role, [])
```

**Identify the circular dependency:**
```
______________________________________________
```

**Fix it using the "extract to third module" approach:**
```python
# constants.py (new file — no imports from users or permissions)
PERMISSION_MAP = ______

# permissions.py (fixed — no longer imports users)
from .constants import ______
def get_permissions(role: str) -> list:
    ______

# users.py (fixed)
from .permissions import get_permissions
class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.permissions = ______
```

---

### C4. The Relative Import in a Script

```python
# Running: python src/student_manager/operations.py
# operations.py

from .models import Student     # ImportError!
from .utils import validate_name

class StudentManager:
    pass
```

**Why does this fail?**
```
______________________________________________
```

**Two ways to fix it:**
```
Fix 1 (run as module, not script):
python ______________________

Fix 2 (use absolute import in the file):
from ______.______ import Student
from ______.______ import validate_name
```

---

### C5. The Venv Not Activated

```bash
# A developer runs:
pip install flask
python app.py   # ImportError: No module named 'flask'
```

**What most likely happened?**
```
______________________________________________
```

**Diagnostic commands to confirm:**
```bash
# Check which Python/pip is active
______
______

# Check if flask is installed in the venv
______

# Fix:
______
______
```

---

## Section D — Write the Code

### D1. Create a Proper Module with `__all__`

```python
# Write a complete 'string_utils.py' module that:
# 1. Has __version__ = "1.0.0" and __author__
# 2. Defines __all__ with only the public functions
# 3. Has these PUBLIC functions:
#    - capitalize_words(text: str) -> str  (capitalize each word)
#    - truncate(text: str, max_len: int, suffix: str = "...") -> str
#    - count_vowels(text: str) -> int
#    - is_palindrome(text: str) -> bool
# 4. Has this PRIVATE function (not in __all__):
#    - _clean(text: str) -> str  (strips and lowercases)
# 5. Has if __name__ == "__main__": block that tests all functions

# Your implementation:
```

**Test it two ways:**
```python
# Test 1: run directly
# python string_utils.py

# Test 2: import it
from string_utils import *
# What functions are available? (only those in __all__)

from string_utils import _clean   # does this work despite not being in __all__?
```

---

### D2. Build the Student Manager Package

Build the complete package from scratch following the structure below:

```
student_manager/
├── src/
│   └── student_manager/
│       ├── __init__.py
│       ├── models.py
│       ├── operations.py
│       └── utils.py
├── tests/
│   └── test_basic.py
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```

**Step 1 — Create the structure:**
```bash
mkdir -p student_manager/src/student_manager
mkdir -p student_manager/tests
cd student_manager
```

**Step 2 — Write `utils.py`:**
```python
# src/student_manager/utils.py
# Must contain:
# - letter_grade(average: float) -> str
# - validate_name(name: str) -> bool
# - format_student_row(student) -> str
# No imports from other package modules (avoids circular deps)
```

**Step 3 — Write `models.py`:**
```python
# src/student_manager/models.py
# Must contain:
# - Student dataclass with fields: name, age, grade, scores, student_id
# - average_score() method
# - __repr__ method
# Import ONLY from utils.py (relative import)
```

**Step 4 — Write `operations.py`:**
```python
# src/student_manager/operations.py
# Must contain StudentManager class with:
# - add(name, age, scores) -> Student
# - get(student_id) -> Optional[Student]
# - update_scores(student_id, scores) -> bool
# - delete(student_id) -> bool
# - list_all() -> list[Student]
# Import from models.py and utils.py (relative imports)
```

**Step 5 — Write `__init__.py`:**
```python
# src/student_manager/__init__.py
# Must:
# - Set __version__ and __author__
# - Re-export StudentManager and Student
# - Define __all__
```

**Step 6 — Write `pyproject.toml`:**
```toml
# Fill in the pyproject.toml
[build-system]
requires = ______
build-backend = ______

[project]
name = ______
version = ______
requires-python = ______
```

**Step 7 — Set up venv and install:**
```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

**Step 8 — Write `tests/test_basic.py`:**
```python
# tests/test_basic.py
from student_manager import StudentManager, Student

def test_add_student():
    mgr = StudentManager()
    s = mgr.add("Alice", 20, [85, 90, 88])
    assert s.name == "Alice"
    assert s.grade == "B"
    assert s.average_score() == 87.7

def test_get_student():
    mgr = StudentManager()
    mgr.add("Bob", 22, [70, 75])
    s = mgr.get(1)
    assert s is not None
    assert s.name == "Bob"

def test_delete_student():
    mgr = StudentManager()
    mgr.add("Carol", 21, [90, 95])
    assert mgr.delete(1) == True
    assert mgr.delete(1) == False   # already deleted

def test_list_all_sorted():
    mgr = StudentManager()
    mgr.add("Zara", 20, [80])
    mgr.add("Alice", 22, [90])
    names = [s.name for s in mgr.list_all()]
    assert names == ["Alice", "Zara"]   # sorted alphabetically

# Run: python -m pytest tests/ -v
```

---

### D3. CLI with argparse

Build a complete CLI for the student manager:

```python
# src/student_manager/cli.py

"""
Complete CLI with these commands:
  add    --name NAME --age AGE [--scores S1,S2,S3]
  list   [--grade GRADE] [--sort-by name|grade|average]
  get    --id ID
  delete --id ID
  stats  (show count, class average, grade distribution)
"""

import argparse
import sys
from . import StudentManager

# Global manager (simplified — no persistence)
_manager = StudentManager()

def cmd_add(args):
    """Handle 'add' command."""
    # Parse scores from comma-separated string
    scores = list(map(float, args.scores.split(","))) if args.scores else []
    student = _manager.add(args.name, args.age, scores)
    print(f"✅ Added: {student}")

def cmd_list(args):
    """Handle 'list' command."""
    students = _manager.list_all()
    # Filter by grade if --grade provided
    if args.grade:
        students = [s for s in students if s.grade == args.grade.upper()]
    # Sort by specified field
    if args.sort_by == "average":
        students.sort(key=lambda s: s.average_score(), reverse=True)
    elif args.sort_by == "grade":
        students.sort(key=lambda s: s.grade)
    # Print table
    # Your implementation

def cmd_get(args):
    """Handle 'get' command."""
    # Your implementation

def cmd_delete(args):
    """Handle 'delete' command."""
    # Your implementation

def cmd_stats(args):
    """Handle 'stats' command."""
    from collections import Counter
    students = _manager.list_all()
    if not students:
        print("No students."); return
    avgs = [s.average_score() for s in students]
    grades = Counter(s.grade for s in students)
    print(f"Total students: {len(students)}")
    print(f"Class average:  {sum(avgs)/len(avgs):.1f}")
    print(f"Highest score:  {max(avgs):.1f}")
    print(f"Lowest score:   {min(avgs):.1f}")
    print(f"Grade distribution: {dict(grades)}")

def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    # Your implementation — create parser with 5 subcommands
    pass

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(1)
    args.func(args)

if __name__ == "__main__":
    main()
```

**Test:**
```bash
python -m student_manager.cli add --name Alice --age 20 --scores 85,90,88
python -m student_manager.cli add --name Bob --age 22 --scores 70,65,72
python -m student_manager.cli list
python -m student_manager.cli list --grade B --sort-by average
python -m student_manager.cli get --id 1
python -m student_manager.cli stats
python -m student_manager.cli delete --id 2
```

---

### D4. Demonstrate Import Resolution

```python
# exploration.py
# Write a script that:
# 1. Prints all sys.path entries with their index
# 2. Checks if 3 modules are in sys.modules before and after import
# 3. Shows the file location of an imported module using __file__
# 4. Shows what names are in a module using dir()
# 5. Shows what's in __all__ if it exists

import sys

# 1. Print sys.path
def show_path():
    print("=== sys.path ===")
    for i, p in enumerate(sys.path):
        print(f"  [{i}] {p or '(current dir)'}")

# 2. Check sys.modules before/after import
def check_modules_cache():
    modules_to_check = ["json", "pathlib", "collections"]
    print("\n=== Before import ===")
    for m in modules_to_check:
        print(f"  {m}: {'cached' if m in sys.modules else 'not cached'}")

    # Now import them
    import json, pathlib, collections

    print("\n=== After import ===")
    for m in modules_to_check:
        print(f"  {m}: {'cached' if m in sys.modules else 'not cached'}")

# 3. Show module file location
def show_module_location():
    import math, os, json
    for mod in [math, os, json]:
        location = getattr(mod, "__file__", "built-in (no file)")
        print(f"  {mod.__name__}: {location}")

# 4. Show module contents
def show_module_contents():
    import math
    public_names = [n for n in dir(math) if not n.startswith("_")]
    print(f"  math public names: {public_names[:8]}...")

# 5. Show __all__ if present
def show_all_attribute():
    import os.path
    if hasattr(os.path, "__all__"):
        print(f"  os.path.__all__: {os.path.__all__}")
    else:
        print("  os.path has no __all__")

if __name__ == "__main__":
    show_path()
    check_modules_cache()
    show_module_location()
    show_module_contents()
    show_all_attribute()
```

---

## Section E — Environment Experiments

### E1. Isolation Proof

```bash
# Run these commands and record the output

# 1. Check global Python packages (outside any venv)
deactivate 2>/dev/null; pip list | head -20

# 2. Create and activate a new venv
python -m venv experiment_venv
source experiment_venv/bin/activate

# 3. Check packages inside venv (should be minimal)
pip list

# 4. Install a specific package
pip install httpx==0.24.0

# 5. Verify it's installed
python -c "import httpx; print(httpx.__version__)"

# 6. Deactivate and try to import (should fail)
deactivate
python -c "import httpx; print(httpx.__version__)"

# 7. What do you observe?
```

**Record observations:**
```
Inside venv — pip list shows:  ______________________
After deactivate — httpx import: ___________________
Why? _______________________________________________
```

---

### E2. `sys.path` Manipulation

```python
# Create these two files:

# /tmp/custom_modules/greeting.py
def hello(name: str) -> str:
    return f"Hello, {name}! (from custom path)"

# explorer.py (in your project directory)
import sys

print("Before sys.path modification:")
try:
    import greeting
    print(greeting.hello("World"))
except ModuleNotFoundError as e:
    print(f"  Not found: {e}")

# Add custom path
sys.path.insert(0, "/tmp/custom_modules")

print("\nAfter sys.path modification:")
import greeting
print(greeting.hello("World"))

print("\nVerify path was added:")
print(f"  sys.path[0] = {sys.path[0]}")
```

**Questions:**
```
1. Before adding the custom path, what error did you get? ______
2. After adding, did the import succeed? ______
3. Would this modification persist to the next Python session? ______
   Why? _______________________________________________
```

---

### E3. The `.gitignore` Generator

```python
# Write a Python script that generates a .gitignore file
# for a Python project.

def generate_gitignore(output_path: str = ".gitignore") -> None:
    """
    Generate a .gitignore file for Python projects.
    Include patterns for:
    - Virtual environments (venv/, .venv/, env/)
    - Python cache (__pycache__/, *.pyc, *.pyo)
    - Distribution files (dist/, build/, *.egg-info/)
    - IDE files (.vscode/, .idea/, *.swp)
    - Environment files (.env, .env.local)
    - OS files (.DS_Store, Thumbs.db)
    - Test/coverage (htmlcov/, .coverage, .pytest_cache/)
    - mypy cache (.mypy_cache/)
    """
    patterns = [
        # Your implementation — list of strings
    ]

    content = "\n".join(patterns)

    with open(output_path, "w") as f:
        f.write(content)

    print(f"✅ Generated {output_path} with {len(patterns)} patterns")

if __name__ == "__main__":
    generate_gitignore()
    # Verify it was created
    with open(".gitignore") as f:
        print(f.read())
```

---

## Section F — Mini Project: Plugin System

Build the complete plugin system from the challenge problem in the theory notes:

```
plugin_system/
├── main.py
├── plugin_loader.py
└── plugins/
    ├── __init__.py
    ├── hello_plugin.py
    ├── math_plugin.py
    └── date_plugin.py
```

**Step 1 — Create structure:**
```bash
mkdir -p plugin_system/plugins
touch plugin_system/plugins/__init__.py
```

**Step 2 — Create plugins (each must have `name`, `version`, `run()`):**
```python
# plugins/hello_plugin.py
name = "Hello Plugin"
version = "1.0.0"

def run(context: dict = None) -> str:
    target = context.get("target", "World") if context else "World"
    return f"Hello, {target}!"

# plugins/math_plugin.py
import math as _math

name = "Math Plugin"
version = "1.0.0"

def run(context: dict = None) -> str:
    n = context.get("number", 16) if context else 16
    return f"sqrt({n}) = {_math.sqrt(n):.4f}, pi ≈ {_math.pi:.4f}"

# plugins/date_plugin.py — write this one yourself
# It should return the current date and time formatted nicely
import datetime

name = "Date Plugin"
version = "1.0.0"

def run(context: dict = None) -> str:
    # Your implementation
    pass
```

**Step 3 — Write `plugin_loader.py`:**
```python
import importlib
import pkgutil
from types import ModuleType

REQUIRED_ATTRS = ["name", "version", "run"]

def load_plugins(package_name: str) -> tuple[list[ModuleType], list[str]]:
    """
    Load all valid plugins from a package.
    Returns (valid_plugins, error_messages)
    """
    # Your implementation
    pass

def run_all(package_name: str, context: dict = None) -> None:
    """Load and run all valid plugins, report errors for invalid ones."""
    # Your implementation
    pass
```

**Step 4 — Write `main.py`:**
```python
# main.py
from plugin_loader import run_all

if __name__ == "__main__":
    context = {"target": "Python", "number": 144}
    run_all("plugins", context)
```

**Expected output:**
```
🔌 Plugin System

▶ Hello Plugin v1.0.0
  Hello, Python!

▶ Date Plugin v1.0.0
  2024-01-15 10:30:45

▶ Math Plugin v1.0.0
  sqrt(144) = 12.0000, pi ≈ 3.1416
```

**Step 5 — Add a broken plugin to test error handling:**
```python
# plugins/broken_plugin.py
# Intentionally missing 'run' function
name = "Broken Plugin"
version = "0.0.1"
# No run() function — should be caught by validator
```

---

## ✅ Answer Key

<details>
<summary>Click to reveal — attempt everything first!</summary>

### A1 Answers
```
Scenario 1 (run directly):
  __name__ is: __main__
  Running as script!
  Hello from predictor!

Scenario 2 (import predictor):
  __name__ is: predictor
  (no other output — __main__ guard prevents it)

Scenario 3 (from predictor import greet):
  __name__ is: predictor
  (same — the module is still executed on import, just the guard stops the block)
```

### A2 Answers
```
Line 1: True   (same object in sys.modules and the math variable)
Line 2: True   (is checks identity — it's the same object)
Line 3: False  (json not yet imported)
Line 4: True   (json now in sys.modules cache)
```

### A3 Answers
```
Line 1: 1      (alpha is in __all__)
Line 2: 2      (beta is in __all__)
Line 3: NameError — gamma is NOT in __all__, so wildcard import skips it
Line 4: NameError — _delta is private, NOT in __all__

Note: explicit 'from mymodule import gamma' WOULD work — __all__ only restricts wildcard
```

### A4 Answers
```
Line 1: "2.0"
Line 2: <class 'type'>  (Helper is a class)
Line 3: "running"
Line 4: "[hello]"
```

### A5 Answers
```
Case 1: 'os' added to namespace
Case 2: 'getcwd' and 'listdir' added
Case 3: 'os' added (os.path is a submodule — 'os' is the access point)
Case 4: 'path_join' added (the alias)
```

### B1 Answers
```python
__version__ = "1.0.0"
__author__ = "Your Name"
from .operations import StudentManager
from .models import Student
__all__ = ["StudentManager", "Student"]
```

### B2 Answers
```python
from .models import Student
from .utils import letter_grade, validate_name
from . import models
from .. import config
from student_manager.models import Student
```

### B3 Answers
```python
epilog = "Example: ..."
"--name", required=True
type=int
action="store_true"
args = parser.parse_args()
```

### B4 Answers
```bash
python -m venv venv
source venv/bin/activate
venv\Scripts\Activate.ps1
which python
pip install django==4.2
pip install -r requirements.txt
pip freeze > requirements.txt
pip install -e .
deactivate
```

### C1 Fix
```
Bug: Python finds the local 'math.py' first (sys.path[0] is the script's dir)
This shadows the stdlib math module which has math.pi

Fix 1: Rename 'math.py' to 'math_utils.py' or 'my_math.py'

Fix 2 (not recommended):
import sys
sys.path = [p for p in sys.path if p != '']  # remove current dir entry
import math
```

### C2 Fix
```
Why: 'utilities' directory has no __init__.py so Python doesn't treat it as a package

Fix:
touch utilities/__init__.py
```

### C3 Fix
```python
# constants.py
PERMISSION_MAP = {
    "admin": ["read", "write", "delete"],
    "user": ["read"],
}

# permissions.py
from .constants import PERMISSION_MAP

def get_permissions(role: str) -> list:
    return PERMISSION_MAP.get(role, [])

# users.py
from .permissions import get_permissions

class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.permissions = get_permissions(role)
```

### C4 Fix
```
Why: Relative imports require the module to be part of an installed/runnable package.
Running 'python operations.py' directly makes __name__ == "__main__" and there's no
parent package context.

Fix 1: python -m student_manager.operations

Fix 2:
from student_manager.models import Student
from student_manager.utils import validate_name
```

### C5 Fix
```
Most likely: the developer ran 'pip install flask' WITHOUT activating the venv.
Flask was installed into the global Python, but when they run 'python app.py'
inside the venv (or with a different Python), flask isn't there.

Diagnostics:
which python      (or 'where python' on Windows)
which pip
pip show flask

Fix:
source venv/bin/activate    (activate first!)
pip install flask
python app.py
```

### D1 Answer (string_utils.py)
```python
"""String utility functions."""

__version__ = "1.0.0"
__author__ = "Your Name"
__all__ = ["capitalize_words", "truncate", "count_vowels", "is_palindrome"]

def _clean(text: str) -> str:
    """Private: strip whitespace and lowercase."""
    return text.strip().lower()

def capitalize_words(text: str) -> str:
    return " ".join(word.capitalize() for word in text.split())

def truncate(text: str, max_len: int, suffix: str = "...") -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len - len(suffix)] + suffix

def count_vowels(text: str) -> int:
    return sum(1 for c in _clean(text) if c in "aeiou")

def is_palindrome(text: str) -> bool:
    cleaned = "".join(c for c in _clean(text) if c.isalnum())
    return cleaned == cleaned[::-1]

if __name__ == "__main__":
    print(capitalize_words("hello world"))      # Hello World
    print(truncate("Hello, World!", 8))         # Hello...
    print(count_vowels("Hello World"))           # 3
    print(is_palindrome("A man a plan a canal Panama"))  # True
```

</details>

---

## 📊 Self-Assessment Checklist

| Concept | ✅ Got it | 🔄 Need review | ❓ Confused |
|---------|-----------|---------------|------------|
| What `sys.path` is and how it's searched | | | |
| `sys.modules` caching behavior | | | |
| All 5 import styles and when to use each | | | |
| `__all__` — purpose and effect on wildcard imports | | | |
| `__name__ == "__main__"` pattern and why it matters | | | |
| `__init__.py` — what it does and what to put in it | | | |
| Absolute vs relative imports | | | |
| How circular imports occur and 3 ways to fix them | | | |
| Creating and activating a virtual environment | | | |
| `pip freeze > requirements.txt` and `pip install -r` | | | |
| `pip install -e .` editable install | | | |
| Package structure — src layout | | | |
| `pyproject.toml` basics | | | |
| `argparse` for CLI argument parsing | | | |
| `.gitignore` — what to exclude from git | | | |
| Development vs production requirements | | | |

**Score:**
- 16/16 ✅ — Excellent! Ready for Day 5 (File I/O & Error Handling)
- 11–15 ✅ — Good. Focus on import system and virtual env — these are daily tools
- < 11 ✅ — Re-do the guided exercises hands-on; this topic is best learned by doing

---

*Day 4 Exercises Complete — Day 5: File I/O, Exception Handling & Context Managers*
