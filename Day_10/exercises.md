# Day 10 — Exercises: Python Iterators & Generators
### Python Full Stack Bootcamp | Hands-on Practice

---

> 📋 **Instructions:**
> - Complete exercises in order — concepts build on each other
> - Run each code block and verify the output matches what's expected
> - Write your own solution first, then check the hints only if stuck
> - All files should be saved as separate `.py` files

---

## Exercise 1 — Warm-Up: Iterator Mechanics (15 min)

**File:** `ex01_iterator_basics.py`

**Goal:** Build intuition about how `iter()` and `next()` work before writing any custom iterators.

### Part A — Predict the Output

Read each snippet and write your expected output *before* running it.

```python
# Snippet 1
data = [10, 20, 30, 40]
it = iter(data)
print(next(it))
print(next(it))
it2 = iter(data)   # fresh iterator
print(next(it2))
print(next(it))    # continues from where it1 left off

# Snippet 2
words = "hello"
char_iter = iter(words)
print(list(char_iter))
print(list(char_iter))   # What happens here?

# Snippet 3
def counter_gen():
    yield "a"
    yield "b"
    yield "c"

gen = counter_gen()
print(next(gen))
for x in gen:        # continues from where next() left off
    print(x)
```

**Write your predictions here:**
```
Snippet 1: ____________________
Snippet 2: ____________________
Snippet 3: ____________________
```

---

### Part B — Safe Iteration

```python
# Fill in the blanks to safely consume an iterator with a default value.

def safe_peek(iterator, default=None):
    """
    Return the next item from iterator without raising StopIteration.
    Return default if iterator is exhausted.
    
    Hint: Use the two-argument form of next()
    """
    return _______________

# Test cases:
it = iter([1, 2, 3])
print(safe_peek(it))          # 1
print(safe_peek(it))          # 2
print(safe_peek(it))          # 3
print(safe_peek(it))          # None
print(safe_peek(it, "done"))  # "done"
```

---

### Part C — Exploring Built-in Iterators

```python
# Answer these by running code:

# 1. Is a range() object an iterable or an iterator?
r = range(5)
print(hasattr(r, "__iter__"))   # ?
print(hasattr(r, "__next__"))   # ?
# Is range() an iterable or iterator? ___

# 2. What about iter(range(5))?
ri = iter(range(5))
print(hasattr(ri, "__next__"))  # ?
# ___

# 3. Can you call iter() on a dict? What do you get?
d = {"a": 1, "b": 2}
it = iter(d)
print(next(it))   # Keys or values? ___

# 4. Is a file object an iterator or just an iterable?
with open(__file__) as f:   # __file__ is this script itself
    print(hasattr(f, "__next__"))  # ?
    print(f is iter(f))            # True or False? ___
```

---

## Exercise 2 — Custom Iterator Classes (30 min)

**File:** `ex02_custom_iterators.py`

### 2.1 — Implement `MyRange` from Scratch

