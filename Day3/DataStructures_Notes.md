# 🐍 DAY 3 — Python Data Structures 

---

## 📌 Table of Contents

1. [Big Picture — Why Data Structures Matter](#big-picture)
2. [Lists](#lists)
3. [Tuples](#tuples)
4. [Sets](#sets)
5. [Dictionaries](#dictionaries)
6. [Nested Data Structures](#nested-data-structures)
7. [Comprehensions](#comprehensions)
8. [Choosing the Right Structure](#choosing-the-right-structure)
9. [Memory & Performance Notes](#memory-and-performance)
10. [Hands-On Exercises](#hands-on-exercises)
11. [Mini Project — Text Analyzer](#mini-project)

---

## 🗺️ Big Picture — Why Data Structures Matter {#big-picture}

Before diving in, it helps to see how all four structures relate to each other.

```
┌─────────────────────────────────────────────────────────┐
│               Python Built-in Data Structures           │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │   LIST   │  │  TUPLE   │  │   SET    │  │  DICT  │  │
│  │          │  │          │  │          │  │        │  │
│  │ ordered  │  │ ordered  │  │unordered │  │key-val │  │
│  │ mutable  │  │immutable │  │ mutable  │  │mutable │  │
│  │duplicates│  │duplicates│  │ unique   │  │unique  │  │
│  │  ✅      │  │  ✅      │  │  ❌      │  │ keys   │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘  │
│                                                         │
│   Think of it as:                                       │
│   List   → Shopping cart (ordered, changeable)          │
│   Tuple  → GPS coordinates (fixed, don't change it)     │
│   Set    → VIP guest list (no duplicates allowed)       │
│   Dict   → Employee ID card (lookup by unique key)      │
└─────────────────────────────────────────────────────────┘
```

---

## 🟦 1. Lists {#lists}

### What is a List?

A list is a mutable, ordered, indexed collection. Think of it like a to-do list on paper — you can add items, cross things out, reorder, and check specific lines.

```python
fruits = ["apple", "banana", "mango"]
mixed  = [1, "hello", 3.14, True]   # lists can hold mixed types
empty  = []
```

### Key Characteristics

| Property | Details |
|----------|---------|
| Ordered | Yes — index-based access, insertion order preserved |
| Mutable | Yes — items can be added, changed, removed |
| Duplicates | Allowed |
| Indexing | 0-based (also supports negative indexing) |
| Memory | Dynamic array — resizes as needed |

### Indexing & Slicing

```python
fruits = ["apple", "banana", "mango", "grapes", "kiwi"]

# Indexing
fruits[0]      # "apple"    (first item)
fruits[-1]     # "kiwi"     (last item)
fruits[-2]     # "grapes"   (second from last)

# Slicing  [start : stop : step]
fruits[1:3]    # ["banana", "mango"]   stop is exclusive
fruits[:2]     # ["apple", "banana"]
fruits[2:]     # ["mango", "grapes", "kiwi"]
fruits[::2]    # ["apple", "mango", "kiwi"]  every 2nd item
fruits[::-1]   # ["kiwi", "grapes", "mango", "banana", "apple"]  reversed
```

> **Observation:** Slicing never modifies the original list. It always returns a new list. This is a common source of confusion for beginners.

### Common List Methods

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]

nums.append(7)           # [3,1,4,1,5,9,2,6,7]    — add to end
nums.insert(0, 0)        # [0,3,1,4,1,5,9,2,6,7]  — insert at index
nums.extend([10, 11])    # adds multiple items at end
nums.remove(1)           # removes FIRST occurrence of 1
nums.pop()               # removes & returns last item
nums.pop(2)              # removes & returns item at index 2
nums.sort()              # sorts in-place (modifies original)
nums.reverse()           # reverses in-place
nums.count(1)            # how many times 1 appears
nums.index(5)            # index of first 5
nums.copy()              # shallow copy
nums.clear()             # empties the list
```

**`sort()` vs `sorted()`** — A key distinction:

```python
original = [3, 1, 4, 1, 5]

# sort() modifies IN PLACE — original changes
original.sort()               # original is now [1,1,3,4,5]

# sorted() returns a NEW list — original unchanged
new_sorted = sorted(original) # original untouched
```

### Real-Time Industry Examples

**1. API Response Handling**

APIs almost always return lists of objects. When you call a REST endpoint for a list of users, you get back something like:

```python
users = [
    {"id": 1, "name": "Priya",  "role": "admin"},
    {"id": 2, "name": "Ravi",   "role": "user"},
    {"id": 3, "name": "Meera",  "role": "user"},
]

# Get all admin names
admins = [u["name"] for u in users if u["role"] == "admin"]
# ["Priya"]
```

**2. Log File Processing**

```python
with open("server.log") as f:
    lines = f.readlines()              # each line becomes a list item

errors   = [l for l in lines if "ERROR" in l]
warnings = [l for l in lines if "WARN"  in l]
```

**3. ML Data Preprocessing**

Before NumPy/Pandas enters the picture, raw data lives in plain Python lists:

```python
raw_scores    = [23, 45, None, 67, None, 89]
clean_scores  = [x for x in raw_scores if x is not None]
normalized    = [x / max(clean_scores) for x in clean_scores]
```

**4. DevOps — Parsing Command Output**

```python
import subprocess
output = subprocess.check_output(["ls", "-la"]).decode()
lines  = output.split("\n")
py_files = [l for l in lines if l.endswith(".py")]
```

### Observations Worth Remembering

- `append()` is O(1) amortized. `insert(0, x)` is O(n) because every element shifts — avoid inserting at the front of large lists.
- Multiplying a list `[0] * 5` gives `[0,0,0,0,0]` but be careful with nested lists — `[[]] * 3` creates three references to the SAME inner list, not three separate ones.
- `in` operator on a list is O(n). If you're doing many membership checks, convert to a set first.

---

## 🟪 2. Tuples {#tuples}

### What is a Tuple?

A tuple is an immutable, ordered collection. Once you create it, you cannot change it. Think of it like a record in a database or a row returned from a SQL query.

```python
location   = ("Hyderabad", 500032)
rgb_color  = (255, 165, 0)       # orange
single     = (42,)               # note the trailing comma — without it, it's just int 42
empty      = ()
```

> **Common Gotcha:** `(42)` is just the integer `42`. You need `(42,)` to create a single-element tuple. The comma makes it a tuple, not the parentheses.

### Key Characteristics

| Property | Details |
|----------|---------|
| Ordered | Yes |
| Mutable | No — cannot add/remove/change after creation |
| Duplicates | Allowed |
| Speed | Faster than lists for iteration |
| Hashable | Yes (if contents are hashable) — can be used as dict keys |

### Tuple Packing & Unpacking

This is one of the most useful features of tuples and Python uses it everywhere:

```python
# Packing
point = 10, 20           # automatically packed into a tuple (10, 20)

# Unpacking
x, y = point             # x=10, y=20

# Extended unpacking
first, *rest = (1, 2, 3, 4, 5)
# first = 1,  rest = [2, 3, 4, 5]

# Swap two variables without a temp variable
a, b = 5, 10
a, b = b, a              # a=10, b=5  — pure Python elegance
```

### Named Tuples — Tuples with Context

Plain tuples can get confusing: what does `record[2]` mean? `collections.namedtuple` solves this:

```python
from collections import namedtuple

Employee = namedtuple("Employee", ["name", "age", "department"])
emp = Employee("Anjali", 29, "Engineering")

print(emp.name)          # "Anjali"   — readable!
print(emp[0])            # "Anjali"   — still works like a regular tuple
print(emp._asdict())     # OrderedDict for easy JSON conversion
```

### Real-Time Industry Examples

**1. Database Row Representation**

When you query a database using raw DB-API connectors (like `psycopg2` for PostgreSQL), rows come back as tuples:

```python
import psycopg2
cursor.execute("SELECT id, name, salary FROM employees")
rows = cursor.fetchall()
# rows = [(1, "Ravi", 85000), (2, "Priya", 92000)]

for emp_id, name, salary in rows:   # unpack directly in for loop
    print(f"{name} earns {salary}")
```

**2. Geolocation & Coordinates**

```python
# Cities
hyderabad = (17.3850, 78.4867)
bangalore = (12.9716, 77.5946)

# Distance calculation (simplified)
import math
def distance(c1, c2):
    return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)
```

**3. Function Multiple Returns**

Python functions technically return a single object. When you write `return a, b`, you're returning a tuple. The caller unpacks it:

```python
def get_min_max(data):
    return min(data), max(data)       # returns a tuple

lo, hi = get_min_max([3, 7, 1, 9])   # lo=1, hi=9
```

**4. Dictionary Keys (Composite Keys)**

Since tuples are hashable, they can be dictionary keys. Useful for multi-dimensional lookups:

```python
# Sales by (region, quarter)
sales = {
    ("North", "Q1"): 150000,
    ("South", "Q1"): 95000,
    ("North", "Q2"): 178000,
}
print(sales[("North", "Q2")])    # 178000
```

### When to Use Tuples vs Lists

```
Use a TUPLE when:                    Use a LIST when:
─────────────────────────────────    ──────────────────────────────
Data shouldn't change (coords,       Data will grow/shrink
DB rows, config constants)

You want to use it as a dict key     You need sort/insert/remove

Returning multiple values from       Order matters AND you'll
a function                           modify it later

Performance matters for large        You need index-based mutation
read-only datasets
```

---

## 🟨 3. Sets {#sets}

### What is a Set?

A set is an unordered collection of unique elements. It's inspired directly by mathematical sets. Under the hood, Python implements sets using hash tables, which is why membership testing is extremely fast.

```python
skills   = {"python", "sql", "docker", "python"}  # duplicate "python" dropped
print(skills)  # {"python", "sql", "docker"}  — order not guaranteed

empty_set = set()    # NOT {} — that creates an empty dict!
```

> **Common Mistake:** `{}` creates an empty dictionary, not an empty set. Always use `set()` for an empty set.

### Key Characteristics

| Property | Details |
|----------|---------|
| Ordered | No — no index access |
| Mutable | Yes (use `frozenset` for immutable version) |
| Duplicates | Not allowed — silently discarded |
| Membership test | O(1) — extremely fast |
| Elements must be | Hashable (so no lists inside a set) |

### Set Operations (Mathematical)

```
Set A = {1, 2, 3, 4}
Set B = {3, 4, 5, 6}

Union (A | B)            → {1, 2, 3, 4, 5, 6}  — all elements
Intersection (A & B)     → {3, 4}               — common elements
Difference (A - B)       → {1, 2}               — in A but NOT in B
Symmetric Diff (A ^ B)   → {1, 2, 5, 6}         — in one but NOT both

Subset:   {3,4}.issubset(A)       → True
Superset: A.issuperset({3,4})     → True
Disjoint: A.isdisjoint({7,8})     → True (no common elements)
```

```python
team_a = {"alice", "bob", "charlie"}
team_b = {"bob", "diana", "charlie"}

both_teams = team_a & team_b       # {"bob", "charlie"}
only_team_a = team_a - team_b      # {"alice"}
all_members = team_a | team_b      # {"alice", "bob", "charlie", "diana"}
```

### Modifying Sets

```python
s = {1, 2, 3}
s.add(4)            # {1,2,3,4}
s.discard(10)       # no error if 10 not present
s.remove(2)         # raises KeyError if 2 not present
s.pop()             # removes and returns an arbitrary element
s.update([5, 6])    # add multiple elements
```

### Real-Time Industry Examples

**1. Deduplication — The Most Common Use Case**

```python
# Raw email list from a form — may have duplicates
raw_emails = [
    "user@example.com",
    "admin@company.com",
    "user@example.com",    # duplicate
    "hr@company.com",
]
unique_emails = list(set(raw_emails))
# ["user@example.com", "admin@company.com", "hr@company.com"]
```

**2. Access Control / Permissions**

```python
admin_permissions = {"read", "write", "delete", "manage_users"}
user_permissions  = {"read", "write"}
guest_permissions = {"read"}

# What can an admin do that a regular user can't?
extra_powers = admin_permissions - user_permissions
# {"delete", "manage_users"}

# Does this user have required permissions?
required = {"read", "write"}
has_access = required.issubset(user_permissions)  # True
```

**3. NLP — Stopword Filtering**

```python
stopwords = {"the", "and", "is", "of", "in", "a", "to", "it"}

text = "Python is the best language in the world"
words = text.lower().split()
filtered = [w for w in words if w not in stopwords]
# ["python", "best", "language", "world"]
```

> Using a set for `stopwords` is critical here. If it were a list, the `in` check would be O(n) per word. As a set, it's O(1) — massive speedup on large documents.

**4. Finding Shared Records Between Systems**

```python
# Users in two different databases after a company merger
db1_users = {"alice", "bob",   "charlie", "diana"}
db2_users = {"bob",   "diana", "eve",     "frank"}

common     = db1_users & db2_users    # need deduplication
only_db1   = db1_users - db2_users    # migrate to db2
only_db2   = db2_users - db1_users    # migrate to db1
all_unique = db1_users | db2_users    # merged set
```

### frozenset — The Immutable Set

```python
# Can be used as a dictionary key (regular set cannot)
permissions_key = frozenset({"read", "write"})
role_map = {
    frozenset({"read"}):               "viewer",
    frozenset({"read", "write"}):      "editor",
    frozenset({"read","write","admin"}): "admin",
}
```

---

## 🟧 4. Dictionaries {#dictionaries}

### What is a Dictionary?

A dictionary is a key-value store — Python's implementation of a hash map. It gives you the ability to look up any value in O(1) time if you know its key.

```python
user = {
    "name":   "Anil",
    "age":    28,
    "skills": ["Python", "AWS", "Docker"],
    "active": True,
}
```

### Key Characteristics

| Property | Details |
|----------|---------|
| Ordered | Yes (since Python 3.7+, insertion order preserved) |
| Mutable | Yes |
| Keys | Must be unique and hashable (strings, ints, tuples) |
| Values | Can be anything — even other dicts or lists |
| Lookup | O(1) average |

> **Historical note:** Before Python 3.7, dicts were unordered. If you're maintaining legacy code, be careful about relying on order.

### Accessing & Modifying

```python
config = {"host": "localhost", "port": 5432, "db": "myapp"}

# Access
config["host"]          # "localhost"
config.get("host")      # "localhost"   — same
config.get("user", "admin")   # "admin"  — returns default if key missing
config["host"]          # raises KeyError if key doesn't exist

# Modify
config["port"] = 3306          # update existing
config["timeout"] = 30         # add new key

# Delete
del config["timeout"]          # remove key
config.pop("db")               # remove and return value
config.pop("db", None)         # safe pop — no error if missing
```

### Common Dictionary Methods

```python
d = {"a": 1, "b": 2, "c": 3}

d.keys()         # dict_keys(["a","b","c"])
d.values()       # dict_values([1,2,3])
d.items()        # dict_items([("a",1),("b",2),("c",3)])

# Iterating
for key, value in d.items():
    print(f"{key} → {value}")

# Merging dicts
d1 = {"x": 1}
d2 = {"y": 2}
merged = {**d1, **d2}       # {"x":1, "y":2}  — spread operator
d1.update(d2)               # d1 is now {"x":1, "y":2}  modifies in place

# Python 3.9+ merge operator
merged = d1 | d2            # clean, readable
```

### defaultdict — Smarter Dictionaries

`collections.defaultdict` automatically creates a default value when a missing key is accessed. Saves a lot of `if key not in dict` boilerplate:

```python
from collections import defaultdict

# Grouping items
word_positions = defaultdict(list)
words = ["apple", "bat", "avocado", "banana", "air"]

for i, word in enumerate(words):
    word_positions[word[0]].append(word)

# {"a": ["apple","avocado","air"], "b": ["bat","banana"]}
```

### Counter — Frequency Counting

```python
from collections import Counter

votes = ["Alice", "Bob", "Alice", "Charlie", "Bob", "Alice"]
tally = Counter(votes)
# Counter({"Alice": 3, "Bob": 2, "Charlie": 1})

tally.most_common(2)   # [("Alice",3), ("Bob",2)]
```

### Real-Time Industry Examples

**1. JSON / REST API Data**

Almost every modern API communicates in JSON, which maps directly to Python dicts:

```python
# Response from a weather API
weather = {
    "city": "Hyderabad",
    "temp": 34,
    "conditions": {"humidity": 60, "wind_speed": 12},
    "forecast": [{"day": "Mon", "high": 36}, {"day": "Tue", "high": 33}]
}

# Navigate nested
humidity   = weather["conditions"]["humidity"]     # 60
monday_hi  = weather["forecast"][0]["high"]        # 36
```

**2. Application Configuration**

```python
DB_CONFIG = {
    "primary":  {"host": "db1.prod.internal", "port": 5432},
    "replica":  {"host": "db2.prod.internal", "port": 5432},
    "timeout":  30,
    "max_pool": 10,
}
```

**3. Caching / Memoization**

```python
cache = {}

def expensive_computation(n):
    if n in cache:
        return cache[n]
    result = sum(range(n))    # slow operation
    cache[n] = result
    return result
```

**4. ML Feature Vectors**

```python
# Each user described as features for a recommendation model
user_features = {
    "user_id":       "u_8821",
    "age_group":     2,       # 0=<18, 1=18-30, 2=30-50, 3=50+
    "purchase_freq": 0.73,
    "avg_spend":     1850.0,
    "preferred_cat": "electronics",
}
```

**5. Word Frequency Counter (Built Manually)**

```python
text = "to be or not to be that is the question"
freq = {}

for word in text.split():
    freq[word] = freq.get(word, 0) + 1
    
# {"to": 2, "be": 2, "or": 1, "not": 1, ...}
sorted_by_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
```

### Observations Worth Remembering

- Never modify a dictionary while iterating over it — use a copy or collect keys to delete separately.
- Dictionary lookups are O(1) on average but O(n) in worst case (hash collisions — rare in practice).
- If you need the number of times something appears, `Counter` is always cleaner than building it manually.
- `dict.get(key, default)` is almost always better than `dict[key]` in production code because it won't crash on missing keys.

---

## 🟦 5. Nested Data Structures {#nested-data-structures}

Real-world data is rarely flat. JSON responses from APIs, config files, ML datasets — they all nest structures inside each other.

### Common Nesting Patterns

```python
# Pattern 1: List of Dicts  (most common — API responses, DB results)
employees = [
    {"id": 1, "name": "Ravi",  "skills": ["Python", "SQL"]},
    {"id": 2, "name": "Priya", "skills": ["Java", "AWS", "Docker"]},
]

# Pattern 2: Dict of Lists  (grouping by category)
dept_employees = {
    "Engineering": ["Ravi", "Kiran", "Nisha"],
    "Marketing":   ["Anand", "Deepa"],
    "HR":          ["Sonia"],
}

# Pattern 3: Dict of Dicts  (hierarchical config)
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "credentials": {"user": "admin", "password": "secret"},
    },
    "cache": {"host": "redis-server", "ttl": 300},
}
```

### Traversing Nested Structures

```python
student = {
    "name": "Rahul",
    "scores": {"math": 90, "science": 84, "english": 78},
    "hobbies": ["cricket", "gaming", "reading"],
}

# Access
student["scores"]["math"]      # 90
student["hobbies"][1]          # "gaming"

# Safe deep access (avoid KeyError)
student.get("scores", {}).get("history", 0)   # 0 — subject not found, default 0

# Iterate nested
for subject, score in student["scores"].items():
    grade = "A" if score >= 85 else "B" if score >= 70 else "C"
    print(f"{subject}: {score} → {grade}")
```

### Working with Lists of Dicts (Very Common)

```python
products = [
    {"id": "p1", "name": "Laptop",     "price": 65000, "stock": 12},
    {"id": "p2", "name": "Mouse",      "price":   850, "stock": 0},
    {"id": "p3", "name": "Headphones", "price":  3200, "stock": 5},
]

# Filter: only in-stock items
in_stock   = [p for p in products if p["stock"] > 0]

# Sort by price descending
by_price   = sorted(products, key=lambda p: p["price"], reverse=True)

# Extract just names
names      = [p["name"] for p in products]

# Build a lookup dict by ID — very useful!
product_map = {p["id"]: p for p in products}
product_map["p2"]["name"]   # "Mouse" — O(1) access
```

### Deep Copy vs Shallow Copy (Critical to Understand)

```python
import copy

original = {"name": "Ravi", "scores": [90, 85, 78]}

# Shallow copy — nested objects are SHARED
shallow = original.copy()
shallow["scores"].append(100)
# original["scores"] is now [90,85,78,100] too! 😱

# Deep copy — completely independent
deep = copy.deepcopy(original)
deep["scores"].append(200)
# original is unaffected ✅
```

> **Industry Rule:** When working with nested structures you're about to modify, always ask yourself whether you need a shallow or deep copy. Silent shared-reference bugs are among the hardest to track down.

---

## 🟩 6. Comprehensions {#comprehensions}

Comprehensions are one of Python's most celebrated features. They let you build collections in a single, readable line — and they're generally faster than equivalent for-loops because they're optimized at the bytecode level.

### List Comprehension

```python
# Basic pattern: [expression for item in iterable if condition]

squares  = [x**2 for x in range(10)]
evens    = [x for x in range(20) if x % 2 == 0]
lengths  = [len(word) for word in ["hello", "world", "python"]]

# With transformation
names    = ["  alice ", "BOB  ", " charlie"]
clean    = [n.strip().title() for n in names]    # ["Alice", "Bob", "Charlie"]
```

**Nested List Comprehension** (flatten a 2D list):

```python
matrix = [[1,2,3], [4,5,6], [7,8,9]]
flat   = [cell for row in matrix for cell in row]
# [1,2,3,4,5,6,7,8,9]
```

### Dictionary Comprehension

```python
# {key_expr: value_expr for item in iterable if condition}

# Invert a dictionary
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
# {1:"a", 2:"b", 3:"c"}

# Build price map from product list
products   = [{"id": "p1", "price": 500}, {"id": "p2", "price": 300}]
price_map  = {p["id"]: p["price"] for p in products}
# {"p1": 500, "p2": 300}

# Square only even numbers
sq_evens   = {x: x**2 for x in range(10) if x % 2 == 0}
# {0:0, 2:4, 4:16, 6:36, 8:64}
```

### Set Comprehension

```python
words        = ["hello", "world", "hello", "python", "world"]
unique_words = {w for w in words}            # {"hello", "world", "python"}
word_lengths = {len(w) for w in words}       # {5, 6}  — unique lengths only
```

### Generator Expressions — Memory-Efficient Alternative

When you don't need the full list in memory at once, use a generator (round brackets):

```python
# List comprehension — builds entire list in memory
total = sum([x**2 for x in range(1_000_000)])

# Generator expression — computes one value at a time
total = sum(x**2 for x in range(1_000_000))   # much lower memory usage
```

### Real-Time Comprehension Examples

**Cleaning ML Data:**

```python
raw_texts = ["  Hello World  ", "PYTHON is GREAT", None, "  spaces  "]
cleaned   = [t.strip().lower() for t in raw_texts if t is not None]
# ["hello world", "python is great", "spaces"]
```

**Filtering Logs:**

```python
log_lines  = open("app.log").readlines()
error_logs = [line.strip() for line in log_lines if "ERROR" in line]
```

**Mapping Product Prices (with discount):**

```python
products    = [{"id": "p1", "price": 1000}, {"id": "p2", "price": 500}]
discounted  = {p["id"]: p["price"] * 0.9 for p in products}
# {"p1": 900.0, "p2": 450.0}
```

**Building Query Params from a Dict:**

```python
params     = {"name": "john", "age": "25", "city": "hyd"}
query_str  = "&".join(f"{k}={v}" for k, v in params.items())
# "name=john&age=25&city=hyd"
```

---

## 🔀 7. Choosing the Right Structure {#choosing-the-right-structure}

This is a judgment call that gets easier with practice. Here's a quick decision guide:

```
What do you need?
│
├── Need to LOOK UP by a label/name?
│   └── → DICTIONARY  {"user_id": data, "config_key": value}
│
├── Need a UNIQUE COLLECTION or fast membership check?
│   └── → SET  seen_ids, active_permissions, stopwords
│
├── Need an ORDERED SEQUENCE you'll MODIFY (add/remove)?
│   └── → LIST  shopping_cart, task_queue, log_lines
│
└── Need an ORDERED SEQUENCE that's FIXED / a record?
    └── → TUPLE  coordinates, DB row, function return values
```

### Performance Quick Reference

| Operation | List | Tuple | Set | Dict |
|-----------|------|-------|-----|------|
| Access by index | O(1) | O(1) | ❌ | O(1) by key |
| Search (`in`) | O(n) | O(n) | **O(1)** | **O(1)** by key |
| Insert at end | O(1) | ❌ | O(1) | O(1) |
| Insert at front | O(n) | ❌ | O(1) | O(1) |
| Delete | O(n) | ❌ | O(1) | O(1) |
| Memory | More | Less | More | Most |

---

## 📊 8. Memory & Performance Notes {#memory-and-performance}

These observations come up constantly in production systems:

**Tuples use less memory than lists:**

```python
import sys
l = [1, 2, 3, 4, 5]
t = (1, 2, 3, 4, 5)
print(sys.getsizeof(l))   # 120 bytes
print(sys.getsizeof(t))   # 80 bytes  — ~33% smaller
```

**Set membership check vs List:**

```python
import time

data_list = list(range(1_000_000))
data_set  = set(data_list)

# List: scans up to 1M items
start = time.time(); 999_999 in data_list; print(time.time()-start)  # ~0.02s

# Set: hash lookup
start = time.time(); 999_999 in data_set;  print(time.time()-start)  # ~0.0000001s
```

**Dict is faster than if-elif chains:**

```python
# Slow for many branches
def get_day(n):
    if n == 0: return "Monday"
    elif n == 1: return "Tuesday"
    # ... 5 more elifs

# Fast — O(1) lookup
DAYS = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
        3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
day = DAYS.get(n, "Unknown")
```

---

## 🧪 9. Hands-On Exercises {#hands-on-exercises}

### Exercise 1: Convert List of Dicts to CSV (without pandas)

```python
employees = [
    {"name": "Ravi",  "age": 30, "dept": "IT"},
    {"name": "Priya", "age": 26, "dept": "HR"},
    {"name": "Arun",  "age": 34, "dept": "Finance"},
]

# Task: write this to employees.csv manually
headers = list(employees[0].keys())
rows    = [",".join(str(e[h]) for h in headers) for e in employees]
csv_content = "\n".join([",".join(headers)] + rows)

with open("employees.csv", "w") as f:
    f.write(csv_content)
```

### Exercise 2: Word Frequency Counter

```python
text = "The quick brown fox jumps over the lazy dog the fox"

# Clean, split, count
words = text.lower().replace(",","").replace(".","").split()
freq  = {}
for w in words:
    freq[w] = freq.get(w, 0) + 1

# Top 3 words
top3 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]
print(top3)  # [("the",3), ("fox",2), ...]
```

### Exercise 3: Common Users Between Two Apps

```python
app1_users = {"john", "mike", "emma", "priya"}
app2_users = {"mike", "emma", "alex", "priya"}

common_users   = app1_users & app2_users            # both apps
only_in_app1   = app1_users - app2_users            # migrate to app2
only_in_app2   = app2_users - app1_users            # migrate to app1
all_users      = app1_users | app2_users            # full user base
exclusive_only = app1_users ^ app2_users            # not on both
```

### Exercise 4: Flatten a Nested List

```python
nested = [[1,2], [3,4,5], [6], [7,8,9,10]]

# Method 1: comprehension
flat1 = [item for sublist in nested for item in sublist]

# Method 2: sum trick
flat2 = sum(nested, [])

# Method 3: itertools (best for production)
import itertools
flat3 = list(itertools.chain.from_iterable(nested))
```

### Exercise 5: Dictionary → Query String

```python
params = {"name": "john", "age": 25, "city": "hyderabad"}
query_string = "&".join(f"{k}={v}" for k, v in params.items())
# "name=john&age=25&city=hyderabad"

# Also available via urllib
from urllib.parse import urlencode
query_string = urlencode(params)
```

### Exercise 6: Reverse a Dictionary

```python
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
# {1: "a", 2: "b", 3: "c"}

# What if values are not unique?
data = {"a": 1, "b": 1, "c": 2}
# Group keys by value using defaultdict
from collections import defaultdict
rev = defaultdict(list)
for k, v in data.items():
    rev[v].append(k)
# {1: ["a","b"], 2: ["c"]}
```

### Exercise 7 (New): Group Employees by Department

```python
employees = [
    {"name": "Ravi",    "dept": "Engineering"},
    {"name": "Priya",   "dept": "HR"},
    {"name": "Kiran",   "dept": "Engineering"},
    {"name": "Meera",   "dept": "Marketing"},
    {"name": "Deepak",  "dept": "HR"},
]

by_dept = defaultdict(list)
for emp in employees:
    by_dept[emp["dept"]].append(emp["name"])

# {"Engineering": ["Ravi","Kiran"], "HR": ["Priya","Deepak"], ...}
```

### Exercise 8 (New): Find Duplicate Items in a List

```python
data = [1, 2, 3, 2, 4, 3, 5, 1]

seen       = set()
duplicates = set()

for item in data:
    if item in seen:
        duplicates.add(item)
    seen.add(item)

print(duplicates)   # {1, 2, 3}
```

---

## 🧩 10. Mini Project — Text Analyzer App {#mini-project}

This project stitches together everything from Day 3. Build it step by step.

### What It Does

- Accepts a block of text
- Reports total words, unique words
- Removes common stopwords
- Shows the top 5 most frequent words
- Reports average word length
- Identifies the longest and shortest word

### Full Implementation

```python
from collections import Counter

def analyze_text(text):
    # --- Setup ---
    STOPWORDS = {"the", "a", "an", "and", "or", "is", "are",
                 "in", "on", "to", "of", "it", "was", "be"}

    # --- Processing ---
    words_raw    = text.lower().split()                           # list
    words_clean  = [w.strip(".,!?;:\"'") for w in words_raw]     # strip punctuation
    words_nostop = [w for w in words_clean if w not in STOPWORDS] # remove stopwords

    freq         = Counter(words_nostop)                          # dict-like
    unique_words = set(words_nostop)                              # set

    avg_len      = sum(len(w) for w in words_nostop) / len(words_nostop)
    longest      = max(words_nostop, key=len)
    shortest     = min(words_nostop, key=len)

    # --- Results ---
    print(f"Total words (raw):     {len(words_raw)}")
    print(f"Total words (cleaned): {len(words_nostop)}")
    print(f"Unique words:          {len(unique_words)}")
    print(f"Average word length:   {avg_len:.2f} characters")
    print(f"Longest word:          '{longest}' ({len(longest)} chars)")
    print(f"Shortest word:         '{shortest}' ({len(shortest)} chars)")
    print(f"\nTop 5 most frequent words:")
    for word, count in freq.most_common(5):
        bar = "█" * count
        print(f"  {word:<15} {bar} ({count})")

# --- Run It ---
sample = """
Python is great and Python is easy to learn.
Python powers machine learning, web development, and automation.
Learning Python opens many doors in the tech industry.
"""
analyze_text(sample)
```

**Expected Output:**

```
Total words (raw):     28
Total words (cleaned): 17
Unique words:          14
Average word length:   6.41 characters
Longest word:          'development' (11 chars)
Shortest word:         'web' (3 chars)

Top 5 most frequent words:
  python          ███ (3)
  learning        ██ (2)
  great           █ (1)
  easy            █ (1)
  machine         █ (1)
```

### Data Structures Used — Breakdown

```
┌──────────────────┬────────────────────────────────────────┐
│ Structure        │ Role in the analyzer                   │
├──────────────────┼────────────────────────────────────────┤
│ list             │ tokens, words_clean, words_nostop      │
│ set              │ STOPWORDS (O(1) lookup), unique_words  │
│ dict / Counter   │ frequency count, most_common()         │
│ list comprehension│ cleaning and filtering words          │
│ generator expr   │ sum(len(w) for w in ...)               │
│ sorted()         │ ranking words by frequency             │
└──────────────────┴────────────────────────────────────────┘
```

---

## 📝 Quick Recap Cheatsheet

```
LIST   → [1,2,3]           mutable, ordered, duplicates OK
TUPLE  → (1,2,3)           immutable, ordered, duplicates OK, hashable
SET    → {1,2,3}           mutable, unordered, NO duplicates, O(1) lookup
DICT   → {"k": "v"}        mutable, ordered (3.7+), unique keys, O(1) lookup

Comprehensions:
  List  → [expr for x in iter if cond]
  Dict  → {k: v for x in iter if cond}
  Set   → {expr for x in iter if cond}
  Gen   → (expr for x in iter if cond)   ← lazy, memory-efficient

Key Rules:
  ✔ Use set for membership tests, not list
  ✔ Use dict.get(k, default) instead of dict[k] in production
  ✔ Prefer tuple over list when data is fixed
  ✔ deep copy nested structures before modifying
  ✔ Counter for frequency, defaultdict for grouping
```

---

*Day 3 Notes — Python Data Structures | Consolidated & Expanded*
