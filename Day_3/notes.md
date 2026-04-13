# 🐍 Python Full Stack — Day 3 of 35
# Topic: Data Structures — Lists, Tuples, Sets, Dictionaries & Complexity
**Audience:** Intermediate | **Duration:** 3 Hours | **Track:** Python → Django/Flask → Frontend → Deployment

---

## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, learners will be able to:
- Choose the right data structure for a given problem based on performance and semantic fit
- Perform all standard operations on lists, tuples, sets, and dictionaries with confidence
- Explain the internal implementation (hash tables, dynamic arrays) and why it matters for performance
- Reason about time complexity (Big O) for common operations on each structure
- Use advanced `collections` module types: `namedtuple`, `defaultdict`, `Counter`, `ChainMap`

### 📋 Prerequisites (Days 1–2 Review)
- Python data types: `int`, `float`, `str`, `bool`, `None`
- Mutable vs immutable distinction (Day 1)
- Comprehensions — list, dict, set (Day 2)
- Loop control flow and functions (Day 2)

### 🔗 Connection to the Full Stack Journey
- **Django ORM (Day 20+):** QuerySets are list-like; model instances are dict-like; filtering uses set-logic
- **REST API responses (Day 22+):** Every JSON response is a Python `dict` or `list` — structure choice directly affects API design
- **Django caching (Day 25+):** Cache backends are dict-like; `defaultdict` patterns mirror cache miss handling
- **Database performance (Day 28+):** Understanding hash maps is the mental model behind database indexes
- **Frontend data shaping (Day 30+):** Transforming API data for templates uses dict/list comprehensions daily

---

## 2. Concept Explanation

### 2.1 Lists — Dynamic Arrays

**The "Why":** Lists are Python's general-purpose ordered container. They're your go-to when you need to maintain order, allow duplicates, and modify the collection over time.

**Internal implementation:** CPython implements lists as **dynamic arrays** — contiguous blocks of memory holding pointers to objects. When a list grows beyond its current allocation, Python allocates a larger block (typically 1.125× the current size) and copies all pointers. This is called **over-allocation** — it makes `append()` fast on average (amortized O(1)) but means `insert(0, x)` is slow (shifts all pointers right).

**Analogy:** Think of a list as a **numbered parking lot** — each space has a fixed position (index), you can add more spaces at the end cheaply, but inserting a space in the middle requires renumbering and moving every car after it.

---

### 2.2 Tuples — Immutable Sequences

**The "Why":** Tuples signal intent: "this collection is fixed — don't change it." They're faster than lists, can be used as dictionary keys, and communicate meaning (a coordinate `(x, y)` is conceptually fixed).

**Key insight:** Immutability is a contract, not just a restriction. When you see a tuple, you know no code has mutated it — this makes reasoning about data flow much easier.

**Named tuples** (`collections.namedtuple`) give you the best of both worlds: the memory efficiency and speed of tuples, plus attribute-style access instead of cryptic integer indexing.

**Analogy:** A list is a **shopping cart** (you add and remove things). A tuple is a **sealed package** — the contents are fixed, but you can read the label.

---

### 2.3 Sets — Hash Table Collections

**The "Why":** Sets answer one question blazingly fast: *"Is this element in the collection?"* Membership testing in a list is O(n) — Python checks every element. In a set, it's O(1) average — Python computes a hash and looks up directly.

**Internal implementation:** Sets use a **hash table** — a sparse array where the position of each element is determined by `hash(element)`. For an element to be stored in a set, it must be **hashable** (immutable and consistent hash value).

**Use sets when:**
- You need to eliminate duplicates
- Membership testing speed matters
- You want to perform mathematical set operations (union, intersection, difference)

**Analogy:** A set is like a **lookup table in a library** — instead of searching every shelf (list), you go directly to the index card, which tells you exactly where the book is.

---

### 2.4 Dictionaries — Hash Maps

**The "Why":** Dictionaries are Python's most versatile and important data structure. Every Python object's attributes live in a `__dict__`. Module namespaces are dicts. Django's request objects, ORM results, and settings are all dict-like.

**Internal implementation:** Dicts use a **hash table** (like sets) but store **key→value pairs**. From Python 3.7+, dicts **preserve insertion order** — this is guaranteed by the language spec, not just an implementation detail.

**Key requirements:** Dictionary keys must be **hashable** — meaning they must be immutable and implement `__hash__`. `int`, `float`, `str`, `tuple` (of hashables) work. `list`, `dict`, `set` cannot be keys.

**`collections` module extensions:**
- `defaultdict` — auto-creates a default value on missing key access (eliminates KeyError)
- `Counter` — specialized dict for counting hashable objects
- `OrderedDict` — dict that explicitly tracks order (redundant since 3.7 but still useful for `.move_to_end()`)
- `ChainMap` — logical merge of multiple dicts without copying

---

### 2.5 Time Complexity — Big O Notation

**The "Why":** Knowing Big O helps you make informed decisions when data scales from 100 rows to 10 million. A choice that works fine at 100 records can become unusable at 1 million.

**Big O basics:** Describes how runtime grows as input size (n) grows — ignoring constants and lower-order terms.

