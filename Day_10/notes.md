# Day 10 — Python Iterators & Generators
### Python Full Stack Bootcamp | Session Duration: 3 Hours

---

## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, students will be able to:
- Explain the iterator protocol (`__iter__` / `__next__`) and build custom iterator classes from scratch
- Write generator functions using `yield` and generator expressions for memory-efficient data processing
- Use `send()`, `throw()`, and `close()` on generators and understand bidirectional data flow
- Apply `itertools` utilities (`chain`, `islice`, `groupby`, `accumulate`, etc.) to solve real data problems
- Measure and compare memory usage between lists and generators on large datasets

### 📚 Prerequisites (Days 1–9)
- Python OOP — classes, `__init__`, dunder methods (Day 7–8)
- Exception handling — `StopIteration`, `try/except` (Day 9)
- Built-in types — lists, tuples, dictionaries, sets (Days 3–5)
- Functions, scope, `*args`/`**kwargs` (Day 6)

### 🔗 Connection to the Full Stack Journey
Iterators and generators are the **engine behind every data pipeline** you will build:
- **Day 11 (File I/O):** Reading huge CSV/log files line-by-line with generators — no memory overflow
- **Day 12–13 (Databases):** ORM querysets in Django are lazy iterators — understanding this prevents N+1 bugs
- **Day 17–20 (Django Views):** Streaming HTTP responses use generators under the hood
- **Day 28–30 (Deployment / ETL):** Production data pipelines are generator chains processing millions of records

---

## 2. Concept Explanation

### 2.1 Iterable vs Iterator — The Core Distinction

**Real-world analogy:**
Think of a **recipe book** (iterable) vs a **bookmark in that recipe book** (iterator).
- The book can give you a bookmark anytime you ask — that's `__iter__()`.
- The bookmark remembers your current page and moves forward one page at a time — that's `__next__()`.
- You can have multiple bookmarks in the same book at the same time — multiple independent iterators from one iterable.
- When you reach the last page and turn, you get nothing — that's `StopIteration`.

| Concept | Has | Example |
|---|---|---|
| **Iterable** | `__iter__()` only | `list`, `str`, `dict`, `range`, file object |
| **Iterator** | `__iter__()` + `__next__()` | `iter([1,2,3])`, generator, `zip()`, `enumerate()` |

Every iterator is also an iterable (its `__iter__` returns itself). Not every iterable is an iterator.

### 2.2 The Iterator Protocol — The "Why"

Python's `for` loop doesn't know anything about lists, strings, or files specifically. It only knows the iterator protocol. This is why `for` works on *any* object that implements the two dunder methods — including your own custom classes. This is **duck typing** at the language level.

```
for item in collection:
    ...
↕ Python translates this to:
_iter = iter(collection)       # calls collection.__iter__()
while True:
    try:
        item = next(_iter)     # calls _iter.__next__()
        ...
    except StopIteration:
        break
```

### 2.3 Generators — The "Why"

**Problem:** You need to process 10 million log lines. A list approach loads all 10M lines into memory at once (~4 GB). A generator produces **one line at a time** — memory usage stays near zero regardless of file size.

**Real-world analogy:** A factory assembly line vs a warehouse.
- **List:** Build every car, park them all in a giant warehouse, then deliver.
- **Generator:** Build one car, deliver it, build the next. The warehouse is never needed.

Generators are **lazy** — they compute values only when you ask for them. This is called **lazy evaluation**.

### 2.4 Generator Functions vs Generator Expressions

| | Generator Function | Generator Expression |
|---|---|---|
| Syntax | `def f(): yield x` | `(x for x in iterable)` |
| Length | Can be long, complex | One-liner |
| Use case | Complex logic, multiple yields | Simple transformations |
| Analogous to | A regular function | A list comprehension |

### 2.5 The `yield` Keyword — The "How"

`yield` is like `return`, but it **pauses** the function instead of ending it. The function's local state (all variables, the position in the code) is frozen. When you call `next()` again, execution resumes *exactly* where it left off.

### 2.6 Coroutines — Generators that Receive Values

Normal generators only *produce* values (you pull from them with `next()`). Using `.send(value)`, you can also *push* values *into* a generator — making it a coroutine. This is the conceptual foundation of Python's `async/await` system (introduced Day 30+).

### 2.7 itertools — The "Why"

`itertools` is a standard library module of building blocks for iterator algebra. It's written in C and is extremely fast. Rather than writing loops manually, combining `itertools` functions lets you express data transformations declaratively and efficiently.

---

## 3. Syntax & Code Examples

### 3.1 The Iterator Protocol — Under the Hood

```python
# Python's built-in iteration — what FOR actually does
numbers = [10, 20, 30]

# Step 1: get an iterator from the iterable
it = iter(numbers)       # calls numbers.__iter__()
print(type(it))          # <class 'list_iterator'>

# Step 2: repeatedly call next()
print(next(it))          # 10  — calls it.__next__()
print(next(it))          # 20
print(next(it))          # 30
print(next(it))          # raises StopIteration!

# next() with a default — never raises StopIteration
it2 = iter([1, 2])
print(next(it2, "done")) # 1
print(next(it2, "done")) # 2
print(next(it2, "done")) # "done"  (default returned instead of raising)
```

