# Day 10 — Interview Questions: Python Iterators & Generators
### Python Full Stack Bootcamp | Interview Prep Reference

---

> 💡 **How to use this file:** Questions are grouped by difficulty. Read the concept, answer mentally, then compare with the model answer. Senior-level questions expect live coding.

---

## 🟢 Beginner Level (0–1 Year Experience)

---

**Q1. What is an iterator in Python? How is it different from an iterable?**

**Model Answer:**
An **iterable** is any object that can return an iterator — it implements `__iter__()`. Examples: `list`, `str`, `dict`, `range`, `tuple`.

An **iterator** is an object that maintains position state and can produce the next item on demand. It implements *both* `__iter__()` and `__next__()`.

The key distinction:
- Iterables can produce **multiple independent iterators** (re-iterable)
- Iterators are **single-use** — once exhausted, they cannot restart

```python
nums = [1, 2, 3]          # iterable — has __iter__ only
it = iter(nums)            # iterator — has __iter__ + __next__

print(next(it))            # 1
print(next(it))            # 2
print(list(iter(nums)))    # [1, 2, 3]  — fresh iterator from same list
print(list(it))            # [3]  — iterator continues from where it left off
```

---

**Q2. What does the `yield` keyword do? How is it different from `return`?**

**Model Answer:**

| | `return` | `yield` |
|---|---|---|
| Ends function? | Yes | No — pauses it |
| Can appear multiple times? | Once (only first is used) | Many times |
| Returns type | The value directly | A generator object |
| State preserved? | No | Yes — entire local scope frozen |

`yield` pauses the function, returns the value to the caller, and preserves all local variables. Execution resumes at the `yield` statement on the next call to `next()`.

```python
def counter():
    print("Starting")
    yield 1               # Pause here, return 1
    print("Resumed")
    yield 2               # Pause here, return 2
    print("Done")

gen = counter()
print(next(gen))    # Prints "Starting", returns 1
print(next(gen))    # Prints "Resumed", returns 2
# next(gen)         # Prints "Done", raises StopIteration
```

---

**Q3. What is a generator expression? How does it differ from a list comprehension?**

**Model Answer:**
A generator expression is a one-liner generator defined with `()` instead of `[]`. It is **lazy** — values are computed only when requested. A list comprehension is **eager** — all values are computed and stored in memory immediately.

```python
# List comprehension — all 1M squares created immediately (~8 MB)
squares_list = [x**2 for x in range(1_000_000)]

# Generator expression — nothing computed yet (~200 bytes)
squares_gen  = (x**2 for x in range(1_000_000))

# Both produce same results when iterated:
print(next(iter(squares_list)))   # 0
print(next(squares_gen))          # 0
```

Use generator expressions when you only need to iterate once and don't need random access.

---

**Q4. What is `StopIteration` and when is it raised?**

**Model Answer:**
`StopIteration` is a built-in exception that signals that an iterator has no more items to produce. It is:
- Raised automatically when a generator function returns (runs off the end or hits `return`)
- Raised by `__next__()` in custom iterators when items are exhausted
- Caught automatically by `for` loops, `list()`, `sum()`, and other consuming constructs

```python
it = iter([1, 2])
print(next(it))   # 1
print(next(it))   # 2
print(next(it))   # raises StopIteration

# Safe alternative with default:
print(next(it, "no more"))   # "no more" — no exception raised
```

---

**Q5. Why would you use a generator instead of returning a list?**

**Model Answer:**
Three main reasons:

1. **Memory efficiency:** Generators compute values one at a time. Processing a 10 GB file with a generator uses ~constant memory; a list would require 10 GB of RAM.

2. **Performance:** For early exit scenarios (e.g., `any()`, `next()` with a condition), generators stop as soon as the answer is found — a list must build everything first.

3. **Infinite sequences:** You can represent infinite sequences (Fibonacci, prime numbers, event streams) that would be impossible as a list.

```python
# Generator — works on a 100 GB file; list() would crash
def read_records(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()

# Finding first match — generator stops at first hit; list checks everything
first_error = next((r for r in read_records("log.txt") if "ERROR" in r), None)
```

---

**Q6. What do `iter()` and `next()` built-in functions do?**

