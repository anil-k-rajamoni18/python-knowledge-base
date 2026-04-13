# 💪 Python Full Stack — Day 3 Exercise & Practice File
# Topic: Data Structures — Lists, Tuples, Sets, Dictionaries & Complexity

> **Instructions:** Work through sections in order. Write your predictions before running. Attempt every problem genuinely before checking the answer key.

---

## 📋 Setup Check

```python
import sys
import timeit
import random
from collections import defaultdict, Counter, namedtuple, OrderedDict, ChainMap
from copy import deepcopy

print(f"Python version: {sys.version}")
print("✅ All imports successful — let's go!")
```

---

## Section A — Predict the Output (No Running Allowed!)

### A1. List Operations

```python
# Snippet 1
lst = [1, 2, 3, 4, 5]
lst.append([6, 7])
print(len(lst))
print(lst[-1])

# Snippet 2
lst2 = [1, 2, 3]
lst2.extend([4, 5])
print(len(lst2))

# Snippet 3
nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
print(nums.count(5))
print(nums.index(4))
```

**Predictions:**
```
Snippet 1 - len:  ___   last element: ___
Snippet 2 - len:  ___
Snippet 3 - count: ___  index: ___
```

---

### A2. Slicing Surprises

```python
data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(data[2:7:2])      # Line 1
print(data[::-2])       # Line 2
print(data[8:2:-1])     # Line 3
print(data[-3:])        # Line 4
print(data[::3])        # Line 5
```

**Predictions:**
```
Line 1: ______
Line 2: ______
Line 3: ______
Line 4: ______
Line 5: ______
```

---

### A3. Set Behavior

```python
# Snippet 1
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}
print(a & b)
print(a - b)
print(a ^ b)

# Snippet 2
s = set()
s.add(1)
s.add(2)
s.add(1)    # duplicate
s.add(1)
print(len(s))
print(s)

# Snippet 3
empty = {}
print(type(empty).__name__)
```

**Predictions:**
```
Snippet 1: a & b = ______   a - b = ______   a ^ b = ______
Snippet 2: len = ___   s = ______
Snippet 3: type = ______
```

---

### A4. Dictionary Behavior

```python
# Snippet 1
d = {"a": 1, "b": 2, "c": 3}
print(d.get("d"))
print(d.get("d", 99))

d.setdefault("e", 5)
d.setdefault("a", 999)     # key already exists
print(d["a"])
print(d["e"])

# Snippet 2
d2 = {"x": 10}
removed = d2.pop("x")
missing = d2.pop("y", 0)   # key doesn't exist
print(removed)
print(missing)
print(len(d2))
```

**Predictions:**
```
Snippet 1: get("d") = ___  get("d",99) = ___  d["a"] = ___  d["e"] = ___
Snippet 2: removed = ___   missing = ___   len = ___
```

---

### A5. Nested List Aliasing

```python
# What prints?
bad = [[0] * 3] * 3
bad[0][1] = 99
print(bad)

good = [[0] * 3 for _ in range(3)]
good[0][1] = 99
print(good)
```

**Predictions:**
```
bad:  ______________________________
good: ______________________________
```

---

### A6. Collections Module

```python
from collections import defaultdict, Counter

# Snippet 1
dd = defaultdict(int)
for word in ["cat", "dog", "cat", "fish", "dog", "cat"]:
    dd[word] += 1
print(sorted(dd.items()))

# Snippet 2
c = Counter("banana")
print(c.most_common(2))
print(c["z"])       # missing key behavior
```

**Predictions:**
```
Snippet 1: ______________________________
Snippet 2 most_common: ______   c["z"] = ___
```

---

## Section B — Fill in the Blanks

### B1. List Operations