| Notation | Name | Example |
|----------|------|---------|
| O(1) | Constant | dict lookup, list append, set membership |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | List search, list insert at index 0 |
| O(n log n) | Linearithmic | Efficient sort (Timsort) |
| O(n²) | Quadratic | Nested loops over same data |

**Amortized complexity:** List `append()` is O(1) *amortized* — occasionally it triggers a reallocation (O(n)) but spread across many appends, the average cost per operation is O(1).

---

## 3. Syntax & Code Examples

### 3.1 Lists

#### Creation and Basic Operations

```python
# Creation
empty = []
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True, None]
nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Indexing (0-based, negative from end)
print(fruits[0])        # apple
print(fruits[-1])       # cherry
print(fruits[-2])       # banana

# Length
print(len(fruits))      # 3
```

---

#### Slicing and Stride

```python
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Syntax: list[start:stop:step]  (stop is exclusive)
print(numbers[2:6])         # [2, 3, 4, 5]
print(numbers[:4])          # [0, 1, 2, 3]   (start defaults to 0)
print(numbers[6:])          # [6, 7, 8, 9]   (stop defaults to end)
print(numbers[::2])         # [0, 2, 4, 6, 8] (every 2nd element)
print(numbers[1::2])        # [1, 3, 5, 7, 9] (every 2nd, starting at 1)
print(numbers[::-1])        # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] (reversed)
print(numbers[7:2:-1])      # [7, 6, 5, 4, 3] (reverse slice)

# Slicing creates a shallow copy
copy = numbers[:]
copy.append(99)
print(numbers)      # unchanged — [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(copy)         # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 99]
```

---

#### Mutating Operations

```python
fruits = ["apple", "banana", "cherry"]

# append — add one item to the end: O(1) amortized
fruits.append("date")
print(fruits)       # ['apple', 'banana', 'cherry', 'date']

# extend — add multiple items from iterable: O(k) where k = items added
fruits.extend(["elderberry", "fig"])
print(fruits)       # ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig']

# insert — insert at index: O(n) (shifts everything after)
fruits.insert(1, "avocado")
print(fruits[0:3])  # ['apple', 'avocado', 'banana']

# remove — removes first occurrence by value: O(n)
fruits.remove("banana")

# pop — remove by index (default: last): O(1) for last, O(n) for middle
last = fruits.pop()         # removes and returns last element
second = fruits.pop(1)      # removes and returns index 1

# sort — in-place, stable Timsort: O(n log n)
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()                             # ascending
nums.sort(reverse=True)                 # descending
nums.sort(key=lambda x: -x)            # custom key

# sorted — returns new list, original unchanged
original = [3, 1, 4, 1, 5]
new_sorted = sorted(original)
print(original)     # [3, 1, 4, 1, 5] — unchanged

# reverse — in-place: O(n)
fruits.reverse()

# count and index
nums = [1, 2, 2, 3, 2, 4]
print(nums.count(2))        # 3
print(nums.index(3))        # 3  (first occurrence)
```

---

#### Nested Lists (Matrices)

```python
# 3×3 matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Access element at row 1, col 2
print(matrix[1][2])         # 6

# Iterate rows
for row in matrix:
    print(row)

# Transpose using zip and list comprehension
transposed = [list(row) for row in zip(*matrix)]
print(transposed)
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

# ❌ Common pitfall: creating 2D list wrong
wrong = [[0] * 3] * 3       # all rows are the SAME object!
wrong[0][0] = 99
print(wrong)                # [[99, 0, 0], [99, 0, 0], [99, 0, 0]] ← bug!

# ✅ Correct: list comprehension creates independent rows
correct = [[0] * 3 for _ in range(3)]
correct[0][0] = 99
print(correct)              # [[99, 0, 0], [0, 0, 0], [0, 0, 0]] ← correct
```

---

### 3.2 Tuples

```python
# Creation
empty = ()
single = (42,)          # trailing comma required for single-element tuple!
point = (3, 4)
rgb = (255, 128, 0)
mixed = (1, "hello", [1, 2])  # tuple can contain mutable objects

# Indexing and slicing — same as list
print(point[0])         # 3
print(rgb[1:])          # (128, 0)

# Packing and unpacking
coords = 10, 20         # packing (parentheses optional)
x, y = coords           # unpacking
print(x, y)             # 10 20

# Extended unpacking
first, *middle, last = [1, 2, 3, 4, 5]
print(first)    # 1
print(middle)   # [2, 3, 4]
print(last)     # 5

# Swap using tuple unpacking
a, b = 5, 10
a, b = b, a
print(a, b)             # 10 5

# Multiple return values (returns a tuple)
def min_max(lst: list) -> tuple[int, int]:
    return min(lst), max(lst)

low, high = min_max([3, 1, 4, 1, 5, 9])
print(low, high)        # 1 9

# Tuples as dict keys (lists cannot be keys)
grid_values = {(0, 0): "start", (3, 4): "end", (1, 2): "waypoint"}
print(grid_values[(1, 2)])  # waypoint
```

---

#### Named Tuples