---

### 3.2 Multiple Iterators from One Iterable

```python
# Iterables can produce multiple INDEPENDENT iterators
numbers = [1, 2, 3, 4, 5]

iter_a = iter(numbers)
iter_b = iter(numbers)   # completely independent — starts from the beginning

print(next(iter_a))  # 1
print(next(iter_a))  # 2
print(next(iter_b))  # 1  ← iter_b starts at 1, unaffected by iter_a

# Iterators cannot be "rewound" — once exhausted, done.
exhausted = iter([1, 2])
list(exhausted)          # consume it: [1, 2]
print(list(exhausted))   # []  — exhausted!
```

---

### 3.3 Custom Iterator Class

```python
class CountDown:
    """An iterator that counts down from a given number to 1."""
    
    def __init__(self, start):
        self.start = start
        self.current = start    # mutable state — tracks position
    
    def __iter__(self):
        """Return the iterator object itself."""
        return self
    
    def __next__(self):
        """Return the next value or raise StopIteration."""
        if self.current <= 0:
            raise StopIteration          # Signal: no more values
        value = self.current
        self.current -= 1                # Advance the state
        return value

# Using the iterator
countdown = CountDown(5)
for n in countdown:
    print(n, end=" ")
# Output: 5 4 3 2 1

# Manual usage
cd = CountDown(3)
print(next(cd))   # 3
print(next(cd))   # 2
print(next(cd))   # 1
print(next(cd))   # StopIteration raised
```

---

### 3.4 Custom Range Iterator (Classic Exercise)

```python
class MyRange:
    """
    Mimics Python's built-in range().
    Supports: MyRange(stop) or MyRange(start, stop, step)
    """
    
    def __init__(self, start, stop=None, step=1):
        if stop is None:            # Handle MyRange(5) → range(0, 5, 1)
            self.start = 0
            self.stop = start
        else:
            self.start = start
            self.stop = stop
        self.step = step
        self.current = self.start
    
    def __iter__(self):
        self.current = self.start   # Reset on each new iteration
        return self
    
    def __next__(self):
        if self.step > 0 and self.current >= self.stop:
            raise StopIteration
        if self.step < 0 and self.current <= self.stop:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value
    
    def __repr__(self):
        return f"MyRange({self.start}, {self.stop}, {self.step})"

# Test it
for x in MyRange(1, 10, 2):
    print(x, end=" ")
# Output: 1 3 5 7 9

for x in MyRange(5, 0, -1):
    print(x, end=" ")
# Output: 5 4 3 2 1

# Re-iterable (because __iter__ resets state)
r = MyRange(3)
print(list(r))    # [0, 1, 2]
print(list(r))    # [0, 1, 2]  ← works again
```

---

### 3.5 Generator Functions with `yield`

```python
# ── Simplest generator ────────────────────────────────────────────────────────
def simple_gen():
    print("Before first yield")
    yield 1
    print("Before second yield")
    yield 2
    print("Before third yield")
    yield 3
    print("Generator done")

gen = simple_gen()
print(type(gen))     # <class 'generator'>

# Execution is paused at each yield
print(next(gen))     # Prints "Before first yield", returns 1
print(next(gen))     # Prints "Before second yield", returns 2
print(next(gen))     # Prints "Before third yield", returns 3
# print(next(gen))   # Prints "Generator done", raises StopIteration

# ── Generator with loop ───────────────────────────────────────────────────────
def count_up_to(limit):
    """Yields integers from 1 to limit (inclusive)."""
    n = 1
    while n <= limit:
        yield n
        n += 1

for num in count_up_to(5):
    print(num, end=" ")
# Output: 1 2 3 4 5
```

---

### 3.6 The Fibonacci Generator (Infinite)

```python
def fibonacci():
    """An INFINITE generator — yields Fibonacci numbers forever."""
    a, b = 0, 1
    while True:          # Infinite loop — that's OK in a generator!
        yield a
        a, b = b, a + b  # Next Fibonacci number

# Never do: list(fibonacci())  ← infinite loop!

# Take only what you need using itertools.islice
from itertools import islice

fib = fibonacci()
first_10 = list(islice(fib, 10))
print(first_10)
# Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Or stop when a condition is met
for n in fibonacci():
    if n > 1000:
        break
    print(n, end=" ")
# Output: 0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987
```

---

### 3.7 Generator Expressions