```python
# 1. Add single item to end
fruits = ["apple", "banana"]
fruits.______(  "cherry")
print(fruits)   # ['apple', 'banana', 'cherry']

# 2. Add multiple items at once
fruits.______(["date", "elderberry"])
print(len(fruits))  # 5

# 3. Insert "avocado" at index 1
fruits.______(1, "avocado")
print(fruits[1])    # avocado

# 4. Remove "banana" (first occurrence) by value
fruits.______("banana")

# 5. Remove and return the LAST item
last = fruits.______()

# 6. Remove and return item at index 0
first = fruits.______(0)

# 7. Sort in-place by string length
fruits.sort(key=______)
```

---

### B2. Set Operations

```python
team_a = {"Alice", "Bob", "Charlie"}
team_b = {"Charlie", "Diana", "Eve"}

# 1. All team members (union)
all_members = team_a ______ team_b

# 2. Members in both teams (intersection)
both_teams = team_a ______ team_b

# 3. Members only in team_a (difference)
only_a = team_a ______ team_b

# 4. Members in exactly one team (symmetric difference)
unique_to_one = team_a ______ team_b

# 5. Is team_a a subset of all_members?
print(team_a ______ all_members)    # True

# 6. Safely try to remove "Bob" — no error if not present
team_a.______("Bob")

# 7. Create an immutable version of team_b (for use as dict key)
immutable_b = ______(team_b)
```

---

### B3. Dictionary Comprehensions

```python
words = ["hello", "world", "python", "data", "structures"]

# 1. Map each word to its length
word_lengths = {______ : ______ for word in words}
print(word_lengths)   # {'hello': 5, 'world': 5, ...}

# 2. Only words longer than 5 characters
long_words = {______ for word in words if ______}
# Note: this should be a SET comprehension, not dict

# 3. Invert word_lengths (length → list of words with that length)
# Hint: use defaultdict(list)
from collections import defaultdict
by_length = ______
for word, length in word_lengths.items():
    by_length[length].append(word)
print(dict(by_length))

# 4. Square number dict
squares = {n: ______ for n in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

---

## Section C — Debugging Exercises

### C1. The Extend vs Append Confusion

```python
# Bug: expected to add 3 elements, but got 1 nested list
basket = ["apple", "banana"]
basket.append(["cherry", "date", "elderberry"])

print(len(basket))          # Expected: 5 — actual?
print(basket[2])            # Expected: "cherry" — actual?
```

**Explain the bug:**
```
______________________________________________
```

**Fix it:**
```python
basket = ["apple", "banana"]
# Your fix here
print(len(basket))      # 5
print(basket[2])        # cherry
```

---

### C2. The Dangerous Matrix

```python
# Bug: setting one cell changes an entire column
board = [["."] * 3] * 3     # create 3x3 board

board[0][1] = "X"
print(board)
# Expected: [['.',  'X', '.'], ['.', '.', '.'], ['.', '.', '.']]
# Actual: ???
```

**Explain what actually happens and why:**
```
______________________________________________
```

**Write the correct matrix initialization:**
```python
board = ______
board[0][1] = "X"
print(board)    # Only first row changes
```

---

### C3. The KeyError Trap

```python
# Bug: crashes when a key doesn't exist
def get_user_email(users: dict, user_id: int) -> str:
    return users[user_id]["email"]  # KeyError if user_id missing!

users = {1: {"name": "Alice", "email": "alice@example.com"}}
print(get_user_email(users, 1))     # works
print(get_user_email(users, 99))    # KeyError!
```

**Rewrite to handle missing user and missing email gracefully:**
```python
def get_user_email(users: dict, user_id: int, default: str = "N/A") -> str:
    # Your fix here — use .get() at both levels
    pass

print(get_user_email(users, 99))    # N/A
print(get_user_email(users, 1))     # alice@example.com
```

---

### C4. The Mutable Key Attempt

```python
# Bug: trying to use a list as a dict key
game_board = {}
player_position = [2, 3]          # row 2, col 3
game_board[player_position] = "player"    # TypeError!
```

**Explain why this fails:**
```
______________________________________________
```

**Two ways to fix it:**
```python
# Fix 1: convert to tuple
game_board[______] = "player"

# Fix 2: if order doesn't matter, use frozenset
game_board[______] = "player"
```

---

### C5. The Modify-While-Iterating Bug

```python
# Bug: some items are skipped
scores = [45, 90, 30, 85, 20, 95, 55]