**Model Answer:**
- `iter(obj)` — calls `obj.__iter__()` and returns the resulting iterator. If `obj` is already an iterator, it returns itself.
- `next(iterator)` — calls `iterator.__next__()` and returns the next value.
- `next(iterator, default)` — returns `default` instead of raising `StopIteration` when exhausted.

```python
data = [10, 20, 30]
it = iter(data)        # list_iterator object

print(next(it))        # 10
print(next(it))        # 20
print(next(it))        # 30
print(next(it, -1))    # -1  (default — no exception)
```

---

**Q7. Name three `itertools` functions and what they do.**

**Model Answer:**

| Function | What it does | Example |
|---|---|---|
| `islice(it, n)` | Take first n items from any iterator | `list(islice(count(), 5))` → `[0,1,2,3,4]` |
| `chain(*iterables)` | Concatenate multiple iterables | `list(chain([1,2],[3,4]))` → `[1,2,3,4]` |
| `accumulate(it)` | Running sum (or custom operation) | `list(accumulate([1,2,3]))` → `[1,3,6]` |
| `cycle(it)` | Loop an iterable forever | `cycle([A, B, C])` → A,B,C,A,B,C,... |
| `takewhile(pred, it)` | Take items while predicate is True | `list(takewhile(lambda x: x<5, [2,4,6,8]))` → `[2,4]` |
| `groupby(it, key)` | Group consecutive items by key | Groups sorted data into key-based clusters |

---

## 🟡 Intermediate Level (1–2 Years Experience)

---

**Q8. Explain the iterator protocol. What methods must a class implement to be iterable vs an iterator?**

**Model Answer:**
The iterator protocol is Python's formal interface for sequential access to data.

**To be an iterable** — implement `__iter__()` which returns an iterator object.

**To be an iterator** — implement both:
- `__iter__()` — must return `self` (the iterator is its own iterator)
- `__next__()` — returns the next value or raises `StopIteration` when done

```python
class EvenNumbers:
    """Iterable — produces fresh iterators each time."""
    def __init__(self, limit):
        self.limit = limit
    
    def __iter__(self):
        return EvenNumbersIterator(self.limit)   # Returns a NEW iterator

class EvenNumbersIterator:
    """Iterator — single-use, maintains state."""
    def __init__(self, limit):
        self.current = 0
        self.limit = limit
    
    def __iter__(self):
        return self      # Iterator's __iter__ returns itself
    
    def __next__(self):
        if self.current > self.limit:
            raise StopIteration
        value = self.current
        self.current += 2
        return value

evens = EvenNumbers(10)
print(list(evens))    # [0, 2, 4, 6, 8, 10]
print(list(evens))    # [0, 2, 4, 6, 8, 10]  — re-iterable!
```

---

**Q9. What is `yield from` and when would you use it?**

**Model Answer:**
`yield from iterable` delegates iteration to a sub-iterable. It's equivalent to `for x in iterable: yield x`, but with two critical advantages:

1. It also correctly forwards `send()`, `throw()`, and `close()` to the sub-generator
2. It captures the `return` value of the sub-generator (stored in `StopIteration.value`)

```python
# Without yield from — verbose and breaks coroutine protocol
def chain_bad(*iterables):
    for it in iterables:
        for item in it:
            yield item

# With yield from — clean and correct
def chain_good(*iterables):
    for it in iterables:
        yield from it

# Recursive use — flattening nested lists
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # Recurse
        else:
            yield item

print(list(flatten([1, [2, [3, 4]], [5, 6]])))
# Output: [1, 2, 3, 4, 5, 6]
```

---

**Q10. Explain lazy evaluation. Give a concrete example where it prevents a bug or saves memory.**

**Model Answer:**
Lazy evaluation means computations are deferred until the result is actually needed. In Python, generators implement lazy evaluation — each value is computed only when `next()` is called.

**Memory saving example:**
```python
import sys

# Finding first 5-digit prime — eager approach
def primes_list_up_to(n):
    return [x for x in range(2, n) if all(x % i != 0 for i in range(2, x))]

# Eager: computes ALL numbers up to 100,000 before you can look at anything
result_list = primes_list_up_to(100_000)
first_5digit = next(x for x in result_list if x >= 10_000)

# Lazy: stops generating as soon as first 5-digit prime found
def primes_gen():
    def is_prime(n):
        return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5)+1))
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1

first_5digit_lazy = next(x for x in primes_gen() if x >= 10_000)
print(first_5digit_lazy)   # 10007 — found immediately, no wasted computation
```

