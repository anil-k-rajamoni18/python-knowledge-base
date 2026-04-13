# 🐍 Python Full Stack — Day 1 of 35
# Topic: Python Basics — Data Types & Variables
**Audience:** Beginners | **Duration:** 3 Hours | **Track:** Python → Django/Flask → Frontend → Deployment

---

## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, learners will be able to:
- Describe how Python source code is executed (CPython pipeline)
- Explain how Python manages memory using the heap, stack, and reference counting
- Distinguish between mutable and immutable data types and predict their behavior
- Understand why Python uses pass-by-object-reference (not pass-by-value)
- Recognize Python's small integer caching and string interning optimizations

### 📋 Prerequisites
- This is **Day 1** — no prior Python knowledge required
- Basic computer literacy (file system, text editor, terminal basics)
- Python 3.10+ installed and accessible via terminal

### 🔗 Connection to the Full Stack Journey
Understanding Python's memory model and data types is the **bedrock** of the entire course:
- **Days 2–5:** Collections (list, dict, set) build directly on mutable/immutable concepts
- **Days 6–10:** Functions and scope rely on pass-by-object-reference
- **Days 20+:** Django ORM models map directly to Python's data type system
- **Debugging:** 80% of beginner bugs come from misunderstanding mutability and references

---

## 2. Concept Explanation

### 2.1 CPython Execution Flow

**The "Why":** When you run a `.py` file, Python doesn't execute raw text. It transforms your code through several stages before your CPU sees it.

**Real-world analogy:** Think of it like a recipe translation process — your English recipe (source code) is translated to a step-by-step chef's shorthand (bytecode) that any kitchen (PVM) can follow, regardless of the original language.

```
Source Code (.py)
      ↓
Lexical Analysis  ← Breaks code into tokens (keywords, symbols, names)
      ↓
AST (Abstract Syntax Tree)  ← Builds a tree structure of your program's logic
      ↓
Bytecode (.pyc)  ← Low-level, platform-independent instructions
      ↓
Python Virtual Machine (PVM)  ← Executes bytecode line by line
```

**Key insight:** The `.pyc` files in `__pycache__/` are the cached bytecode — Python reuses them if the source hasn't changed, making subsequent runs faster.

---

### 2.2 Python Memory Model

**The "Why":** Knowing where data lives helps you predict how your variables behave — especially when passing data to functions.

**Analogy:** 
- The **heap** is a warehouse — objects (your actual data) are stored here
- **Variable names** are sticky labels pointing to boxes in the warehouse
- The **stack** holds the current "task list" (call frames) — which function is running and what labels it knows about

```
Stack (Call Frames)         Heap (Objects)
┌─────────────────┐         ┌────────────────┐
│  Frame: main    │         │  int object: 42│ ← x points here
│   x ──────────────────►   └────────────────┘
│   y ──────────────────►   ┌────────────────┐
└─────────────────┘         │  str: "hello"  │ ← y points here
                            └────────────────┘
```

> **Variables are not boxes — they are labels (references) pointing to objects on the heap.**

---

### 2.3 Reference Counting

**The "Why":** Python needs to automatically free memory so you don't have to do it manually (unlike C/C++).

Every object on the heap has a hidden counter: **how many variable names (references) point to it?**

- When a new name points to an object → counter goes **up**
- When a name is deleted or reassigned → counter goes **down**
- When counter hits **0** → Python immediately frees that memory

```python
import sys
x = [1, 2, 3]       # ref count = 1
y = x               # ref count = 2
del x               # ref count = 1
del y               # ref count = 0 → object destroyed
```

---

### 2.4 Small Integer Caching

**The "Why":** Creating a new integer object for every tiny number would waste memory. Python is smart about it.

Python pre-creates integer objects for values **-5 to 256** and reuses them. For values outside this range, a fresh object is created every time.

```python
a = 100
b = 100
print(a is b)   # True  → same object in memory

a = 1000
b = 1000
print(a is b)   # False → two different objects
```

> **Rule of thumb:** Use `==` to compare values, `is` to check if two names point to the *same object*.

---

### 2.5 String Interning

**The "Why":** Similar to integer caching, Python reuses memory for short, identifier-like strings.

Python automatically interns strings that look like valid Python identifiers (letters, digits, underscores, no spaces). This is an optimization — not a guarantee you should rely on.

```python
a = "hello"
b = "hello"
print(a is b)       # True  → interned

a = "hello world"
b = "hello world"
print(a is b)       # False → spaces prevent interning (implementation-dependent)
```

