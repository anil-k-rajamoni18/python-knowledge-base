# 💪 Python Full Stack — Day 2 Exercise & Practice File
# Topic: Control Flow & Functions

> **Instructions:** Work through sections in order. Write predictions before running code. Do NOT peek at answers until you've genuinely attempted each problem.

---

## 📋 Setup Check

```python
import sys
import math
from functools import partial, reduce, lru_cache

print(f"Python version: {sys.version}")
assert sys.version_info >= (3, 10), "Need Python 3.10+ for match/case"
print("✅ All good — let's go!")
```

---

## Section A — Predict the Output (No Running Allowed!)

### A1. Loop `else` Behavior

```python
# Snippet 1
for i in [1, 2, 3]:
    pass
else:
    print("done")

# Snippet 2
for i in [1, 2, 3]:
    if i == 2:
        break
else:
    print("no break")

# Snippet 3
for i in []:           # empty iterable
    print(i)
else:
    print("empty loop else")
```

**Predictions:**
```
Snippet 1: ______
Snippet 2: ______
Snippet 3: ______
```

---

### A2. Argument Types

```python
def mystery(a, b=10, *args, c, **kwargs):
    print(f"a={a}, b={b}, args={args}, c={c}, kwargs={kwargs}")

mystery(1, 2, 3, 4, c=5, x=6, y=7)
```

**Prediction:**
```
Output: ______________________________________
```

---

### A3. Closure Capture

```python
def make_funcs():
    funcs = []
    for i in range(3):
        funcs.append(lambda: i)
    return funcs

results = [f() for f in make_funcs()]
print(results)
```

**Prediction:**
```
Output: ______
```

**Why?**
```
_______________________________________
```

---

### A4. LEGB Resolution

```python
x = 1

def outer():
    x = 2
    def inner():
        print(x)     # Line A
    inner()
    print(x)         # Line B

outer()
print(x)             # Line C
```

**Predictions:**
```
Line A: ___
Line B: ___
Line C: ___
```

---

### A5. Comprehension Types

```python
a = [x*2 for x in range(5)]
b = (x*2 for x in range(5))
c = {x*2 for x in range(5)}
d = {x: x*2 for x in range(5)}

print(type(a).__name__)
print(type(b).__name__)
print(type(c).__name__)
print(type(d).__name__)
print(list(b))
```

**Predictions:**
```
type(a): ______
type(b): ______
type(c): ______
type(d): ______
list(b): ______
```

---

## Section B — Fill in the Blanks

### B1. Complete the Control Flow

```python
# 1. Rewrite this using a ternary operator (one line)
score = 75
if score >= 60:
    result = "pass"
else:
    result = "fail"

# One-liner version:
result = ______

# 2. Add the correct keyword so this prints "Not found"
def search(lst, target):
    for item in lst:
        if item == target:
            break
    ______:
        print("Not found")

search([1, 2, 3], 99)   # Should print: Not found

# 3. Fill in so only odd numbers are printed
for i in range(10):
    if i % 2 == 0:
        ______           # skip even
    print(i)

# 4. Complete the match/case
def day_type(day: str) -> str:
    match day.lower():
        case "saturday" | ______:
            return "weekend"
        case ______:
            return "weekday"

print(day_type("Sunday"))      # weekend
print(day_type("Monday"))      # weekday
```

---

### B2. Complete the Function Signatures

```python
# 1. Function accepts any number of positional integers, returns their product
def product(______) -> int:
    result = 1
    for n in args:
        result *= n
    return result

print(product(2, 3, 4))     # 24

# 2. Function accepts keyword arguments, returns them as a formatted string
def format_record(______) -> str:
    return ", ".join(f"{k}={v}" for k, v in kwargs.items())

print(format_record(name="Alice", age=25))  # name=Alice, age=25

# 3. Function with type hints — accepts list of floats, returns average
def average(______ : list[______]) -> ______:
    return sum(numbers) / len(numbers)

print(average([1.0, 2.0, 3.0]))     # 2.0
```

---

### B3. Fix the Scope Issues

```python
# 1. Fix so 'count' is properly modified
total = 0

def add(n):
    ______
    total += n

add(5)
add(10)
print(total)    # Should print 15

# 2. Fix so the closure counter works correctly
def make_counter():
    count = 0
    def increment():
        ______
        count += 1
        return count
    return increment

c = make_counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3
```