```python
class MyRange:
    """
    Re-implement Python's built-in range() as a class-based iterator.
    
    Requirements:
    - Support MyRange(stop) and MyRange(start, stop, step)
    - Support both positive and negative steps
    - Be re-iterable (calling iter() multiple times should reset)
    - Support len() — return number of elements in the range
    - Support 'in' operator — check if a value is in the range
    
    Do NOT use range() anywhere in your implementation!
    """
    
    def __init__(self, start, stop=None, step=1):
        # Handle MyRange(5) vs MyRange(1, 10) vs MyRange(1, 10, 2)
        # YOUR CODE HERE
        pass
    
    def __iter__(self):
        # Reset current position and return self
        # YOUR CODE HERE
        pass
    
    def __next__(self):
        # Return next value or raise StopIteration
        # YOUR CODE HERE
        pass
    
    def __len__(self):
        # Return number of elements (hint: use math.ceil)
        # YOUR CODE HERE
        pass
    
    def __contains__(self, value):
        # Return True if value is in this range
        # YOUR CODE HERE
        pass
    
    def __repr__(self):
        return f"MyRange({self.start}, {self.stop}, {self.step})"

# ── Test Cases ────────────────────────────────────────────────────────────────

print("=== Basic iteration ===")
print(list(MyRange(5)))           # [0, 1, 2, 3, 4]
print(list(MyRange(2, 8)))        # [2, 3, 4, 5, 6, 7]
print(list(MyRange(1, 10, 2)))    # [1, 3, 5, 7, 9]
print(list(MyRange(10, 0, -2)))   # [10, 8, 6, 4, 2]
print(list(MyRange(5, 5)))        # []  (empty range)

print("\n=== Re-iteration ===")
r = MyRange(1, 4)
print(list(r))    # [1, 2, 3]
print(list(r))    # [1, 2, 3]  — should work again

print("\n=== len() ===")
print(len(MyRange(10)))        # 10
print(len(MyRange(1, 10, 2)))  # 5
print(len(MyRange(10, 1, -1))) # 9

print("\n=== in operator ===")
r = MyRange(0, 10, 2)
print(0 in r)    # True
print(3 in r)    # False (3 is not even)
print(8 in r)    # True
print(10 in r)   # False (stop is exclusive)

print("\n=== Works with built-ins ===")
r = MyRange(1, 6)
print(sum(r))    # 15
print(max(r))    # 5
print(min(r))    # 1
```

---

### 2.2 — Linked List Iterator

```python
"""
Implement a simple linked list with an iterator.
This demonstrates iterator state management for non-array data structures.
"""

class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

class LinkedList:
    """A singly linked list that is iterable."""
    
    def __init__(self):
        self.head = None
        self._size = 0
    
    def append(self, value):
        """Add value to end of list."""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1
    
    def __iter__(self):
        """
        Return an iterator that traverses the linked list.
        
        Option A: Return a separate LinkedListIterator object.
        Option B: Use a generator inside __iter__ (simpler!).
        
        Implement Option B using yield:
        """
        # YOUR CODE HERE — hint: start at self.head, traverse using .next
        pass
    
    def __len__(self):
        return self._size
    
    def __repr__(self):
        return "LinkedList(" + " → ".join(str(x) for x in self) + ")"

# ── Tests ─────────────────────────────────────────────────────────────────────
ll = LinkedList()
for val in [10, 20, 30, 40, 50]:
    ll.append(val)

print(ll)                  # LinkedList(10 → 20 → 30 → 40 → 50)
print(list(ll))            # [10, 20, 30, 40, 50]
print(sum(ll))             # 150
print(30 in ll)            # True
print(99 in ll)            # False

# Re-iteration test
print(list(ll))            # [10, 20, 30, 40, 50]  — should still work
print(list(ll))            # [10, 20, 30, 40, 50]  — and again
```

---

## Exercise 3 — Generator Functions (35 min)

**File:** `ex03_generators.py`

### 3.1 — Fibonacci Generator

```python
def fibonacci():
    """
    Infinite generator that yields Fibonacci numbers: 0, 1, 1, 2, 3, 5, 8, ...
    
    Requirements:
    - Must be infinite (no stopping condition)
    - Must use yield (not a list)
    - Must work with islice to get first N values
    """
    # YOUR CODE HERE
    pass

# ── Tests ─────────────────────────────────────────────────────────────────────
from itertools import islice

fib = fibonacci()
print(list(islice(fib, 10)))
# Expected: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Sum of first 20 Fibonacci numbers
print(sum(islice(fibonacci(), 20)))
# Expected: 10945

# First Fibonacci number greater than 1000
first_over_1000 = next(f for f in fibonacci() if f > 1000)
print(first_over_1000)
# Expected: 1597

# All Fibonacci numbers up to 100
fibs_under_100 = list(takewhile(lambda x: x <= 100, fibonacci()))
from itertools import takewhile
fibs_under_100 = list(takewhile(lambda x: x <= 100, fibonacci()))
print(fibs_under_100)
# Expected: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

---

### 3.2 — Multi-Yield Generator: Collatz Sequence

```python
def collatz(n):
    """
    Yields the Collatz sequence starting from n.
    Rules:
    - If n is even: next number is n // 2
    - If n is odd:  next number is 3*n + 1
    - Stop when n reaches 1 (yield 1 before stopping)
    
    Example: collatz(6) → 6, 3, 10, 5, 16, 8, 4, 2, 1
    """
    # YOUR CODE HERE
    pass