**Bug prevention — infinite sequences:**
```python
# You can't even represent this as a list:
def naturals():
    n = 1
    while True:
        yield n
        n += 1

# But you can process it safely:
total = sum(islice(naturals(), 1_000_000))   # Sum first million naturals
```

---

**Q11. What is a coroutine? How do `send()`, `throw()`, and `close()` work?**

**Model Answer:**
A coroutine is a generator that can both *produce* values (via `yield`) and *consume* values (via `send()`). Regular generators are pull-only; coroutines are bidirectional.

- **`send(value)`** — resumes the generator and makes `value` the result of the `yield` expression inside. Requires priming with `next()` first.
- **`throw(ExcType, value)`** — resumes the generator but raises an exception at the `yield` point. The generator can catch and handle it.
- **`close()`** — throws `GeneratorExit` into the generator, causing it to clean up and terminate.

```python
def logger_coroutine(logfile):
    """Receives log messages via send(), writes to file."""
    print(f"Opening {logfile}")
    with open(logfile, "w") as f:
        try:
            while True:
                message = yield              # Pause, wait for send()
                f.write(message + "\n")
        except GeneratorExit:
            print("Logger shutting down")   # Triggered by close()

logger = logger_coroutine("output.log")
next(logger)                      # Prime
logger.send("INFO: App started")  # Write to file
logger.send("ERROR: DB failed")   # Write to file
logger.close()                    # Clean shutdown — triggers GeneratorExit
```

---

**Q12. Why must `itertools.groupby()` receive sorted data? What happens if you forget?**

**Model Answer:**
`groupby()` groups only **consecutive** items with the same key — it does not scan the entire sequence. If unsorted data has the same key value in non-consecutive positions, each cluster becomes its own separate group.

```python
from itertools import groupby

# ❌ Unsorted — "A" appears in two separate groups
data = [("Alice", "A"), ("Bob", "B"), ("Carol", "A")]
for grade, group in groupby(data, key=lambda x: x[1]):
    print(grade, [x[0] for x in group])
# A ['Alice']
# B ['Bob']
# A ['Carol']   ← separate group! Not merged with first A

# ✅ Sort first — all A's grouped together
data.sort(key=lambda x: x[1])
for grade, group in groupby(data, key=lambda x: x[1]):
    print(grade, [x[0] for x in group])
# A ['Alice', 'Carol']
# B ['Bob']
```

---

**Q13. How does a Python `for` loop actually work under the hood?**

**Model Answer:**
A `for` loop is syntactic sugar for the iterator protocol:

```python
for item in collection:
    do_something(item)

# Translates exactly to:
_iterator = iter(collection)         # 1. Get iterator via __iter__()
while True:
    try:
        item = next(_iterator)       # 2. Get next item via __next__()
        do_something(item)           # 3. Execute loop body
    except StopIteration:            # 4. Catch exhaustion signal
        break                        # 5. Exit loop cleanly
```

This is why `for` works on *any* object implementing the iterator protocol — lists, strings, generators, database cursors, HTTP response streams — it's completely generic.

---

## 🔴 Advanced Level (2+ Years / Senior Roles)

---

**Q14. Design a memory-efficient pipeline to process a 10 GB CSV file: filter rows where revenue > 1000, compute the top 5 product categories by total revenue. No pandas.**

**Model Answer:**
```python
import csv
from itertools import islice
from collections import defaultdict

def read_csv_rows(filepath):
    """Stage 1: Yield one row at a time — O(1) memory."""
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        yield from reader              # delegates, preserves send/throw

def parse_revenue(rows):
    """Stage 2: Convert revenue field to float, skip bad rows."""
    for row in rows:
        try:
            row["revenue"] = float(row["revenue"])
            yield row
        except (ValueError, KeyError):
            pass    # Skip malformed rows silently

def filter_high_revenue(rows, threshold=1000):
    """Stage 3: Keep only high-revenue rows."""
    return (row for row in rows if row["revenue"] > threshold)

def aggregate_by_category(rows):
    """Stage 4: Accumulate totals — must consume all rows."""
    totals = defaultdict(float)
    for row in rows:
        totals[row["category"]] += row["revenue"]
    return totals

def top_n(totals, n=5):
    """Stage 5: Return top N categories."""
    return sorted(totals.items(), key=lambda x: x[1], reverse=True)[:n]

# Assemble pipeline
pipeline = filter_high_revenue(
    parse_revenue(
        read_csv_rows("sales.csv")
    )
)

totals = aggregate_by_category(pipeline)
for category, revenue in top_n(totals, 5):
    print(f"{category}: ₹{revenue:,.2f}")

# Memory footprint: ~constant — only one CSV row + running totals in RAM
```