---

## Section C — Debugging Exercises

### C1. The Broken Search

```python
# Bug: This should print "Found!" when target exists, "Not found" otherwise.
# But it always prints "Not found".

def search_list(lst, target):
    for item in lst:
        if item == target:
            print("Found!")
    else:
        print("Not found")

search_list([1, 2, 3, 4], 3)
```

**What's the bug?**
```
_______________________________________________________
```

**Fixed version:**
```python
def search_list(lst, target):
    # Your fix here
    pass
```

---

### C2. The Scope Trap

```python
# Bug: UnboundLocalError when calling increment()
total = 100

def increment(amount):
    total += amount     # UnboundLocalError!
    return total

print(increment(50))
```

**Explain why the error occurs:**
```
_______________________________________________________
```

**Two ways to fix it:**
```python
# Fix 1: Using global
def increment_v1(amount):
    # Your fix
    pass

# Fix 2: Better design — no global needed
def increment_v2(current_total: int, amount: int) -> int:
    # Your fix
    pass
```

---

### C3. The Closure Loop Bug

```python
# Bug: All buttons print the same message
buttons = []
for i in range(5):
    buttons.append(lambda: f"Button {i} clicked")

# All print "Button 4 clicked"
for btn in buttons:
    print(btn())
```

**Fix this using a default argument:**
```python
buttons = []
for i in range(5):
    buttons.append(______)   # Fix the lambda here

for btn in buttons:
    print(btn())             # Should print Button 0, 1, 2, 3, 4
```

---

### C4. The Mutable Default Trap

```python
# Bug: The function accumulates state between calls
def build_report(title, sections=[]):
    sections.append(title)
    return sections

r1 = build_report("Chapter 1")
r2 = build_report("Chapter 2")
r3 = build_report("Chapter 3")

print(r1)   # Expected: ['Chapter 1']
print(r2)   # Expected: ['Chapter 2']
print(r3)   # Expected: ['Chapter 3']
```

**Fixed version:**
```python
def build_report(title: str, sections=None) -> list[str]:
    # Your fix here
    pass
```

---

### C5. The Wrong Argument Order

```python
# Bug: SyntaxError — fix the function signature
def process(**kwargs, *args, pos1, pos2):
    print(pos1, pos2, args, kwargs)

process(1, 2, 3, x=10)
```

**Correct signature:**
```python
def process(______):
    print(pos1, pos2, args, kwargs)
```

---

## Section D — Write the Code

### D1. Number Utilities Suite

Implement all three functions with clean control flow:

```python
def is_prime(n: int) -> bool:
    """
    Returns True if n is prime.
    Use for/else — no flag variable allowed.
    Edge cases: n < 2 → False
    """
    # Your code here
    pass

def is_palindrome(text: str) -> bool:
    """
    Returns True if text is a palindrome.
    Ignore case and spaces.
    """
    # Your code here
    pass

def fibonacci(n: int) -> list[int]:
    """
    Returns first n Fibonacci numbers.
    Use while loop.
    fibonacci(0) → []
    fibonacci(1) → [0]
    fibonacci(8) → [0, 1, 1, 2, 3, 5, 8, 13]
    """
    # Your code here
    pass

# Test suite
assert is_prime(2) == True
assert is_prime(17) == True
assert is_prime(18) == False
assert is_prime(1) == False
assert is_prime(0) == False

assert is_palindrome("racecar") == True
assert is_palindrome("A man a plan a canal Panama") == True
assert is_palindrome("hello") == False

assert fibonacci(0) == []
assert fibonacci(1) == [0]
assert fibonacci(8) == [0, 1, 1, 2, 3, 5, 8, 13]

print("✅ All D1 tests passed!")
```

---

### D2. Argument Pattern Showcase