```python
# ── List comprehension (eager — all values created immediately) ───────────────
squares_list = [x**2 for x in range(1_000_000)]   # ~8 MB in memory

# ── Generator expression (lazy — values created one at a time) ───────────────
squares_gen = (x**2 for x in range(1_000_000))     # ~200 bytes!

# They behave the same in iteration:
print(sum(squares_gen))         # 333332833333500000

# Generator expressions in function calls — no double parens needed
total = sum(x**2 for x in range(100))     # ✅ clean
total = sum((x**2 for x in range(100)))   # ✅ also fine, but redundant parens

# Filtering with genexp
evens = (x for x in range(20) if x % 2 == 0)
print(list(evens))
# Output: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

---

### 3.8 Memory Comparison

```python
import sys
import tracemalloc

def measure_memory(label, factory):
    tracemalloc.start()
    obj = factory()
    _ = list(obj) if hasattr(obj, '__next__') else obj   # consume
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{label:30s}: peak = {peak / 1024:.1f} KB")

N = 1_000_000

measure_memory("List [x**2 for x in range(N)]",
               lambda: [x**2 for x in range(N)])
measure_memory("Generator (x**2 for x in range(N))",
               lambda: (x**2 for x in range(N)))

# Approximate output:
# List [x**2 for x in range(N)]  : peak = 8700.4 KB
# Generator (x**2 for x in range(N)): peak = 0.1 KB
```

---

### 3.9 File Reader Generator — Line by Line

```python
def read_lines(filepath):
    """
    Yields one line at a time from a file.
    Works on files of ANY size — only one line in memory at a time.
    """
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")    # Remove trailing newline

# Usage — memory safe regardless of file size
for line in read_lines("large_file.txt"):
    process(line)

# ── Generator pipeline for log parsing ────────────────────────────────────────
def parse_log(filepath):
    """Yields only ERROR lines, with timestamp and message extracted."""
    for line in read_lines(filepath):
        if "ERROR" in line:
            parts = line.split("|")
            if len(parts) >= 3:
                yield {
                    "timestamp": parts[0].strip(),
                    "level":     parts[1].strip(),
                    "message":   parts[2].strip()
                }

# Chain generators together — each step transforms the stream
for error in parse_log("app.log"):
    print(f"[{error['timestamp']}] {error['message']}")
```

---

### 3.10 Generator Methods: `send()`, `throw()`, `close()`

```python
# ── send() — push a value INTO the generator ──────────────────────────────────
def running_average():
    """
    Coroutine: receives numbers via send(), yields running average.
    Must be 'primed' with next() or send(None) before first send().
    """
    total = 0
    count = 0
    while True:
        value = yield (total / count if count > 0 else 0)   # yield avg, receive next value
        if value is not None:
            total += value
            count += 1

avg = running_average()
next(avg)           # Prime the coroutine — advances to first yield

print(avg.send(10)) # Send 10, get back running average: 10.0
print(avg.send(20)) # Send 20, running average: 15.0
print(avg.send(30)) # Send 30, running average: 20.0

# ── throw() — inject an exception into the generator ─────────────────────────
def safe_counter():
    count = 0
    while True:
        try:
            yield count
            count += 1
        except ValueError as e:
            print(f"Counter reset due to: {e}")
            count = 0

c = safe_counter()
print(next(c))                        # 0
print(next(c))                        # 1
c.throw(ValueError, "reset now")      # Counter reset due to: reset now
print(next(c))                        # 0  (was reset)

# ── close() — terminate the generator cleanly ─────────────────────────────────
def infinite_counter():
    n = 0
    while True:
        try:
            yield n
            n += 1
        except GeneratorExit:
            print("Generator cleaning up...")
            return            # Must return (or raise StopIteration) — not yield

cnt = infinite_counter()
print(next(cnt))   # 0
print(next(cnt))   # 1
cnt.close()        # Prints "Generator cleaning up..."
```

---

### 3.11 Generator Pipeline — Composable Data Processing

```python
# Each function is a generator stage — they compose like Unix pipes

def read_csv_rows(filepath):
    """Stage 1: Read raw lines."""
    with open(filepath) as f:
        next(f)           # Skip header
        for line in f:
            yield line.strip()

def parse_row(rows):
    """Stage 2: Parse each CSV row into a dict."""
    for row in rows:
        parts = row.split(",")
        yield {"name": parts[0], "score": float(parts[1]), "grade": parts[2]}

def filter_passing(records, min_score=60):
    """Stage 3: Keep only passing records."""
    for record in records:
        if record["score"] >= min_score:
            yield record

def add_rank(records):
    """Stage 4: Add a rank number."""
    for rank, record in enumerate(records, start=1):
        record["rank"] = rank
        yield record

# Compose the pipeline — nothing executes until you consume the final iterator
pipeline = add_rank(
    filter_passing(
        parse_row(
            read_csv_rows("students.csv")
        )
    )
)

for student in pipeline:
    print(f"Rank {student['rank']}: {student['name']} — {student['score']}")
```

---

### 3.12 itertools — Essential Utilities

```python
from itertools import (
    count, cycle, repeat,
    chain, zip_longest,
    islice, takewhile, dropwhile,
    accumulate, groupby,
    combinations, permutations
)