---

### 2.6 Mutable vs Immutable

**The "Why":** This is arguably the most important concept for avoiding bugs in Python.

| Category   | Types                                     |
|------------|-------------------------------------------|
| Immutable  | `int`, `float`, `str`, `tuple`, `frozenset`, `bytes` |
| Mutable    | `list`, `dict`, `set`, `bytearray`        |

**Analogy:**
- **Immutable** = a laminated card. You can't change it. If you "change" it, you actually get a new card.
- **Mutable** = a whiteboard. You can change what's written on it in-place.

```python
# Immutable — reassignment creates a new object
x = "hello"
x += " world"   # x now points to a BRAND NEW string object

# Mutable — modification changes the SAME object in-place
my_list = [1, 2, 3]
my_list.append(4)   # same object, now contains [1, 2, 3, 4]
```

---

### 2.7 Pass-by-Object-Reference

**The "Why":** Understanding this prevents a massive class of bugs when writing functions.

Python passes the **reference** (the label/pointer) to the function — not a copy of the value, not the variable itself.

- If you pass a **mutable** object and modify it inside the function → the caller sees the change
- If you pass an **immutable** object and "modify" it → the function just gets a new object, original is unchanged

```python
# Mutable — caller sees the change
def add_item(lst):
    lst.append(99)

my_list = [1, 2, 3]
add_item(my_list)
print(my_list)  # [1, 2, 3, 99] ← changed!

# Immutable — caller doesn't see the "change"
def try_change(n):
    n = n + 10

x = 5
try_change(x)
print(x)  # 5 ← unchanged
```

---

## 3. Syntax & Code Examples

### 3.1 Variable Assignment & Type Checking

```python
# Basic assignment — Python infers the type automatically
name = "Alice"          # str
age = 25                # int
height = 5.7            # float
is_student = True       # bool
nothing = None          # NoneType

# Check the type of any variable
print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>

# Check identity (same object in memory)
print(id(age))          # Memory address (e.g., 140234567)
```

**Output:**
```
<class 'str'>
<class 'int'>
140234567891234
```

---

### 3.2 Multiple Assignment Patterns

```python
# Assign multiple variables in one line
x, y, z = 10, 20, 30
print(x, y, z)          # 10 20 30

# Swap without a temp variable (Python magic!)
a, b = 5, 10
a, b = b, a
print(a, b)             # 10 5

# Assign the same value to multiple names
p = q = r = 0
print(p, q, r)          # 0 0 0
```

---

### 3.3 Demonstrating Reference Counting Live

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))  # 2 (x + the getrefcount argument itself)

y = x
print(sys.getrefcount(x))  # 3 (x, y, + argument)

del y
print(sys.getrefcount(x))  # 2 again
```

---

### 3.4 Proving Mutability

```python
# Mutable: list — same id before and after modification
my_list = [1, 2, 3]
print(id(my_list))      # e.g., 4501234567

my_list.append(4)
print(id(my_list))      # SAME id — same object was modified

# Immutable: string — different id after "modification"
my_str = "hello"
print(id(my_str))       # e.g., 4501239999

my_str += " world"
print(id(my_str))       # DIFFERENT id — new object was created
```

---

### 3.5 Integer Caching Deep Dive

```python
# Cached range (-5 to 256) — same object
a = 256
b = 256
print(a is b)           # True
print(id(a) == id(b))   # True

# Outside cached range — different objects
a = 257
b = 257
print(a is b)           # False
print(id(a) == id(b))   # False

# But equality still works!
print(a == b)           # True
```

---

### 3.6 Pass-by-Object-Reference — All Cases

```python
# Case 1: Mutating a mutable object inside function
def append_zero(data):
    data.append(0)
    print("Inside:", id(data))

nums = [1, 2, 3]
print("Outside:", id(nums))
append_zero(nums)
print("After call:", nums)

# Output:
# Outside: 140234567890
# Inside:  140234567890   ← same id!
# After call: [1, 2, 3, 0]

# Case 2: Reassigning inside function does NOT affect caller
def reassign(data):
    data = [99, 100]     # data now points to a NEW list
    print("Inside:", data)

nums = [1, 2, 3]
reassign(nums)
print("After call:", nums)

# Output:
# Inside: [99, 100]
# After call: [1, 2, 3]  ← unchanged
```

---

## 4. Common Mistakes & Gotchas

### ❌ Mistake 1: Using `is` Instead of `==` for Value Comparison

```python
# ❌ Wrong — works by accident for small ints, fails for large ones
x = 1000
y = 1000
if x is y:              # Unpredictable! May be False
    print("equal")