```python
# 1. Implement join_words: accepts any number of words,
# keyword-only separator (default: ", ")
def join_words(*args: str, separator: str = ", ") -> str:
    # Your code here
    pass

print(join_words("Python", "Django", "Flask"))              # Python, Django, Flask
print(join_words("a", "b", "c", separator=" → "))          # a → b → c

# 2. Implement a function that accepts a "base" dict and keyword overrides,
# returns a merged dict with overrides winning
def merge_config(base: dict, **overrides) -> dict:
    # Your code here
    pass

defaults = {"debug": False, "timeout": 30, "retries": 3}
custom = merge_config(defaults, debug=True, timeout=60)
print(custom)   # {'debug': True, 'timeout': 60, 'retries': 3}

# 3. Implement a flexible logger
def log(level: str, *messages: str, separator: str = " ", **context) -> str:
    """
    Returns: "[LEVEL] message1 message2 | key=val key=val"
    """
    # Your code here
    pass

print(log("INFO", "Server", "started", port=8000, env="prod"))
# [INFO] Server started | port=8000 env=prod
```

---

### D3. Higher-Order Function Toolkit

```python
from typing import Callable, TypeVar
T = TypeVar("T")

# 1. Implement 'apply_n': applies func to value, n times
def apply_n(func: Callable, value, n: int):
    """Apply func to value n times."""
    # Your code here
    pass

double = lambda x: x * 2
print(apply_n(double, 1, 5))       # 32  (1→2→4→8→16→32)

# 2. Implement 'compose': returns a function that applies g then f
def compose(f: Callable, g: Callable) -> Callable:
    """Returns h(x) = f(g(x))"""
    # Your code here
    pass

add_one = lambda x: x + 1
square = lambda x: x ** 2
square_then_add = compose(add_one, square)
print(square_then_add(4))          # 17

# 3. Implement 'memoize': caches results of expensive function calls
def memoize(func: Callable) -> Callable:
    """Cache function results based on arguments."""
    cache = {}
    def wrapper(*args):
        # Your code here
        pass
    return wrapper

@memoize
def slow_fibonacci(n: int) -> int:
    if n < 2: return n
    return slow_fibonacci(n-1) + slow_fibonacci(n-2)

print(slow_fibonacci(35))          # 9227465 (fast with cache)
```

---

### D4. Scope Explorer

```python
# Write a function 'scope_demo' that:
# 1. Has a local variable 'x = "local"'
# 2. Contains a nested function that reads x from enclosing scope (no nonlocal)
# 3. Contains another nested function that MODIFIES x using nonlocal
# 4. Returns a dict with results: {"read": ..., "modified": ...}

def scope_demo() -> dict:
    x = "original"

    def reader():
        # reads x from enclosing scope
        # Your code here
        pass

    def modifier():
        nonlocal x
        # modifies x
        x = "modified"

    # Your code here
    pass

result = scope_demo()
print(result)   # {"read": "original", "modified": "modified"}
```

---

## Section E — Comprehension Mastery

### E1. Rewrite as Comprehensions

```python
# Convert each loop to a comprehension

# 1. Simple filter + transform
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = []
for n in numbers:
    if n % 2 != 0:
        result.append(n ** 3)
# Comprehension: ______________________________

# 2. Build a dict from two lists
keys = ["name", "age", "city"]
values = ["Alice", 25, "Pune"]
result = {}
for k, v in zip(keys, values):
    result[k] = v
# Comprehension: ______________________________

# 3. Flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = []
for row in matrix:
    for num in row:
        flat.append(num)
# Comprehension: ______________________________

# 4. Unique word lengths from a sentence
sentence = "the quick brown fox jumps over the lazy dog"
lengths = set()
for word in sentence.split():
    lengths.add(len(word))
# Set comprehension: ______________________________
```

---

### E2. Generator vs List Benchmark

```python
import sys
import time

# Compare memory usage
n = 1_000_000

list_comp = [x**2 for x in range(n)]
gen_expr = (x**2 for x in range(n))

print(f"List size: {sys.getsizeof(list_comp):,} bytes")
print(f"Generator size: {sys.getsizeof(gen_expr):,} bytes")

# Compare speed for sum (should be similar)
start = time.perf_counter()
total_list = sum([x**2 for x in range(n)])
list_time = time.perf_counter() - start

start = time.perf_counter()
total_gen = sum(x**2 for x in range(n))
gen_time = time.perf_counter() - start

print(f"\nList sum time:      {list_time:.3f}s")
print(f"Generator sum time: {gen_time:.3f}s")
print(f"Results match: {total_list == total_gen}")
```

**Questions to answer after running:**
```
1. How much memory did the list use vs the generator? ______
2. Which was faster for sum()? ______
3. When would you ALWAYS use a generator? ______
```