# ── Infinite iterators ────────────────────────────────────────────────────────
# count(start, step) — like range() but infinite
for i in islice(count(10, 2), 5):
    print(i, end=" ")      # 10 12 14 16 18

# cycle(iterable) — loops forever
traffic = cycle(["Red", "Green", "Yellow"])
for _ in range(6):
    print(next(traffic), end=" ")   # Red Green Yellow Red Green Yellow

# repeat(value, n) — repeats value n times (or forever if n omitted)
print(list(repeat("hello", 3)))    # ['hello', 'hello', 'hello']

# ── Combining iterators ───────────────────────────────────────────────────────
# chain — concatenate multiple iterables
a = [1, 2, 3]
b = [4, 5, 6]
c = ["x", "y"]
print(list(chain(a, b, c)))        # [1, 2, 3, 4, 5, 6, 'x', 'y']

# zip_longest — like zip() but pads shorter iterables with fillvalue
names  = ["Alice", "Bob", "Carol"]
scores = [95, 87]
for name, score in zip_longest(names, scores, fillvalue=0):
    print(f"{name}: {score}")
# Alice: 95
# Bob: 87
# Carol: 0

# ── Slicing & filtering ───────────────────────────────────────────────────────
# islice — slice a (possibly infinite) iterator
gen = fibonacci()
print(list(islice(gen, 5, 10)))    # Fibonacci numbers at indices 5–9

# takewhile — take items while condition is True, then stop
data = [2, 4, 6, 7, 8, 10]
evens = list(takewhile(lambda x: x % 2 == 0, data))
print(evens)    # [2, 4, 6]  — stops at 7, doesn't restart for 8

# dropwhile — skip items while condition is True, then yield rest
remaining = list(dropwhile(lambda x: x % 2 == 0, data))
print(remaining)  # [7, 8, 10]

# ── Aggregation ───────────────────────────────────────────────────────────────
# accumulate — running totals (or any binary function)
import operator
values = [1, 2, 3, 4, 5]
print(list(accumulate(values)))                         # [1, 3, 6, 10, 15]  (running sum)
print(list(accumulate(values, operator.mul)))           # [1, 2, 6, 24, 120] (running product)

# ── groupby — group consecutive items by a key ────────────────────────────────
# IMPORTANT: data must be sorted by the key first!
students = [
    {"name": "Alice", "grade": "A"},
    {"name": "Bob",   "grade": "A"},
    {"name": "Carol", "grade": "B"},
    {"name": "David", "grade": "B"},
    {"name": "Eve",   "grade": "A"},   # Would be its own group — not sorted!
]
# Sort first
students.sort(key=lambda s: s["grade"])

for grade, group in groupby(students, key=lambda s: s["grade"]):
    names = [s["name"] for s in group]
    print(f"Grade {grade}: {names}")
# Grade A: ['Alice', 'Bob']
# Grade B: ['Carol', 'David']
# (Eve moved to Grade A group at top after sort)

# ── Combinatorics ─────────────────────────────────────────────────────────────
items = ["A", "B", "C"]
print(list(combinations(items, 2)))       # [('A','B'), ('A','C'), ('B','C')]
print(list(permutations(items, 2)))       # [('A','B'), ('A','C'), ('B','A'), ...]
```

---

### 3.13 Coroutine Preview — Bidirectional Generators

```python
# A coroutine is a generator that both produces AND consumes values.
# This is the conceptual foundation of Python's async/await.

def data_pipeline():
    """
    Receives raw data via send(), transforms it, yields result.
    Pattern: value = yield transformed_value
    """
    processed = []
    while True:
        # Yield current result AND receive next input simultaneously
        raw = yield processed
        if raw is None:
            break
        processed.append(raw.upper().strip())

pipeline = data_pipeline()
next(pipeline)                             # Prime it

pipeline.send("  hello  ")                # Send raw data
pipeline.send("  world  ")
result = pipeline.send("  python  ")      # Get accumulated results
print(result)                             # ['HELLO', 'WORLD', 'PYTHON']
```

---

## 4. Common Mistakes & Gotchas

### Mistake 1 — Iterating an Exhausted Iterator

```python
# ❌ WRONG — iterators are single-use!
numbers_iter = iter([1, 2, 3, 4, 5])
evens = [x for x in numbers_iter if x % 2 == 0]
odds  = [x for x in numbers_iter if x % 2 != 0]   # Empty! iterator exhausted

print(evens)   # [2, 4]
print(odds)    # []  ← Bug! Expected [1, 3, 5]

# ✅ CORRECT — iterate the original list (iterable, not iterator)
numbers = [1, 2, 3, 4, 5]
evens = [x for x in numbers if x % 2 == 0]
odds  = [x for x in numbers if x % 2 != 0]
```

### Mistake 2 — Calling `list()` on an Infinite Generator

```python
# ❌ WRONG — hangs forever (infinite loop consuming infinite values)
def naturals():
    n = 1
    while True:
        yield n
        n += 1

# all_naturals = list(naturals())   # ← NEVER do this!