# ── Tests ─────────────────────────────────────────────────────────────────────
print(list(collatz(6)))
# Expected: [6, 3, 10, 5, 16, 8, 4, 2, 1]

print(list(collatz(27)))
# Should be a long sequence — the Collatz conjecture says it always reaches 1

# Find which starting number under 100 produces the longest Collatz sequence
longest_start = max(range(1, 100), key=lambda n: sum(1 for _ in collatz(n)))
print(f"Starting at {longest_start} gives the longest sequence")
# Expected: 97
```

---

### 3.3 — Generator with Cleanup: Chunked File Reader

```python
def read_in_chunks(filepath, chunk_size=1024):
    """
    Yields chunks of bytes from a binary file.
    
    Requirements:
    - Yield exactly chunk_size bytes per chunk (except possibly the last)
    - File must be properly closed after iteration (use try/finally or 'with')
    - Must handle FileNotFoundError gracefully — raise it to the caller
    - Should yield nothing if file is empty
    
    This pattern is used for streaming large files without loading into memory.
    """
    # YOUR CODE HERE
    pass

# ── Test Setup ────────────────────────────────────────────────────────────────
# Create a test file
with open("test_chunks.bin", "wb") as f:
    f.write(b"A" * 2500)    # 2500 bytes

# ── Tests ─────────────────────────────────────────────────────────────────────
chunks = list(read_in_chunks("test_chunks.bin", chunk_size=1000))
print(f"Number of chunks: {len(chunks)}")     # 3 (1000 + 1000 + 500)
print(f"Chunk sizes: {[len(c) for c in chunks]}")  # [1000, 1000, 500]
print(f"Total bytes: {sum(len(c) for c in chunks)}")  # 2500

# File not found
try:
    list(read_in_chunks("nonexistent.bin"))
except FileNotFoundError as e:
    print(f"Correctly raised: {e}")
```

---

### 3.4 — `yield from` Practice: Tree Traversal

```python
"""
Implement depth-first traversal of a tree using yield from.

Tree structure:
         1
        / \\
       2   3
      / \\   \\
     4   5   6
"""

class TreeNode:
    def __init__(self, value, *children):
        self.value = value
        self.children = list(children)
    
    def __repr__(self):
        return f"TreeNode({self.value})"

def depth_first(node):
    """
    Generator that yields node values in depth-first order.
    
    Requirements:
    - Use yield from for recursive traversal
    - Visit current node before its children (pre-order)
    
    Expected output for the tree above: 1, 2, 4, 5, 3, 6
    """
    # YOUR CODE HERE
    pass

def breadth_first(root):
    """
    Generator that yields node values in breadth-first (level) order.
    
    Requirements:
    - Use a queue (collections.deque)
    - Yield values level by level
    
    Expected output for the tree above: 1, 2, 3, 4, 5, 6
    """
    from collections import deque
    # YOUR CODE HERE
    pass

# ── Build tree ────────────────────────────────────────────────────────────────
tree = TreeNode(1,
    TreeNode(2,
        TreeNode(4),
        TreeNode(5)
    ),
    TreeNode(3,
        TreeNode(6)
    )
)

print("Depth-first:", list(depth_first(tree)))
# Expected: [1, 2, 4, 5, 3, 6]

print("Breadth-first:", list(breadth_first(tree)))
# Expected: [1, 2, 3, 4, 5, 6]
```

---

## Exercise 4 — Generator Expressions & Memory (20 min)

**File:** `ex04_genexp_memory.py`

### 4.1 — List vs Generator Expression

```python
import sys
import time

N = 10_000_000

# Complete each measurement:

# Measurement 1: List comprehension
start = time.time()
lst = [x * 2 for x in range(N)]
list_time = time.time() - start
list_mem = sys.getsizeof(lst)