---

## Section F — Mini Project: CLI Calculator

Build a complete CLI calculator that demonstrates all Day 2 concepts.

### Requirements

```python
"""
CLI Calculator — Day 2 Mini Project

Features to implement:
✅ Basic operations: +, -, *, /, //, %, **
✅ Scientific: sin, cos, sqrt (via math module)
✅ Memory: MS (store), MR (recall), MC (clear)
✅ History: last 10 operations
✅ Error handling: division by zero, invalid input, domain errors
✅ Type hints on ALL functions
✅ match/case for operation dispatch
✅ *args for multi-operand operations (e.g., add 1 2 3 4)
"""

import math
from typing import Optional

# ── State ──────────────────────────────────────────────────────────────────
history: list[str] = []
memory: float = 0.0

# ── Core Operations ────────────────────────────────────────────────────────
def calculate(op: str, *operands: float) -> float:
    """Dispatch to the correct operation using match/case."""
    match op:
        case "+" | "add":
            return sum(operands)
        case "-" | "sub":
            # Hint: operands[0] - sum(operands[1:])
            pass
        case "*" | "mul":
            # Hint: use reduce or a loop
            pass
        case "/" | "div":
            # Hint: handle ZeroDivisionError
            pass
        case "//" | "floordiv":
            pass
        case "%" | "mod":
            pass
        case "**" | "pow":
            pass
        case "sqrt":
            # Hint: math.sqrt, handle ValueError for negatives
            pass
        case "sin":
            pass
        case "cos":
            pass
        case _:
            raise ValueError(f"Unknown operation: {op}")

# ── Memory Functions ───────────────────────────────────────────────────────
def memory_store(value: float) -> None:
    """Store value in memory."""
    # Hint: use global
    pass

def memory_recall() -> float:
    """Return stored memory value."""
    pass

def memory_clear() -> None:
    """Clear memory to 0.0."""
    pass

# ── History Functions ──────────────────────────────────────────────────────
def add_to_history(expression: str, result: float) -> None:
    """Add entry to history, keep last 10."""
    pass

def show_history() -> None:
    """Print all history entries."""
    pass

# ── Input Parsing ──────────────────────────────────────────────────────────
def parse_input(raw: str) -> tuple[str, list[float]]:
    """
    Parse user input into (operation, operands).
    Examples:
        "3 + 4"     → ("+", [3.0, 4.0])
        "sqrt 16"   → ("sqrt", [16.0])
        "add 1 2 3" → ("add", [1.0, 2.0, 3.0])
    """
    pass

# ── REPL ───────────────────────────────────────────────────────────────────
def main() -> None:
    """Main read-eval-print loop."""
    print("🧮 CLI Calculator — type 'help' for commands, 'quit' to exit")
    print()

    while True:
        try:
            raw = input("calc> ").strip()

            match raw.lower():
                case "quit" | "exit" | "q":
                    print("Goodbye!")
                    break
                case "history" | "h":
                    show_history()
                case "mr":
                    print(f"Memory: {memory_recall()}")
                case "mc":
                    memory_clear()
                    print("Memory cleared.")
                case "help":
                    print("Operations: +, -, *, /, //, %, **, sqrt, sin, cos")
                    print("Memory: MS <value>, MR, MC")
                    print("Other: history, quit")
                case _ if raw.lower().startswith("ms "):
                    value = float(raw.split()[1])
                    memory_store(value)
                    print(f"Stored {value} in memory.")
                case _:
                    op, operands = parse_input(raw)
                    result = calculate(op, *operands)
                    expression = f"{raw} = {result}"
                    add_to_history(expression, result)
                    print(f"  = {result}")

        except ValueError as e:
            print(f"❌ Input error: {e}")
        except ZeroDivisionError:
            print("❌ Cannot divide by zero")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
```

**Testing your calculator manually:**
```
calc> 3 + 4            → 7.0
calc> sqrt 16          → 4.0
calc> 2 ** 10          → 1024.0
calc> add 1 2 3 4 5    → 15.0
calc> ms 42            → Stored 42 in memory
calc> mr               → Memory: 42.0
calc> history          → shows last entries
calc> quit
```

---

## ✅ Answer Key

<details>
<summary>Click to reveal — attempt everything first!</summary>