# ✅ CORRECT — use islice, takewhile, or a for loop with break
from itertools import islice
first_100 = list(islice(naturals(), 100))
```

### Mistake 3 — Forgetting to Prime a Coroutine

```python
# ❌ WRONG — send() before first next() raises TypeError
def accumulator():
    total = 0
    while True:
        value = yield total
        total += value

acc = accumulator()
acc.send(10)    # TypeError: can't send non-None value to a just-started generator

# ✅ CORRECT — always call next() (or send(None)) to advance to first yield
acc = accumulator()
next(acc)       # Prime: advance to first yield, returns 0
acc.send(10)    # Now works: returns 10
acc.send(20)    # Returns 30
```

### Mistake 4 — `return` in a Generator Returns, Doesn't Yield

```python
# ❌ WRONG — thinking return yields a value
def bad_generator():
    return [1, 2, 3]    # This is a regular function, not a generator at all!
                        # (No yield anywhere = no generator object created)

# ❌ ALSO WRONG — thinking return yields the value in a generator
def also_bad():
    yield 1
    return 2    # This raises StopIteration(2) — 2 is NOT yielded!

gen = also_bad()
print(next(gen))    # 1
# print(next(gen))  # StopIteration — '2' is stored in e.value, not returned normally

# ✅ CORRECT — use yield to produce values
def good_generator():
    yield 1
    yield 2
    yield 3
```

### Mistake 5 — Mutating a List While Iterating Over It

```python
# ❌ WRONG — modifying the list during iteration causes skipped items
numbers = [1, 2, 3, 4, 5, 6]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)   # Mutating while iterating = chaos!
print(numbers)   # [1, 3, 5]  ← looks right but is wrong for other cases

# ✅ CORRECT — iterate over a copy, or build a new list with a comprehension
numbers = [1, 2, 3, 4, 5, 6]
odds = [n for n in numbers if n % 2 != 0]
print(odds)   # [1, 3, 5]
```

---

## 5. Hands-on Exercises

### Guided Exercise 1 — Custom Iterator: Squared Numbers (25 min)

**Goal:** Build a `SquaredRange` iterator class that yields the squares of integers in a range.

**Step 1:** Basic structure
```python
class SquaredRange:
    """
    Yields squares of integers from start to stop (exclusive).
    Example: SquaredRange(1, 5) → 1, 4, 9, 16
    """
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.current = start
    
    def __iter__(self):
        self.current = self.start   # Allow re-iteration
        return self
    
    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        value = self.current ** 2
        self.current += 1
        return value
```

**Step 2:** Test it
```python
sr = SquaredRange(1, 6)
print(list(sr))           # [1, 4, 9, 16, 25]
print(list(sr))           # [1, 4, 9, 16, 25]  ← re-iterable? Yes!
print(sum(sr))            # 55
print(max(sr))            # 25
```

**Step 3:** Extend it — add `__len__` and `__contains__`
```python
    def __len__(self):
        return max(0, self.stop - self.start)
    
    def __contains__(self, item):
        """Check if item is a perfect square in our range."""
        import math
        root = math.isqrt(item)
        return root * root == item and self.start <= root < self.stop

sr = SquaredRange(1, 6)
print(len(sr))            # 5
print(9 in sr)            # True  (3² = 9, 3 is in range)
print(10 in sr)           # False (not a perfect square)
print(36 in sr)           # False (6² = 36, but 6 is NOT in range [1,6))
```

---

### Guided Exercise 2 — Generator Pipeline: Log File Analyzer (30 min)

**Goal:** Build a composable generator pipeline that reads, filters, and aggregates a log file.

**Setup:** Create a sample log file
```python
import random
from datetime import datetime, timedelta