# ✅ Correct — always use == for value comparison
if x == y:
    print("equal")      # Reliable
```
**Why it happens:** Beginners confuse identity (`is`) with equality (`==`). Use `is` only for `None` checks.

---

### ❌ Mistake 2: Mutable Default Argument

```python
# ❌ Wrong — the default list is created ONCE and shared across all calls
def add_item(item, lst=[]):
    lst.append(item)
    return lst

print(add_item(1))      # [1]
print(add_item(2))      # [1, 2]  ← BUG! Expected [2]

# ✅ Correct — use None as default, create fresh list inside
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(add_item(1))      # [1]
print(add_item(2))      # [2]  ← correct
```
**Why it happens:** Default arguments are evaluated at function *definition* time, not call time.

---

### ❌ Mistake 3: Unexpected Aliasing with Mutable Types

```python
# ❌ Wrong — both names point to the SAME list
original = [1, 2, 3]
copy = original         # NOT a copy! Just another label

copy.append(99)
print(original)         # [1, 2, 3, 99] ← unexpected!

# ✅ Correct — create a real copy
copy = original[:]          # Shallow copy via slicing
# or
copy = list(original)       # Shallow copy via constructor
# or
import copy
copy = copy.deepcopy(original)  # Deep copy (for nested structures)
```

---

### ❌ Mistake 4: Confusing `None` with `0` or `False`

```python
# ❌ Wrong — all of these are "falsy" but not None
if not 0:     print("0 is None?")    # Prints — but 0 is not None!
if not "":    print("'' is None?")   # Prints — but "" is not None!
if not []:    print("[] is None?")   # Prints — but [] is not None!

# ✅ Correct — use explicit None check
value = None
if value is None:
    print("Value has not been set")
```

---

### ❌ Mistake 5: Assuming Strings Are Mutable

```python
# ❌ Wrong — strings cannot be changed in place
name = "Alice"
name[0] = "B"           # TypeError: 'str' object does not support item assignment

# ✅ Correct — create a new string
name = "B" + name[1:]   # "Blice"
```

---

## 5. Hands-on Exercises

### 🧑‍🏫 Guided Exercise 1: Exploring the Memory Model

**Goal:** See with your own eyes that variables are references, not boxes.

**Steps:**
1. Create two variables pointing to the same list
2. Print their `id()` — observe they are the same
3. Modify via one name — check the other
4. Reassign one name — check ids again

```python
# Step 1
a = [10, 20, 30]
b = a

# Step 2
print(id(a))    # note the number
print(id(b))    # should be identical

# Step 3
b.append(40)
print(a)        # what do you expect?

# Step 4
b = [1, 2, 3]   # b now points elsewhere
print(id(a))    # a's id unchanged
print(id(b))    # b has a new id
print(a)        # a is unchanged
```

**Discussion questions:**
- Why did `a` change in Step 3?
- Why didn't `a` change in Step 4?

---

### 🧑‍🏫 Guided Exercise 2: Mutable vs Immutable in Functions

**Goal:** Understand when functions affect the caller's data and when they don't.

```python
def modify_list(lst):
    lst.append("added")

def modify_string(s):
    s = s + " modified"
    return s

# Test with list (mutable)
my_list = ["original"]
modify_list(my_list)
print(my_list)          # ["original", "added"] — changed!

# Test with string (immutable)
my_str = "original"
result = modify_string(my_str)
print(my_str)           # "original" — unchanged
print(result)           # "original modified"
```

**Key takeaway:** With immutable types, to "return" changes you must explicitly `return` the new value.

---

### 💻 Independent Practice 1

**Task:** Without running the code, predict the output of each `print`. Then run and verify.

```python
x = 50
y = 50
print(x is y)        # Predict: ?

x = 500
y = 500
print(x is y)        # Predict: ?

a = "python"
b = "python"
print(a is b)        # Predict: ?

c = [1, 2]
d = [1, 2]
print(c is d)        # Predict: ?
print(c == d)        # Predict: ?
```

> **Hint:** Think about integer caching range (-5 to 256) and string interning rules.

---

### 💻 Independent Practice 2

**Task:** Fix the buggy function below so it works correctly for ALL calls.

```python
# Buggy version
def collect_names(name, names=[]):
    names.append(name)
    return names