Key design decisions to explain:
- Each stage is a generator — data flows one row at a time
- `aggregate_by_category` *must* materialize all data (aggregation requires seeing everything)
- Stages 1–3 are zero-copy pipelines; Stage 4 is the only memory consumer (dict of categories)

---

**Q15. What is the difference between a generator-based coroutine and `async def` / `await`?**

**Model Answer:**
Both are based on the same underlying Python mechanism (suspension/resumption of execution), but serve different purposes:

| | Generator Coroutine | `async/await` Coroutine |
|---|---|---|
| Syntax | `def` + `yield` / `send()` | `async def` + `await` |
| Purpose | Data pipelines, bidirectional streaming | Concurrent I/O (network, files, DB) |
| Runtime | Standard Python | Requires event loop (`asyncio`) |
| Yielding to | Caller | Event loop (to resume when I/O is ready) |
| Introduced | PEP 342 (Python 2.5) | PEP 492 (Python 3.5) |

`async/await` is built *on top of* generator coroutines — `await expr` is essentially `yield from expr.__await__()`. The event loop uses `send()` to resume coroutines when their awaited I/O completes.

```python
# Generator coroutine (manual, low-level)
def pipeline_stage():
    while True:
        data = yield           # receive via send()
        yield data.upper()     # produce transformed result

# async coroutine (high-level, I/O-focused)
async def fetch_user(user_id):
    async with aiohttp.ClientSession() as session:
        response = await session.get(f"/users/{user_id}")   # yield to event loop
        return await response.json()
```

---

**Q16. Implement a `@coroutine` decorator that automatically primes a coroutine.**

**Model Answer:**
```python
import functools

def coroutine(func):
    """
    Decorator that automatically primes a generator coroutine.
    Eliminates the need to call next() before first send().
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)     # Prime: advance to first yield
        return gen
    return wrapper

@coroutine
def accumulate_and_report(label):
    """Receives numbers, prints running total with label."""
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value
        print(f"[{label}] received {value}, total: {total}")

acc = accumulate_and_report("Sales")
# No next() needed — decorator primed it
acc.send(100)    # [Sales] received 100, total: 100
acc.send(250)    # [Sales] received 250, total: 350
acc.send(75)     # [Sales] received 75, total: 425
```

---

**Q17. How does Django's QuerySet implement lazy evaluation? What's the risk if you don't understand this?**

**Model Answer:**
Django's `QuerySet` is a lazy iterator — building a queryset (e.g., `User.objects.filter(active=True)`) does **not** hit the database. The SQL query is only executed when the queryset is *evaluated*: by iterating (`for user in qs`), calling `list(qs)`, slicing (`qs[:10]`), calling `len(qs)`, or calling `.count()`.

**The N+1 Problem (a classic misunderstanding of lazy loading):**
```python
# ❌ N+1 Problem — understanding generators/lazy eval prevents this bug
posts = Post.objects.all()          # Lazy — no query yet
for post in posts:                   # Query 1: SELECT * FROM post
    print(post.author.name)          # Query 2,3,4...N: SELECT * FROM user WHERE id=?
# For 1000 posts → 1001 queries!

# ✅ Fix with select_related — tells Django to JOIN eagerly
posts = Post.objects.select_related("author").all()   # One query with JOIN
for post in posts:
    print(post.author.name)          # No additional queries — already loaded
```

**Double-evaluation trap:**
```python
# ❌ Each evaluation hits the DB again
qs = User.objects.filter(active=True)
count = len(qs)        # DB hit #1
first = list(qs)       # DB hit #2

# ✅ Evaluate once
users = list(User.objects.filter(active=True))   # One DB hit
count = len(users)      # In memory — no DB
first = users[0]        # In memory — no DB
```