def create_sample_log(filepath, num_lines=1000):
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    messages = {
        "DEBUG":    ["Cache miss", "DB query executed", "Template rendered"],
        "INFO":     ["User logged in", "Page viewed", "File uploaded"],
        "WARNING":  ["High memory usage", "Slow query detected", "Deprecated API"],
        "ERROR":    ["Payment failed", "DB connection timeout", "File not found"],
        "CRITICAL": ["Server out of memory", "DB unreachable", "Disk full"],
    }
    base_time = datetime.now()
    with open(filepath, "w") as f:
        for i in range(num_lines):
            ts = (base_time + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S")
            level = random.choice(levels)
            msg = random.choice(messages[level])
            f.write(f"{ts} | {level:8s} | {msg}\n")

create_sample_log("app.log")
```

**Build the pipeline:**
```python
# Stage 1: Raw line reader
def read_log_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()

# Stage 2: Parse each line into a dict
def parse_log_line(lines):
    for line in lines:
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 3:
            yield {
                "timestamp": parts[0],
                "level":     parts[1],
                "message":   parts[2]
            }

# Stage 3: Filter by level
def filter_by_level(records, *levels):
    level_set = set(levels)
    for record in records:
        if record["level"] in level_set:
            yield record

# Stage 4: Count occurrences per message
def count_messages(records):
    from collections import Counter
    counts = Counter(r["message"] for r in records)
    for message, count in counts.most_common():
        yield {"message": message, "count": count}

# Build and run the pipeline
pipeline = count_messages(
    filter_by_level(
        parse_log_line(
            read_log_lines("app.log")
        ),
        "ERROR", "CRITICAL"
    )
)

print("=== Top Error Messages ===")
for item in pipeline:
    print(f"  {item['count']:4d}x  {item['message']}")
```

---

### Independent Practice 1 — Prime Number Generator (20 min)

**Task:** Write a generator function `primes()` that yields prime numbers infinitely.

**Requirements:**
- No hard-coded list — compute each prime on the fly
- Must correctly identify all primes
- Use `islice` to get the first N primes
- Bonus: write a `is_prime(n)` helper and use it in the generator

**Hints:**
- A number is prime if it's divisible by no integer from 2 to √n
- Use `math.isqrt(n)` for the square root check
- Start your generator at n=2

**Expected output:**
```python
from itertools import islice
gen = primes()
print(list(islice(gen, 10)))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

---

### Independent Practice 2 — Running Statistics with itertools (20 min)

**Task:** Given a list of daily temperatures, use `itertools.accumulate` and generator expressions to compute:
1. Running total of temperatures
2. Running average (as a generator)
3. The day (index) when the running average first exceeded 25°C
4. Identify "hot streaks" — consecutive days above 30°C

```python
temperatures = [22, 25, 28, 31, 33, 30, 29, 32, 35, 34, 27, 24, 26, 31, 30]

# Your code here using itertools.accumulate, takewhile, dropwhile, groupby
```

**Hints:**
- `accumulate(temps)` gives running sums — divide by index+1 for average
- `groupby(enumerate(temps), key=lambda x: x[1] > 30)` groups hot/cool days

---

### 🏆 Challenge Problem — Infinite Sequence Algebra (Stretch Goal)

**Task:** Implement a `LazySequence` class that wraps a generator and supports:
- `take(n)` — return a list of the next n items
- `skip(n)` — skip n items and return self (chainable)
- `filter(func)` — return a new LazySequence with only matching items
- `map(func)` — return a new LazySequence with transformed items
- `zip_with(other)` — return a new LazySequence zipped with another

```python
# Expected usage:
result = (LazySequence(fibonacci())
          .skip(2)
          .filter(lambda x: x % 2 == 0)
          .map(lambda x: x * 10)
          .take(5))

print(result)    # [20, 80, 340, 1440, 6120]  (even Fibonacci × 10, starting from index 2)
```

---

## 6. Best Practices & Industry Standards

### Iterator / Generator Design
1. **Prefer generators over custom iterator classes** for simple sequences — they're shorter, cleaner, and automatically handle `StopIteration`.
2. **Make iterables re-iterable** — if you write a class, implement `__iter__` to return a fresh iterator each time (reset state in `__iter__`, not `__init__`).
3. **Name generators with verbs** — `read_lines()`, `parse_records()`, `filter_errors()` describe what they *do*, not what they *are*.
4. **Keep generator stages small and single-purpose** — one transformation per function. This makes pipelines easy to test and reason about.
5. **Use `yield from`** to delegate to a sub-generator:
   ```python
   def chain_files(*filepaths):
       for path in filepaths:
           yield from read_lines(path)   # Clean delegation
   ```

### Logging
6. **Use `islice` as a safety valve** on potentially large generators during debugging:
   ```python
   for item in islice(large_pipeline(), 100):   # Never process more than 100 during dev
       print(item)
   ```
7. **Never store a generator result if you'll iterate it twice** — convert to `list()` or `tuple()` first if you need multiple passes.
8. **Prefer `itertools` over manual loops** — it's C-level speed, battle-tested, and expressive. Reach for it before writing any iteration loop manually.
9. **Use `collections.deque(gen, maxlen=N)`** to efficiently get the last N items from a generator without storing all items.

### Performance Tips
- `sum(x**2 for x in data)` is faster than `sum([x**2 for x in data])` — no intermediate list
- `any(pred(x) for x in data)` short-circuits on first `True` — use it instead of `len([x for x in data if pred(x)]) > 0`
- `all(pred(x) for x in data)` short-circuits on first `False` — same idea

---

## 7. Real-World Application

### Where Are Iterators & Generators Used?

| Context | Use Case |
|---|---|
| **Django ORM** | `User.objects.filter(active=True)` is a lazy iterator — SQL runs only when consumed |
| **Pandas** | `df.iterrows()`, `read_csv(chunksize=1000)` — stream large DataFrames |
| **Flask/Streaming** | `Response(generate_csv(), mimetype='text/csv')` — stream large file downloads |
| **Celery/Queues** | Task results are lazy — not fetched until `.get()` |
| **Python stdlib** | `csv.reader`, `json.JSONDecoder`, `xml.etree.ElementTree.iterparse()` |
| **Data pipelines** | ETL jobs reading millions of rows without RAM overflow |

### Mini Project — Django-style Lazy Query Simulator

```python
# This shows the pattern that Django's QuerySet uses internally.
# In Django, User.objects.filter() returns a lazy object — the DB query
# runs only when you iterate, call list(), or access len().

class LazyQuery:
    """Simulates Django's queryset lazy evaluation."""
    
    def __init__(self, data_source, filters=None, limit=None):
        self._data_source = data_source   # Could be a DB connection
        self._filters = filters or []
        self._limit = limit
        self._cache = None                # Results cached after first eval
    
    def filter(self, func):
        """Returns a new LazyQuery with an additional filter — does NOT execute yet."""
        new_filters = self._filters + [func]
        return LazyQuery(self._data_source, new_filters, self._limit)
    
    def limit(self, n):
        return LazyQuery(self._data_source, self._filters, n)
    
    def _evaluate(self):
        """Actually runs the query — lazy evaluation happens here."""
        if self._cache is not None:
            return self._cache
        print("[DB] Executing query now...")   # Proves laziness
        result = self._data_source
        for f in self._filters:
            result = (item for item in result if f(item))
        if self._limit:
            from itertools import islice
            result = islice(result, self._limit)
        self._cache = list(result)
        return self._cache
    
    def __iter__(self):
        return iter(self._evaluate())
    
    def __len__(self):
        return len(self._evaluate())

# Simulated database
all_users = [
    {"id": i, "name": f"User{i}", "active": i % 2 == 0, "age": 20 + (i % 40)}
    for i in range(1, 1001)
]

# This chain is LAZY — no data processed yet
query = (LazyQuery(iter(all_users))
         .filter(lambda u: u["active"])
         .filter(lambda u: u["age"] >= 30)
         .limit(5))

print("Query built — nothing executed yet.")
print(f"Results: {list(query)}")   # ← DB query runs HERE
```

### Connection to Upcoming Days
- **Day 11 (File I/O):** `csv.reader` is an iterator; generator-based file processing
- **Day 12 (Databases):** SQLite cursor is an iterator; Django QuerySet is a lazy iterator
- **Day 13 (Comprehensions / Functional):** Generator expressions, `map()`, `filter()`, `zip()` tie directly to today
- **Day 20 (Django ORM Deep Dive):** `QuerySet.iterator()`, chunked evaluation, `select_related` lazy loading

---

## 8. Quick Revision Summary

### Key Terms
| Term | Definition |
|---|---|
| **Iterable** | Any object with `__iter__()` — can produce an iterator |
| **Iterator** | Object with `__iter__()` + `__next__()` — maintains position state |
| **StopIteration** | Exception signalling the iterator has no more values |
| **Generator function** | Function with `yield` — returns a generator object |
| **Generator object** | An iterator created by a generator function |
| **Generator expression** | Lazy version of a list comprehension: `(x for x in ...)` |
| **yield** | Pauses a function, returns a value, preserves state |
| **yield from** | Delegates iteration to a sub-iterable |
| **Lazy evaluation** | Computing values only when needed, not all at once |
| **Coroutine** | Generator that can receive values via `send()` |
| **send()** | Push a value into a paused generator |
| **throw()** | Inject an exception into a running generator |
| **close()** | Terminate a generator by throwing `GeneratorExit` |
| **itertools** | Standard library of composable, C-speed iterator building blocks |
| **islice** | Slice a (possibly infinite) iterator by index |
| **chain** | Concatenate multiple iterables into one |
| **groupby** | Group consecutive items by a key function |
| **accumulate** | Running aggregation (sum, product, etc.) |

### Core Syntax Cheat Sheet

```python
# Custom iterator class
class MyIter:
    def __iter__(self): return self
    def __next__(self):
        if done: raise StopIteration
        return next_value

# Generator function
def gen_func():
    yield value1
    yield value2

# Generator expression
genexp = (expr for x in iterable if condition)

# yield from (delegation)
def outer():
    yield from inner_generator()

# Priming and using a coroutine
coro = my_coroutine()
next(coro)               # prime
coro.send(value)         # send value, get yielded value back
coro.throw(ValueError)   # inject exception
coro.close()             # terminate

# itertools essentials
from itertools import islice, chain, count, cycle, takewhile, dropwhile, accumulate, groupby

list(islice(gen, 10))                     # first 10 items
list(chain([1,2], [3,4]))                 # [1, 2, 3, 4]
list(islice(count(0, 2), 5))              # [0, 2, 4, 6, 8]
list(takewhile(lambda x: x < 5, data))   # items while < 5
list(accumulate(data))                    # running sums
```

### 5 MCQ Recap Questions

**Q1.** What is the difference between an *iterable* and an *iterator* in Python?
- A) They are the same thing
- B) An iterator can only be used once; an iterable can be re-iterated
- **C) An iterable has `__iter__()`; an iterator has both `__iter__()` and `__next__()` ✅**
- D) Iterators are faster than iterables