for score in scores:
    if score < 60:
        scores.remove(score)    # modifying list during iteration!

print(scores)   # Expected: [90, 85, 95] — but likely wrong!
```

**Explain why this is buggy:**
```
______________________________________________
```

**Fix it using a comprehension:**
```python
scores = [45, 90, 30, 85, 20, 95, 55]
scores = ______    # one line
print(scores)      # [90, 85, 95]
```

---

## Section D — Write the Code

### D1. Word Frequency Analyzer

```python
def analyze_text(text: str, stop_words: set[str] = None) -> dict:
    """
    Analyze word frequencies in text.

    Returns a dict with:
    - 'counts': Counter of word frequencies (excluding stop words)
    - 'top_5': list of (word, count) for 5 most common
    - 'unique': set of words appearing exactly once
    - 'by_letter': defaultdict grouping words by first letter
    - 'total_words': int — total word count (before stop word removal)
    """
    if stop_words is None:
        stop_words = {"the", "a", "an", "is", "in", "it", "to", "and", "of", "for"}

    # Your implementation here
    pass

# Test
text = """
Python is a versatile programming language used for web development,
data science, artificial intelligence, and automation. Python is easy
to learn and widely used in the industry. The Python community is large.
"""

result = analyze_text(text)
print("Top 5 words:", result["top_5"])
print("Unique words:", sorted(result["unique"]))
print("Words by letter 'p':", sorted(result["by_letter"]["p"]))
print("Total words:", result["total_words"])
```

---

### D2. Student Grade Report

```python
students = [
    {"name": "Alice", "grades": [85, 92, 78, 96, 88]},
    {"name": "Bob", "grades": [72, 68, 74, 80, 65]},
    {"name": "Carol", "grades": [95, 98, 92, 97, 99]},
    {"name": "Diana", "grades": [55, 60, 58, 62, 70]},
    {"name": "Eve", "grades": [88, 85, 90, 87, 92]},
]

def generate_report(students: list[dict]) -> dict:
    """
    Generate a grade report with:
    - 'student_averages': dict of name → average grade (rounded to 1 decimal)
    - 'letter_grades': dict of name → letter grade (A:90+, B:80+, C:70+, D:60+, F:<60)
    - 'grade_distribution': Counter of letter grades
    - 'top_student': name of student with highest average
    - 'struggling': list of names with average < 70
    - 'class_average': overall average across all students
    """
    # Your implementation here
    pass

report = generate_report(students)
print("Averages:", report["student_averages"])
print("Grades:", report["letter_grades"])
print("Distribution:", report["grade_distribution"])
print("Top student:", report["top_student"])
print("Need help:", report["struggling"])
print("Class average:", report["class_average"])

# Expected output (approximately):
# Averages: {'Alice': 87.8, 'Bob': 71.8, 'Carol': 96.2, 'Diana': 61.0, 'Eve': 88.4}
# Grades: {'Alice': 'B', 'Bob': 'C', 'Carol': 'A', 'Diana': 'D', 'Eve': 'B'}
# Distribution: Counter({'B': 2, 'C': 1, 'A': 1, 'D': 1})
# Top student: Carol
# Need help: ['Diana']
# Class average: 81.04
```

---

### D3. Simple Cache Implementation

```python
from collections import OrderedDict
from typing import Any, Optional

class LRUCache:
    """
    Least Recently Used cache with fixed capacity.

    - get(key): return value or None; marks as recently used
    - put(key, value): store item; evict LRU item if at capacity
    - size property: current number of items
    """

    def __init__(self, capacity: int):
        # Your initialization here
        pass

    def get(self, key: str) -> Optional[Any]:
        # Your implementation
        # Hint: if found, move_to_end() to mark as recently used
        pass

    def put(self, key: str, value: Any) -> None:
        # Your implementation
        # Hint: if at capacity, popitem(last=False) removes oldest
        pass

    @property
    def size(self) -> int:
        pass

    def __repr__(self) -> str:
        return f"LRUCache(capacity={self.capacity}, items={dict(self.cache)})"