```python
from collections import namedtuple

# Define — acts like a class with named fields
Point = namedtuple("Point", ["x", "y"])
Student = namedtuple("Student", ["name", "age", "grade"])

# Create instances
p = Point(3, 4)
s = Student("Alice", 20, "A")

# Access by name (readable!) or by index (compatible with tuple)
print(p.x, p.y)             # 3 4
print(p[0], p[1])           # 3 4 (index still works)
print(s.name, s.grade)      # Alice A

# Still immutable — can't assign
# p.x = 10   → AttributeError

# Useful methods
print(s._asdict())          # {'name': 'Alice', 'age': 20, 'grade': 'A'}
s2 = s._replace(grade="B") # returns new namedtuple with changed field
print(s2)                   # Student(name='Alice', age=20, grade='B')

# Memory efficient — same as tuple, much smaller than dict
import sys
d = {"name": "Alice", "age": 20, "grade": "A"}
t = Student("Alice", 20, "A")
print(sys.getsizeof(d))     # ~232 bytes
print(sys.getsizeof(t))     # ~72 bytes
```

---

### 3.3 Sets

```python
# Creation
empty_set = set()       # NOT {} — that creates an empty dict!
fruits = {"apple", "banana", "cherry", "apple"}  # duplicates removed
print(fruits)           # {'apple', 'banana', 'cherry'} — order NOT guaranteed

# From other iterables
from_list = set([1, 2, 2, 3, 3, 3])
from_str = set("hello")
print(from_list)        # {1, 2, 3}
print(from_str)         # {'h', 'e', 'l', 'o'} — unique characters

# Membership testing: O(1) average
print("apple" in fruits)    # True  (O(1))
print("mango" in fruits)    # False (O(1))

# vs list membership: O(n)
fruits_list = list(fruits)
print("apple" in fruits_list)   # True, but O(n) scan

# Adding and removing
fruits.add("date")
fruits.add("apple")         # no error — just ignored (already exists)
fruits.discard("mango")     # no error if not present
fruits.remove("cherry")     # raises KeyError if not present!

# Set comprehension
squares = {x**2 for x in range(10)}
print(squares)      # {0, 1, 4, 9, 16, 25, 36, 49, 64, 81}
```

---

#### Set Operations

```python
python_devs = {"Alice", "Bob", "Charlie", "Diana"}
django_devs = {"Charlie", "Diana", "Eve", "Frank"}

# Union — all elements from both
print(python_devs | django_devs)
# or: python_devs.union(django_devs)
# {'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'}

# Intersection — only elements in BOTH
print(python_devs & django_devs)
# or: python_devs.intersection(django_devs)
# {'Charlie', 'Diana'}

# Difference — in first but NOT in second
print(python_devs - django_devs)
# or: python_devs.difference(django_devs)
# {'Alice', 'Bob'}

# Symmetric difference — in either but NOT both
print(python_devs ^ django_devs)
# or: python_devs.symmetric_difference(django_devs)
# {'Alice', 'Bob', 'Eve', 'Frank'}

# Subset / superset checks
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}
print(a <= b)           # True  — a is subset of b
print(a < b)            # True  — a is proper subset (not equal)
print(b >= a)           # True  — b is superset of a
print(a.isdisjoint({6, 7}))  # True — no common elements

# frozenset — immutable set (can be used as dict key)
frozen = frozenset(["read", "write"])
permissions = {frozen: "editor"}
print(permissions[frozen])      # editor
```

---

### 3.4 Dictionaries

#### Creation and Basic Access

```python
# Creation
empty = {}
user = {"name": "Alice", "age": 25, "city": "Pune"}
from_pairs = dict([("a", 1), ("b", 2)])
from_keys = dict.fromkeys(["x", "y", "z"], 0)
print(from_keys)    # {'x': 0, 'y': 0, 'z': 0}

# Access
print(user["name"])             # Alice
print(user.get("age"))          # 25
print(user.get("email"))        # None  (no KeyError!)
print(user.get("email", "N/A")) # N/A   (default value)

# Modification
user["email"] = "alice@example.com"     # add new key
user["age"] = 26                        # update existing
user.update({"city": "Mumbai", "role": "dev"})  # bulk update

# Deletion
del user["city"]
removed = user.pop("role")              # returns and removes
last_item = user.popitem()              # removes and returns last (key, value) pair

# Check existence
print("name" in user)           # True
print("salary" in user)         # False
```

---

#### Dictionary Views and Iteration

```python
user = {"name": "Alice", "age": 25, "city": "Pune"}

# Views — live, reflect changes to the dict
keys_view = user.keys()
vals_view = user.values()
items_view = user.items()

print(list(keys_view))          # ['name', 'age', 'city']
print(list(vals_view))          # ['Alice', 25, 'Pune']
print(list(items_view))         # [('name', 'Alice'), ('age', 25), ('city', 'Pune')]

# Iterate
for key in user:
    print(key, "→", user[key])

for key, value in user.items():     # most Pythonic
    print(f"{key}: {value}")

# setdefault — get value or set default if key missing
user.setdefault("email", "unknown@example.com")
print(user["email"])    # unknown@example.com (set and returned)

user.setdefault("name", "Bob")  # key exists — NOT overwritten
print(user["name"])     # Alice (unchanged)
```

---

#### Dictionary Comprehensions

```python
# Basic
squares = {x: x**2 for x in range(6)}
print(squares)          # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filtered
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)     # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# Invert a dict
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)         # {1: 'a', 2: 'b', 3: 'c'}

# Transform from list of dicts (common in API work)
users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Carol"},
]
id_to_name = {u["id"]: u["name"] for u in users}
print(id_to_name)       # {1: 'Alice', 2: 'Bob', 3: 'Carol'}
```