**Q2.** What happens when you call `next()` on an exhausted iterator?
- A) Returns `None`
- B) Returns the last value again
- **C) Raises `StopIteration` ✅**
- D) Restarts from the beginning

**Q3.** Which of these creates a **generator object**, not a list?
- A) `[x**2 for x in range(10)]`
- **B) `(x**2 for x in range(10))` ✅**
- C) `{x**2 for x in range(10)}`
- D) `list(x**2 for x in range(10))`

**Q4.** What must you do before calling `.send(value)` on a freshly created generator?
- A) Call `.start()`
- B) Call `.run()`
- **C) Call `next()` on it (prime the generator) ✅**
- D) Nothing — `.send()` works immediately

**Q5.** `itertools.groupby()` requires the data to be:
- A) In any order — it groups all matching items regardless of position
- B) Sorted in reverse order
- **C) Sorted by the grouping key — it only groups *consecutive* matching items ✅**
- D) Converted to a list first

---

## 9. Instructor Notes

### Common Student Questions to Anticipate

| Question | Answer |
|---|---|
| "Is every `for`-able thing an iterator?" | No — lists, strings, dicts are *iterables*, not iterators. `iter()` creates an iterator from them. |
| "Can I use a generator twice?" | No — generators are single-use. Store as `list()` if you need multiple passes. |
| "What's the point of `yield from`?" | Cleaner delegation — avoids writing `for x in sub: yield x`. Also correctly propagates `send()` and `throw()`. |
| "When should I use a class-based iterator vs a generator?" | Generator almost always — it's shorter and cleaner. Class-based only when you need extra methods (like `__len__`, `__contains__`) or complex state sharing. |
| "Is `async/await` the same as generators?" | They're built on the same machinery (`__await__` uses `__next__` under the hood), but `async/await` is a higher-level abstraction for I/O concurrency. Preview for Day 30+. |
| "Why is `takewhile` different from list comprehension filtering?" | `takewhile` *stops at the first False* and never processes the rest. A filter comprehension checks *every* item even after a False. |