# Test suite
cache = LRUCache(3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
print(cache)                    # LRUCache(capacity=3, items={'a': 1, 'b': 2, 'c': 3})
print(cache.get("a"))           # 1 — 'a' is now most recently used
cache.put("d", 4)               # evict LRU — which is 'b' (since 'a' was just accessed)
print(cache)                    # items={'c': 3, 'a': 1, 'd': 4}
print(cache.get("b"))           # None — evicted!
print(cache.size)               # 3
```

---

### D4. Multi-Structure Data Pipeline

```python
"""
Build a pipeline that processes a list of product records and produces
multiple views/aggregations using the right data structure for each.
"""

products = [
    {"id": 1, "name": "Widget A", "category": "electronics", "price": 29.99, "tags": ["sale", "new"]},
    {"id": 2, "name": "Gadget B", "category": "electronics", "price": 149.99, "tags": ["premium"]},
    {"id": 3, "name": "Tool C", "category": "hardware", "price": 12.50, "tags": ["sale"]},
    {"id": 4, "name": "Device D", "category": "electronics", "price": 89.99, "tags": ["new", "premium"]},
    {"id": 5, "name": "Part E", "category": "hardware", "price": 5.99, "tags": ["sale", "clearance"]},
    {"id": 6, "name": "Item F", "category": "hardware", "price": 34.99, "tags": []},
]

def process_products(products: list[dict]) -> dict:
    """
    Return a dict containing:

    1. 'by_id': dict mapping id → product  (for O(1) lookup)
    2. 'by_category': defaultdict grouping product names by category
    3. 'price_range': tuple (min_price, max_price)
    4. 'all_tags': set of all unique tags used
    5. 'on_sale': list of product names with "sale" tag, sorted by price
    6. 'category_totals': dict of category → total price value
    7. 'tag_counts': Counter of how many products have each tag
    """
    # Your implementation here
    pass

result = process_products(products)
print("By ID lookup:", result["by_id"][3]["name"])          # Tool C
print("Electronics:", result["by_category"]["electronics"])
print("Price range:", result["price_range"])
print("All tags:", result["all_tags"])
print("On sale:", result["on_sale"])
print("Category totals:", result["category_totals"])
print("Tag counts:", result["tag_counts"])
```

---

## Section E — Performance Experiments

### E1. List vs Set Membership — The Proof

```python
import timeit
import random

def run_membership_benchmark(n: int):
    """Compare list vs set membership testing at scale."""
    data = list(range(n))
    data_set = set(data)

    # Search for an element in the second half (harder for list)
    targets = [random.randint(n//2, n-1) for _ in range(1000)]

    list_time = timeit.timeit(
        lambda: all(t in data for t in targets),
        number=100
    )

    set_time = timeit.timeit(
        lambda: all(t in data_set for t in targets),
        number=100
    )

    speedup = list_time / set_time
    print(f"n={n:>8,} | list: {list_time:.3f}s | set: {set_time:.4f}s | speedup: {speedup:.0f}x")

print("Membership Testing Benchmark")
print("-" * 60)
for size in [1_000, 10_000, 100_000, 1_000_000]:
    run_membership_benchmark(size)
```

**Record your results and answer:**
```
At n=1,000:     speedup = ___x
At n=100,000:   speedup = ___x

Does speedup grow as n grows? _______
Why? ______________________________________________
What Big O complexity explains this difference? ___
```

---

### E2. List Append vs Concatenation

```python
import timeit

n = 100_000

# Method 1: append() — O(n) total
def use_append():
    result = []
    for i in range(n):
        result.append(i)
    return result

# Method 2: concatenation — O(n²) total
def use_concat():
    result = []
    for i in range(n):
        result = result + [i]
    return result

# Method 3: comprehension
def use_comprehension():
    return [i for i in range(n)]

t1 = timeit.timeit(use_append, number=5)
t2 = timeit.timeit(use_concat, number=5)
t3 = timeit.timeit(use_comprehension, number=5)

print(f"append():       {t1:.3f}s")
print(f"concatenation:  {t2:.3f}s")
print(f"comprehension:  {t3:.3f}s")
print(f"\nconcat is {t2/t1:.0f}x slower than append")
print(f"comprehension is {t1/t3:.1f}x {'faster' if t1>t3 else 'slower'} than append")
```

**Questions to answer:**
```
1. Why is concatenation O(n²)?
   _______________________________________________

2. Why is comprehension often the fastest?
   _______________________________________________
```

---

### E3. Memory Comparison

```python
import sys
from collections import namedtuple

# Compare memory usage of different structures for same data
name, age, city = "Alice", 25, "Pune"

# Dict
d = {"name": name, "age": age, "city": city}

# Namedtuple
Person = namedtuple("Person", ["name", "age", "city"])
nt = Person(name, age, city)

# Regular tuple
t = (name, age, city)

# List
lst = [name, age, city]

print(f"dict:       {sys.getsizeof(d)} bytes")
print(f"namedtuple: {sys.getsizeof(nt)} bytes")
print(f"tuple:      {sys.getsizeof(t)} bytes")
print(f"list:       {sys.getsizeof(lst)} bytes")

print(f"\ndict is {sys.getsizeof(d)/sys.getsizeof(nt):.1f}x larger than namedtuple")
```

**Questions:**
```
1. Which structure uses the most memory? ______
2. Which uses the least? ______
3. When would the memory difference matter in practice?
   _______________________________________________
```

---

## Section F — Mini Project: Student Records System

Build a complete student records system that demonstrates every major data structure from Day 3.

### Requirements

```python
"""
Student Records System — Day 3 Mini Project

Features:
✅ Add / update / delete students (dict-based CRUD)
✅ Search by ID, name, grade (multiple dict indexes)
✅ Grade statistics using Counter
✅ Enrollment by subject using defaultdict
✅ Fast tag-based filtering using sets
✅ Ranked leaderboard using sorted()
✅ Named tuple for immutable report snapshots
✅ Export summary using dict comprehension
"""

from collections import defaultdict, Counter, namedtuple
from typing import Optional

# ── Data Types ──────────────────────────────────────────────────────────────
StudentReport = namedtuple("StudentReport", [
    "student_id", "name", "average", "letter_grade", "rank"
])

# ── Database (Multiple Indexes) ─────────────────────────────────────────────
_db: dict[int, dict] = {}           # id → student
_by_name: dict[str, int] = {}       # name.lower() → id
_by_grade: dict[str, set] = defaultdict(set)   # grade → set of ids
_by_subject: dict[str, set] = defaultdict(set) # subject → set of ids
_next_id = 1

# ── Core CRUD ───────────────────────────────────────────────────────────────
def add_student(
    name: str,
    scores: list[float],
    subjects: list[str],
    tags: list[str] = None
) -> dict:
    """Add a student and return the created record."""
    global _next_id
    # Your implementation here
    pass

def get_student(student_id: int) -> Optional[dict]:
    """Look up student by ID — O(1)."""
    pass

def find_by_name(name: str) -> Optional[dict]:
    """Look up student by name (case-insensitive) — O(1)."""
    pass

def find_by_grade(grade: str) -> list[dict]:
    """Return all students with given letter grade — O(k) where k = results."""
    pass

def find_by_subject(subject: str) -> list[dict]:
    """Return all students enrolled in a subject."""
    pass

def find_by_tags(required_tags: set[str]) -> list[dict]:
    """Return students who have ALL of the required tags."""
    # Hint: use set intersection on each student's tags
    pass

def update_scores(student_id: int, new_scores: list[float]) -> bool:
    """Update student scores and recalculate grade. Returns True if updated."""
    pass

# ── Analytics ───────────────────────────────────────────────────────────────
def grade_distribution() -> Counter:
    """Return Counter of letter grades across all students."""
    pass

def leaderboard(top_n: int = 5) -> list[StudentReport]:
    """Return top_n students as named tuples, sorted by average descending."""
    pass

def class_statistics() -> dict:
    """
    Return dict with:
    - 'total': int
    - 'class_average': float
    - 'highest': float
    - 'lowest': float
    - 'grade_counts': Counter
    """
    pass

# ── Helper ──────────────────────────────────────────────────────────────────
def _calc_average(scores: list[float]) -> float:
    return round(sum(scores) / len(scores), 1) if scores else 0.0

def _letter_grade(avg: float) -> str:
    if avg >= 90: return "A"
    if avg >= 80: return "B"
    if avg >= 70: return "C"
    if avg >= 60: return "D"
    return "F"

# ── Test Harness ────────────────────────────────────────────────────────────
def run_tests():
    print("=== Student Records System Test ===\n")

    # Add students
    add_student("Alice", [95, 92, 98, 96], ["math", "physics"], ["honor_roll"])
    add_student("Bob", [72, 68, 74, 70], ["math", "history"], [])
    add_student("Carol", [88, 85, 90, 87], ["physics", "chemistry"], ["honor_roll", "lab_assistant"])
    add_student("Diana", [55, 60, 58, 50], ["history"], ["needs_support"])
    add_student("Eve", [92, 88, 95, 91], ["math", "chemistry"], ["honor_roll"])

    # Test lookups
    print("Find Alice:", find_by_name("alice")["name"])
    print("Find by grade A:", [s["name"] for s in find_by_grade("A")])
    print("Math students:", [s["name"] for s in find_by_subject("math")])
    print("Honor roll:", [s["name"] for s in find_by_tags({"honor_roll"})])

    # Analytics
    print("\nGrade distribution:", grade_distribution())
    print("\nClass statistics:", class_statistics())
    print("\nTop 3 leaderboard:")
    for rank, report in enumerate(leaderboard(3), 1):
        print(f"  {rank}. {report.name}: {report.average} ({report.letter_grade})")

    # Update and re-check
    update_scores(find_by_name("bob")["id"], [80, 82, 85, 83])
    print("\nBob after update:", find_by_name("bob")["grade"])

if __name__ == "__main__":
    run_tests()
```

---

## ✅ Answer Key

<details>
<summary>Click to reveal — attempt everything first!</summary>

### A1 Answers
```
Snippet 1: len = 6, last = [6, 7]  (append adds the list as ONE element)
Snippet 2: len = 5                  (extend adds each element individually)
Snippet 3: count = 2, index = 2
```

### A2 Answers
```
Line 1: [2, 4, 6]
Line 2: [9, 7, 5, 3, 1]
Line 3: [8, 7, 6, 5, 4, 3]
Line 4: [7, 8, 9]
Line 5: [0, 3, 6, 9]
```

### A3 Answers
```
a & b = {3, 4, 5}
a - b = {1, 2}
a ^ b = {1, 2, 6, 7}
len = 2, s = {1, 2}
type = dict   (empty {} is a dict, not a set!)
```

### A4 Answers
```
get("d") = None
get("d", 99) = 99
d["a"] = 1  (setdefault doesn't overwrite existing)
d["e"] = 5
removed = 10, missing = 0, len = 0
```

### A5 Answers
```
bad: [[0, 99, 0], [0, 99, 0], [0, 99, 0]]   (all rows changed — same object!)
good: [[0, 99, 0], [0, 0, 0], [0, 0, 0]]    (only first row changed)
```

### A6 Answers
```
Snippet 1: [('cat', 3), ('dog', 2), ('fish', 1)]
Snippet 2 most_common: [('a', 3), ('n', 2)]    c["z"] = 0
```

### B1 Answers
```python
fruits.append("cherry")
fruits.extend(["date", "elderberry"])
fruits.insert(1, "avocado")
fruits.remove("banana")
last = fruits.pop()
first = fruits.pop(0)
fruits.sort(key=len)
```

### B2 Answers
```python
all_members = team_a | team_b
both_teams = team_a & team_b
only_a = team_a - team_b
unique_to_one = team_a ^ team_b
print(team_a <= all_members)
team_a.discard("Bob")
immutable_b = frozenset(team_b)
```

### C1 Fix
```python
# Bug: append() adds the list as a single element
# Fix: use extend()
basket = ["apple", "banana"]
basket.extend(["cherry", "date", "elderberry"])
```

### C2 Explanation + Fix
```
All 3 rows are the SAME inner list object. [["."] * 3] * 3
creates one list [".", ".", "."] and then creates 3 references to it.

Fix:
board = [["." ] * 3 for _ in range(3)]
```

### C3 Fix
```python
def get_user_email(users: dict, user_id: int, default: str = "N/A") -> str:
    user = users.get(user_id, {})
    return user.get("email", default)
```

### C4 Fix
```python
# Fix 1:
game_board[tuple(player_position)] = "player"

# Fix 2:
game_board[frozenset(player_position)] = "player"
```

### C5 Fix
```python
scores = [score for score in scores if score >= 60]
```

### D1 Answer
```python
def analyze_text(text, stop_words=None):
    if stop_words is None:
        stop_words = {"the", "a", "an", "is", "in", "it", "to", "and", "of", "for"}
    
    words = text.lower().split()
    total_words = len(words)
    filtered = [w.strip(".,!?") for w in words if w.strip(".,!?") not in stop_words]
    
    counts = Counter(filtered)
    top_5 = counts.most_common(5)
    unique = {word for word, count in counts.items() if count == 1}
    
    by_letter = defaultdict(list)
    for word in counts:
        by_letter[word[0]].append(word)
    
    return {
        "counts": counts,
        "top_5": top_5,
        "unique": unique,
        "by_letter": by_letter,
        "total_words": total_words
    }
```

### D2 Answer
```python
def generate_report(students):
    averages = {s["name"]: round(sum(s["grades"]) / len(s["grades"]), 1) for s in students}
    
    def letter(avg):
        if avg >= 90: return "A"
        if avg >= 80: return "B"
        if avg >= 70: return "C"
        if avg >= 60: return "D"
        return "F"
    
    letter_grades = {name: letter(avg) for name, avg in averages.items()}
    distribution = Counter(letter_grades.values())
    top_student = max(averages, key=averages.get)
    struggling = [name for name, avg in averages.items() if avg < 70]
    class_avg = round(sum(averages.values()) / len(averages), 2)
    
    return {
        "student_averages": averages,
        "letter_grades": letter_grades,
        "grade_distribution": distribution,
        "top_student": top_student,
        "struggling": struggling,
        "class_average": class_avg
    }
```

### D3 Answer
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    @property
    def size(self):
        return len(self.cache)
```

</details>

---

## 📊 Self-Assessment Checklist

| Concept | ✅ Got it | 🔄 Need review | ❓ Confused |
|---------|-----------|---------------|------------|
| List slicing with step | | | |
| append() vs extend() difference | | | |
| Nested list aliasing bug | | | |
| Set creation — `set()` not `{}` | | | |
| Set operations: `|`, `&`, `-`, `^` | | | |
| Dict safe access with `.get()` | | | |
| `setdefault()` behavior | | | |
| Dict views — live references | | | |
| Dict comprehensions | | | |
| `defaultdict` auto-creation | | | |
| `Counter` and `.most_common()` | | | |
| `namedtuple` creation and access | | | |
| `ChainMap` lookup priority | | | |
| List O(n) vs Set O(1) membership | | | |
| Why `list.insert(0)` is slow | | | |
| Amortized O(1) for `append()` | | | |

**Score:**
- 16/16 ✅ — Excellent! Ready for Day 4 (OOP & Classes)
- 11–15 ✅ — Good. Re-read theory sections for "🔄" items
- < 11 ✅ — Focus on hash tables, set operations, and dict methods — these are used daily in Django

---

*Day 3 Exercises Complete — Day 4: Object-Oriented Programming — Classes, Inheritance, Dunder Methods, Dataclasses*