# Measurement 2: Generator expression
start = time.time()
gen = (x * 2 for x in range(N))
gen_time = time.time() - start
gen_mem = sys.getsizeof(gen)

print(f"List: {list_mem / 1024 / 1024:.1f} MB, created in {list_time:.3f}s")
print(f"Gen : {gen_mem} bytes, created in {gen_time:.6f}s")
print(f"Memory ratio: {list_mem // gen_mem}x")
```

**Questions to answer in comments:**
1. How much faster is the generator to *create*?
2. When would you prefer the list despite higher memory?
3. When is the generator clearly superior?

---

### 4.2 — Efficient Search with Short-Circuit Evaluation

```python
"""
Demonstrate how generator expressions enable short-circuit evaluation
with any() and all().
"""
import time

data = list(range(10_000_000))

# Task: Find if any number in data is divisible by 9999991 (a prime near 10M)

# Method 1: List comprehension then check
def search_list(data):
    matches = [x for x in data if x % 9_999_991 == 0]   # ALL elements checked
    return len(matches) > 0

# Method 2: Generator expression with any() — short-circuits!
def search_gen(data):
    return any(x % 9_999_991 == 0 for x in data)   # Stops at first match

# Measure both
start = time.time()
result1 = search_list(data)
t1 = time.time() - start

start = time.time()
result2 = search_gen(data)
t2 = time.time() - start

print(f"List method: {t1:.3f}s, found: {result1}")
print(f"Gen method:  {t2:.3f}s, found: {result2}")
print(f"Speedup: {t1/t2:.1f}x")

# Repeat with a target that DOESN'T exist — what happens to the speedup?
```

---

## Exercise 5 — itertools Mastery (30 min)

**File:** `ex05_itertools.py`

```python
from itertools import (
    count, cycle, repeat,
    chain, zip_longest, islice,
    takewhile, dropwhile,
    accumulate, groupby,
    combinations, permutations, product
)
import operator
```

### 5.1 — Fill in the Blanks

```python
# Use ONE itertools function per blank. No loops allowed.

# 1. Generate first 10 odd numbers starting from 1
odds = list(islice(______, 10))
print(odds)   # [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

# 2. Repeat the pattern [True, False] for 8 elements
pattern = list(islice(______, 8))
print(pattern)   # [True, False, True, False, True, False, True, False]

# 3. Combine two lists into one sequence
a = [1, 2, 3]
b = ["a", "b", "c"]
combined = list(______)
print(combined)   # [1, 2, 3, 'a', 'b', 'c']

# 4. Zip two lists of different lengths, filling missing with 0
names = ["Alice", "Bob", "Carol", "Dave"]
scores = [90, 85]
paired = list(______)
print(paired)   # [('Alice', 90), ('Bob', 85), ('Carol', 0), ('Dave', 0)]

# 5. Running product of [1, 2, 3, 4, 5]
running_prod = list(______)
print(running_prod)   # [1, 2, 6, 24, 120]

# 6. All 2-element combinations from ['A', 'B', 'C', 'D']
combos = list(______)
print(combos)   # [('A','B'), ('A','C'), ('A','D'), ('B','C'), ('B','D'), ('C','D')]
```

---

### 5.2 — groupby Analysis

```python
"""
Given a list of transactions, use groupby to:
1. Group by category and compute total spend per category
2. Find the category with the highest total spend
3. Find all categories with more than 3 transactions
"""

transactions = [
    {"category": "Food",       "amount": 450},
    {"category": "Food",       "amount": 320},
    {"category": "Transport",  "amount": 200},
    {"category": "Food",       "amount": 180},
    {"category": "Shopping",   "amount": 1200},
    {"category": "Transport",  "amount": 150},
    {"category": "Shopping",   "amount": 890},
    {"category": "Food",       "amount": 95},
    {"category": "Health",     "amount": 500},
    {"category": "Transport",  "amount": 75},
    {"category": "Shopping",   "amount": 340},
    {"category": "Food",       "amount": 210},
]

# Step 1: Sort by category (required for groupby!)
transactions.sort(key=lambda t: t["category"])