### A1 Answers
```
Snippet 1: "done"              (loop ended naturally, else runs)
Snippet 2: (nothing)           (break hit, else skipped)
Snippet 3: "empty loop else"   (loop ran zero times without break — else still runs!)
```

### A2 Answer
```
a=1, b=2, args=(3, 4), c=5, kwargs={'x': 6, 'y': 7}
```

### A3 Answer
```
[2, 2, 2]   — all lambdas capture the SAME variable 'i', which is 2 at end of loop
```

### A4 Answers
```
Line A: 2  (finds 'x' in enclosing scope)
Line B: 2  (outer's local x)
Line C: 1  (module global x)
```

### A5 Answers
```
type(a): list
type(b): generator
type(c): set
type(d): dict
list(b): [0, 2, 4, 6, 8]
```

### B1 Answers
```python
result = "pass" if score >= 60 else "fail"

# search fix:
else:
    print("Not found")

# skip even:
continue

# match/case:
case "saturday" | "sunday": return "weekend"
case _: return "weekday"
```

### B2 Answers
```python
def product(*args) -> int: ...
def format_record(**kwargs) -> str: ...
def average(numbers: list[float]) -> float: ...
```

### B3 Answers
```python
# 1:
global total

# 2:
nonlocal count
```

### C1 Fix
```python
def search_list(lst, target):
    for item in lst:
        if item == target:
            print("Found!")
            break
    else:                       # else belongs to for, not if
        print("Not found")
```

### C2 Explanation & Fixes
```
Python sees 'total += amount' and detects 'total' is assigned in this scope,
so it treats it as local everywhere in the function — even before the assignment,
causing UnboundLocalError.

Fix 1:
def increment_v1(amount):
    global total
    total += amount
    return total

Fix 2 (better):
def increment_v2(current_total: int, amount: int) -> int:
    return current_total + amount
```

### C3 Fix
```python
buttons.append(lambda i=i: f"Button {i} clicked")
```

### C4 Fix
```python
def build_report(title: str, sections=None) -> list[str]:
    if sections is None:
        sections = []
    sections.append(title)
    return sections
```

### C5 Fix
```python
def process(pos1, pos2, *args, **kwargs):
    print(pos1, pos2, args, kwargs)
```

### D1 Answers
```python
def is_prime(n: int) -> bool:
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    else:
        return True

def is_palindrome(text: str) -> bool:
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

def fibonacci(n: int) -> list[int]:
    if n <= 0: return []
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]
```

### E1 Answers
```python
# 1:
result = [n**3 for n in numbers if n % 2 != 0]

# 2:
result = {k: v for k, v in zip(keys, values)}

# 3:
flat = [num for row in matrix for num in row]

# 4:
lengths = {len(word) for word in sentence.split()}
```

### D3 Answers
```python
def apply_n(func, value, n):
    for _ in range(n):
        value = func(value)
    return value

def compose(f, g):
    return lambda *args, **kwargs: f(g(*args, **kwargs))

def memoize(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
```

</details>

---

## 📊 Self-Assessment Checklist

| Concept | ✅ Got it | 🔄 Need review | ❓ Confused |
|---------|-----------|---------------|------------|
| `for/else` — when else runs | | | |
| `break`, `continue`, `pass` distinction | | | |
| `match/case` structural patterns | | | |
| List, dict, set comprehensions | | | |
| Generator expression — lazy evaluation | | | |
| `*args` and `**kwargs` — types and usage | | | |
| Correct argument ordering in signatures | | | |
| Lambda — when to use vs `def` | | | |
| LEGB rule — name resolution order | | | |
| `global` and `nonlocal` keywords | | | |
| Closures — what they capture and how | | | |
| Closure loop trap — how to fix | | | |
| Mutable default argument trap | | | |
| Higher-order functions | | | |
| Type hints on function signatures | | | |

**Score:**
- 15/15 ✅ — Excellent! Ready for Day 3 (OOP & Classes)
- 10–14 ✅ — Good foundation. Review "🔄" items, re-read theory for gaps
- < 10 ✅ — Spend extra time on LEGB + closures; they are critical for Day 8 (Decorators)

---

*Day 2 Exercises Complete — Day 3: Object-Oriented Programming — Classes, Inheritance, Dunder Methods*