print(collect_names("Alice"))   # Should be: ['Alice']
print(collect_names("Bob"))     # Should be: ['Bob'] but returns ['Alice', 'Bob']
print(collect_names("Carol"))   # Should be: ['Carol'] but returns ['Alice', 'Bob', 'Carol']
```

> **Hint:** Default mutable arguments are evaluated once at definition time.

---

### 🏆 Challenge Problem

**Task:** Write a function `safe_copy` that:
1. Accepts any variable
2. Returns `"immutable"` if the type is immutable
3. Returns a proper copy (not an alias) if the type is mutable
4. Verify your function using `id()` checks

```python
def safe_copy(obj):
    # Your code here
    pass

# Test cases
print(safe_copy(42))            # "immutable"
print(safe_copy("hello"))       # "immutable"

original_list = [1, 2, 3]
copied_list = safe_copy(original_list)
print(copied_list)              # [1, 2, 3]
print(original_list is copied_list)  # False — must be a real copy!
```

---

## 6. Best Practices & Industry Standards

### PEP 8 Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Variables | `snake_case` | `user_name`, `total_count` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_SIZE`, `API_KEY` |
| Private variables | `_leading_underscore` | `_internal_state` |
| "Magic" / dunder | `__double_underscore__` | `__init__`, `__str__` |

```python
# ❌ Bad naming
a = "John"
MyVar = 42
USERLIST = []

# ✅ Good naming
user_name = "John"
retry_count = 42
user_list = []
MAX_RETRIES = 5          # constant
```

### Type Hints (Modern Python 3.6+)

```python
# Add type hints for clarity and IDE support
def greet(name: str) -> str:
    return f"Hello, {name}"

age: int = 25
scores: list[int] = [90, 85, 92]
```

### None Checks — Always Use `is`

```python
# ✅ Industry standard
if value is None:
    ...

if value is not None:
    ...
```

### Avoid Shadowing Built-in Names

```python
# ❌ Never name variables these
list = [1, 2, 3]    # shadows built-in list()
str = "hello"       # shadows built-in str()
id = 42             # shadows built-in id()

# ✅ Add context to the name
user_list = [1, 2, 3]
user_str = "hello"
user_id = 42
```

---

## 7. Real-World Application

### Where These Concepts Appear in Full Stack Projects

**Django Models (Day 20+):** Every Django model field maps to a Python type
```python
# models.py — Django
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150)  # str → immutable
    age = models.IntegerField()                  # int → immutable
    tags = models.JSONField(default=list)        # list → mutable, use callable default!
    # Note: default=list (not default=[]) — avoids mutable default argument bug!
```

**API Response Handling (Flask/Django REST):**
```python
# Mutable dict is built up and returned as JSON
def build_response(user_data: dict) -> dict:
    response = {}           # mutable — we'll add to it
    response["id"] = user_data["id"]
    response["name"] = user_data["name"]
    response["status"] = "active"
    return response         # reference passed back efficiently
```

**Configuration Constants (any project):**
```python
# config.py
DATABASE_URL = "postgresql://localhost/mydb"    # str — immutable, safe to share
MAX_CONNECTIONS = 10                            # int — immutable, safe to share
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]     # list — mutable, don't share across threads without care
```

### 🔭 Connection to Upcoming Days
- **Day 2:** Lists, Tuples, Dicts, Sets — all built on today's mutable/immutable foundation
- **Day 3:** Strings in depth — immutability, formatting, slicing
- **Day 4:** Functions — pass-by-object-reference becomes critical when writing reusable functions

---

## 8. Quick Revision Summary

### Key Terms

| Term | One-line Definition |
|------|---------------------|
| CPython | The reference Python implementation written in C |
| AST | Tree representation of your code's logical structure |
| Bytecode | Platform-independent intermediate code stored in `.pyc` |
| PVM | The engine that executes Python bytecode |
| Heap | Memory region where Python objects live |
| Stack | Memory region for call frames (active function contexts) |
| Reference | A name/pointer that points to an object on the heap |
| Reference Counting | Tracking how many names point to an object; free when count = 0 |
| Immutable | Object whose value cannot change after creation |
| Mutable | Object that can be modified in-place |
| Interning | Reusing the same object for identical small strings/integers |
| Pass-by-object-reference | Python passes the reference to the object, not a copy |

---

### Core Syntax Cheat Sheet