### Suggested Whiteboard Diagrams

1. **Iterable vs Iterator Venn Diagram** — Two circles: "Has `__iter__`" (large, containing lists/strings/etc.) and "Has `__iter__` + `__next__`" (smaller, inside, for iterators/generators). Show `iter()` as the bridge.
2. **Generator Execution Timeline** — A timeline showing a generator function's execution: code runs → hits `yield` → freezes (value returned to caller) → caller calls `next()` → resumes exactly where it left off.
3. **Generator Pipeline Diagram** — Draw each stage as a pipe segment with arrows. Show data flowing through: `read_file` → `parse` → `filter` → `aggregate`. Emphasize that data flows one item at a time.
4. **Memory Comparison Bar Chart** — Draw two bars: "List 1M items" (~8 MB) vs "Generator 1M items" (~200 bytes). Visual impact is powerful.

### ⏱ Timing Guide (3 Hours)

| Time | Activity | Duration |
|---|---|---|
| 0:00 – 0:10 | Recap Day 9, session overview | 10 min |
| 0:10 – 0:30 | Iterable vs Iterator concept + demo with `iter()` / `next()` | 20 min |
| 0:30 – 0:50 | Custom iterator class — live code `CountDown` then `MyRange` | 20 min |
| 0:50 – 1:10 | Generator functions — `yield`, state, infinite generators | 20 min |
| 1:10 – 1:20 | ☕ Short Break | 10 min |
| 1:20 – 1:35 | Generator expressions + memory comparison demo | 15 min |
| 1:35 – 1:55 | `send()`, `throw()`, `close()` + coroutine preview | 20 min |
| 1:55 – 2:20 | itertools deep-dive + live demos | 25 min |
| 2:20 – 2:40 | Guided Exercise 2 — log pipeline (instructor-led) | 20 min |
| 2:40 – 2:55 | Independent practice (primes generator) | 15 min |
| 2:55 – 3:00 | MCQ recap + preview Day 11 | 5 min |

*Challenge problem and Exercise 1 (SquaredRange) assigned as homework.*

### Resources & Further Reading
- 📖 [Python Docs — Iterator Types](https://docs.python.org/3/library/stdtypes.html#iterator-types)
- 📖 [Python Docs — itertools](https://docs.python.org/3/library/itertools.html)
- 📖 [PEP 255 — Simple Generators](https://peps.python.org/pep-0255/)
- 📖 [PEP 342 — Coroutines via Enhanced Generators](https://peps.python.org/pep-0342/)
- 📖 [PEP 380 — yield from](https://peps.python.org/pep-0380/)
- 📺 [David Beazley — Generator Tricks for Systems Programmers](http://www.dabeaz.com/generators/)
- 📖 [Real Python — Introduction to Python Generators](https://realpython.com/introduction-to-python-generators/)
- 📖 [Fluent Python Ch. 17 — Iterators, Generators, and Classic Coroutines](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/)