---

#### Collections Module

```python
from collections import defaultdict, Counter, OrderedDict, ChainMap

# ── defaultdict ───────────────────────────────────────────────────────────
# Automatically creates default value on first missing key access
word_counts = defaultdict(int)          # default: 0
for word in "the cat sat on the mat the cat".split():
    word_counts[word] += 1              # no KeyError on first access
print(dict(word_counts))
# {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}

# Group items by category
grouped = defaultdict(list)
for name, dept in [("Alice","Eng"), ("Bob","HR"), ("Carol","Eng")]:
    grouped[dept].append(name)
print(dict(grouped))
# {'Eng': ['Alice', 'Carol'], 'HR': ['Bob']}

# ── Counter ───────────────────────────────────────────────────────────────
# Specialized dict for counting
text = "mississippi"
letter_count = Counter(text)
print(letter_count)         # Counter({'s': 4, 'i': 4, 'p': 2, 'm': 1})
print(letter_count.most_common(2))  # [('s', 4), ('i', 4)]

# Counter arithmetic
c1 = Counter("aab")
c2 = Counter("abb")
print(c1 + c2)              # Counter({'b': 3, 'a': 3})
print(c1 - c2)              # Counter({'a': 1})

# ── ChainMap ─────────────────────────────────────────────────────────────
# Logical merge of multiple dicts — searches each in order
defaults = {"color": "blue", "size": "medium", "debug": False}
user_prefs = {"color": "red"}
env_vars = {"debug": True}

config = ChainMap(env_vars, user_prefs, defaults)
print(config["color"])      # red   (found in user_prefs)
print(config["size"])       # medium (found in defaults)
print(config["debug"])      # True  (found in env_vars — highest priority)
```

---

### 3.5 Time Complexity Summary Table

```python
import timeit
import random

# Generate test data
n = 100_000
data = list(range(n))
data_set = set(data)
target = n - 1              # worst case: last element

# List membership: O(n)
list_time = timeit.timeit(lambda: target in data, number=1000)

# Set membership: O(1) average
set_time = timeit.timeit(lambda: target in data_set, number=1000)

print(f"List search (n={n}): {list_time:.4f}s")
print(f"Set search  (n={n}): {set_time:.4f}s")
print(f"Set is {list_time/set_time:.0f}x faster")
# Typically set is 1000x+ faster for large n
```

| Operation | List | Tuple | Set | Dict |
|-----------|------|-------|-----|------|
| Access by index | O(1) | O(1) | N/A | O(1) avg |
| Search / `in` | O(n) | O(n) | O(1) avg | O(1) avg |
| Append / Add | O(1) amort | N/A | O(1) avg | O(1) avg |
| Insert at index | O(n) | N/A | N/A | N/A |
| Delete by index | O(n) | N/A | N/A | O(1) avg |
| Sort | O(n log n) | N/A | N/A | N/A |
| Iteration | O(n) | O(n) | O(n) | O(n) |

---

## 4. Common Mistakes & Gotchas

### ❌ Mistake 1: Creating an Empty Set with `{}`

```python
# ❌ Wrong — {} creates an empty DICT, not a set
empty = {}
print(type(empty))      # <class 'dict'>  ← surprise!

# ✅ Correct — use set() for empty set
empty_set = set()
print(type(empty_set))  # <class 'set'>

# Non-empty sets can use {} syntax (works fine)
fruits = {"apple", "banana"}    # this IS a set
```

---

### ❌ Mistake 2: Aliasing vs Copying Nested Lists

```python
# ❌ Wrong — [[0]*3]*3 creates 3 references to the SAME inner list
matrix = [[0] * 3] * 3
matrix[0][0] = 1
print(matrix)   # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] ← ALL rows changed!

# ✅ Correct — list comprehension creates independent rows
matrix = [[0] * 3 for _ in range(3)]
matrix[0][0] = 1
print(matrix)   # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] ← only first row
```

**Why it happens:** `[[0]*3]*3` multiplies a list by repeating the same inner list object (reference) three times.

---

### ❌ Mistake 3: Using `KeyError` Instead of `.get()`

```python
user = {"name": "Alice", "age": 25}

# ❌ Wrong — crashes if key is missing
email = user["email"]       # KeyError: 'email'

# ✅ Option 1: .get() with default
email = user.get("email", "not provided")
print(email)                # not provided

# ✅ Option 2: setdefault (also stores the default)
email = user.setdefault("email", "default@example.com")
print(user["email"])        # default@example.com ← stored in dict

# ✅ Option 3: defaultdict for dicts that always need a default
```

---

### ❌ Mistake 4: Modifying a List While Iterating Over It

```python
# ❌ Wrong — skips elements because indices shift during deletion
numbers = [1, 2, 3, 4, 5, 6]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)   # modifies list mid-iteration!
print(numbers)              # [1, 3, 5] — looks right, but worked by accident!

# Try with [2, 4, 6]:
numbers = [2, 4, 6]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)
print(numbers)              # [4] ← bug! 4 was skipped

# ✅ Correct — iterate over a copy, modify original; or use comprehension
numbers = [2, 4, 6, 7, 8]
numbers = [n for n in numbers if n % 2 != 0]   # filter with comprehension
print(numbers)              # [7]
```