# Step 2: Group and compute stats using groupby
# YOUR CODE HERE

# Expected output:
# Category totals:
#   Food:      ₹1255 (5 transactions)
#   Health:    ₹500 (1 transaction)
#   Shopping:  ₹2430 (3 transactions)
#   Transport: ₹425 (3 transactions)
#
# Highest spend: Shopping (₹2430)
# Categories with > 3 transactions: ['Food']
```

---

### 5.3 — Build Your Own Pipeline with itertools

```python
"""
You have a stream of server access log entries.
Using only generator expressions and itertools (no explicit for loops except for output),
build a pipeline that:

1. Parses each log line into a dict
2. Filters to only GET requests
3. Filters to only 200 status codes  
4. Groups by URL path
5. Counts hits per path
6. Returns top 5 paths by hit count
"""

import random

# Generate sample log data
def generate_logs(n=1000):
    methods = ["GET", "POST", "PUT", "DELETE"]
    paths = ["/home", "/api/users", "/api/products", "/api/orders",
             "/login", "/dashboard", "/static/css", "/api/search"]
    statuses = [200, 200, 200, 404, 500, 301, 200, 403]   # 200 is most common
    for _ in range(n):
        yield f"{random.choice(methods)} {random.choice(paths)} {random.choice(statuses)}"

# Parse a single log line into a dict
def parse_log(line):
    parts = line.split()
    return {"method": parts[0], "path": parts[1], "status": int(parts[2])}

# YOUR PIPELINE CODE HERE using itertools and generator expressions
# No explicit for loops (except the final print loop)

logs = generate_logs(1000)
# ... build pipeline ...
# Print top 5
```

---

## Exercise 6 — Full Integration: Log File Analyzer (40 min)

**File:** `ex06_log_analyzer.py`

**Goal:** Build a complete, memory-efficient log analysis tool using custom iterators, generators, and itertools.

### Requirements

Build a `LogAnalyzer` class that:
- Reads a log file lazily (one line at a time)
- Parses lines into structured records
- Supports method chaining for filter/transform operations
- Computes statistics without loading the whole file into memory
- Reports results in a formatted summary

**Log format:** `YYYY-MM-DD HH:MM:SS | LEVEL | module | message`

### Step 1 — Generate Sample Logs

```python
import random
import logging
from datetime import datetime, timedelta

def generate_log_file(filepath, num_lines=50_000):
    """Creates a realistic sample log file for testing."""
    levels   = ["DEBUG", "INFO", "INFO", "INFO", "WARNING", "ERROR", "CRITICAL"]
    modules  = ["auth", "payment", "database", "api", "cache", "worker"]
    messages = {
        "DEBUG":    ["Cache lookup: {key}", "Query executed in {ms}ms", "Template compiled"],
        "INFO":     ["User {id} logged in", "Request processed: {path}", "Job {id} completed"],
        "WARNING":  ["High memory: {pct}%", "Slow query: {ms}ms", "Retry attempt {n}"],
        "ERROR":    ["Payment failed for user {id}", "DB timeout after {ms}ms", "File not found: {path}"],
        "CRITICAL": ["OOM: {mb}MB", "DB unreachable", "Worker crashed: {id}"],
    }
    
    base = datetime(2024, 1, 15, 8, 0, 0)
    with open(filepath, "w") as f:
        for i in range(num_lines):
            ts    = (base + timedelta(seconds=i * 2)).strftime("%Y-%m-%d %H:%M:%S")
            level = random.choice(levels)
            mod   = random.choice(modules)
            tmpl  = random.choice(messages[level])
            msg   = tmpl.format(key=f"k{i}", ms=random.randint(1,5000),
                                id=random.randint(1,100), pct=random.randint(50,99),
                                n=random.randint(1,5), path=f"/path/{i}",
                                mb=random.randint(100,2000))
            f.write(f"{ts} | {level:8s} | {mod:10s} | {msg}\n")

generate_log_file("server.log")
print("Log file created.")
```

---

### Step 2 — Implement the LogAnalyzer

```python
from itertools import islice, groupby
from collections import Counter, defaultdict
from datetime import datetime

