# 🐍 Python Full Stack — Day 1: Complete Notes

---

## 📜 SECTION 0 — A Brief History of Python

Python was created by **Guido van Rossum** and first released in **1991**. He began developing it in the late 1980s as a hobby project during the Christmas holidays, intending it to be a successor to the ABC language — with a strong focus on readability and simplicity.

| Version | Year | Key Milestone |
|---------|------|---------------|
| Python 1.0 | 1994 | First official release |
| Python 2.0 | 2000 | List comprehensions, garbage collection added |
| Python 3.0 | 2008 | Major redesign; intentionally NOT backward-compatible with Python 2 |
| Python 3.6+ | 2016+ | f-strings, type hints, async/await improvements |
| Python 3.10+ | 2021+ | Structural pattern matching, better error messages |

> ⚠️ **Python 2 reached end-of-life in January 2020.** Always use **Python 3** for any new project.

The name "Python" was inspired by **Monty Python's Flying Circus**, the British comedy group — not the snake. Today, Python consistently ranks as the **#1 most popular programming language** (TIOBE Index, Stack Overflow surveys), powering AI/ML research, web backends, data science, automation, DevOps, and more.

---

## 📋 SECTION 1 — Session Overview

### Learning Objectives
By the end of Day 1, you will be able to:
- Install Python and choose the right IDE for the job
- Declare variables and use all core data types
- Accept user input and display formatted output
- Use arithmetic, comparison, and logical operators
- Perform string operations and formatting
- Understand how Python executes code (CPython pipeline)
- Understand Python's memory model (heap, stack, reference counting)
- Distinguish between mutable and immutable types

### Prerequisites
- No prior Python knowledge required
- Basic computer literacy (file system, text editor, terminal basics)
- Python 3.10+ installed and accessible via terminal

---

## ✅ SECTION 2 — Python Installation & IDE

### 🔍 What is Python?

Python is a high-level, interpreted programming language known for:
- **Simplicity** — clean, readable syntax
- **Readability** — code that reads like English
- **Versatility** — AI, ML, Web, DevOps, Automation, Data Science, Scripting

### 📌 Real-World Use Cases

| Domain | Companies Using Python | Usage |
|--------|------------------------|-------|
| AI/ML | OpenAI, Google, Meta | Model training, LLM pipelines |
| Web Dev | Instagram, Dropbox | Backend services |
| Automation | Netflix, Uber | System automation |
| DevOps | AWS, Azure | Infrastructure tools, CLIs |
| Data | NASA, CERN | Data analysis & visualization |

### 🔧 Installing Python