---

### ❌ Mistake 5: Using a Mutable Type as a Dict Key

```python
# ❌ Wrong — list is not hashable, cannot be a dict key
scores = {}
player_hand = [1, 5, 7]
scores[player_hand] = 100   # TypeError: unhashable type: 'list'

# ✅ Correct — convert to tuple (immutable, hashable)
scores[tuple(player_hand)] = 100
print(scores)               # {(1, 5, 7): 100}

# ✅ Or use frozenset if order doesn't matter
scores[frozenset(player_hand)] = 100
```

---

## 5. Hands-on Exercises

### 🧑‍🏫 Guided Exercise 1: Student Record CRUD System

**Goal:** Build a dict-based student database with full CRUD operations.

```python
# Database — dict of dicts
student_db: dict[int, dict] = {}
next_id = 1

def create_student(name: str, age: int, grade: str) -> dict:
    """Add a student and return the created record."""
    global next_id
    student = {"id": next_id, "name": name, "age": age, "grade": grade}
    student_db[next_id] = student
    next_id += 1
    return student

def read_student(student_id: int) -> dict | None:
    """Return student dict or None if not found."""
    return student_db.get(student_id)

def update_student(student_id: int, **updates) -> bool:
    """Update student fields. Returns True if updated, False if not found."""
    student = student_db.get(student_id)
    if student is None:
        return False
    student.update(updates)
    return True

def delete_student(student_id: int) -> bool:
    """Delete student. Returns True if deleted, False if not found."""
    return student_db.pop(student_id, None) is not None

def list_students() -> list[dict]:
    """Return all students sorted by name."""
    return sorted(student_db.values(), key=lambda s: s["name"])

# Test it
create_student("Alice", 20, "A")
create_student("Bob", 22, "B")
create_student("Carol", 21, "A")

print("All students:", list_students())
print("Student 2:", read_student(2))

update_student(2, grade="A", age=23)
print("After update:", read_student(2))

delete_student(3)
print("After delete:", list_students())

# Grade distribution using Counter
from collections import Counter
grades = [s["grade"] for s in student_db.values()]
print("Grade distribution:", Counter(grades))
```

**Discussion:** Why is a `dict` better than a `list` here for looking up students by ID?

---

### 🧑‍🏫 Guided Exercise 2: Set-Based Data Filtering

**Goal:** Use set operations to analyze user and product data.

```python
# E-commerce scenario
all_users = {"alice", "bob", "carol", "diana", "eve", "frank"}
premium_users = {"alice", "carol", "eve"}
users_who_bought = {"bob", "carol", "diana", "eve"}
users_who_reviewed = {"alice", "carol", "frank"}

# 1. Free users who made a purchase
free_buyers = (all_users - premium_users) & users_who_bought
print("Free users who bought:", free_buyers)       # {'bob', 'diana'}

# 2. Premium users who haven't bought yet
premium_no_buy = premium_users - users_who_bought
print("Premium, no purchase:", premium_no_buy)     # {'alice'}

# 3. Users who bought AND reviewed (engaged users)
engaged = users_who_bought & users_who_reviewed
print("Engaged users:", engaged)                   # {'carol', 'eve'}

# 4. Users who did exactly one thing (bought XOR reviewed)
one_action = users_who_bought ^ users_who_reviewed
print("Only one action:", one_action)              # {'bob', 'diana', 'alice', 'frank'}

# 5. Deduplication speed demo
import time, random

big_list = [random.randint(0, 1000) for _ in range(100_000)]
target = 999

start = time.perf_counter()
for _ in range(10_000): _ = target in big_list
list_ms = (time.perf_counter() - start) * 1000

big_set = set(big_list)
start = time.perf_counter()
for _ in range(10_000): _ = target in big_set
set_ms = (time.perf_counter() - start) * 1000

print(f"\nList lookup: {list_ms:.1f}ms")
print(f"Set lookup:  {set_ms:.1f}ms")
print(f"Set is {list_ms/set_ms:.0f}x faster")
```

---

### 💻 Independent Practice 1: Word Frequency Analyzer

**Task:** Analyze a block of text and produce a frequency report.

```python
text = """
Python is a high-level programming language. Python is used for web development,
data science, artificial intelligence, and automation. Python is easy to learn
and Python is widely used in industry.
"""

# Your tasks:
# 1. Count word frequencies using Counter
# Hint: text.lower().split() for basic word list

# 2. Remove common "stop words" from the count
stop_words = {"is", "a", "and", "for", "in", "to", "the", "are"}
# Hint: set difference or filter in comprehension

# 3. Find the top 5 most common meaningful words
# Hint: Counter.most_common(5)

# 4. Find words that appear exactly once (hapax legomena)
# Hint: {word for word, count in counter.items() if count == 1}

# 5. Group words by their first letter using defaultdict
# Hint: defaultdict(list) + for word in unique_words

# Expected output (approximately):
# Top 5: [('python', 4), ('used', 3), ('web', 1), ...]
# Unique words: {'high-level', 'language', ...}
# By letter: {'p': ['python', 'programming'], ...}
```

> **Hints:** `Counter`, `str.lower()`, `str.split()`, set difference, `defaultdict(list)`

---