class LogRecord:
    """Represents a single parsed log entry."""
    __slots__ = ("timestamp", "level", "module", "message")
    
    def __init__(self, timestamp, level, module, message):
        self.timestamp = timestamp
        self.level     = level
        self.module    = module
        self.message   = message
    
    def __repr__(self):
        return f"LogRecord({self.level}, {self.module})"

class LogAnalyzer:
    """
    Lazy log file analyzer using generator pipeline.
    All operations are lazy until .report() or .count() is called.
    """
    
    def __init__(self, filepath):
        self._filepath = filepath
        self._filters  = []      # List of filter functions
        self._limit    = None    # Optional record limit
    
    # ── Generator pipeline stages ─────────────────────────────────────────────
    
    def _read_lines(self):
        """Stage 1: Yield raw lines from file."""
        # YOUR CODE HERE
        pass
    
    def _parse_lines(self, lines):
        """Stage 2: Parse each line into a LogRecord. Skip malformed lines."""
        # Format: "YYYY-MM-DD HH:MM:SS | LEVEL    | module     | message"
        # YOUR CODE HERE — use try/except to skip bad lines
        pass
    
    def _apply_filters(self, records):
        """Stage 3: Apply all registered filter functions."""
        for record in records:
            if all(f(record) for f in self._filters):
                yield record
    
    def _get_pipeline(self):
        """Assemble the full pipeline."""
        records = self._parse_lines(self._read_lines())
        records = self._apply_filters(records)
        if self._limit:
            records = islice(records, self._limit)
        return records
    
    # ── Chainable filter methods ──────────────────────────────────────────────
    
    def filter_level(self, *levels):
        """Keep only records at specified levels."""
        level_set = set(levels)
        self._filters.append(lambda r: r.level in level_set)
        return self   # Enable chaining
    
    def filter_module(self, *modules):
        """Keep only records from specified modules."""
        mod_set = set(modules)
        self._filters.append(lambda r: r.module in mod_set)
        return self
    
    def filter_message_contains(self, keyword):
        """Keep only records where message contains keyword."""
        self._filters.append(lambda r: keyword.lower() in r.message.lower())
        return self
    
    def limit(self, n):
        """Process only the first n matching records."""
        self._limit = n
        return self
    
    # ── Terminal methods (trigger evaluation) ─────────────────────────────────
    
    def count(self):
        """Count matching records (consumes pipeline)."""
        return sum(1 for _ in self._get_pipeline())
    
    def count_by_level(self):
        """Return dict of {level: count} for matching records."""
        return Counter(r.level for r in self._get_pipeline())
    
    def count_by_module(self):
        """Return dict of {module: count} for matching records."""
        return Counter(r.module for r in self._get_pipeline())
    
    def top_messages(self, n=10):
        """Return top N most common messages."""
        return Counter(r.message for r in self._get_pipeline()).most_common(n)
    
    def report(self):
        """Print a formatted analysis report."""
        print(f"\n{'='*60}")
        print(f"  Log Analysis Report: {self._filepath}")
        print(f"{'='*60}")
        
        # Run pipeline ONCE and accumulate all stats simultaneously
        level_counts  = Counter()
        module_counts = Counter()
        message_counts = Counter()
        total = 0
        
        for record in self._get_pipeline():
            level_counts[record.level]    += 1
            module_counts[record.module]  += 1
            message_counts[record.message] += 1
            total += 1
        
        print(f"\n📊 Total matching records: {total:,}")
        
        print(f"\n📈 By Level:")
        for level, count in sorted(level_counts.items(),
                                    key=lambda x: x[1], reverse=True):
            bar = "█" * (count * 30 // max(level_counts.values()))
            print(f"  {level:10s} {count:6,} {bar}")
        
        print(f"\n🔧 By Module:")
        for module, count in module_counts.most_common():
            print(f"  {module:12s} {count:6,}")
        
        print(f"\n🔝 Top 5 Messages:")
        for msg, count in message_counts.most_common(5):
            print(f"  {count:4,}x  {msg[:50]}")
        
        print(f"{'='*60}\n")
```

---

### Step 3 — Test the Analyzer

```python
# ── Basic usage ───────────────────────────────────────────────────────────────
print("=== Full Report ===")
LogAnalyzer("server.log").report()

# ── Filtered reports ──────────────────────────────────────────────────────────
print("=== Errors and Criticals ===")
(LogAnalyzer("server.log")
    .filter_level("ERROR", "CRITICAL")
    .report())

print("=== Payment module issues ===")
(LogAnalyzer("server.log")
    .filter_module("payment")
    .filter_level("WARNING", "ERROR", "CRITICAL")
    .report())

# ── Quick stats ───────────────────────────────────────────────────────────────
error_count = LogAnalyzer("server.log").filter_level("ERROR").count()
print(f"Total errors: {error_count:,}")

db_errors = (LogAnalyzer("server.log")
             .filter_module("database")
             .filter_level("ERROR", "CRITICAL")
             .count())
print(f"Database errors: {db_errors:,}")

# ── Memory verification ───────────────────────────────────────────────────────
import tracemalloc

tracemalloc.start()
LogAnalyzer("server.log").report()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"Peak memory used for analysis: {peak / 1024:.1f} KB")
print("(This should be tiny despite reading 50,000 lines!)")
```

---

## Exercise 7 — Challenge: LazySequence Fluent API (Stretch Goal)

**File:** `ex07_lazy_sequence.py`

**Task:** Implement a `LazySequence` class that wraps any generator and provides a fluent, chainable API for lazy transformations.

```python
class LazySequence:
    """
    A lazy wrapper around any iterator that supports chainable operations.
    No computation happens until take(), to_list(), or iteration.
    """
    
    def __init__(self, iterable):
        self._gen = iter(iterable)
    
    def map(self, func):
        """Apply func to each element. Returns a new LazySequence."""
        # Hint: return LazySequence(func(x) for x in self._gen)
        # YOUR CODE HERE
        pass
    
    def filter(self, pred):
        """Keep only elements where pred(element) is True."""
        # YOUR CODE HERE
        pass
    
    def skip(self, n):
        """Skip first n elements."""
        from itertools import islice
        # Hint: consume n items first, then wrap rest in LazySequence
        # YOUR CODE HERE
        pass
    
    def take(self, n):
        """Return a list of the next n elements."""
        from itertools import islice
        # YOUR CODE HERE
        pass
    
    def take_while(self, pred):
        """Take elements while pred is True. Returns LazySequence."""
        from itertools import takewhile
        # YOUR CODE HERE
        pass
    
    def zip_with(self, other):
        """Zip with another iterable. Returns LazySequence of tuples."""
        # YOUR CODE HERE
        pass
    
    def flatten(self):
        """Flatten one level of nesting. Returns LazySequence."""
        # YOUR CODE HERE
        pass
    
    def to_list(self):
        """Materialize the entire sequence into a list."""
        return list(self._gen)
    
    def __iter__(self):
        return self._gen
    
    def __next__(self):
        return next(self._gen)