```python
# Assignment
x = 42
name = "Alice"
values = [1, 2, 3]

# Type checking
type(x)             # <class 'int'>
isinstance(x, int)  # True

# Identity vs equality
x is y              # same object?
x == y              # same value?

# Reference count
import sys
sys.getrefcount(x)  # number of references

# Object id (memory address)
id(x)               # e.g. 140234567890

# Copying a list (shallow)
copy = original[:]
copy = list(original)

# Type hints
age: int = 25
name: str = "Alice"
```

---

### 5 MCQ Recap Questions

**Q1.** What does Python use to automatically manage memory?
- A) Manual `free()` calls
- B) Garbage collection only
- **C) Reference counting (+ cyclic GC for cycles)** ✅
- D) Stack-based allocation

**Q2.** Which of the following is **immutable**?
- A) `list`
- B) `dict`
- **C) `tuple`** ✅
- D) `set`

**Q3.** What will `a is b` return if `a = 300` and `b = 300`?
- **A) `False` — integers above 256 are not cached** ✅
- B) `True` — all integers are cached
- C) Depends on the OS
- D) `TypeError`

**Q4.** You pass a list to a function and the function calls `.append()` on it. After the function returns, the original list...
- A) Is unchanged — Python copies lists on pass
- **B) Is changed — both the caller and function reference the same object** ✅
- C) Is deleted from memory
- D) Raises a TypeError

**Q5.** What is the correct way to check if a variable holds `None`?
- A) `if x == None:`
- **B) `if x is None:`** ✅
- C) `if x = None:`
- D) `if type(x) == "NoneType":`

---

## 9. Instructor Notes

### 📌 Anticipated Student Questions

| Question | Suggested Answer |
|----------|-----------------|
| "Why does `is` sometimes work for small ints but not big ones?" | CPython caches -5 to 256 as an optimization. Always use `==` for value comparisons. |
| "Is Python slow because of bytecode?" | Bytecode is already much faster than re-parsing. For speed-critical tasks, use NumPy, Cython, or C extensions. |
| "What's the difference between shallow and deep copy?" | Shallow copy copies the container but not nested objects. Deep copy copies everything recursively. Show with nested lists. |
| "Why does Python allow mutable default arguments if they cause bugs?" | Historical design decision. Python 3 type hints + linters (pylint, mypy) now catch this. |
| "What is `__pycache__`?" | Folder Python creates to store compiled bytecode (`.pyc` files) so it doesn't reparse source every run. |

---

### 🖊️ Whiteboard Diagrams to Draw

1. **CPython Pipeline:** Draw boxes: `.py` → Lexer → AST → `.pyc` → PVM → Output
2. **Heap vs Stack:** Two columns — stack with function frames on the left, heap with objects on the right, arrows from stack labels to heap objects
3. **Reference Counting:** Draw an object box with a counter; add arrows for each reference; erase arrows and decrement; show box disappearing at 0
4. **Mutable vs Immutable:** Two boxes — one showing a list with same `id` before/after append; one showing a string with different `id` after concatenation
5. **Pass-by-object-reference:** Draw a function frame receiving a copy of the *arrow* (not the box) pointing to the same heap object

---

### ⏱️ Timing Guide (3 Hours)

| Time | Activity |
|------|----------|
| 0:00 – 0:10 | Welcome, course overview, setup check |
| 0:10 – 0:30 | CPython execution flow + whiteboard diagram |
| 0:30 – 0:50 | Memory model: heap, stack, references + live demo with `id()` |
| 0:50 – 1:10 | Reference counting + `sys.getrefcount()` demo |
| 1:10 – 1:20 | ☕ Break |
| 1:20 – 1:40 | Mutable vs Immutable — code examples + whiteboard |
| 1:40 – 2:00 | Small integer caching + string interning demos |
| 2:00 – 2:20 | Pass-by-object-reference — all four cases in code |
| 2:20 – 2:35 | Common mistakes + gotchas walkthrough |
| 2:35 – 2:50 | Guided exercises 1 & 2 (instructor-led) |
| 2:50 – 3:00 | MCQ recap, Q&A, preview of Day 2 |

> 💡 **Tip:** Independent practice and challenge problem are best assigned as take-home after class.

---

### 📚 Resources & Further Reading

- [Python Official Docs — Data Model](https://docs.python.org/3/reference/datamodel.html)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Python Memory Management (Real Python)](https://realpython.com/python-memory-management/)
- [Ned Batchelder — Facts and Myths about Python names and values](https://nedbatchelder.com/text/names.html) ← highly recommended
- [Python Tutor — Visualize code execution](https://pythontutor.com/) ← great for showing heap/stack live in class