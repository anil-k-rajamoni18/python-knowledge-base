# 🐍 Python — Day 1 Notes
---

## Table of Contents

1. [What is Python?](#1-what-is-python)
2. [How Python Code Works Under the Hood](#2-how-python-code-works-under-the-hood)
3. [Python Installation & IDE Setup](#3-python-installation--ide-setup)
4. [Variables & Data Types](#4-variables--data-types)
5. [Memory Internals — Reference Counting & Small Integer Caching](#5-memory-internals--reference-counting--small-integer-caching)
6. [Input & Output Functions (Deep Dive)](#6-input--output-functions-deep-dive)
7. [Operators & Expressions (Deep Dive)](#7-operators--expressions-deep-dive)
8. [String Introduction (Deep Dive)](#8-string-introduction-deep-dive)
9. [Collection / Sequence Types Basics](#9-collection--sequence-types-basics)
10. [Built-in Functions (Complete Reference)](#10-built-in-functions-complete-reference)
11. [Hands-On Exercises](#11-hands-on-exercises)
12. [Mini Project — Personal Info CLI App](#12-mini-project--personal-info-cli-app)

---

## 1. What is Python?

Python is a high-level, interpreted, dynamically typed programming language. Guido van Rossum created it in 1991 with one core philosophy: code should be readable, almost like English.

**Key characteristics:**

- Interpreted — runs line by line, no separate compile step
- Dynamically typed — no need to declare variable types
- Garbage collected — memory is managed automatically
- Multi-paradigm — supports OOP, functional, and procedural styles

**Real-World Use Cases:**

| Domain | Companies | Usage |
|--------|-----------|-------|
| AI / ML | OpenAI, Google, Meta | Model training, LLM pipelines |
| Web Backend | Instagram, Dropbox | REST APIs, microservices |
| Automation | Netflix, Uber | System scripting, workflows |
| DevOps | AWS, Azure | Infrastructure tools, CLIs |
| Data | NASA, CERN | Analysis and visualization |

---

## 2. How Python Code Works Under the Hood

This is the part most tutorials skip. Understanding this makes you a better debugger and a much stronger candidate in interviews.

### 2.1 The Execution Pipeline

When you write `python app.py` and press Enter, Python does not directly run your code as-is. It goes through multiple stages:

```
Your Source Code (.py)
        │
        ▼
  [Lexer / Tokenizer]
  Breaks code into tokens
  e.g. name, =, "John", print, (, )
        │
        ▼
  [Parser / AST Builder]
  Builds an Abstract Syntax Tree (AST)
  — a tree representing the structure
        │
        ▼
  [Compiler]
  Converts AST → Bytecode (.pyc)
  Stored in __pycache__/
        │
        ▼
  [Python Virtual Machine (PVM)]
  Executes bytecode instruction by instruction
        │
        ▼
     OUTPUT
```

Think of bytecode as a middle ground — it's not machine code (like C produces), but it's not source code either. It's Python's own compact instruction format that the PVM understands.

### 2.2 What is CPython?

When you download Python from python.org, you're downloading **CPython** — the reference implementation of Python, written in C. There are other implementations too:

| Implementation | Written In | Use Case |
|----------------|------------|----------|
| CPython | C | Default, most widely used |
| PyPy | Python/RPython | Faster execution via JIT |
| Jython | Java | Runs on JVM |
| IronPython | C# | Runs on .NET |

> **Observation:** Most production systems use CPython. PyPy is chosen when raw performance matters (e.g., heavy numerical loops).

### 2.3 The `.pyc` File and `__pycache__`

Every time Python compiles your source file, it saves the bytecode in a `__pycache__` directory:

```
myproject/
├── app.py
└── __pycache__/
    └── app.cpython-311.pyc
```

The `.pyc` file includes a timestamp and magic number. If the source hasn't changed, Python skips recompilation — making subsequent runs faster.

> **Real-world note:** You never commit `__pycache__` to Git. Always add it to `.gitignore`.

### 2.4 How the Python Virtual Machine (PVM) Works

The PVM is a **stack-based machine**. It maintains an evaluation stack and processes bytecode operations one at a time.

You can actually peek at the bytecode Python generates:

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

Output (simplified):
```
  2           0 LOAD_FAST    0 (a)
              2 LOAD_FAST    1 (b)
              4 BINARY_ADD
              6 RETURN_VALUE
```

Each line is one bytecode instruction the PVM executes. The PVM pushes `a` and `b` onto the stack, pops them, adds them, and returns the result.

### 2.5 The GIL — Global Interpreter Lock

The GIL is a mutex (lock) in CPython that allows only **one thread to execute Python bytecode at a time**, even on multi-core systems.

```
Thread 1 ──►  GIL acquired  ──► executes Python code
Thread 2 ──►  waiting ...
Thread 1 ──►  GIL released
Thread 2 ──►  GIL acquired  ──► executes Python code
```

This is why Python multithreading doesn't give true parallelism for CPU-bound tasks. For CPU-heavy work, use `multiprocessing` instead. For I/O-heavy work (network, disk), threading works fine because the GIL is released during I/O waits.

> **Interview tip:** "Why is Python slow for CPU-bound parallelism?" → The GIL. Solution → `multiprocessing` or use PyPy.

---

## 3. Python Installation & IDE Setup

### Installation Steps

1. Download from [python.org](https://python.org)
2. Check **"Add Python to PATH"** during installation (critical step!)
3. Verify:

```bash
python --version
pip --version
```

### IDE Comparison

| Feature | VS Code | PyCharm |
|---------|---------|---------|
| Weight | Lightweight | Heavy |
| Best for | Scripts, APIs, DevOps | Large OOP projects |
| Extensions | Python, Pylance, GitLens | Built-in everything |
| Cost | Free | Free (Community) / Paid (Pro) |

### Best Practice — Always Use Virtual Environments

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate.bat       # Windows
```

Never install packages globally for a project. It causes version conflicts across projects — a lesson most developers learn the hard way.

---

## 4. Variables & Data Types

### 4.1 What is a Variable?

A variable is a name that points to an object in memory. In Python, variables don't store values — they store **references** to objects. This distinction becomes important when understanding mutability and aliasing.

```python
age = 25        # 'age' points to the integer object 25
name = "John"   # 'name' points to the string object "John"
```

Think of it like a sticky label on a box. The label is the variable name; the box is the object in memory.

### 4.2 Naming Rules

```
✅ Valid                ❌ Invalid
----------             ----------
user_name              2user       (starts with digit)
userName               user-name   (hyphen not allowed)
_internal              user name   (space not allowed)
User1                  class       (reserved keyword)
```

> **Convention:** Python uses `snake_case` for variables and functions. `CamelCase` is for class names.

### 4.3 Data Types

```
Python Data Types
│
├── Numeric
│   ├── int        → 10, -5, 1000000
│   ├── float      → 3.14, -0.001
│   └── complex    → 3+4j
│
├── Text
│   └── str        → "hello", 'world'
│
├── Boolean
│   └── bool       → True, False
│
├── None
│   └── NoneType   → None
│
└── Collections (covered later)
    ├── list
    ├── tuple
    ├── dict
    └── set
```

**Industry use cases by type:**

| Type | Real-World Use |
|------|---------------|
| `int` | User IDs, order counts, ML label encoding |
| `float` | Model accuracy, sensor readings, prices |
| `str` | Log messages, API responses, LLM prompts |
| `bool` | Feature flags, auth checks, pipeline switches |
| `None` | Missing DB fields, optional function returns |

### 4.4 Dynamic Typing

Python figures out the type at runtime, not at compile time:

```python
x = 10       # x is int
x = "hello"  # now x is str — Python is fine with this
x = [1, 2]   # now x is list
```

This is called **dynamic typing**. The variable is just a label; it can point to anything.

> **Observation:** This is different from Java/C++ where `int x = 10` locks `x` as an integer forever.

### 4.5 Type Checking

```python
type(42)           # <class 'int'>
type("hello")      # <class 'str'>
isinstance(42, int)  # True — preferred in production code
```

---

## 5. Memory Internals — Reference Counting & Small Integer Caching

This section covers Python's memory model. It's the kind of knowledge that separates someone who uses Python from someone who truly understands it.

### 5.1 Everything is an Object

In Python, **everything** — integers, strings, functions, classes — is an object. Each object has:

- A **type** (what kind of object it is)
- A **value** (the data it holds)
- A **reference count** (how many names point to it)

### 5.2 Reference Counting

Python's garbage collector uses reference counting as its primary mechanism. Every object tracks how many variables are pointing to it.

```python
a = [1, 2, 3]   # list object created, ref count = 1
b = a            # b also points to same list, ref count = 2
del a            # ref count drops to 1
del b            # ref count drops to 0 → object destroyed
```

Diagram:
```
a ──────────────────►  [1, 2, 3]  (ref count = 2)
b ──────────────────►  (same object)

After del a:
b ──────────────────►  [1, 2, 3]  (ref count = 1)

After del b:
                       [1, 2, 3]  (ref count = 0) → 🗑️ GARBAGE COLLECTED
```

You can check reference count using:
```python
import sys
x = [1, 2, 3]
sys.getrefcount(x)   # usually returns count + 1 (function arg also counts)
```

### 5.3 The `id()` Function — Memory Addresses

`id()` returns the memory address of an object:

```python
a = "hello"
b = "hello"
print(id(a))   # e.g. 140234567890
print(id(b))   # same address! Python reuses string objects
```

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(id(a))   # different address
print(id(b))   # different address — lists are NOT cached
```

### 5.4 Small Integer Caching

Python pre-creates and caches integer objects in the range **-5 to 256**. This means every time you use the number `100` anywhere in your program, Python reuses the same object rather than creating a new one.

```python
a = 100
b = 100
print(a is b)   # True — same object in memory

a = 1000
b = 1000
print(a is b)   # False — outside cache range, two different objects
```

Diagram:
```
Python starts up and creates:
┌──────────────────────────────────────┐
│  Integer Cache: -5 to 256            │
│  [-5] [-4] ... [0] [1] ... [256]    │
└──────────────────────────────────────┘

a = 100  ──► points to cached object at index 100
b = 100  ──► points to SAME cached object
a is b   ──► True

a = 1000 ──► new object created on heap
b = 1000 ──► another new object created on heap
a is b   ──► False
```

> **Interview trap:** People often confuse `==` (value equality) with `is` (identity/same object). Always use `==` to compare values. Use `is` only for `None` checks (`if x is None:`).

### 5.5 String Interning

Similar to integer caching, Python also interns (reuses) short strings that look like valid identifiers:

```python
a = "hello"
b = "hello"
print(a is b)   # True — interned

a = "hello world"
b = "hello world"
print(a is b)   # May be False — spaces prevent automatic interning
```

You can force interning manually with `sys.intern()`, though this is rarely needed.

### 5.6 Mutable vs Immutable Objects

This is one of the most important concepts in Python memory management.

| Immutable | Mutable |
|-----------|---------|
| int, float, str, tuple, bool | list, dict, set |
| Cannot change after creation | Can be modified in place |
| Multiple variables can safely share | Sharing can cause unexpected side effects |

```python
# Immutable — strings
a = "hello"
b = a
a = "world"     # creates a NEW string object; b still points to "hello"
print(b)        # "hello" — b is unaffected

# Mutable — lists
x = [1, 2, 3]
y = x           # y points to SAME list
x.append(4)
print(y)        # [1, 2, 3, 4] — y is affected! same object was modified
```

> **Real-world impact:** This aliasing behavior with mutable objects causes bugs in function arguments. If you pass a list to a function and modify it inside, the original is changed. Use `.copy()` or `list()` to avoid this.

### 5.7 Cyclic Garbage Collection

Reference counting alone has a problem: **circular references**.

```python
a = {}
b = {}
a['other'] = b
b['other'] = a
# a and b point to each other — ref count never hits 0
# Python's cyclic garbage collector handles this separately
```

Python's `gc` module has a cyclic garbage collector running in the background to catch these cases. You can interact with it via `import gc`.

---

## 6. Input & Output Functions (Deep Dive)

### 6.1 The `print()` Function — Full Breakdown

Most people use `print()` as a basic debug tool. It's actually quite powerful.

**Signature:**
```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

**Parameters explained:**

```python
# Default behavior
print("Hello", "World")          # Hello World

# Custom separator
print("2026", "05", "11", sep="-")  # 2026-05-11

# Custom end (no newline)
print("Loading", end="...")       # Loading...

# Multiple arguments
print("Name:", "John", "Age:", 25)  # Name: John Age: 25
```

**Writing to a file:**
```python
with open("log.txt", "w") as f:
    print("Error: timeout", file=f)
```

**Flush — important for real-time logging:**
```python
import time
print("Processing...", end="", flush=True)
time.sleep(2)
print(" Done!")
```

Without `flush=True`, the output might not appear until the buffer is full. In Docker containers or CI/CD pipelines, always use `flush=True` or set `PYTHONUNBUFFERED=1`.

**Real-world use — structured log output:**
```python
import datetime
level = "INFO"
message = "User login successful"
timestamp = datetime.datetime.now().isoformat()
print(f"[{timestamp}] [{level}] {message}")
# [2026-05-11T10:30:00] [INFO] User login successful
```

### 6.2 f-Strings — The Modern Way (Python 3.6+)

f-strings are the fastest and most readable way to format strings. Don't use `%` formatting or `.format()` in new code.

```python
name = "Anil"
score = 98.567

# Basic
print(f"Name: {name}")

# Expression inside
print(f"Score: {score:.2f}")          # Score: 98.57

# Arithmetic inline
print(f"Double: {score * 2}")         # Double: 197.134

# Conditionals inline
print(f"Status: {'Pass' if score > 50 else 'Fail'}")

# Dict access
user = {"name": "Anil", "role": "admin"}
print(f"User: {user['name']}, Role: {user['role']}")
```

> **Python 3.12+ feature:** f-strings now support even more complex expressions, including multi-line and nested quotes without escaping.

### 6.3 The `input()` Function — Full Breakdown

`input()` always returns a string. This is the single most common source of bugs for beginners.

```python
x = input("Enter a number: ")
print(type(x))    # <class 'str'> — always str, no matter what you type
```

**Type conversion patterns:**

```python
age = int(input("Enter age: "))
price = float(input("Enter price: "))
is_active = input("Active? (yes/no): ").strip().lower() == "yes"
```

**Safe input with validation:**

```python
while True:
    try:
        age = int(input("Enter age: "))
        if age < 0 or age > 120:
            print("Please enter a realistic age.")
            continue
        break
    except ValueError:
        print("That's not a valid number. Try again.")

print(f"Age recorded: {age}")
```

**Real-world equivalent:** This pattern mirrors form validation in web frameworks — reject bad input early, before it reaches your database or business logic.

**Taking multiple inputs on one line:**

```python
# User types: 10 20 30
values = input("Enter numbers: ").split()   # ['10', '20', '30']
numbers = list(map(int, values))            # [10, 20, 30]

# Or even more Pythonic:
a, b, c = map(int, input("Enter three numbers: ").split())
```

### 6.4 Output Formatting Comparison

| Method | Style | Recommended? |
|--------|-------|--------------|
| `"Hello " + name` | Concatenation | No — slow and ugly |
| `"Hello %s" % name` | % formatting | No — legacy |
| `"Hello {}".format(name)` | .format() | Okay, but verbose |
| `f"Hello {name}"` | f-string | Yes — modern standard |

---

## 7. Operators & Expressions (Deep Dive)

### 7.1 Arithmetic Operators

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `10 - 4` | `6` |
| `*` | Multiplication | `3 * 4` | `12` |
| `/` | Division | `10 / 3` | `3.333...` |
| `//` | Floor Division | `10 // 3` | `3` |
| `%` | Modulus | `10 % 3` | `1` |
| `**` | Exponentiation | `2 ** 10` | `1024` |

> **Observation:** `/` always returns a float in Python 3, even if the result is a whole number (`4/2 = 2.0`). Use `//` when you need integer division.

**Real-world — E-commerce discount:**
```python
price = 4999
discount_percent = 18
discount_amount = price * discount_percent / 100
final_price = price - discount_amount
gst = final_price * 0.18
total = final_price + gst
print(f"Final: ₹{total:.2f}")
```

**Real-world — Pagination logic:**
```python
total_records = 157
per_page = 10
total_pages = (total_records + per_page - 1) // per_page
# or equivalently:
import math
total_pages = math.ceil(total_records / per_page)
print(f"Total pages: {total_pages}")   # 16
```

**Real-world — Checking even/odd (modulus):**
```python
def is_even(n):
    return n % 2 == 0

# Used in zebra striping of table rows, round-robin task assignment, etc.
```

### 7.2 Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `a == b` |
| `!=` | Not equal | `a != b` |
| `>` | Greater than | `a > b` |
| `<` | Less than | `a < b` |
| `>=` | Greater or equal | `a >= b` |
| `<=` | Less or equal | `a <= b` |

**Chaining comparisons — a Python superpower:**
```python
# Most languages require two conditions:
if 0 <= age and age <= 120:

# Python lets you chain naturally:
if 0 <= age <= 120:
    print("Valid age")
```

**Real-world — API rate limit check:**
```python
requests_this_minute = 58
limit = 60
if requests_this_minute >= limit:
    print("Rate limit reached. Throttling...")
```

### 7.3 Logical Operators

| Operator | Meaning | Short-circuits? |
|----------|---------|----------------|
| `and` | Both must be True | Yes — stops at first False |
| `or` | At least one True | Yes — stops at first True |
| `not` | Inverts truth value | No |

**Short-circuit evaluation — important for performance and safety:**
```python
# If 'user' is None, user.is_admin would crash
# Short-circuit prevents the crash:
if user is not None and user.is_admin:
    grant_access()

# Or pattern — default fallback:
display_name = user_input or "Anonymous"
```

**Real-world — Role-based access:**
```python
is_logged_in = True
is_admin = False
is_manager = True

if is_logged_in and (is_admin or is_manager):
    print("Access granted to dashboard")
```

### 7.4 Assignment Operators

```python
x = 10
x += 5    # x = x + 5  → 15
x -= 3    # x = x - 3  → 12
x *= 2    # x = x * 2  → 24
x //= 5   # x = x // 5 → 4
x **= 3   # x = x ** 3 → 64
x %= 10   # x = x % 10 → 4
```

### 7.5 Bitwise Operators (Brief Introduction)

Used in low-level programming, flags, permissions:

| Operator | Name | Example |
|----------|------|---------|
| `&` | AND | `5 & 3 = 1` |
| `\|` | OR | `5 \| 3 = 7` |
| `^` | XOR | `5 ^ 3 = 6` |
| `~` | NOT | `~5 = -6` |
| `<<` | Left shift | `2 << 3 = 16` |
| `>>` | Right shift | `16 >> 2 = 4` |

**Real-world — Unix file permissions:**
```python
READ    = 0b100   # 4
WRITE   = 0b010   # 2
EXECUTE = 0b001   # 1

# User has read + write:
user_perm = READ | WRITE   # 0b110 = 6

# Check if user can read:
if user_perm & READ:
    print("Can read")
```

### 7.6 Identity and Membership Operators

```python
# Identity — checks if same object in memory
a is b        # True if same object
a is not b    # True if different objects

# Membership — checks if value exists in a collection
"a" in "apple"           # True
3 in [1, 2, 3]           # True
"admin" not in user_roles  # True if not in list
```

**Real-world — feature flag check:**
```python
allowed_roles = ["admin", "manager", "hr"]
user_role = "admin"

if user_role in allowed_roles:
    print("Access granted")
```

### 7.7 Operator Precedence (PEMDAS for Python)

```
Highest to Lowest:
  **               (Exponentiation)
  ~, +, -          (Unary)
  *, /, //, %      (Multiplication family)
  +, -             (Addition family)
  <<, >>           (Bit shifts)
  &                (Bitwise AND)
  ^                (Bitwise XOR)
  |                (Bitwise OR)
  ==, !=, <, >, <=, >=, is, in  (Comparisons)
  not              (Logical NOT)
  and              (Logical AND)
  or               (Logical OR)
```

When in doubt, use parentheses. Explicit is always better than relying on precedence rules.

---

## 8. String Introduction (Deep Dive)

Strings are probably the most used data type in any real application — API responses, logs, user input, file paths, database queries. Understanding them well pays off immediately.

### 8.1 String Creation

```python
# Single or double quotes — no difference
name = 'Anil'
name = "Anil"

# Triple quotes — for multi-line strings
address = """
123 MG Road,
Hyderabad, Telangana
500001
"""

# Raw strings — backslashes are not treated as escape characters
# Used for file paths and regex patterns
path = r"C:\Users\Anil\Documents"
regex = r"\d{3}-\d{4}"
```

### 8.2 String Indexing

Strings in Python are sequences. Every character has a position (index) starting from 0.

```
  P   y   t   h   o   n
  0   1   2   3   4   5    (positive indexing)
 -6  -5  -4  -3  -2  -1   (negative indexing)
```

```python
text = "Python"
print(text[0])    # P
print(text[-1])   # n  (last character)
print(text[2])    # t
```

> **Observation:** Negative indexing is very handy for accessing elements from the end. `text[-1]` is much cleaner than `text[len(text)-1]`.

### 8.3 String Slicing

Slicing lets you extract a portion of a string. The syntax is `[start:stop:step]`. The stop index is **exclusive** (not included).

```python
text = "Python Programming"

text[0:6]      # "Python"     — chars at 0,1,2,3,4,5
text[7:]       # "Programming" — from index 7 to end
text[:6]       # "Python"     — from beginning to 5
text[::2]      # "Pto rgamn"  — every second character
text[::-1]     # "gnimmargorP nohtyP" — reversed string
```

**Real-world — parsing log timestamps:**
```python
log_line = "2026-05-11T10:30:00 ERROR timeout"
date = log_line[:10]       # "2026-05-11"
time = log_line[11:19]     # "10:30:00"
message = log_line[20:]    # "ERROR timeout"
```

### 8.4 String Immutability

Strings are immutable in Python. You cannot change a character in place:

```python
text = "hello"
text[0] = "H"   # ❌ TypeError: 'str' object does not support item assignment

# Instead, create a new string:
text = "H" + text[1:]   # "Hello"
```

This is why string operations always return new strings.

### 8.5 Essential String Methods

```python
text = "  Hello, World!  "

# Case
text.lower()          # "  hello, world!  "
text.upper()          # "  HELLO, WORLD!  "
text.title()          # "  Hello, World!  "
text.swapcase()       # "  hELLO, wORLD!  "

# Whitespace
text.strip()          # "Hello, World!"  (both sides)
text.lstrip()         # "Hello, World!  " (left only)
text.rstrip()         # "  Hello, World!" (right only)

# Search
text.find("World")    # 8  (returns index, or -1 if not found)
text.count("l")       # 3
text.startswith("  H")  # True
text.endswith("!  ")    # True

# Replace
text.replace("World", "Python")   # "  Hello, Python!  "

# Split and Join
"a,b,c,d".split(",")         # ['a', 'b', 'c', 'd']
",".join(["a", "b", "c"])    # "a,b,c"

# Check content
"12345".isdigit()    # True
"hello".isalpha()    # True
"hello123".isalnum() # True
"  ".isspace()       # True
```

**Real-world — parsing CSV-like data:**
```python
line = "Anil,Rajamoni,Hyderabad,Python Developer"
fields = line.split(",")
first_name, last_name, city, role = fields
print(f"{first_name} works as {role} in {city}")
```

**Real-world — URL slug generation:**
```python
title = "  How to Build REST APIs with FastAPI  "
slug = title.strip().lower().replace(" ", "-")
# "how-to-build-rest-apis-with-fastapi"
```

### 8.6 String Formatting — All Methods Compared

```python
name = "Anil"
score = 98.5

# Old way — C-style (avoid in new code)
print("Name: %s, Score: %.1f" % (name, score))

# .format() — still used, but verbose
print("Name: {}, Score: {:.1f}".format(name, score))

# f-strings — modern, fast, readable (use this)
print(f"Name: {name}, Score: {score:.1f}")
```

**f-string format specifiers:**
```python
pi = 3.14159265

f"{pi:.2f}"        # 3.14       — 2 decimal places
f"{pi:10.3f}"      # "     3.142" — width 10, right-aligned
f"{pi:<10.3f}"     # "3.142     " — left-aligned
f"{1000000:,}"     # "1,000,000" — comma separator
f"{0.875:.0%}"     # "88%"       — percentage
f"{255:#x}"        # "0xff"      — hex with prefix
f"{42:05d}"        # "00042"     — zero-padded
```

### 8.7 Multiline Strings and Docstrings

```python
# Multiline string
query = """
    SELECT user_id, name, email
    FROM users
    WHERE is_active = TRUE
    ORDER BY created_at DESC
    LIMIT 100;
"""

# Docstring (first string in a function/class) — used by help() and IDEs
def calculate_gst(amount, rate=0.18):
    """
    Calculate GST for a given amount.

    Args:
        amount: The base price
        rate: GST rate (default 18%)

    Returns:
        The GST amount as float
    """
    return amount * rate
```

### 8.8 String Concatenation vs Join — Performance

```python
# ❌ Avoid in loops — creates a new string object every iteration
result = ""
for word in words:
    result += word + " "

# ✅ Use join — much faster, single allocation
result = " ".join(words)
```

> **Why?** Strings are immutable. `+=` creates a brand new string object every time. `join()` pre-calculates the total length and allocates once.

---

## 9. Collection / Sequence Types Basics

Python has four main built-in collection types. Each serves a specific purpose. Picking the wrong one is a common source of subtle bugs.

### 9.1 Overview

```
Collection Types
│
├── list   — ordered, mutable, allows duplicates
│            [1, 2, 3, "hello", True]
│
├── tuple  — ordered, immutable, allows duplicates
│            (1, 2, 3, "hello")
│
├── dict   — key-value pairs, ordered (Python 3.7+), mutable
│            {"name": "Anil", "age": 28}
│
└── set    — unordered, mutable, NO duplicates
             {1, 2, 3, 4}
```

### 9.2 List — The Workhorse

Lists are your go-to ordered collection when you need to store, iterate, or modify a sequence of items.

```python
# Creation
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True, None]
nested = [[1, 2], [3, 4], [5, 6]]

# Access
fruits[0]      # "apple"
fruits[-1]     # "cherry"
fruits[1:3]    # ["banana", "cherry"]

# Modify
fruits.append("date")          # add to end
fruits.insert(1, "avocado")    # insert at index 1
fruits.extend(["elderberry"])  # add multiple items
fruits.remove("banana")        # remove by value
popped = fruits.pop()          # remove and return last item
fruits.pop(0)                  # remove at index

# Query
len(fruits)
"apple" in fruits
fruits.index("cherry")   # returns index
fruits.count("apple")    # how many times it appears

# Sort
fruits.sort()             # in-place sort
sorted_fruits = sorted(fruits)   # returns new sorted list
fruits.sort(reverse=True)

# Copy (important!)
copy1 = fruits.copy()          # shallow copy
copy2 = fruits[:]              # also shallow copy
import copy
deep = copy.deepcopy(nested)   # deep copy — for nested structures
```

**Real-world — storing API response items:**
```python
users = []
for record in db_result:
    users.append({
        "id": record.id,
        "name": record.name,
        "email": record.email
    })
```

**List comprehension — the Python way:**
```python
# Traditional loop
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension — more Pythonic
squares = [x ** 2 for x in range(10)]

# With filter
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
```

### 9.3 Tuple — Immutable Sequence

Tuples are like lists, but they cannot be changed after creation. Use them when the data should not be modified.

```python
# Creation
point = (10, 20)
rgb = (255, 128, 0)
single = (42,)    # comma is required for single-element tuple!
empty = ()

# Access — same as list
point[0]    # 10
point[-1]   # 20

# Unpacking — very common in Python
x, y = point
r, g, b = rgb

# Swap variables using tuple packing/unpacking
a, b = 10, 20
a, b = b, a   # swap — no temp variable needed
```

**When to use tuple over list:**
- Function returning multiple values
- Dictionary keys (lists can't be dict keys)
- Data that shouldn't change (coordinates, RGB values, DB records)
- Slightly faster than list for iteration

```python
# Function returning multiple values (returns a tuple)
def get_min_max(data):
    return min(data), max(data)

low, high = get_min_max([5, 3, 8, 1, 9])
```

**Named tuples — more readable:**
```python
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(p.x, p.y)   # 10 20 — readable attribute access
```

### 9.4 Dictionary — Key-Value Store

Dictionaries are Python's most powerful built-in data structure. They underlie many Python internals (including the way objects work).

```python
# Creation
user = {
    "name": "Anil",
    "age": 28,
    "city": "Hyderabad",
    "is_active": True
}

# Access
user["name"]               # "Anil"
user.get("email")          # None — safe, no KeyError
user.get("email", "N/A")   # "N/A" — with default

# Modify
user["email"] = "anil@example.com"   # add or update
user.update({"age": 29, "city": "Bangalore"})
del user["city"]

# Query
"name" in user            # True
len(user)                 # number of key-value pairs
user.keys()               # dict_keys(['name', 'age', ...])
user.values()             # dict_values(['Anil', 29, ...])
user.items()              # dict_items([('name','Anil'), ...])

# Pop
age = user.pop("age")             # removes and returns value
user.setdefault("role", "user")   # sets key only if not already present
```

**Real-world — API response parsing:**
```python
response = {
    "status": "success",
    "data": {
        "user_id": 1042,
        "username": "anil_k",
        "permissions": ["read", "write"]
    }
}

username = response["data"]["username"]
can_write = "write" in response["data"]["permissions"]
```

**Dictionary comprehension:**
```python
# Square lookup table
squares = {x: x**2 for x in range(1, 11)}
# {1: 1, 2: 4, 3: 9, ..., 10: 100}

# Filter and transform
active_users = {uid: info for uid, info in users.items() if info["active"]}
```

### 9.5 Set — Unique Collection

Sets store unique items. They're great for membership testing, deduplication, and mathematical set operations.

```python
# Creation
tech_stack = {"Python", "FastAPI", "PostgreSQL", "Redis"}
empty_set = set()    # NOTE: {} creates an empty dict, not set!

# Add / Remove
tech_stack.add("Docker")
tech_stack.discard("Redis")   # no error if not found
tech_stack.remove("Redis")    # raises KeyError if not found

# Membership (very fast — O(1) average)
"Python" in tech_stack    # True

# Set operations
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}

a | b   # union:        {1, 2, 3, 4, 5, 6, 7}
a & b   # intersection: {3, 4, 5}
a - b   # difference:   {1, 2}
a ^ b   # symmetric diff: {1, 2, 6, 7}
```

**Real-world — deduplication:**
```python
# Remove duplicate emails from signup list
raw_emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com"]
unique_emails = list(set(raw_emails))

# Find common tags between two articles
tags_a = {"python", "backend", "api", "fastapi"}
tags_b = {"python", "web", "api", "django"}
common_tags = tags_a & tags_b   # {"python", "api"}
```

### 9.6 Choosing the Right Collection

```
Question: Do you need key-value pairs?
    YES → dict
    NO  ↓

Question: Do you need uniqueness / set operations?
    YES → set
    NO  ↓

Question: Should the data be immutable?
    YES → tuple
    NO  → list
```

| Need | Use |
|------|-----|
| Ordered sequence you'll modify | `list` |
| Fixed coordinates, config tuples | `tuple` |
| User profile, config key-value | `dict` |
| Unique tags, permissions | `set` |
| Fast membership test (large data) | `set` |
| Returning multiple values from function | `tuple` |

---

## 10. Built-in Functions (Complete Reference)

Python ships with a rich set of built-in functions — always available, no imports needed. They're implemented in C, which makes them faster than equivalent Python code.

```python
import builtins
print(dir(builtins))   # full list of built-ins
```

### 10.1 Type Conversion Functions

```python
int("10")         # 10
int(10.9)         # 10  — truncates toward zero, not rounds
int("10.5")       # ❌ ValueError — use float() first

float("3.14")     # 3.14
float(True)       # 1.0

str(100)          # "100"
str(None)         # "None"

bool(0)           # False
bool("")          # False
bool([])          # False
bool(None)        # False
bool("False")     # True  — non-empty string is truthy!
bool("0")         # True  — same reason

list("abc")       # ['a', 'b', 'c']
list(range(5))    # [0, 1, 2, 3, 4]
tuple([1,2,3])    # (1, 2, 3)
set([1,1,2,3])    # {1, 2, 3}  — duplicates removed
dict(a=1, b=2)    # {'a': 1, 'b': 2}
```

**Falsy values (critical for interviews):**
```
False, 0, 0.0, 0j, None, "", [], {}, set(), ()
```

Everything else is truthy.

### 10.2 Mathematical Built-ins

```python
abs(-42)              # 42
abs(-3.14)            # 3.14

round(3.14159, 2)     # 3.14
round(2.5)            # 2  — Banker's rounding (rounds to even)
round(3.5)            # 4

pow(2, 10)            # 1024
pow(2, -1)            # 0.5

min(3, 1, 4, 1, 5)    # 1
max(3, 1, 4, 1, 5)    # 5
min([5, 3, 8])        # 3  — works with iterables too
max("apple", "banana")  # "banana" — works with strings

sum([1, 2, 3, 4, 5])  # 15
sum(range(101))        # 5050  — Gauss's formula result
```

> **Banker's Rounding:** `round(2.5)` returns 2, not 3. Python rounds to the nearest even number at the midpoint. This is statistically fairer for financial calculations. Use `decimal.Decimal` for precise financial math.

### 10.3 Iterable & Sequence Built-ins

```python
len("Python")         # 6
len([1, 2, 3])        # 3
len({"a": 1, "b": 2}) # 2

sorted([3,1,4,1,5])          # [1, 1, 3, 4, 5] — returns new list
sorted("hello")              # ['e', 'h', 'l', 'l', 'o']
sorted(users, key=lambda u: u["name"])   # sort dicts by field
sorted(nums, reverse=True)   # descending

nums = [3, 1, 4]
nums.sort()           # in-place, returns None

list(range(5))        # [0, 1, 2, 3, 4]
list(range(2, 10, 2)) # [2, 4, 6, 8]
list(range(10, 0, -1)) # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
```

**`enumerate()` — the right way to loop with index:**
```python
fruits = ["apple", "banana", "cherry"]

# ❌ Avoid
for i in range(len(fruits)):
    print(i, fruits[i])

# ✅ Use enumerate
for i, fruit in enumerate(fruits):
    print(i, fruit)

# Start index at 1
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
```

**`zip()` — parallel iteration:**
```python
names = ["Anil", "Bob", "Carol"]
scores = [95, 82, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# Create dict from two lists
lookup = dict(zip(names, scores))
# {"Anil": 95, "Bob": 82, "Carol": 78}
```

**`reversed()` and `map()` and `filter()`:**
```python
list(reversed([1, 2, 3]))      # [3, 2, 1]

list(map(int, ["1", "2", "3"]))   # [1, 2, 3]
list(map(str.upper, ["a", "b"]))  # ["A", "B"]

list(filter(None, [0, 1, "", "a", None, True]))  # [1, "a", True]
list(filter(lambda x: x > 0, [-1, 0, 1, 2]))    # [1, 2]
```

### 10.4 Object Introspection

```python
type(42)               # <class 'int'>
type("hello")          # <class 'str'>

isinstance(42, int)    # True — preferred over type() ==
isinstance(42, (int, float))  # True — check multiple types at once

dir(list)              # all attributes and methods of list class
dir("hello")           # all string methods
help(str.format)       # documentation for str.format
id(x)                  # memory address of x
```

### 10.5 Logical Built-ins

```python
all([True, True, True])    # True
all([True, False, True])   # False
all([])                    # True — vacuously true (empty)

any([False, False, True])  # True
any([False, False, False]) # False
any([])                    # False

# Real use — validate all required fields present:
required = ["name", "email", "password"]
data = {"name": "Anil", "email": "a@x.com", "password": "secret"}
if all(field in data for field in required):
    print("All fields present")
```

### 10.6 Memory & Identity

```python
id(x)         # memory address as integer
hash("hello") # hash value — used internally by dict and set
callable(print)   # True — print is callable
callable(42)      # False — integers are not callable
```

### 10.7 Dynamic Execution (Use with Extreme Caution)

```python
eval("2 + 3")        # 5 — evaluates expression
eval("__import__('os').system('rm -rf /')") # 💀 NEVER do this with user input

exec("x = 10\nprint(x)")   # executes statements
```

> **Security Rule:** Never use `eval()` or `exec()` with any input that comes from a user, API, or file you don't fully control. This is a serious security vulnerability that has caused real production incidents.

---

## 11. Hands-On Exercises

### Exercise 1 — CLI Calculator with Full Validation

```python
def calculate():
    print("=== Python Calculator ===")
    
    while True:
        try:
            num1 = float(input("Enter first number: "))
            break
        except ValueError:
            print("Invalid input. Enter a number.")
    
    while True:
        op = input("Operator (+, -, *, /, //, %, **): ").strip()
        if op in ("+", "-", "*", "/", "//", "%", "**"):
            break
        print("Invalid operator.")
    
    while True:
        try:
            num2 = float(input("Enter second number: "))
            break
        except ValueError:
            print("Invalid input. Enter a number.")
    
    if op == "/" and num2 == 0:
        print("Error: Division by zero.")
        return
    
    ops = {
        "+":  lambda a, b: a + b,
        "-":  lambda a, b: a - b,
        "*":  lambda a, b: a * b,
        "/":  lambda a, b: a / b,
        "//": lambda a, b: a // b,
        "%":  lambda a, b: a % b,
        "**": lambda a, b: a ** b,
    }
    
    result = ops[op](num1, num2)
    print(f"\n{num1} {op} {num2} = {result}")

calculate()
```

### Exercise 2 — String Analyzer

```python
text = input("Enter a sentence: ").strip()

print(f"\nOriginal:    {text}")
print(f"Upper:       {text.upper()}")
print(f"Lower:       {text.lower()}")
print(f"Title:       {text.title()}")
print(f"Reversed:    {text[::-1]}")
print(f"Word count:  {len(text.split())}")
print(f"Char count:  {len(text)}")
print(f"Char count (no spaces): {len(text.replace(' ', ''))}")

words = text.split()
longest = max(words, key=len)
shortest = min(words, key=len)
print(f"Longest word:  {longest}")
print(f"Shortest word: {shortest}")

vowels = sum(1 for c in text.lower() if c in "aeiou")
print(f"Vowel count: {vowels}")
```

### Exercise 3 — Collection Operations

```python
# Demonstrate all four collection types with a real scenario

# Shopping cart — list (ordered, can have duplicates)
cart = ["laptop", "mouse", "keyboard", "mouse"]
print(f"Cart: {cart}")
print(f"Total items: {len(cart)}")

# Remove duplicate items
unique_items = list(set(cart))
print(f"Unique items: {unique_items}")

# Product catalog — dict
catalog = {
    "laptop": 75000,
    "mouse": 999,
    "keyboard": 2499
}

# Calculate cart total
total = sum(catalog.get(item, 0) for item in cart)
print(f"Cart total: ₹{total:,}")

# Applied discounts — set (no duplicates)
applied_coupons = {"FLAT10", "WELCOME"}
available_coupons = {"FLAT10", "NEWUSER", "FESTIVE"}
already_used = applied_coupons & available_coupons
new_coupons = available_coupons - applied_coupons
print(f"New available coupons: {new_coupons}")
```

---

## 12. Mini Project — Personal Info CLI App

```python
def collect_info():
    print("=" * 40)
    print("     PERSONAL INFO COLLECTOR")
    print("=" * 40)
    
    name = input("Full name: ").strip().title()
    
    while True:
        try:
            age = int(input("Age: "))
            if not (0 < age < 120):
                print("Please enter a valid age.")
                continue
            break
        except ValueError:
            print("Enter a valid number.")
    
    city = input("City: ").strip().title()
    profession = input("Profession: ").strip().title()
    skills_raw = input("Skills (comma-separated): ").strip()
    
    skills = [s.strip().title() for s in skills_raw.split(",") if s.strip()]
    unique_skills = list(dict.fromkeys(skills))   # deduplicate, preserve order
    
    print()
    print("=" * 40)
    print("     YOUR PROFILE SUMMARY")
    print("=" * 40)
    print(f"  Name       : {name}")
    print(f"  Age        : {age}")
    print(f"  City       : {city}")
    print(f"  Profession : {profession}")
    print(f"  Skills     : {', '.join(unique_skills)}")
    print("=" * 40)
    
    return {
        "name": name,
        "age": age,
        "city": city,
        "profession": profession,
        "skills": unique_skills
    }

profile = collect_info()
```

**Real-world equivalent:** This is structurally identical to onboarding flows in HR platforms, user registration in SaaS apps, and intake forms in CRM tools.

---

## Quick Reference — Common Pitfalls & Observations

| Pitfall | Wrong | Right |
|---------|-------|-------|
| Comparing with `is` | `x is 5` | `x == 5` |
| Mutable default argument | `def f(lst=[])` | `def f(lst=None): lst = lst or []` |
| Input type assumption | `x = input("Num: ")` then `x + 1` | `x = int(input("Num: "))` |
| Empty set creation | `s = {}` (creates dict!) | `s = set()` |
| Modifying list while iterating | `for x in lst: lst.remove(x)` | Iterate over a copy |
| `==` vs `is` for None | `if x == None` | `if x is None` |
| String as loop accumulator | `s = ""; for c in chars: s += c` | `s = "".join(chars)` |

---

*Notes compiled for SDE Track — Python Full Stack | Day 1*