# ── Helper — fibonacci generator from Ex 3.1 ─────────────────────────────────
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# ── Test Cases ────────────────────────────────────────────────────────────────

# Test 1: Basic chaining
result = (LazySequence(range(100))
          .filter(lambda x: x % 2 == 0)   # even numbers
          .map(lambda x: x ** 2)           # squared
          .take(5))
print(result)
# Expected: [0, 4, 16, 36, 64]

# Test 2: Infinite generator with skip + take
result = (LazySequence(fibonacci())
          .skip(5)                         # skip first 5 (0,1,1,2,3)
          .filter(lambda x: x % 2 == 0)   # even Fibonacci only
          .take(5))
print(result)
# Expected: [8, 34, 144, 610, 2584]

# Test 3: zip_with
result = (LazySequence(fibonacci())
          .zip_with(range(1, 11))          # pair with 1..10
          .take(5))
print(result)
# Expected: [(0,1), (1,2), (1,3), (2,4), (3,5)]

# Test 4: flatten
nested = LazySequence([[1,2,3], [4,5], [6,7,8,9]])
print(nested.flatten().to_list())
# Expected: [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Test 5: Full pipeline — first 5 even Fibonacci > 100, scaled by 0.01
result = (LazySequence(fibonacci())
          .filter(lambda x: x > 100)
          .filter(lambda x: x % 2 == 0)
          .map(lambda x: x * 0.01)
          .take(5))