### 💻 Independent Practice 2: Simple LRU-style Cache

**Task:** Implement a dictionary-based function result cache.

```python
# Build a simple cache using a dict + OrderedDict for eviction

from collections import OrderedDict

class SimpleCache:
    """
    A fixed-size cache that evicts the least recently used item.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()

    def get(self, key: str) -> int | None:
        """Return cached value, or None if not found."""
        # Hint: if key in cache, move_to_end() and return value
        # Hint: if not, return None
        pass

    def put(self, key: str, value: int) -> None:
        """Store key-value pair. Evict LRU item if over capacity."""
        # Hint: if key exists, update and move_to_end()
        # Hint: if at capacity, popitem(last=False) to remove oldest
        pass

    def __repr__(self) -> str:
        return f"Cache({dict(self.cache)})"

# Test
cache = SimpleCache(3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
print(cache)            # Cache({'a': 1, 'b': 2, 'c': 3})

cache.get("a")          # access 'a' — moves it to most recent
cache.put("d", 4)       # capacity exceeded — evict LRU ('b', since 'a' was just accessed)
print(cache)            # Cache({'a': 1, 'c': 3, 'd': 4})
```

> **Hints:** `OrderedDict.move_to_end(key)`, `OrderedDict.popitem(last=False)`

---

### 🏆 Challenge Problem: Multi-Index Student Search Engine

```python
"""
Build a search engine over a student dataset that supports:
1. Lookup by student ID: O(1)
2. Lookup by name: O(1) (case-insensitive)
3. Lookup by grade: returns ALL students with that grade
4. Lookup by age range: returns students within age range
5. Statistics: average age per grade

The trick: maintain MULTIPLE indexes (dicts/sets) for the same data
so every lookup is fast regardless of which field you search by.
"""

from collections import defaultdict
from typing import Optional

class StudentSearchEngine:
    def __init__(self):
        self._by_id: dict[int, dict] = {}
        self._by_name: dict[str, dict] = {}          # name.lower() → student
        self._by_grade: dict[str, set[int]] = defaultdict(set)  # grade → set of IDs
        self._next_id = 1

    def add_student(self, name: str, age: int, grade: str) -> dict:
        # Your implementation
        pass

    def find_by_id(self, student_id: int) -> Optional[dict]:
        pass

    def find_by_name(self, name: str) -> Optional[dict]:
        pass

    def find_by_grade(self, grade: str) -> list[dict]:
        pass

    def find_by_age_range(self, min_age: int, max_age: int) -> list[dict]:
        pass

    def grade_statistics(self) -> dict[str, float]:
        """Return average age per grade."""
        pass

# Test
engine = StudentSearchEngine()
engine.add_student("Alice", 20, "A")
engine.add_student("Bob", 22, "B")
engine.add_student("Carol", 21, "A")
engine.add_student("Diana", 20, "B")

print(engine.find_by_name("alice"))         # {'id': 1, 'name': 'Alice', ...}
print(engine.find_by_grade("A"))            # [Alice, Carol]
print(engine.find_by_age_range(20, 21))     # [Alice, Carol, Diana]
print(engine.grade_statistics())            # {'A': 20.5, 'B': 21.0}
```

---

## 6. Best Practices & Industry Standards

### Choose the Right Structure for the Job

```python
# ✅ Use a set when you need fast membership testing
valid_status_codes = {200, 201, 204, 400, 401, 403, 404, 500}
if response.status_code in valid_status_codes:  # O(1)
    ...

# ❌ Don't use a list for this
valid_codes_list = [200, 201, 204, ...]
if response.status_code in valid_codes_list:    # O(n) — unnecessary

# ✅ Use tuple for fixed, ordered data (function returns, coordinates)
def get_dimensions() -> tuple[int, int]:
    return 1920, 1080

width, height = get_dimensions()

# ✅ Use namedtuple or dataclass for structured records
from collections import namedtuple
DBConfig = namedtuple("DBConfig", ["host", "port", "name", "user"])
config = DBConfig("localhost", 5432, "mydb", "admin")
print(config.host)      # readable!
```

---

### Dict Access Patterns

```python
# ✅ Always use .get() when key might be missing
value = config.get("timeout", 30)

# ✅ Use .setdefault() to initialize nested structures
graph = {}
graph.setdefault("node_a", []).append("node_b")

# ✅ Use defaultdict to eliminate existence checks
from collections import defaultdict
adjacency = defaultdict(list)
adjacency["node_a"].append("node_b")    # no KeyError, no if-check needed

# ✅ dict.update() or | operator (Python 3.9+) for merging
base = {"a": 1, "b": 2}
extra = {"b": 99, "c": 3}
merged = base | extra               # Python 3.9+ — creates new dict
base |= extra                       # Python 3.9+ — in-place update
print(merged)   # {'a': 1, 'b': 99, 'c': 3}
```

---

### Memory and Performance Tips

```python
# ✅ Generator over list when you only need to iterate once
total = sum(x**2 for x in range(1_000_000))    # ~200 bytes
# NOT: sum([x**2 for x in range(1_000_000)])   # ~8MB

# ✅ Use set for deduplication
unique = list(set(items_with_duplicates))

# ✅ Prefer list.append() over list concatenation in loops
# ❌ Slow: creates a new list each iteration
result = []
for x in data:
    result = result + [x * 2]   # O(n²) total!

# ✅ Fast: O(n) total
result = []
for x in data:
    result.append(x * 2)        # or: result = [x*2 for x in data]

# ✅ Sort with key= instead of cmp function
# ❌ Don't use comparison lambdas (Python 2 style)
students.sort(key=lambda s: s["grade"])     # correct
```