1. Download from → [python.org](https://python.org)
2. ⚠️ **CLICK: "Add Python to PATH"** during installation — critical!
3. Verify installation:

```bash
python --version
# Expected: Python 3.x.x
```

### 🧑‍💻 IDE Choices

#### VS Code
- Lightweight, fast startup
- Extensions: Python, Pylance, Git integration
- Works great for all levels and project sizes

#### PyCharm
- Heavyweight IDE (like IntelliJ for Python)
- Best for large enterprise/OOP-heavy projects
- Better refactoring tools, built-in debugger

### 🧠 Industry Usage
- Data scientists → Jupyter Notebook for experiments
- Backend engineers → PyCharm for structured projects
- DevOps engineers → VS Code for scripting & automation

### ⭐ Best Practices
- Use VS Code for small to medium apps
- Use PyCharm for large, OOP-heavy backend projects
- **Always use virtual environments (`venv`) from Day 1**

```bash
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

---

## ✅ SECTION 3 — Variables & Data Types

### 🔍 What is a Variable?

A variable is a name (label/reference) pointing to a piece of data stored in memory.

**🧠 Analogy:** Variables are like sticky labels pointing to boxes in a warehouse (the heap). The label is not the data — it just tells you where to find it.

```python
age = 25
name = "John"
height = 5.9
```

### 🎯 Rules for Naming Variables

- Must start with a letter or `_`
- Cannot start with a number
- Cannot include spaces
- Case-sensitive (`Name` ≠ `name`)

```python
# ✅ Correct
user_name = "john"
_internal = True

# ❌ Incorrect
2user = "john"       # starts with number
user-name = "john"   # hyphen not allowed
```

### 🔢 Data Types with Industry Examples

#### 🟦 `int` — Integer Numbers
```python
order_count = 150
user_age = 25
employee_id = 10042
```
**Used in:** billing systems, user profiles, ML label encoding

#### 🟩 `float` — Decimal Numbers
```python
model_accuracy = 0.98
response_time = 23.5
tax_rate = 0.18
```
**Used in:** percentages, sensor readings, ML accuracy, latency

#### 🟪 `str` — Strings
```python
message = "Hello World"
api_url = "https://api.example.com"
log_entry = "[INFO] Server started"
```
**Used in:** logs, API responses, chat messages, LLM prompts

#### 🟨 `bool` — True/False
```python
is_verified = True
is_admin = False
feature_enabled = True
```
**Used in:** authentication, authorization, feature toggles, AI flags

#### 🟥 `NoneType` — Represents Absence
```python
deleted_at = None
optional_field = None
```
**Used in:** missing values, optional fields, default returns, web forms

### Multiple Assignment Patterns

```python
# Assign multiple variables in one line
x, y, z = 10, 20, 30

# Swap without temp variable (Python magic!)
a, b = 5, 10
a, b = b, a          # a=10, b=5

# Same value to multiple names
p = q = r = 0
```

### Type Checking

```python
print(type(name))          # <class 'str'>
print(type(age))           # <class 'int'>
print(isinstance(age, int))  # True
print(id(age))             # Memory address
```

---

## ✅ SECTION 4 — Input & Output

### 🖥 Input Handling

`input()` **always returns a string** — convert as needed.

```python
name = input("Enter your name: ")         # str
age = int(input("Enter your age: "))      # int
price = float(input("Enter price: "))     # float
```

### 📤 `print()` — Complete Syntax & All Parameters

```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `*objects` | any | — | One or more values to print |
| `sep` | str | `' '` | Separator between multiple values |
| `end` | str | `'\n'` | What to print at the very end |
| `file` | file object | `sys.stdout` | Where to send output |
| `flush` | bool | `False` | Force flush the output buffer immediately |

#### Examples of Every Parameter

```python
# Default behaviour
print("Hello", "World")              # Hello World

# Custom separator
print("2024", "01", "15", sep="-")  # 2024-01-15
print("a", "b", "c", sep=" | ")     # a | b | c

# Custom end (suppress newline)
print("Loading", end="")
print("...", end="\n")               # Loading...

# Print multiple items inline
for i in range(5):
    print(i, end=" ")                # 0 1 2 3 4

# Write to a file
with open("log.txt", "w") as f:
    print("Server started", file=f)

# Flush (useful in real-time logging, progress bars)
import time
for i in range(3):
    print(f"Step {i+1}", end="\r", flush=True)
    time.sleep(1)

# Print nothing (blank line)
print()

# Multiple values with sep
print("Name:", "Alice", sep="")      # Name:Alice
```

#### f-Strings — Modern Best Practice (Python 3.6+)

```python
name = "Alice"
age = 30
score = 95.678

# Basic f-string
print(f"Hello {name}, you are {age} years old.")

# Formatting numbers
print(f"Score: {score:.2f}")          # Score: 95.68
print(f"Pi: {3.14159:.4f}")          # Pi: 3.1416

# Padding and alignment
print(f"{'Left':<10}|")              # Left      |
print(f"{'Right':>10}|")             #      Right|
print(f"{'Center':^10}|")            #   Center  |

# Expressions inside f-strings
print(f"2 + 2 = {2 + 2}")            # 2 + 2 = 4
print(f"Upper: {name.upper()}")      # Upper: ALICE
```

#### Real-World print() Usage

```python
# Log formatting
print(f"[INFO] User {username} logged in at {timestamp}")

# API URL construction
url = f"https://api.company.com/user/{user_id}"
print(url)

# Progress reporting
print(f"Processing {current}/{total} records...", end="\r", flush=True)

# Debug separator
print("-" * 40)
print(f"{'REPORT':^40}")
print("-" * 40)
```

### ⭐ Best Practices
- Always convert `input()` to the required type
- Use f-strings for readability (avoid `+` concatenation)
- Use `.strip()` to remove accidental whitespace from user inputs

---

## ✅ SECTION 5 — Operators & Expressions

### ⚡ 1. Arithmetic Operators

| Operator | Meaning | Example | Result |
|----------|---------|---------|--------|
| `+` | Add | `5 + 3` | `8` |
| `-` | Subtract | `5 - 2` | `3` |
| `*` | Multiply | `3 * 4` | `12` |
| `/` | Divide (float) | `10 / 4` | `2.5` |
| `//` | Floor division | `10 // 4` | `2` |
| `%` | Modulus | `10 % 3` | `1` |
| `**` | Power | `2 ** 3` | `8` |

```python
# Real-World — E-commerce Discount
price = 1000
discount = 15
final = price - (price * discount / 100)
print(f"Final price: ₹{final}")        # ₹850.0
```

### 🔍 2. Comparison Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal | `a == b` |
| `!=` | Not equal | `a != b` |
| `>` | Greater than | `a > b` |
| `<` | Less than | `a < b` |
| `>=` | Greater or equal | `a >= b` |
| `<=` | Less or equal | `a <= b` |

```python
# Real-World — Payment Validation
balance = 5000
amount = 3000
if balance >= amount:
    print("Payment successful")
else:
    print("Insufficient funds")
```

### 🔄 3. Logical Operators

| Operator | Example | Meaning |
|----------|---------|---------|
| `and` | `a > 10 and a < 20` | Both must be True |
| `or` | `is_admin or is_manager` | At least one True |
| `not` | `not is_active` | Inverts the boolean |

```python
# Real-World — Login Logic
if is_user and is_verified:
    print("Access granted")

if is_admin or is_superuser:
    print("Admin panel accessible")
```

### 🧠 Expressions
Anything that evaluates to a value:
```python
x = (10 + 3) * 2          # 26
result = 10 > 5 and 3 < 7  # True
```

### ⭐ Best Practices
- Use parentheses in long expressions for clarity
- Avoid deeply nested conditions (extract to variables or functions)

---

## ✅ SECTION 6 — String Operations

Strings are **immutable sequences** — used everywhere in software.

### 🔤 Creation
```python
name = "John"
multi = """Line 1
Line 2"""
```

### 🔎 Indexing & Slicing
```python
text = "Python"
text[0]       # 'P'   — first character
text[-1]      # 'n'   — last character
text[0:3]     # 'Pyt' — slice
text[::-1]    # 'nohtyP' — reversed
```

### 🧼 Useful Methods
```python
name = "  John Doe  "
name.lower()              # "  john doe  "
name.upper()              # "  JOHN DOE  "
name.strip()              # "John Doe"   — removes whitespace
name.lstrip()             # "John Doe  " — left only
name.rstrip()             # "  John Doe" — right only
name.replace("o", "0")   # "  J0hn D0e  "
name.split()              # ['John', 'Doe']
name.split(",")           # split by comma
"hello".startswith("he") # True
"hello".endswith("lo")   # True
"hello".find("ll")       # 2 (index)
"hello".count("l")       # 2
",".join(["a","b","c"])  # "a,b,c"
"hello world".title()    # "Hello World"
```

### 🧱 Concatenation
```python
full = first + " " + last     # old way
full = f"{first} {last}"      # ✅ preferred
```

### 🏭 Real-World Examples

```python
# Log formatting
print(f"[INFO] User {user} logged in at {timestamp}")

# API URL construction
url = f"https://api.company.com/user/{user_id}"

# Input sanitization
username = input("Username: ").strip().lower()
```

### ⭐ Best Practices
- Prefer f-strings over `+` concatenation
- Always `.strip()` user inputs before processing
- Never concatenate strings inside loops — use `.join()` instead

---

## ✅ SECTION 7 — Python Built-in Functions

Python ships with a rich set of built-in functions — no imports needed.

### 🔢 Type Conversion

| Function | Description | Example |
|----------|-------------|---------|
| `int(x)` | Convert to integer | `int("42")` → `42` |
| `float(x)` | Convert to float | `float("3.14")` → `3.14` |
| `str(x)` | Convert to string | `str(100)` → `"100"` |
| `bool(x)` | Convert to boolean | `bool(0)` → `False` |
| `list(x)` | Convert to list | `list("abc")` → `['a','b','c']` |
| `tuple(x)` | Convert to tuple | `tuple([1,2])` → `(1,2)` |
| `set(x)` | Convert to set | `set([1,1,2])` → `{1,2}` |
| `dict()` | Create dictionary | `dict(a=1, b=2)` |

### 📐 Math & Numbers

| Function | Description | Example |
|----------|-------------|---------|
| `abs(x)` | Absolute value | `abs(-5)` → `5` |
| `round(x, n)` | Round to n decimals | `round(3.14159, 2)` → `3.14` |
| `pow(x, y)` | x to the power y | `pow(2, 10)` → `1024` |
| `max(iter)` | Maximum value | `max([3,1,4])` → `4` |
| `min(iter)` | Minimum value | `min([3,1,4])` → `1` |
| `sum(iter)` | Sum of iterable | `sum([1,2,3])` → `6` |
| `divmod(a,b)` | (quotient, remainder) | `divmod(10,3)` → `(3,1)` |

### 📋 Sequences & Iterables

| Function | Description | Example |
|----------|-------------|---------|
| `len(x)` | Length | `len("hello")` → `5` |
| `range(n)` | Integer sequence | `range(5)` → 0,1,2,3,4 |
| `range(a,b,step)` | Controlled range | `range(0,10,2)` → 0,2,4,6,8 |
| `enumerate(x)` | Index + value pairs | `enumerate(["a","b"])` |
| `zip(a,b)` | Pair up iterables | `zip([1,2],["a","b"])` |
| `sorted(x)` | Return sorted copy | `sorted([3,1,2])` → `[1,2,3]` |
| `reversed(x)` | Reverse iterator | `list(reversed([1,2,3]))` |
| `map(fn, iter)` | Apply fn to each | `list(map(str, [1,2,3]))` |
| `filter(fn, iter)` | Keep if fn=True | `list(filter(None, [0,1,2]))` |

### 🔍 Introspection & Identity

| Function | Description | Example |
|----------|-------------|---------|
| `type(x)` | Get type | `type(42)` → `<class 'int'>` |
| `isinstance(x, T)` | Check if type T | `isinstance(42, int)` → `True` |
| `id(x)` | Memory address | `id(x)` → `140234...` |
| `dir(x)` | List attributes/methods | `dir([])` |
| `help(x)` | Interactive help | `help(str)` |
| `callable(x)` | Is it a function? | `callable(print)` → `True` |
| `hasattr(obj,name)` | Has attribute? | `hasattr([], "append")` → `True` |
| `getattr(obj,name)` | Get attribute | `getattr([], "__len__")` |

### 📤 Input / Output

| Function | Description |
|----------|-------------|
| `print(*args, sep, end, file, flush)` | Output to stdout (see Section 4) |
| `input(prompt)` | Read string from user |
| `open(file, mode)` | Open a file |

### 🧮 Other Useful Built-ins

| Function | Description | Example |
|----------|-------------|---------|
| `hash(x)` | Hash value (immutables only) | `hash("hello")` |
| `hex(n)` | Integer to hex string | `hex(255)` → `'0xff'` |
| `bin(n)` | Integer to binary string | `bin(10)` → `'0b1010'` |
| `oct(n)` | Integer to octal string | `oct(8)` → `'0o10'` |
| `chr(n)` | ASCII/Unicode char | `chr(65)` → `'A'` |
| `ord(c)` | Char to ASCII number | `ord('A')` → `65` |
| `vars(obj)` | Object's `__dict__` | `vars()` |
| `globals()` | Global variables dict | — |
| `locals()` | Local variables dict | — |
| `eval(str)` | Evaluate expression string | `eval("2+2")` → `4` |
| `exec(str)` | Execute code string | `exec("x=5")` |

### 🏭 Real-World Built-in Usage

```python
# Normalize user ratings to 2 decimal places
ratings = [4.567, 3.2, 5.0, 2.891]
normalized = [round(r, 2) for r in ratings]

# Find highest-paid employee
salaries = [55000, 82000, 47000, 95000]
print(f"Max: {max(salaries)}, Min: {min(salaries)}, Avg: {sum(salaries)/len(salaries):.0f}")

# Enumerate for indexed loops (instead of range + index)
users = ["Alice", "Bob", "Carol"]
for idx, user in enumerate(users, start=1):
    print(f"{idx}. {user}")

# zip for pairing data
names = ["Alice", "Bob"]
scores = [95, 87]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# map for transformations
ids = ["001", "002", "003"]
int_ids = list(map(int, ids))   # [1, 2, 3]

# filter for selections
data = [0, 1, None, 2, "", 3]
valid = list(filter(None, data))   # [1, 2, 3]
```

---

## ✅ SECTION 8 — How Python Executes Code (CPython Internals)

### 🔍 CPython Execution Flow

When you run a `.py` file, Python transforms your code through several stages before the CPU sees it.

**Real-world analogy:** Like translating an English recipe (source code) into a step-by-step chef's shorthand (bytecode) that any kitchen (PVM) can follow.

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

> The `.pyc` files in `__pycache__/` are cached bytecode — Python reuses them if the source hasn't changed, making subsequent runs faster.

### 🧠 Python Memory Model

| Region | What Lives Here |
|--------|----------------|
| **Heap** | All Python objects (your actual data) |
| **Stack** | Call frames — which function is running and what names it knows |

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

### 🔄 Reference Counting

Every object tracks how many names point to it. When count hits 0, Python frees the memory.

```python
import sys
x = [1, 2, 3]       # ref count = 1
y = x               # ref count = 2
del x               # ref count = 1
del y               # ref count = 0 → object destroyed

# Inspect reference count
print(sys.getrefcount(x))   # Always +1 (argument itself)
```

### 🔢 Small Integer Caching

Python pre-creates integer objects for **-5 to 256** and reuses them:

```python
a = 100; b = 100
print(a is b)   # True  → same cached object

a = 1000; b = 1000
print(a is b)   # False → two separate objects

print(a == b)   # True  → but values are equal!
```

> **Rule:** Always use `==` to compare values. Use `is` only for `None` checks.

### 📝 String Interning

Python reuses memory for short, identifier-like strings (no spaces):

```python
a = "hello";  b = "hello"
print(a is b)         # True  — interned

a = "hello world"; b = "hello world"
print(a is b)         # False — spaces prevent interning
```

### 🔀 Mutable vs Immutable

| Category | Types |
|----------|-------|
| **Immutable** | `int`, `float`, `str`, `tuple`, `frozenset`, `bytes` |
| **Mutable** | `list`, `dict`, `set`, `bytearray` |

```python
# Immutable — reassignment creates a NEW object
x = "hello"
x += " world"     # x now points to a brand new string

# Mutable — modification changes the SAME object in-place
my_list = [1, 2, 3]
my_list.append(4)  # same object, now [1, 2, 3, 4]

# Prove it with id()
my_list = [1, 2, 3]
print(id(my_list))   # e.g. 4501234567
my_list.append(4)
print(id(my_list))   # SAME id

my_str = "hello"
print(id(my_str))    # e.g. 4501239999
my_str += " world"
print(id(my_str))    # DIFFERENT id
```

### 🔗 Pass-by-Object-Reference

Python passes the **reference** to the function — not a copy.

```python
# Mutable — caller sees the change
def add_item(lst):
    lst.append(99)

my_list = [1, 2, 3]
add_item(my_list)
print(my_list)  # [1, 2, 3, 99] ← changed!

# Immutable — caller does NOT see the change
def try_change(n):
    n = n + 10

x = 5
try_change(x)
print(x)  # 5 ← unchanged
```

---

## ❌ SECTION 9 — Common Mistakes & Gotchas

### Mistake 1: Using `is` Instead of `==` for Values
```python
# ❌ Wrong
x = 1000; y = 1000
if x is y: ...          # Unpredictable for large ints

# ✅ Correct
if x == y: ...          # Always reliable
```

### Mistake 2: Mutable Default Arguments
```python
# ❌ Wrong — shared list across all calls
def add_item(item, lst=[]):
    lst.append(item)
    return lst

# ✅ Correct
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### Mistake 3: Unexpected Aliasing
```python
# ❌ Wrong — both names point to the SAME list
original = [1, 2, 3]
copy = original           # NOT a copy!
copy.append(99)
print(original)           # [1, 2, 3, 99] ← unexpected!

# ✅ Correct
copy = original[:]        # Shallow copy
import copy
deep = copy.deepcopy(original)  # Deep copy for nested structures
```

### Mistake 4: Confusing `None` with `0` or `False`
```python
# ✅ Always use `is` for None checks
if value is None:
    print("Not set")

if value is not None:
    print("Has a value")
```

### Mistake 5: Assuming Strings Are Mutable
```python
# ❌ Wrong
name = "Alice"
name[0] = "B"        # TypeError!

# ✅ Correct
name = "B" + name[1:]   # "Blice"
```

### Mistake 6: Shadowing Built-in Names
```python
# ❌ Never do this
list = [1, 2, 3]    # shadows built-in list()
str = "hello"       # shadows built-in str()
id = 42             # shadows built-in id()

# ✅ Add context
user_list = [1, 2, 3]
user_str = "hello"
user_id = 42
```

---

## ✅ SECTION 10 — Best Practices & PEP 8

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Variables | `snake_case` | `user_name`, `total_count` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_SIZE`, `API_KEY` |
| Private variables | `_leading_underscore` | `_internal_state` |
| Dunder/magic | `__double_underscore__` | `__init__`, `__str__` |

### Type Hints (Python 3.6+)

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

age: int = 25
scores: list[int] = [90, 85, 92]
```

### None Checks
```python
# ✅ Always use `is`, never `==`
if value is None: ...
if value is not None: ...
```

---

## 🧪 SECTION 11 — Hands-On Exercises

### Exercise 1: CLI Calculator
```python
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
op = input("Enter operator (+, -, *, /): ")

if op == "+":
    print(num1 + num2)
elif op == "-":
    print(num1 - num2)
elif op == "*":
    print(num1 * num2)
elif op == "/":
    if num2 == 0:
        print("Cannot divide by zero!")
    else:
        print(num1 / num2)
else:
    print("Invalid operator!")
```

### Exercise 2: String Formatter
```python
name = input("Enter name: ").strip().title()
age = input("Enter age: ")
city = input("Enter city: ").strip().title()

print(f"Hello {name}, you are {age} years old and live in {city}.")
```

### Exercise 3: Predict the Output (Memory Model)
```python
# Without running, predict each output. Then verify.
x = 50;  y = 50
print(x is y)        # Predict: ?

x = 500; y = 500
print(x is y)        # Predict: ?

a = "python"; b = "python"
print(a is b)        # Predict: ?

c = [1, 2]; d = [1, 2]
print(c is d)        # Predict: ?
print(c == d)        # Predict: ?
```
> **Hint:** Think about integer caching range (-5 to 256) and string interning rules.

---

## 🏆 SECTION 12 — Mini Project: Personal Info CLI App

### Requirements
- Ask user for multiple details
- Validate and format input
- Print a clean, professional summary

```python
print("=== Personal Info Collector ===")

name       = input("Your full name: ").strip().title()
age        = int(input("Your age: "))
city       = input("Your city: ").strip().title()
profession = input("Your profession: ").strip().title()
hobby      = input("Your favorite hobby: ").strip()

summary = f"""
----------------------------------
      PERSONAL INFORMATION
----------------------------------
Name        : {name}
Age         : {age}
City        : {city}
Profession  : {profession}
Hobby       : {hobby}
----------------------------------
"""

print(summary)
```

### 🏭 Real-World Equivalent
This pattern is used in: AWS CLI input prompting, user registration flows, HR onboarding systems, customer intake forms.

---

## 📊 SECTION 13 — Quick Revision Summary

### Key Terms

| Term | One-line Definition |
|------|---------------------|
| CPython | Reference Python implementation written in C |
| AST | Tree representation of your code's logical structure |
| Bytecode | Platform-independent intermediate code in `.pyc` files |
| PVM | Engine that executes Python bytecode |
| Heap | Memory region where Python objects live |
| Stack | Memory region for call frames (active function contexts) |
| Reference | A name/pointer that points to an object on the heap |
| Reference Counting | Tracking how many names point to an object |
| Immutable | Object whose value cannot change after creation |
| Mutable | Object that can be modified in-place |
| Interning | Reusing the same object for identical small strings/ints |
| Pass-by-object-reference | Python passes the reference, not a copy of the value |

### Core Syntax Cheat Sheet

```python
# Assignment & type checking
x = 42
type(x)               # <class 'int'>
isinstance(x, int)    # True
id(x)                 # memory address

# Identity vs equality
x is y                # same object in memory?
x == y                # same value?

# Reference count inspection
import sys
sys.getrefcount(x)

# Copying
copy = original[:]         # shallow copy (list/str)
copy = list(original)      # shallow copy
import copy
deep = copy.deepcopy(obj)  # deep copy

# Type hints
age: int = 25
name: str = "Alice"
```

### MCQ Recap

**Q1.** What does Python use to automatically manage memory?
- A) Manual `free()` calls
- B) Garbage collection only
- **C) Reference counting + cyclic GC** ✅
- D) Stack-based allocation

**Q2.** Which of the following is **immutable**?
- A) `list`  B) `dict`  **C) `tuple`** ✅  D) `set`

**Q3.** `a = 300; b = 300; print(a is b)` → ?
- **A) `False` — integers above 256 are not cached** ✅
- B) `True`  C) Depends on OS  D) TypeError

**Q4.** You pass a list to a function that calls `.append()`. The original list after the call is:
- A) Unchanged  **B) Changed — same object referenced** ✅  C) Deleted  D) TypeError

**Q5.** Correct way to check for `None`:
- A) `if x == None:`  **B) `if x is None:`** ✅  C) `if x = None:`  D) `if type(x) == "NoneType":`

---

## 📚 SECTION 14 — Resources & Further Reading

- [Python Official Docs — Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Python Official Built-in Functions](https://docs.python.org/3/library/functions.html)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Python Memory Management (Real Python)](https://realpython.com/python-memory-management/)
- [Ned Batchelder — Facts and Myths about Python names and values](https://nedbatchelder.com/text/names.html) ← highly recommended
- [Python Tutor — Visualize code execution live](https://pythontutor.com/) ← great for heap/stack visualization