print(result)
# Expected: [1.44, 6.1, 25.84, 109.46, 464.14] (approximately)
```

---

## ✅ Exercise Checklist

| Exercise | Topic | Difficulty | Done? |
|---|---|---|---|
| Ex 1 — Iterator Basics | `iter()`, `next()`, exhaustion | ⭐ | ⬜ |
| Ex 2.1 — MyRange | Custom iterator class | ⭐⭐ | ⬜ |
| Ex 2.2 — LinkedList | Iterator in a data structure | ⭐⭐ | ⬜ |
| Ex 3.1 — Fibonacci | Infinite generator | ⭐ | ⬜ |
| Ex 3.2 — Collatz | Multi-condition generator | ⭐⭐ | ⬜ |
| Ex 3.3 — Chunked Reader | Generator with resource cleanup | ⭐⭐ | ⬜ |
| Ex 3.4 — Tree Traversal | `yield from`, recursion | ⭐⭐⭐ | ⬜ |
| Ex 4 — Memory Comparison | genexp vs list performance | ⭐ | ⬜ |
| Ex 5 — itertools Mastery | All major itertools functions | ⭐⭐ | ⬜ |
| Ex 6 — Log Analyzer | Full pipeline integration | ⭐⭐⭐ | ⬜ |
| Ex 7 — LazySequence | Fluent API challenge | ⭐⭐⭐⭐ | ⬜ |

---

## 💡 Hints & Tips

### Exercise 2.1 (MyRange)
- `__iter__` should reset `self.current = self.start` before returning self
- For `__len__`: number of steps = `ceil((stop - start) / step)` — use `math.ceil`
- For `__contains__`: check if `(value - start)` is divisible by `step` AND in range

### Exercise 2.2 (LinkedList)
- In `__iter__`, use `current = self.head` then loop `while current:` and `yield current.value; current = current.next`
- Because `__iter__` is a generator function (contains `yield`), it automatically returns a fresh generator each time — making LinkedList re-iterable!

### Exercise 3.2 (Collatz)
- Start by yielding `n`, then update according to the rules, repeat until `n == 1`

### Exercise 3.3 (Chunked Reader)
- Open file in binary mode (`"rb"`), use `f.read(chunk_size)` in a loop, break when `chunk == b""`

### Exercise 3.4 (Tree Traversal)
- `depth_first`: `yield node.value`, then `yield from depth_first(child)` for each child
- `breadth_first`: Use `deque`, start with root, loop: `node = q.popleft(); yield node.value; q.extend(node.children)`

### Exercise 5 (itertools fill-in-blanks)
- Odd numbers: `count(1, 2)` — starts at 1, step 2
- Pattern repeat: `cycle([True, False])`
- Combined list: `chain(a, b)`
- zip with fill: `zip_longest(names, scores, fillvalue=0)`
- Running product: `accumulate(values, operator.mul)` — import `operator`
- Combinations: `combinations(['A','B','C','D'], 2)`

### Exercise 6 (LogAnalyzer)
- Parse using `line.split("|")` — there are exactly 4 parts
- Strip whitespace from each part with `.strip()`
- The timestamp format is `"%Y-%m-%d %H:%M:%S"` for `datetime.strptime()`
- In `report()`: iterate the pipeline **once** and update multiple counters in the same loop

### Exercise 7 (LazySequence)
- Each method should return `LazySequence(generator_expression)` for lazy chaining
- `skip(n)`: use `from itertools import islice; collections.deque(islice(self._gen, n), maxlen=0)` to consume n items efficiently, then wrap remaining
- `flatten()`: use `(item for sublist in self._gen for item in sublist)`