---

## 7. Real-World Application

### Django ORM Returns Dict/List Structures

```python
# Django ORM queryset → list of model instances (Day 20+ preview)
# values() → list of dicts; values_list() → list of tuples

# views.py
from django.http import JsonResponse
from myapp.models import Product

def product_list(request):
    # QuerySet → list of dicts (efficient for JSON responses)
    products = list(
        Product.objects
        .filter(is_active=True)
        .values("id", "name", "price")     # returns dicts
    )
    # products = [{"id": 1, "name": "Widget", "price": 9.99}, ...]

    # Group by category using defaultdict
    from collections import defaultdict
    by_category = defaultdict(list)
    for p in products:
        by_category[p["category"]].append(p)

    return JsonResponse({"products": products})
```

### API Request Parsing — Dicts Everywhere

```python
# Every Django/Flask request body is parsed into a dict
import json

def create_user(request):
    data = json.loads(request.body)     # → dict

    # Safe access with .get() and defaults
    name = data.get("name", "").strip()
    age = data.get("age", 0)
    roles = set(data.get("roles", []))  # convert to set for fast lookup

    required = {"name", "email"}
    missing = required - set(data.keys())   # set difference!
    if missing:
        return error_response(f"Missing fields: {missing}")
```

### Caching Pattern with Dicts

```python
# Simple in-memory cache (precursor to Redis/Django cache — Day 25+)
_cache: dict = {}

def get_user_profile(user_id: int) -> dict:
    cache_key = f"user:{user_id}"

    # Cache hit
    if cache_key in _cache:
        return _cache[cache_key]

    # Cache miss — fetch from DB
    profile = fetch_from_database(user_id)  # expensive call
    _cache[cache_key] = profile
    return profile
```

### 🔭 Connection to Upcoming Days
- **Day 4:** OOP — class attributes and instance attributes are dictionaries internally
- **Day 5:** File I/O — reading CSV data into list-of-dicts is the most common pattern
- **Day 8:** Decorators — use closures + dicts for caching (`functools.lru_cache` wraps a dict)
- **Day 20:** Django models — every model instance is backed by a dict; QuerySets are lazy list-like objects

---

## 8. Quick Revision Summary

### Key Terms

| Term | One-line Definition |
|------|---------------------|
| Dynamic array | List's internal storage — contiguous memory block that grows automatically |
| Amortized O(1) | Operation is occasionally expensive but cheap on average across many calls |
| Hash table | Internal structure for sets/dicts — uses hash to find position in O(1) |
| Hashable | Object with a fixed, consistent hash value — required for set/dict keys |
| Tuple packing | Creating a tuple without parentheses: `a, b = 1, 2` |
| Tuple unpacking | Assigning tuple elements to separate variables: `x, y = point` |
| Named tuple | Tuple subclass with named fields — readable, memory-efficient |
| `defaultdict` | Dict subclass that auto-creates default values on missing key access |
| `Counter` | Dict subclass optimized for counting hashable objects |
| `ChainMap` | Logical layered view of multiple dicts without merging them |
| `frozenset` | Immutable set — hashable, usable as dict key |
| Big O notation | Mathematical notation describing how algorithm runtime scales with input size |
| Dictionary view | Live, read-only reference to dict's keys/values/items |

---

### Core Syntax Cheat Sheet

```python
# ── Lists ──────────────────────────────────────────────────────
lst = [1, 2, 3]
lst.append(x)           # O(1) add to end
lst.insert(i, x)        # O(n) insert at index
lst.pop()               # O(1) remove last
lst.pop(i)              # O(n) remove at index
lst.remove(x)           # O(n) remove first occurrence
lst[start:stop:step]    # slicing — creates copy
lst.sort(key=fn)        # in-place sort
sorted(lst, key=fn)     # returns new sorted list

# ── Tuples ─────────────────────────────────────────────────────
t = (1, 2, 3)
a, b, c = t             # unpack
first, *rest = t        # extended unpack

# ── Sets ───────────────────────────────────────────────────────
s = {1, 2, 3}
s = set()               # empty set (not {}!)
s.add(x)
s.discard(x)            # safe remove
A | B                   # union
A & B                   # intersection
A - B                   # difference
A ^ B                   # symmetric difference
x in s                  # O(1) membership

# ── Dicts ──────────────────────────────────────────────────────
d = {"key": "value"}
d.get(k, default)       # safe access
d.setdefault(k, v)      # get or set default
d.update({...})         # bulk update
d | other               # merge (Python 3.9+)
d.pop(k, default)       # remove with default
for k, v in d.items()   # iterate pairs

# ── Collections ────────────────────────────────────────────────
from collections import defaultdict, Counter, namedtuple, ChainMap
defaultdict(list)       # default factory
Counter(iterable)       # count elements
namedtuple("T", ["a","b"])  # named tuple factory
ChainMap(d1, d2)        # layered lookup
```

---

