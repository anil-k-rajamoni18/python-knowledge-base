# 🐍 Python — Day 2 Notes
---

## Table of Contents

1. [Conditionals — if / elif / else](#1-conditionals--if--elif--else)
2. [How Python Evaluates Conditions Internally](#2-how-python-evaluates-conditions-internally)
3. [Ternary / Inline Conditionals](#3-ternary--inline-conditionals)
4. [match / case — Python's Switch Statement (3.10+)](#4-match--case--pythons-switch-statement-310)
5. [for Loops — Deep Dive](#5-for-loops--deep-dive)
6. [while Loops — Deep Dive](#6-while-loops--deep-dive)
7. [Loop Control — break / continue / pass / else](#7-loop-control--break--continue--pass--else)
8. [Iterators & Iterables — What Happens Under the Hood](#8-iterators--iterables--what-happens-under-the-hood)
9. [List Comprehensions — Deep Dive](#9-list-comprehensions--deep-dive)
10. [Dict, Set & Generator Comprehensions](#10-dict-set--generator-comprehensions)
11. [Nested Loops & Nested Comprehensions](#11-nested-loops--nested-comprehensions)
12. [Common Patterns & Anti-Patterns](#12-common-patterns--anti-patterns)
13. [Hands-On Exercises (All 20+)](#13-hands-on-exercises-all-20)
14. [Mini Project — Number Guessing Game (Enhanced)](#14-mini-project--number-guessing-game-enhanced)

---

## 1. Conditionals — if / elif / else

### What Are Conditionals?

Every real program needs to make decisions. Conditionals are how Python chooses which block of code to run based on whether a condition is True or False.

Think of it like a crossroads. Your program arrives at a decision point, evaluates the situation, and takes one path forward.

```
if condition_A:          ← checked first
    # path A
elif condition_B:        ← only checked if A is False
    # path B
elif condition_C:        ← only checked if A and B are False
    # path C
else:                    ← runs if nothing above matched
    # fallback path
```

Key rule: Python checks conditions **top to bottom** and stops as soon as one matches. The `else` block is the safety net — it runs only when everything above it was False.

### Real-World Industry Uses

| Industry | Conditional Use Case |
|----------|---------------------|
| Banking | Block transaction if balance insufficient |
| E-commerce | Show "Out of Stock" if inventory = 0 |
| AI/ML | Classify prediction confidence levels |
| Security | Grant/deny access based on role |
| DevOps | Trigger different deployment paths per environment |

### Basic Structure with Examples

```python
# Authentication check
username = input("Username: ").strip()
password = input("Password: ").strip()

if not username or not password:
    print("Error: Fields cannot be empty.")
elif username == "admin" and password == "secret123":
    print("Welcome, Administrator.")
elif username == "guest":
    print("Welcome, Guest. Limited access.")
else:
    print("Invalid credentials. Access denied.")
```

### Real-World Example — Fraud Detection Score

In ML-powered payment systems, a model outputs a score between 0 and 1. The business logic then routes the transaction based on that score.

```python
fraud_score = 0.82   # comes from ML model output

if fraud_score >= 0.95:
    action = "BLOCK"
    notify_fraud_team = True
elif fraud_score >= 0.75:
    action = "MANUAL_REVIEW"
    notify_fraud_team = False
elif fraud_score >= 0.50:
    action = "CHALLENGE"   # trigger OTP or CAPTCHA
    notify_fraud_team = False
else:
    action = "ALLOW"
    notify_fraud_team = False

print(f"Transaction action: {action}")
```

### Real-World Example — HTTP Status Code Routing

```python
status_code = 404

if status_code == 200:
    print("OK — serve the response")
elif status_code == 201:
    print("Created — resource added")
elif status_code in (301, 302):
    print("Redirect — follow location header")
elif status_code == 400:
    print("Bad Request — client error")
elif status_code == 401:
    print("Unauthorized — prompt login")
elif status_code == 403:
    print("Forbidden — deny access")
elif status_code == 404:
    print("Not Found — show error page")
elif status_code >= 500:
    print("Server Error — alert on-call engineer")
else:
    print("Unknown status code")
```

### Nested Conditionals — Use Sparingly

```python
# Too deeply nested — hard to read
if is_logged_in:
    if is_verified:
        if has_subscription:
            if not is_banned:
                grant_access()

# Better — early return pattern (or early continue in loops)
if not is_logged_in:
    return "Please log in"
if not is_verified:
    return "Please verify your email"
if not has_subscription:
    return "Subscribe to access this feature"
if is_banned:
    return "Account suspended"

grant_access()
```

The second version is called the **guard clause** pattern. It's used heavily in production codebases because it keeps the "happy path" at the lowest nesting level.

### Best Practices

- Use `elif` instead of multiple separate `if` blocks when conditions are mutually exclusive
- Put the most likely condition first (performance)
- Never write `if x == True:` — just write `if x:`
- Never write `if x == False:` — write `if not x:`
- Avoid more than 2–3 levels of nesting; refactor using guard clauses or helper functions

---

## 2. How Python Evaluates Conditions Internally

### Truthiness — Every Object Has a Boolean Value

Python doesn't require a strict `True` or `False` in an `if` statement. Any expression works, and Python internally calls `bool()` on it.

```
FALSY — evaluates to False:          TRUTHY — evaluates to True:
──────────────────────────           ───────────────────────────
False                                Everything else
None
0, 0.0, 0j
"" (empty string)
[] (empty list)
{} (empty dict)
set() (empty set)
() (empty tuple)
```

```python
# Real-world example — checking if data came back from DB
results = db.query("SELECT * FROM users WHERE active=1")

if results:          # empty list is falsy — this is idiomatic Python
    process(results)
else:
    print("No active users found")
```

### Short-Circuit Evaluation

Python doesn't evaluate more of a condition than it needs to.

```
x and y:
  → if x is falsy, return x immediately (never evaluates y)
  → if x is truthy, evaluate and return y

x or y:
  → if x is truthy, return x immediately (never evaluates y)
  → if x is falsy, evaluate and return y
```

```python
# Safe: if user is None, user.is_admin is never evaluated
if user is not None and user.is_admin:
    show_admin_panel()

# Default value pattern — very common in Python
name = user_input or "Anonymous"
config = provided_config or load_default_config()

# Conditional execution in one line
debug_mode and print("Debug:", payload)
```

### Comparison Chaining

Python allows chaining comparisons, which reads almost like English:

```python
# Python — clean and readable
if 18 <= age <= 65:
    print("Eligible for work visa")

if 0.0 <= probability <= 1.0:
    print("Valid probability")

if "a" <= char <= "z":
    print("Lowercase letter")
```

Internally, Python evaluates `18 <= age <= 65` as `18 <= age and age <= 65`, but you only write it once. No other mainstream language has this.

---

## 3. Ternary / Inline Conditionals

A ternary expression is a one-liner `if/else`. Use it for simple value assignments — not for complex logic.

```python
# Syntax:
value = result_if_true if condition else result_if_false

# Examples:
status = "Adult" if age >= 18 else "Minor"
label = "Pass" if score >= 50 else "Fail"
sign = "positive" if n > 0 else ("zero" if n == 0 else "negative")

# Real-world — API response field
response = {
    "status": "success" if error is None else "error",
    "message": data if error is None else str(error)
}
```

> **Observation:** Ternary expressions are great for simple cases. If you find yourself nesting them, switch to a regular `if/elif/else` block for readability.

---

## 4. match / case — Python's Switch Statement (3.10+)

Python 3.10 introduced structural pattern matching. It's more powerful than a traditional switch/case because it matches on structure, not just equality.

```python
# Basic value matching
command = input("Enter command: ").lower()

match command:
    case "start":
        print("Starting service...")
    case "stop":
        print("Stopping service...")
    case "restart":
        print("Restarting service...")
    case "status":
        print("Checking status...")
    case _:
        print(f"Unknown command: {command}")
```

The `_` is the wildcard — it matches anything, like `else`.

```python
# Matching on data structures
def handle_event(event):
    match event:
        case {"type": "login", "user": user}:
            print(f"Login event for user: {user}")
        case {"type": "logout", "user": user}:
            print(f"Logout event for user: {user}")
        case {"type": "error", "code": code}:
            print(f"Error event with code: {code}")
        case _:
            print("Unknown event type")

handle_event({"type": "login", "user": "anil"})
# Login event for user: anil
```

```python
# HTTP method routing — clean alternative to elif chains
def route(method, path):
    match (method, path):
        case ("GET", "/users"):
            return list_users()
        case ("POST", "/users"):
            return create_user()
        case ("GET", "/health"):
            return {"status": "ok"}
        case _:
            return {"error": "Not found"}, 404
```

> **When to use match vs if/elif:** Use `match` when you're branching on a single value with many cases, or when matching against data structure shapes. Use `if/elif` for complex boolean expressions.

---

## 5. for Loops — Deep Dive

### How `for` Works

A `for` loop works with any **iterable** — anything that can produce items one at a time. Under the hood, Python calls `iter()` on the object to get an iterator, then calls `next()` repeatedly until it raises `StopIteration`. (More on this in section 8.)

```
for item in iterable:
    body

→ Internally:
_iterator = iter(iterable)
while True:
    try:
        item = next(_iterator)
        body
    except StopIteration:
        break
```

### Iterating Common Types

```python
# List
for product in ["laptop", "mouse", "keyboard"]:
    print(f"Processing: {product}")

# String — character by character
for char in "Python":
    print(char, end=" ")    # P y t h o n

# Range — start, stop, step
for i in range(0, 10, 2):   # 0 2 4 6 8
    print(i)

for i in range(10, 0, -1):  # countdown
    print(i)

# Tuple
for name, age in [("Anil", 28), ("Bob", 32)]:
    print(f"{name} is {age}")

# Dictionary
config = {"host": "localhost", "port": 5432, "db": "sprox"}
for key, value in config.items():
    print(f"{key} = {value}")
```

### `enumerate()` — Always Use Instead of range(len())

```python
tasks = ["Write tests", "Fix bug #42", "Deploy to staging"]

# ❌ C-style — avoid this
for i in range(len(tasks)):
    print(f"{i+1}. {tasks[i]}")

# ✅ Pythonic
for i, task in enumerate(tasks, start=1):
    print(f"{i}. {task}")
```

### `zip()` — Parallel Iteration

```python
employees = ["Anil", "Bob", "Carol"]
salaries = [85000, 72000, 91000]
departments = ["Engineering", "Marketing", "Data"]

for emp, sal, dept in zip(employees, salaries, departments):
    print(f"{emp} | {dept} | ₹{sal:,}")
```

`zip()` stops at the shortest iterable. If you need to handle different-length iterables, use `itertools.zip_longest()`.

### `zip()` to Build a Dict

```python
keys = ["name", "age", "city"]
values = ["Anil", 28, "Hyderabad"]
profile = dict(zip(keys, values))
# {"name": "Anil", "age": 28, "city": "Hyderabad"}
```

### Real-World Example — Processing JSON API Response

```python
api_response = {
    "status": "success",
    "items": [
        {"id": 1, "title": "Python Basics", "views": 1542},
        {"id": 2, "title": "FastAPI Tutorial", "views": 3210},
        {"id": 3, "title": "Docker Deep Dive", "views": 892},
    ]
}

total_views = 0
for item in api_response["items"]:
    print(f"[{item['id']}] {item['title']} — {item['views']:,} views")
    total_views += item["views"]

print(f"\nTotal views: {total_views:,}")
```

### Real-World Example — Batch Processing with Chunking

```python
def chunks(lst, size):
    """Split a list into chunks of given size."""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

user_ids = list(range(1, 1001))   # 1000 users

for batch in chunks(user_ids, 100):
    print(f"Processing batch of {len(batch)} users: {batch[0]}–{batch[-1]}")
    # send_email_batch(batch)
```

This pattern is standard in data pipelines and bulk database operations where you can't process 100,000 records in one shot.

---

## 6. while Loops — Deep Dive

### When to Use `while`

Use `while` when you don't know in advance how many iterations you'll need. The loop continues as long as a condition is True.

```
while condition:
    body
    (condition must eventually become False, or use break)
```

### Examples

```python
# Countdown
countdown = 10
while countdown > 0:
    print(countdown)
    countdown -= 1
print("Blast off! 🚀")

# User input loop — keep asking until valid
while True:
    age = input("Enter your age: ").strip()
    if age.isdigit() and 0 < int(age) < 120:
        age = int(age)
        break
    print("Invalid age. Try again.")

print(f"Age recorded: {age}")
```

### Real-World Example — API Retry with Exponential Backoff

In production systems, network calls fail. The professional way to handle this is retrying with increasing wait times.

```python
import time
import random

def call_api():
    """Simulates an API call that sometimes fails."""
    return random.random() > 0.6   # 40% chance of failure

max_retries = 5
retry_count = 0
wait_seconds = 1

while retry_count < max_retries:
    success = call_api()
    
    if success:
        print(f"✅ API call succeeded on attempt {retry_count + 1}")
        break
    
    retry_count += 1
    print(f"❌ Attempt {retry_count} failed. Retrying in {wait_seconds}s...")
    time.sleep(wait_seconds)
    wait_seconds *= 2   # exponential backoff: 1s, 2s, 4s, 8s, 16s
else:
    print("🚨 All retries exhausted. Alert on-call engineer.")
```

### Real-World Example — Queue Consumer

```python
from collections import deque

task_queue = deque(["send_email", "resize_image", "generate_report"])

while task_queue:
    task = task_queue.popleft()
    print(f"Processing task: {task}")
    # do_task(task)

print("Queue empty. Worker idle.")
```

### Real-World Example — Simple CLI Menu

```python
def show_menu():
    print("\n=== MAIN MENU ===")
    print("1. View profile")
    print("2. Edit profile")
    print("3. Change password")
    print("4. Logout")

while True:
    show_menu()
    choice = input("Choose an option: ").strip()
    
    if choice == "1":
        print("Showing profile...")
    elif choice == "2":
        print("Opening editor...")
    elif choice == "3":
        print("Password change flow...")
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
```

### Infinite Loop — `while True`

`while True` isn't bad — it's a common and valid pattern. The key is that there must be a clear `break` condition inside.

```python
# Web server main loop (simplified)
while True:
    request = server.accept()      # blocks until request arrives
    if request is None:
        continue
    response = handle(request)
    server.send(response)
```

Real servers, daemon processes, and background workers use `while True` loops extensively.

---

## 7. Loop Control — break / continue / pass / else

### `break` — Exit the Loop Immediately

When Python hits `break`, it exits the innermost loop entirely. Code after the loop continues.

```python
# Search for first admin user
users = ["alice", "bob", "admin_carol", "dave"]

for user in users:
    if user.startswith("admin_"):
        print(f"Found admin: {user}")
        break
else:
    print("No admin found")
```

```
Flow diagram:
[alice]  → not admin → continue loop
[bob]    → not admin → continue loop
[admin_carol] → FOUND → print → BREAK → exit loop
[dave]   → never reached
```

### `continue` — Skip to Next Iteration

`continue` skips the rest of the current iteration's body and moves to the next one.

```python
# Process only valid records, skip bad ones
records = [
    {"id": 1, "email": "anil@x.com", "active": True},
    {"id": 2, "email": None, "active": True},           # invalid
    {"id": 3, "email": "bob@x.com", "active": False},   # inactive
    {"id": 4, "email": "carol@x.com", "active": True},
]

for record in records:
    if not record["email"]:
        print(f"⚠ Record {record['id']}: Missing email — skipping")
        continue
    if not record["active"]:
        print(f"⚠ Record {record['id']}: Inactive — skipping")
        continue
    print(f"✅ Processing record {record['id']}: {record['email']}")
```

Output:
```
✅ Processing record 1: anil@x.com
⚠ Record 2: Missing email — skipping
⚠ Record 3: Inactive — skipping
✅ Processing record 4: carol@x.com
```

### `pass` — Intentional No-Op

`pass` does absolutely nothing. It's a placeholder — useful when Python's syntax requires a block but you have nothing to put there yet.

```python
# TODO stubs — design first, implement later
class UserService:
    def create_user(self, data):
        pass   # implement later

    def delete_user(self, user_id):
        pass

# Silently ignore specific exceptions
for item in items:
    try:
        process(item)
    except TemporaryError:
        pass   # will be retried later

# Empty conditional branch
for log in system_logs:
    if log.level == "DEBUG":
        pass   # ignore debug logs in production
    else:
        send_to_monitoring(log)
```

> **Observation:** `pass` is different from `continue`. `pass` does nothing and the loop body continues. `continue` skips to the next iteration.

### The `else` Clause on Loops — Python's Hidden Feature

Python has a lesser-known `else` clause on `for` and `while` loops. The `else` block runs **only if the loop completed without hitting a `break`**.

```python
# Search scenario — did we find it or not?
target = 7
numbers = [2, 4, 6, 8, 10]

for num in numbers:
    if num == target:
        print(f"Found {target}!")
        break
else:
    print(f"{target} not found in the list.")

# Output: 7 not found in the list.
```

```python
# Login attempt with max retries
MAX_ATTEMPTS = 3
correct_password = "secret"

for attempt in range(1, MAX_ATTEMPTS + 1):
    password = input(f"Password (attempt {attempt}/{MAX_ATTEMPTS}): ")
    if password == correct_password:
        print("Access granted.")
        break
else:
    print("Too many failed attempts. Account locked.")
```

This pattern is much cleaner than using a flag variable like `found = False`.

### `break` vs `continue` vs `pass` — Side by Side

```
LOOP ITERATION:
┌────────────────────────────────────────────────────┐
│  for item in collection:                           │
│      if condition:                                 │
│          break     → EXIT loop entirely            │
│          continue  → SKIP to next iteration        │
│          pass      → DO NOTHING, continue normally │
│      rest_of_body  ← pass reaches here, continue doesn't │
└────────────────────────────────────────────────────┘
```

---

## 8. Iterators & Iterables — What Happens Under the Hood

Understanding this makes you a much stronger Python programmer. It explains why `for` loops work with so many different types.

### Iterable vs Iterator

```
ITERABLE                       ITERATOR
────────                       ────────
An object that CAN be          An object that PRODUCES
iterated over.                 items one at a time.

Has __iter__() method          Has __iter__() AND __next__()
that returns an iterator.      methods.

Examples:                      Examples:
- list, str, dict, set         - what iter(list) returns
- range, tuple, file           - generators
- any custom class             - map(), filter(), zip() objects
  with __iter__
```

```python
# Every for loop does this internally:
my_list = [10, 20, 30]
iterator = iter(my_list)       # calls my_list.__iter__()
print(next(iterator))          # 10
print(next(iterator))          # 20
print(next(iterator))          # 30
print(next(iterator))          # raises StopIteration → loop ends
```

```python
# Checking if something is iterable
from collections.abc import Iterable

print(isinstance([1,2,3], Iterable))   # True
print(isinstance("hello", Iterable))   # True
print(isinstance(42, Iterable))        # False
```

### Why This Matters

```python
# range() is lazy — doesn't store all numbers in memory
r = range(1, 1_000_000)
print(sys.getsizeof(r))   # ~48 bytes — always the same!

# List stores everything
l = list(range(1, 1_000_000))
print(sys.getsizeof(l))   # ~8 MB

# map(), filter(), zip() are also lazy iterators
squares = map(lambda x: x**2, range(1_000_000))
# Nothing computed yet — only when you iterate
```

This lazy evaluation is how Python handles big data efficiently. You never load 10 million records into memory at once — you process them one at a time.

---

## 9. List Comprehensions — Deep Dive

### The Pattern

List comprehensions give you a concise, readable way to build lists. They're one of the most distinctly "Pythonic" features.

```python
# Traditional loop approach:
result = []
for item in iterable:
    if condition:
        result.append(expression)

# List comprehension — equivalent and more readable:
result = [expression for item in iterable if condition]
```

### Progressive Examples

```python
# 1. Basic transformation
squares = [x ** 2 for x in range(1, 11)]
# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# 2. With filter condition
even_squares = [x ** 2 for x in range(1, 11) if x % 2 == 0]
# [4, 16, 36, 64, 100]

# 3. String transformation
names = ["  alice", "BOB  ", "   carol  "]
cleaned = [name.strip().title() for name in names]
# ["Alice", "Bob", "Carol"]

# 4. Conditional expression in the output
grades = [85, 42, 91, 55, 73, 38]
results = ["Pass" if g >= 50 else "Fail" for g in grades]
# ["Pass", "Fail", "Pass", "Pass", "Pass", "Fail"]

# 5. Working with dict items
inventory = {"laptop": 5, "mouse": 0, "keyboard": 12, "monitor": 0}
in_stock = [item for item, qty in inventory.items() if qty > 0]
# ["laptop", "keyboard"]
```

### Real-World Examples

```python
# Extract all email addresses from a list of user dicts
users = [
    {"name": "Anil", "email": "anil@company.com", "active": True},
    {"name": "Bob", "email": "bob@company.com", "active": False},
    {"name": "Carol", "email": "carol@company.com", "active": True},
]

active_emails = [u["email"] for u in users if u["active"]]
# ["anil@company.com", "carol@company.com"]

# Normalize file extensions
filenames = ["report.PDF", "data.CSV", "script.py", "notes.TXT"]
normalized = [f.lower() for f in filenames]

# Extract only Python files
py_files = [f for f in filenames if f.lower().endswith(".py")]

# Parse log file — extract error lines
log_lines = [
    "INFO 2026-05-11 Server started",
    "ERROR 2026-05-11 Connection timeout",
    "INFO 2026-05-11 Request processed",
    "ERROR 2026-05-11 DB query failed",
]
errors = [line for line in log_lines if line.startswith("ERROR")]
```

### Flat Map Pattern — Flatten Nested Lists

```python
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flat = [item for sublist in nested for item in sublist]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

The order reads left to right, mirroring the nested loop structure:
```python
# Equivalent to:
flat = []
for sublist in nested:
    for item in sublist:
        flat.append(item)
```

### When NOT to Use List Comprehensions

```python
# ❌ Too complex — hard to read
result = [transform(x) for x in data if valid(x) and x.attr > threshold and x not in seen]

# ✅ Better as a regular loop
result = []
for x in data:
    if not valid(x):
        continue
    if x.attr <= threshold:
        continue
    if x in seen:
        continue
    result.append(transform(x))
```

Rule of thumb: if the comprehension doesn't fit comfortably on one line, or if you need to explain what it does, use a regular loop.

---

## 10. Dict, Set & Generator Comprehensions

### Dict Comprehension

```python
# Syntax:
{key_expr: value_expr for item in iterable if condition}

# Examples:
# Square lookup table
squares = {x: x**2 for x in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Invert a dictionary (swap keys and values)
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
# {1: "a", 2: "b", 3: "c"}

# Filter a dict
inventory = {"laptop": 5, "mouse": 0, "keyboard": 3}
available = {k: v for k, v in inventory.items() if v > 0}
# {"laptop": 5, "keyboard": 3}

# Normalize config keys
raw_config = {"HOST": "localhost", "PORT": "5432", "DB_NAME": "sprox"}
config = {k.lower(): v for k, v in raw_config.items()}
# {"host": "localhost", "port": "5432", "db_name": "sprox"}
```

### Set Comprehension

```python
# Syntax:
{expression for item in iterable if condition}

# Unique domains from email list
emails = ["anil@gmail.com", "bob@yahoo.com", "carol@gmail.com", "dave@outlook.com"]
domains = {email.split("@")[1] for email in emails}
# {"gmail.com", "yahoo.com", "outlook.com"}

# Unique word lengths in a sentence
sentence = "the quick brown fox jumps over the lazy dog"
word_lengths = {len(w) for w in sentence.split()}
# {3, 4, 5}
```

### Generator Expressions — Memory-Efficient Iteration

A generator expression looks like a list comprehension but uses `()` instead of `[]`. Crucially, it **doesn't create the full list in memory** — it generates items one at a time on demand.

```python
# List comprehension — computes everything now, stores in memory
squares_list = [x**2 for x in range(1_000_000)]   # uses ~8MB RAM

# Generator expression — computes lazily, uses almost no memory
squares_gen = (x**2 for x in range(1_000_000))    # uses ~120 bytes

# Both work the same way when you iterate
for sq in squares_gen:
    process(sq)
```

```python
# Most efficient: pass generator directly to sum/max/min/any/all
total = sum(x**2 for x in range(1000))           # no intermediate list
any_over_100 = any(x > 100 for x in data)        # stops early on first True
largest = max(len(line) for line in file_lines)  # streaming
```

> **Real-world use:** When reading a 2GB log file, you never load it all into memory. You use a generator to stream line by line. This is the difference between a script that works and one that crashes your server.

---

## 11. Nested Loops & Nested Comprehensions

### Nested `for` Loops

```python
# Multiplication table
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} × {j} = {i*j}", end="  ")
    print()

# Output:
# 1 × 1 = 1  1 × 2 = 2  1 × 3 = 3
# 2 × 1 = 2  2 × 2 = 4  2 × 3 = 6
# 3 × 1 = 3  3 × 2 = 6  3 × 3 = 9
```

### Star Pattern — Classic Interview Question

```python
rows = 5

# Right triangle
for i in range(1, rows + 1):
    print("*" * i)

# Inverted triangle
for i in range(rows, 0, -1):
    print("*" * i)

# Pyramid
for i in range(1, rows + 1):
    spaces = " " * (rows - i)
    stars = "*" * (2 * i - 1)
    print(spaces + stars)
```

### Nested List Comprehension — Matrix Operations

```python
# Create a 3×3 matrix
matrix = [[i * 3 + j for j in range(1, 4)] for i in range(3)]
# [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Transpose a matrix (rows become columns)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

### Real-World — Generating Report Combinations

```python
regions = ["North", "South", "East"]
quarters = ["Q1", "Q2", "Q3", "Q4"]

report_keys = [f"{region}_{q}" for region in regions for q in quarters]
# ["North_Q1", "North_Q2", ..., "East_Q4"]
```

---

## 12. Common Patterns & Anti-Patterns

### Pattern 1 — Accumulator Pattern

```python
# Sum, count, collect
total = 0
count = 0
errors = []

for record in records:
    if record.is_valid():
        total += record.amount
        count += 1
    else:
        errors.append(record.id)

average = total / count if count > 0 else 0
```

### Pattern 2 — Guard Clause (Early Exit)

```python
# ❌ Arrow anti-pattern — deeply nested
def process_order(order):
    if order:
        if order.is_paid:
            if order.in_stock:
                if not order.is_cancelled:
                    ship(order)

# ✅ Guard clauses — flat and readable
def process_order(order):
    if not order:
        return
    if not order.is_paid:
        return
    if not order.in_stock:
        return
    if order.is_cancelled:
        return
    ship(order)
```

### Pattern 3 — Find First Match

```python
# Using next() with a generator — stops at first match
users = [{"id": 1, "name": "Anil"}, {"id": 2, "name": "Bob"}, {"id": 3, "name": "Carol"}]

target_id = 2
user = next((u for u in users if u["id"] == target_id), None)

if user:
    print(f"Found: {user['name']}")
else:
    print("User not found")
```

This is much more efficient than building a full list when you only need the first match.

### Pattern 4 — Grouping with a Dict

```python
# Group employees by department
employees = [
    {"name": "Anil", "dept": "Engineering"},
    {"name": "Bob", "dept": "Marketing"},
    {"name": "Carol", "dept": "Engineering"},
    {"name": "Dave", "dept": "Marketing"},
    {"name": "Eve", "dept": "Engineering"},
]

by_dept = {}
for emp in employees:
    dept = emp["dept"]
    if dept not in by_dept:
        by_dept[dept] = []
    by_dept[dept].append(emp["name"])

# Or more Pythonically:
from collections import defaultdict
by_dept = defaultdict(list)
for emp in employees:
    by_dept[emp["dept"]].append(emp["name"])

# {"Engineering": ["Anil", "Carol", "Eve"], "Marketing": ["Bob", "Dave"]}
```

### Anti-Patterns to Avoid

```python
# ❌ Modifying a list while iterating it
for item in my_list:
    if condition(item):
        my_list.remove(item)   # skips items, unpredictable behavior

# ✅ Iterate over a copy, or use comprehension
my_list = [item for item in my_list if not condition(item)]

# ❌ Using range(len()) when you need items
for i in range(len(items)):
    process(items[i])

# ✅ Iterate directly
for item in items:
    process(item)

# ❌ Checking for empty collection the verbose way
if len(my_list) == 0:

# ✅ Pythonic
if not my_list:

# ❌ Catching all exceptions blindly
try:
    risky()
except:
    pass   # hides real errors

# ✅ Catch specific exceptions
try:
    risky()
except ValueError as e:
    handle_error(e)
```

---

## 13. Hands-On Exercises (All 20+)

### if/elif/else Exercises

**1. Positive / Negative / Zero**
```python
n = int(input("Enter a number: "))
if n > 0:
    print("Positive")
elif n < 0:
    print("Negative")
else:
    print("Zero")
```

**2. Age Category**
```python
age = int(input("Enter age: "))
if age < 0:
    print("Invalid age")
elif age < 13:
    print("Child")
elif age < 18:
    print("Teenager")
elif age < 60:
    print("Adult")
else:
    print("Senior")
```

**3. Strong Password Validator**
```python
import re

password = input("Enter password: ")
issues = []

if len(password) < 8:
    issues.append("at least 8 characters")
if not any(c.isupper() for c in password):
    issues.append("at least one uppercase letter")
if not any(c.islower() for c in password):
    issues.append("at least one lowercase letter")
if not any(c.isdigit() for c in password):
    issues.append("at least one number")
if not any(c in "!@#$%^&*()" for c in password):
    issues.append("at least one special character")

if issues:
    print("Weak password. Must contain: " + ", ".join(issues))
else:
    print("Strong password ✅")
```

**4. Leap Year Check**
```python
year = int(input("Enter year: "))
is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
print(f"{year} is {'a leap' if is_leap else 'not a leap'} year.")
```

### for Loop Exercises

**5. Sum of First N Numbers**
```python
n = int(input("Enter N: "))
total = sum(range(1, n + 1))
print(f"Sum of 1 to {n}: {total}")
# Compare with Gauss formula: n*(n+1)//2
```

**6. Print All Vowels in a String**
```python
text = input("Enter text: ")
vowels = [c for c in text.lower() if c in "aeiou"]
print(f"Vowels found: {vowels}")
print(f"Count: {len(vowels)}")
```

**7. Star Patterns**
```python
rows = int(input("Rows: "))

print("Right Triangle:")
for i in range(1, rows + 1):
    print("*" * i)

print("\nPyramid:")
for i in range(1, rows + 1):
    print(" " * (rows - i) + "*" * (2 * i - 1))
```

**8. Count Uppercase and Lowercase**
```python
text = input("Enter text: ")
upper = sum(1 for c in text if c.isupper())
lower = sum(1 for c in text if c.islower())
digits = sum(1 for c in text if c.isdigit())
others = len(text) - upper - lower - digits

print(f"Uppercase: {upper}")
print(f"Lowercase: {lower}")
print(f"Digits:    {digits}")
print(f"Others:    {others}")
```

### while Loop Exercises

**9. Reverse a Number**
```python
num = int(input("Enter a number: "))
original = num
reversed_num = 0
while num > 0:
    digit = num % 10
    reversed_num = reversed_num * 10 + digit
    num //= 10
print(f"Reversed: {reversed_num}")
print(f"Palindrome: {original == reversed_num}")
```

**10. Input Until "exit"**
```python
items = []
print("Enter items (type 'exit' to stop):")
while True:
    item = input("> ").strip()
    if item.lower() == "exit":
        break
    if item:
        items.append(item)

print(f"\nYou entered {len(items)} items:")
for i, item in enumerate(items, 1):
    print(f"  {i}. {item}")
```

**11. Password Guess Game**
```python
import hashlib

correct_hash = hashlib.sha256("python2026".encode()).hexdigest()
max_attempts = 3

for attempt in range(1, max_attempts + 1):
    guess = input(f"Password ({attempt}/{max_attempts}): ")
    if hashlib.sha256(guess.encode()).hexdigest() == correct_hash:
        print("✅ Correct! Access granted.")
        break
else:
    print("❌ Too many attempts. Account locked.")
```

### break/continue/pass Exercises

**12. Skip Multiples of 4**
```python
skipped = []
printed = []
for n in range(1, 21):
    if n % 4 == 0:
        skipped.append(n)
        continue
    printed.append(n)

print("Printed:", printed)
print("Skipped:", skipped)
```

**13. Stop at Number 13**
```python
for n in range(1, 50):
    if n == 13:
        print(f"⚠ Found 13 at position {n}. Stopping.")
        break
    print(n, end=" ")
```

**14. Pass in Empty Function Stubs**
```python
class PaymentService:
    def charge(self, amount, card):
        pass   # TODO: implement Stripe integration

    def refund(self, transaction_id):
        pass   # TODO: implement refund logic

    def get_history(self, user_id):
        pass   # TODO: implement DB query
```

### List Comprehension Exercises

**15. Cubes for 1–10**
```python
cubes = [x**3 for x in range(1, 11)]
print(cubes)
```

**16. Words Starting With 'A'**
```python
words = ["apple", "banana", "avocado", "cherry", "apricot", "blueberry"]
a_words = [w for w in words if w.lower().startswith("a")]
print(a_words)
```

**17. Number List to String List**
```python
numbers = [1, 2, 3, 42, 100]
str_nums = [str(n) for n in numbers]
print(str_nums)
csv_line = ",".join(str_nums)
print(csv_line)
```

**18. Even Numbers from User Input**
```python
raw = input("Enter numbers separated by spaces: ")
numbers = list(map(int, raw.split()))
evens = [n for n in numbers if n % 2 == 0]
print(f"Even numbers: {evens}")
```

### Combined Logic Exercises

**19. Basic ATM Menu**
```python
balance = 10000.0

while True:
    print("\n=== ATM ===")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Choose: ").strip()

    if choice == "1":
        print(f"Balance: ₹{balance:,.2f}")

    elif choice == "2":
        try:
            amount = float(input("Deposit amount: ₹"))
            if amount <= 0:
                print("Amount must be positive.")
            else:
                balance += amount
                print(f"Deposited ₹{amount:,.2f}. New balance: ₹{balance:,.2f}")
        except ValueError:
            print("Invalid amount.")

    elif choice == "3":
        try:
            amount = float(input("Withdraw amount: ₹"))
            if amount <= 0:
                print("Amount must be positive.")
            elif amount > balance:
                print("Insufficient funds.")
            else:
                balance -= amount
                print(f"Dispensing ₹{amount:,.2f}. Remaining: ₹{balance:,.2f}")
        except ValueError:
            print("Invalid amount.")

    elif choice == "4":
        print("Thank you. Goodbye!")
        break

    else:
        print("Invalid option. Try again.")
```

**20. Login System with Max Attempts**
```python
USERS = {
    "anil": "dev@2026",
    "admin": "superSecret!",
}
MAX_ATTEMPTS = 3

for attempt in range(1, MAX_ATTEMPTS + 1):
    username = input("Username: ").strip().lower()
    password = input("Password: ")

    if username in USERS and USERS[username] == password:
        print(f"\n✅ Welcome, {username}! Login successful.")
        break
    else:
        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print(f"❌ Invalid credentials. {remaining} attempt(s) remaining.")
        else:
            print("❌ Account temporarily locked. Try again later.")
else:
    pass   # already handled inside loop
```

---

## 14. Mini Project — Number Guessing Game (Enhanced)

This enhanced version adds difficulty levels, a score system, hint quality based on remaining attempts, and a replay loop.

```python
import random

def get_hint(guess, secret, attempts_left):
    """Give progressively more helpful hints as attempts run low."""
    diff = abs(guess - secret)
    direction = "higher" if guess < secret else "lower"
    
    if diff == 0:
        return "Exactly right!"
    elif diff <= 2 and attempts_left <= 2:
        return f"Extremely close! Go {direction}."
    elif diff <= 5:
        return f"Very close! Go {direction}."
    elif diff <= 10:
        return f"Getting warm. Go {direction}."
    elif diff <= 20:
        return f"A bit off. Go {direction}."
    else:
        return f"Way off. Go {direction}."

def play_round(difficulty):
    """Play one round of the guessing game."""
    settings = {
        "easy":   {"range": (1, 50),  "attempts": 10},
        "medium": {"range": (1, 100), "attempts": 7},
        "hard":   {"range": (1, 200), "attempts": 5},
    }
    
    cfg = settings[difficulty]
    low, high = cfg["range"]
    max_attempts = cfg["attempts"]
    
    secret = random.randint(low, high)
    print(f"\nGuess the number between {low} and {high}. You have {max_attempts} attempts.")
    
    for attempt in range(1, max_attempts + 1):
        attempts_left = max_attempts - attempt
        
        while True:
            try:
                guess = int(input(f"Attempt {attempt}/{max_attempts}: "))
                if low <= guess <= high:
                    break
                print(f"Please enter a number between {low} and {high}.")
            except ValueError:
                print("Enter a valid integer.")
        
        if guess == secret:
            score = max(10, (max_attempts - attempt + 1) * 10)
            print(f"\n🎉 Correct! You guessed it in {attempt} attempt(s).")
            print(f"Score: {score} points")
            return score
        else:
            hint = get_hint(guess, secret, attempts_left)
            print(f"  → {hint} ({attempts_left} attempts left)")
    
    print(f"\n❌ Out of attempts! The number was {secret}.")
    return 0

def main():
    print("=" * 40)
    print("     NUMBER GUESSING GAME")
    print("=" * 40)
    
    total_score = 0
    rounds_played = 0
    
    while True:
        print("\nDifficulty: easy / medium / hard")
        difficulty = input("Choose difficulty: ").strip().lower()
        
        if difficulty not in ("easy", "medium", "hard"):
            print("Invalid choice. Defaulting to medium.")
            difficulty = "medium"
        
        score = play_round(difficulty)
        total_score += score
        rounds_played += 1
        
        print(f"\nTotal score after {rounds_played} round(s): {total_score}")
        
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            break
    
    print(f"\nFinal score: {total_score} across {rounds_played} round(s). Thanks for playing!")

main()
```

---

## Quick Reference — Control Flow Cheat Sheet

```
CONDITIONALS:
  if condition:           → runs if True
  elif other_condition:   → runs if above is False and this is True
  else:                   → runs if nothing matched
  x if cond else y        → ternary / inline
  match val: case ...:    → structural pattern matching (3.10+)

LOOPS:
  for item in iterable:   → known iterations
  while condition:        → unknown iterations
  while True: ... break   → loop-and-a-half pattern

LOOP CONTROL:
  break      → exit loop entirely
  continue   → skip current iteration, go to next
  pass       → do nothing (placeholder)
  for/else   → else runs only if loop didn't break

COMPREHENSIONS:
  [expr for x in it]           → list
  [expr for x in it if cond]   → list with filter
  {k: v for x in it}           → dict
  {expr for x in it}           → set
  (expr for x in it)           → generator (lazy)
```

| Pattern | Use When |
|---------|----------|
| Guard clause / early return | Validation, multiple preconditions |
| `for/else` | Search problems (did we find it?) |
| Generator expression | Large datasets, streaming |
| `enumerate()` | Need index + item together |
| `zip()` | Parallel iteration over multiple sequences |
| `while True` + `break` | Menu loops, event loops, retry loops |
| `next(gen, default)` | Find first match efficiently |

---

*Notes compiled for SDE Track — Python Full Stack | Day 2*