### 5 MCQ Recap Questions

**Q1.** What is the time complexity of searching for an element in a Python list?
- A) O(1)
- B) O(log n)
- **C) O(n)** ✅
- D) O(n log n)

**Q2.** What does `{}` create in Python?
- A) An empty set
- **B) An empty dict** ✅
- C) An empty frozenset
- D) A SyntaxError

**Q3.** Which of the following CANNOT be used as a dictionary key?
- A) `"hello"` (str)
- B) `(1, 2, 3)` (tuple of ints)
- **C) `[1, 2, 3]` (list)** ✅
- D) `42` (int)

**Q4.** What does `defaultdict(list)` do when you access a missing key?
- A) Raises a KeyError
- B) Returns `None`
- **C) Creates an empty list for that key and returns it** ✅
- D) Returns 0

**Q5.** What is the output of `[0] * 3` used as a row in `[[0]*3] * 3` when you modify one cell?
- A) Only the targeted cell changes
- B) The entire matrix becomes 0
- **C) All rows change because they reference the same inner list** ✅
- D) A TypeError is raised

---

## 9. Instructor Notes

### 📌 Anticipated Student Questions

| Question | Suggested Answer |
|----------|-----------------|
| "Why is dict search O(1) but list search O(n)?" | Dict uses a hash table — computes a hash of the key and jumps directly to that position. List must check every element sequentially. |
| "When should I use a namedtuple vs a dataclass?" | `namedtuple` for read-only, simple records (good for return values, dict keys). `dataclass` (Day 4) for mutable records with methods. |
| "Is Python dict order guaranteed?" | Yes, since Python 3.7 — insertion order is guaranteed by the language spec. |
| "What's the difference between `remove()` and `discard()` on sets?" | Both remove an element, but `remove()` raises `KeyError` if the element isn't present; `discard()` silently does nothing. |
| "When would I use ChainMap?" | When you have layered configs — e.g., env vars override user preferences which override defaults — without copying or merging dicts. |
| "Can a frozenset contain mutable objects?" | No — frozenset requires all its elements to be hashable (immutable). |
| "What's amortized O(1)?" | The occasional expensive operation (list reallocation) is averaged over many cheap operations. Each append costs O(1) on average, even though some cost O(n). |

---

### 🖊️ Whiteboard Diagrams to Draw

1. **List as Dynamic Array:** Draw a row of contiguous boxes. Show pointer from variable name. When full, draw a bigger box being allocated and pointers copied.
2. **Hash Table for Dict/Set:** Draw an array with 8 slots. Show `hash("key") % 8 = 3` pointing to slot 3. Show key-value pair stored there.
3. **Set Operations (Venn Diagram):** Classic 2-circle Venn — shade union, intersection, difference, symmetric difference separately.
4. **Nested List Aliasing Bug:** Draw `[[0]*3]*3` as 3 pointers pointing to the SAME inner list object. Show the correct version with 3 independent list objects.
5. **Big O Growth Curves:** Axes: x=input size, y=time. Draw O(1) flat line, O(n) diagonal, O(n²) curve, O(log n) gentle curve. Point to which operations land on which line.
6. **ChainMap Lookup:** Draw 3 dict boxes stacked. Arrow showing lookup searching from top to bottom and stopping at first match.

---

### ⏱️ Timing Guide (3 Hours)

| Time | Activity |
|------|----------|
| 0:00 – 0:10 | Day 2 quick recap (closures, LEGB, comprehensions) |
| 0:10 – 0:35 | Lists — dynamic arrays, slicing, operations, nested list pitfall |
| 0:35 – 0:50 | Tuples — immutability, packing/unpacking, namedtuple |
| 0:50 – 1:10 | Sets — hash table intuition, operations, Venn diagram + live speed demo |
| 1:10 – 1:20 | ☕ Break |
| 1:20 – 1:45 | Dicts — hash map internals, methods, views, comprehensions |
| 1:45 – 2:00 | Collections module — defaultdict, Counter, ChainMap |
| 2:00 – 2:15 | Big O — complexity table, timeit benchmark live demo |
| 2:15 – 2:40 | Guided exercises 1 & 2 (instructor-led) |
| 2:40 – 2:50 | Common mistakes walkthrough |
| 2:50 – 3:00 | MCQ recap, Q&A, Day 4 preview (OOP) |

> 💡 **Tip:** The hash table intuition (sets/dicts) often needs a whiteboard diagram before code — draw first, code second.
> 💡 **Live demo:** Run the `timeit` list vs set benchmark live — the dramatic speedup (100x–1000x) makes Big O concrete and memorable.

---

### 📚 Resources & Further Reading

- [Python Docs — Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python Docs — collections module](https://docs.python.org/3/library/collections.html)
- [Real Python — Lists vs Tuples](https://realpython.com/python-lists-tuples/)
- [Real Python — Dictionaries](https://realpython.com/python-dicts/)
- [Real Python — Sets](https://realpython.com/python-sets/)
- [Raymond Hettinger — Modern Python Dictionaries (PyCon 2017)](https://www.youtube.com/watch?v=p33CVV29OG8) ← must-watch
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [Visualgo — Hash Table Visualization](https://visualgo.net/en/hashtable)
- [Python Tutor](https://pythontutor.com/) ← visualize nested list aliasing bug live