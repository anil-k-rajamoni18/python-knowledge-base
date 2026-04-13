# 🐍 Python Full Stack — Day 2 of 35
# Topic: Control Flow & Functions
**Audience:** Intermediate | **Duration:** 3 Hours | **Track:** Python → Django/Flask → Frontend → Deployment

---

## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, learners will be able to:
- Write expressive control flow using `if/elif/else`, loops with `else`, and pattern matching (`match/case`)
- Define functions with positional, keyword, `*args`, and `**kwargs` arguments confidently
- Explain and apply the LEGB scope rule, including `global` and `nonlocal`
- Create closures and higher-order functions
- Use list, dict, and set comprehensions as idiomatic Python alternatives to loops
- Apply type hints (PEP 484) to all function signatures

### 📋 Prerequisites (Day 1 Review)
- Python data types: `int`, `float`, `str`, `list`, `dict`, `set`, `tuple`
- Mutable vs immutable distinction
- Variable assignment and reference model
- Pass-by-object-reference behavior

### 🔗 Connection to the Full Stack Journey
- **Django views (Day 20+):** Every view function uses conditionals, loops, and argument patterns covered today
- **REST APIs (Day 22+):** Request routing logic is built on `if/elif` chains and function dispatch
- **Django ORM queries (Day 21+):** Comprehensions are used heavily to transform querysets
- **Decorators (Day 8):** Understanding closures today is the direct prerequisite
- **Middleware (Day 25+):** Higher-order functions are the pattern middleware uses

---

## 2. Concept Explanation

### 2.1 Control Flow Deep Dive

#### if / elif / else and Ternary Operators

**The "Why":** Decision-making is the backbone of any program. Python's `if` blocks are deliberately readable — the English-like syntax reduces cognitive overhead.

**Ternary operator** (inline conditional) lets you express simple if/else in one line — useful in comprehensions and assignments but should never sacrifice clarity.

```
Standard:   if condition: ... else: ...
Ternary:    value_if_true if condition else value_if_false
```

---

#### for / while Loops with `else` Clause

**The "Why":** Python's loop `else` is one of its most misunderstood features. The `else` block runs **only if the loop completed without hitting a `break`**. This elegantly solves the "search and report not found" pattern without a flag variable.

**Analogy:** Think of it as: "Did you finish looking through everything without finding it? Then do this."

---

#### break, continue, pass

| Keyword | Behavior |
|---------|----------|
| `break` | Exit the loop immediately |
| `continue` | Skip to the next iteration |
| `pass` | Do nothing — placeholder for empty blocks |

---

#### Pattern Matching — `match / case` (Python 3.10+)

**The "Why":** Python's `match/case` is far more powerful than a simple `switch` — it does **structural pattern matching**, meaning it can match against shapes, types, and values simultaneously.

**Analogy:** Where `if/elif` checks conditions one at a time, `match/case` says "check what *shape* this data has."

---

#### Comprehensions

**The "Why":** Comprehensions are Python's answer to the question: "How do I transform/filter a collection without writing a 5-line loop?" They are more readable, faster (C-level loop in CPython), and more Pythonic.

| Type | Syntax | Returns |
|------|--------|---------|
| List comprehension | `[expr for x in iterable if cond]` | `list` |
| Dict comprehension | `{k: v for k, v in iterable}` | `dict` |
| Set comprehension | `{expr for x in iterable}` | `set` |
| Generator expression | `(expr for x in iterable)` | lazy iterator |

**Generator vs List comprehension:** Generator expressions are **lazy** — they produce values one at a time on demand. Use them when you don't need all values at once (saves memory).

---

### 2.2 Functions In-Depth

#### Definition and Calling Convention

**The "Why":** Functions are the primary unit of code reuse. A well-named function makes code self-documenting. Python functions are **first-class objects** — they can be assigned to variables, passed as arguments, and returned from other functions.

---

#### Argument Types

Python supports four kinds of arguments:

| Type | Syntax | Description |
|------|--------|-------------|
| Positional | `f(a, b)` | Matched by position |
| Keyword | `f(a=1, b=2)` | Matched by name |
| *args | `f(*args)` | Captures extra positional args as tuple |
| **kwargs | `f(**kwargs)` | Captures extra keyword args as dict |

**Order rule:** `positional → *args → keyword-only → **kwargs`

---

#### Return Values vs Side Effects

**The "Why":** This is a critical distinction in clean code:
- **Pure function:** Takes inputs, returns output, no external changes (predictable, testable)
- **Side effect function:** Modifies external state (prints, writes to DB, modifies a list)

Python implicitly returns `None` if no `return` statement is reached.

---

#### First-Class Functions and Lambda

Since functions are objects, you can:
- Assign them to variables
- Store them in lists/dicts
- Pass them to other functions (`map`, `filter`, `sorted`)
- Return them from functions

**Lambda:** Anonymous, single-expression function. Best for short, throwaway function arguments (e.g., sort keys). If a lambda needs more than one line — use `def`.

---

#### Type Hints (PEP 484)

**The "Why":** Type hints don't change runtime behavior but enable:
- IDE autocompletion and error detection
- `mypy` static analysis
- Clearer API documentation
- Django REST Framework serializer validation

---

### 2.3 Scope & Namespace — The LEGB Rule

**The "Why":** When Python sees a name, it must decide *which* object that name refers to. The LEGB rule is the lookup order:

```
L → Local        (inside current function)
E → Enclosing    (outer function, for closures)
G → Global       (module-level)
B → Built-in     (Python's built-in names: print, len, range...)
```

**Analogy:** LEGB is like looking for your keys — first check your pocket (Local), then your jacket (Enclosing), then the hall table (Global), then every drawer in the house (Built-in).

---

#### Closures and Variable Capture

**The "Why":** A closure is a function that "remembers" the enclosing scope even after the outer function has returned. This is the foundation of **decorators** (Day 8) and **factory functions**.

A closure is created when:
1. There is a nested function
2. The nested function refers to a variable from the enclosing scope
3. The enclosing function returns the nested function

---

## 3. Syntax & Code Examples

### 3.1 Control Flow

#### if / elif / else + Ternary

```python
# Standard if/elif/else
score = 72

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(grade)    # C

# Ternary operator — single-line for simple cases
status = "pass" if score >= 60 else "fail"
print(status)   # pass

# Nested ternary — use sparingly (readability drops fast)
label = "high" if score >= 80 else ("medium" if score >= 60 else "low")
print(label)    # medium
```

---

#### for Loop with else

```python
# Classic use case: search and report "not found"
def find_prime_factor(n, factors):
    for f in factors:
        if n % f == 0:
            print(f"Found factor: {f}")
            break
    else:
        # Only runs if loop completed WITHOUT hitting break
        print(f"No factor found in {factors}")

find_prime_factor(15, [2, 3, 5])    # Found factor: 3
find_prime_factor(17, [2, 3, 5])    # No factor found in [2, 3, 5]
```

---

#### while Loop with else

```python
# Password retry system
attempts = 0
max_attempts = 3
correct_password = "secure123"

while attempts < max_attempts:
    password = input("Enter password: ")
    if password == correct_password:
        print("Access granted.")
        break
    attempts += 1
    print(f"Wrong. {max_attempts - attempts} attempts remaining.")
else:
    # Only runs if while condition became False (not from break)
    print("Account locked — too many failed attempts.")
```

---

#### break / continue / pass

```python
# break — exit loop early
for i in range(10):
    if i == 5:
        break
    print(i, end=" ")
# Output: 0 1 2 3 4

print()

# continue — skip current iteration
for i in range(10):
    if i % 2 == 0:
        continue        # skip even numbers
    print(i, end=" ")
# Output: 1 3 5 7 9

print()

# pass — placeholder for future code
def future_feature():
    pass    # TODO: implement later

class EmptyBase:
    pass    # Valid empty class definition
```

---

#### Pattern Matching (Python 3.10+)

```python
# Basic value matching
def classify_http_status(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        case _:             # wildcard — matches anything
            return "Unknown status"

print(classify_http_status(404))    # Not Found

# Structural pattern matching — match on shape/type
def process_command(command):
    match command.split():
        case ["quit"]:
            print("Quitting...")
        case ["go", direction]:
            print(f"Going {direction}")
        case ["pick", "up", item]:
            print(f"Picking up {item}")
        case ["drop", *items]:          # captures remaining words
            print(f"Dropping: {items}")
        case _:
            print(f"Unknown command: {command}")

process_command("go north")         # Going north
process_command("pick up sword")    # Picking up sword
process_command("drop key coin")    # Dropping: ['key', 'coin']
```

---

#### Comprehensions

```python
# List comprehension — squares of even numbers
squares = [x**2 for x in range(10) if x % 2 == 0]
print(squares)      # [0, 4, 16, 36, 64]

# vs equivalent for loop (more verbose)
squares_loop = []
for x in range(10):
    if x % 2 == 0:
        squares_loop.append(x**2)

# Dict comprehension — invert a dictionary
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)     # {1: 'a', 2: 'b', 3: 'c'}

# Set comprehension — unique first letters
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
first_letters = {word[0] for word in words}
print(first_letters)    # {'a', 'b', 'c'}

# Generator expression — lazy, memory-efficient
total = sum(x**2 for x in range(1_000_000))   # no list created in memory
print(total)

# Nested comprehension — flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)     # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

### 3.2 Functions

#### Argument Patterns

```python
# Positional arguments
def add(a: int, b: int) -> int:
    return a + b

print(add(3, 4))        # 7
print(add(b=4, a=3))    # 7 — keyword order doesn't matter

# Default arguments
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

print(greet("Alice"))               # Hello, Alice!
print(greet("Bob", "Good morning")) # Good morning, Bob!

# *args — variable positional arguments (captured as tuple)
def total(*args: float) -> float:
    return sum(args)

print(total(1, 2, 3, 4, 5))    # 15.0

# **kwargs — variable keyword arguments (captured as dict)
def display_info(**kwargs: str) -> None:
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

display_info(name="Alice", role="Developer", city="Mumbai")
# name: Alice
# role: Developer
# city: Mumbai

# Combining all argument types
def complex_func(a, b, *args, keyword_only, **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"keyword_only={keyword_only}")
    print(f"kwargs={kwargs}")

complex_func(1, 2, 3, 4, 5, keyword_only="must", extra="value")
# a=1, b=2
# args=(3, 4, 5)
# keyword_only=must
# kwargs={'extra': 'value'}
```

---

#### Return Values and None

```python
# Explicit return
def divide(a: float, b: float) -> float | None:
    if b == 0:
        return None     # explicit None
    return a / b

result = divide(10, 0)
print(result)           # None

# Implicit None — function with no return statement
def log_message(msg: str) -> None:
    print(f"[LOG] {msg}")
    # implicitly returns None

result = log_message("test")
print(result)           # None

# Multiple return values (actually returns a tuple)
def min_max(numbers: list[int]) -> tuple[int, int]:
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9])
print(low, high)        # 1 9
```

---

#### First-Class Functions and Lambda

```python
# Functions as variables
def square(x): return x ** 2
def cube(x): return x ** 3

operations = [square, cube]
for op in operations:
    print(op(3))        # 9, then 27

# Functions as arguments
def apply(func, value):
    return func(value)

print(apply(square, 5))     # 25

# Functions as return values (factory pattern)
def multiplier(factor: int):
    def multiply(x: int) -> int:
        return x * factor
    return multiply     # returns the inner function

double = multiplier(2)
triple = multiplier(3)
print(double(10))       # 20
print(triple(10))       # 30

# Lambda — anonymous functions
# Best for short, throwaway functions
nums = [3, 1, 4, 1, 5, 9, 2, 6]
sorted_nums = sorted(nums, key=lambda x: -x)    # sort descending
print(sorted_nums)      # [9, 6, 5, 4, 3, 2, 1, 1]

# Lambda with map and filter
evens = list(filter(lambda x: x % 2 == 0, nums))
doubled = list(map(lambda x: x * 2, evens))
print(evens)            # [4, 2, 6]
print(doubled)          # [8, 4, 12]
```

---

#### Type Hints (PEP 484)

```python
from typing import Optional, Union

# Basic type hints
def greet(name: str, times: int = 1) -> str:
    return (name + " ") * times

# Optional parameter (can be None)
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)   # returns None if not found

# Union type — accepts multiple types
def process(value: Union[int, str]) -> str:
    return str(value).upper()

# Python 3.10+ — cleaner union syntax with |
def process_new(value: int | str) -> str:
    return str(value).upper()

# Type hints for collections
def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)

def merge(d1: dict[str, int], d2: dict[str, int]) -> dict[str, int]:
    return {**d1, **d2}
```

---

### 3.3 Scope and Closures

#### LEGB Rule

```python
x = "global"        # G — global scope

def outer():
    x = "enclosing" # E — enclosing scope

    def inner():
        x = "local" # L — local scope
        print(x)    # Finds 'local' first

    inner()
    print(x)        # Finds 'enclosing'

outer()
print(x)            # Finds 'global'

# Output:
# local
# enclosing
# global

# Built-in scope — len, print, range are all in built-in scope
print(len([1, 2, 3]))   # len found in B (built-in)
```

---

#### global and nonlocal

```python
# global — modify a global variable from inside a function
counter = 0

def increment():
    global counter      # declare intent to modify global
    counter += 1

increment()
increment()
print(counter)          # 2

# nonlocal — modify an enclosing (not global) variable
def make_counter():
    count = 0

    def increment():
        nonlocal count  # modify enclosing scope's 'count'
        count += 1
        return count

    return increment

counter_fn = make_counter()
print(counter_fn())     # 1
print(counter_fn())     # 2
print(counter_fn())     # 3
```

---

#### Closures

```python
# Closure: inner function captures outer function's variable
def make_adder(n: int):
    """Returns a function that adds n to its argument."""
    def add(x: int) -> int:
        return x + n    # 'n' is captured from enclosing scope
    return add

add5 = make_adder(5)
add10 = make_adder(10)

print(add5(3))      # 8
print(add10(3))     # 13

# Inspect closure variables
print(add5.__closure__[0].cell_contents)    # 5

# Real-world closure: rate limiter factory
def make_rate_limiter(max_calls: int):
    calls = 0

    def limiter(func):
        nonlocal calls
        if calls >= max_calls:
            raise Exception("Rate limit exceeded")
        calls += 1
        return func()

    return limiter

api_call = make_rate_limiter(3)
# api_call(some_function)  # works up to 3 times
```

---

#### Namespace Inspection

```python
def demo():
    local_var = 42
    print(locals())     # {'local_var': 42}

demo()

# globals() returns the module-level namespace dict
module_var = "hello"
print("module_var" in globals())    # True
```

---

## 4. Common Mistakes & Gotchas

### ❌ Mistake 1: Misunderstanding Loop `else`

```python
# ❌ Wrong assumption — thinking else runs when loop body is empty
numbers = []

for n in numbers:
    print(n)
else:
    print("No numbers!")   # This WILL run — loop completed without break

# ❌ Wrong — thinking else runs on break
for n in [1, 2, 3]:
    if n == 2:
        break
else:
    print("Done!")         # This will NOT run — break was hit

# ✅ Correct mental model:
# else runs if and only if the loop was NOT terminated by break
```

---

### ❌ Mistake 2: Mutable Default Argument (Day 1 revisited, now in function context)

```python
# ❌ Wrong — default list is shared across all calls
def append_item(item, lst=[]):
    lst.append(item)
    return lst

print(append_item("a"))     # ['a']
print(append_item("b"))     # ['a', 'b'] ← BUG

# ✅ Correct — use None sentinel
def append_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(append_item("a"))     # ['a']
print(append_item("b"))     # ['b'] ← correct
```

---

### ❌ Mistake 3: Closure Variable Capture in Loops

```python
# ❌ Wrong — all lambdas capture the SAME variable 'i'
funcs = [lambda: i for i in range(5)]
print([f() for f in funcs])    # [4, 4, 4, 4, 4] — all see final value of i

# ✅ Fix 1: Capture current value with default argument
funcs = [lambda i=i: i for i in range(5)]
print([f() for f in funcs])    # [0, 1, 2, 3, 4]

# ✅ Fix 2: Use functools.partial
from functools import partial
def identity(x): return x
funcs = [partial(identity, i) for i in range(5)]
print([f() for f in funcs])    # [0, 1, 2, 3, 4]
```
**Why it happens:** Closures capture the *variable*, not its *value* at the time of creation.

---

### ❌ Mistake 4: Using `*args` After `**kwargs`

```python
# ❌ Wrong — SyntaxError
def func(**kwargs, *args):
    pass

# ✅ Correct order: positional → *args → keyword-only → **kwargs
def func(pos1, pos2, *args, keyword_only, **kwargs):
    pass
```

---

### ❌ Mistake 5: Overwriting Built-in Names

```python
# ❌ Wrong — shadows Python's built-in list, filter, etc.
list = [1, 2, 3]        # now 'list' the built-in is gone!
print(list([4, 5, 6]))  # TypeError: 'list' object is not callable

# ✅ Correct — use descriptive names
numbers = [1, 2, 3]
filtered_items = [4, 5, 6]
```

---

## 5. Hands-on Exercises

### 🧑‍🏫 Guided Exercise 1: Number Utilities with Control Flow

**Goal:** Implement classic number functions using clean control flow.

```python
# Step 1: Prime checker using for/else
def is_prime(n: int) -> bool:
    """Returns True if n is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False    # found a factor — not prime
    else:
        return True         # loop completed without finding a factor

print(is_prime(17))     # True
print(is_prime(18))     # False
print(is_prime(1))      # False

# Step 2: Palindrome checker using string slicing
def is_palindrome(text: str) -> bool:
    """Returns True if text reads the same forwards and backwards."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

print(is_palindrome("racecar"))     # True
print(is_palindrome("A man a plan a canal Panama"))  # True
print(is_palindrome("hello"))       # False

# Step 3: Fibonacci using while loop
def fibonacci(n: int) -> list[int]:
    """Returns first n Fibonacci numbers."""
    if n <= 0:
        return []
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

print(fibonacci(8))     # [0, 1, 1, 2, 3, 5, 8, 13]
```

**Discussion:** How does `for/else` make `is_prime` cleaner than using a flag variable?

---

### 🧑‍🏫 Guided Exercise 2: Scope and Closures in Action

**Goal:** Build a counter factory that demonstrates closures and `nonlocal`.

```python
# Step 1: Basic closure counter
def make_counter(start: int = 0, step: int = 1):
    """Factory that creates a counter function."""
    count = start

    def counter() -> int:
        nonlocal count
        current = count
        count += step
        return current

    return counter

# Create independent counters
count_by_1 = make_counter()
count_by_5 = make_counter(0, 5)

print(count_by_1())     # 0
print(count_by_1())     # 1
print(count_by_5())     # 0
print(count_by_5())     # 5
print(count_by_1())     # 2  ← independent!

# Step 2: Inspect what the closure captured
print(count_by_1.__closure__)               # tuple of cell objects
print(count_by_1.__code__.co_freevars)      # ('count', 'step')
```

**Discussion:** Why are `count_by_1` and `count_by_5` independent even though they share the same `make_counter` code?

---

### 💻 Independent Practice 1: Argument Patterns

**Task:** Implement the following functions demonstrating each argument type.

```python
# 1. A function that accepts any number of strings and returns them joined
def join_strings(*args: str, separator: str = ", ") -> str:
    # Hint: use str.join()
    pass

print(join_strings("Python", "Django", "Flask"))            # Python, Django, Flask
print(join_strings("a", "b", "c", separator=" | "))         # a | b | c

# 2. A function that formats a profile using **kwargs
def format_profile(**kwargs: str) -> str:
    # Hint: build a string from kwargs.items()
    pass

print(format_profile(name="Alice", role="Dev", city="Pune"))
# Expected: name=Alice, role=Dev, city=Pune

# 3. A function that unpacks a list into positional args
def volume(length: float, width: float, height: float) -> float:
    return length * width * height

dimensions = [3.0, 4.0, 5.0]
# Call volume() by unpacking dimensions using *
# Hint: volume(*dimensions)
print(volume(*dimensions))      # 60.0
```

> **Hints:** `str.join()`, `f-string`, `*` unpacking operator

---

### 💻 Independent Practice 2: Higher-Order Functions

**Task:** Create a mini "function pipeline" system.

```python
# Build a pipeline function that applies a list of functions in sequence
def pipeline(*funcs):
    """Returns a function that applies funcs left-to-right."""
    def apply(value):
        result = value
        for func in funcs:
            result = func(result)
        return result
    return apply

# Test with these transformations
double = lambda x: x * 2
add_ten = lambda x: x + 10
square = lambda x: x ** 2

transform = pipeline(double, add_ten, square)
print(transform(3))     # ((3*2)+10)^2 = 16^2 = 256

# Now create a string pipeline
strip_ws = str.strip
to_upper = str.upper
add_exclaim = lambda s: s + "!"

clean = pipeline(strip_ws, to_upper, add_exclaim)
print(clean("  hello world  "))     # HELLO WORLD!
```

---

### 🏆 Challenge Problem: Build a Mini Dispatch Router

```python
"""
Build a command dispatcher that:
1. Stores command handlers in a dictionary
2. Supports registering new commands via a decorator-style function
3. Dispatches commands with arguments using *args and **kwargs
4. Returns a "command not found" message for unknown commands
"""

class CommandRouter:
    def __init__(self):
        self._routes: dict = {}

    def register(self, command: str):
        """Decorator-style registration."""
        def decorator(func):
            self._routes[command] = func
            return func
        return decorator

    def dispatch(self, command: str, *args, **kwargs):
        # Your code here
        pass

# Usage
router = CommandRouter()

@router.register("greet")
def greet_handler(name: str, formal: bool = False) -> str:
    prefix = "Good day" if formal else "Hey"
    return f"{prefix}, {name}!"

@router.register("add")
def add_handler(*numbers: float) -> float:
    return sum(numbers)

print(router.dispatch("greet", "Alice"))                    # Hey, Alice!
print(router.dispatch("greet", "Bob", formal=True))         # Good day, Bob!
print(router.dispatch("add", 1, 2, 3, 4))                   # 10.0
print(router.dispatch("unknown"))                           # Command 'unknown' not found
```

---

## 6. Best Practices & Industry Standards

### Comprehension Readability Rules

```python
# ✅ Good — short, readable comprehension
active_users = [u for u in users if u.is_active]

# ❌ Bad — too complex, use a regular loop + function instead
result = [transform(item) for sublist in matrix
          for item in sublist if item.valid and item.score > threshold]

# ✅ Better — extract into a named function
def should_include(item): return item.valid and item.score > threshold
result = [transform(item) for sublist in matrix for item in sublist if should_include(item)]
```

### Function Design Principles

```python
# ✅ Single responsibility — one function, one job
def validate_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]

def send_email(to: str, subject: str, body: str) -> bool:
    # send logic here
    pass

# ❌ Bad — function does too much
def validate_and_send_email(email, subject, body):
    if "@" not in email:
        print("invalid")
        return
    # send logic...
```

### Lambda Guidelines

```python
# ✅ Good use of lambda — short sort key
students.sort(key=lambda s: s.grade)

# ❌ Bad — lambda too complex
process = lambda x: x**2 if x > 0 else abs(x) + 10  # use def instead

# ✅ Better
def process(x: int) -> int:
    return x**2 if x > 0 else abs(x) + 10
```

### PEP 8 for Functions

```python
# ✅ Correct
def calculate_total_price(base_price: float, tax_rate: float = 0.18) -> float:
    """Calculate total price including tax."""
    return base_price * (1 + tax_rate)

# ✅ Two blank lines between top-level functions
def another_function():
    pass
```

### Avoid `global` — Prefer Return Values

```python
# ❌ Using global — hard to test and reason about
total = 0
def add_to_total(x):
    global total
    total += x

# ✅ Better — pure function, return the value
def add(current_total: float, x: float) -> float:
    return current_total + x

total = 0
total = add(total, 5)
total = add(total, 10)
```

---

## 7. Real-World Application

### Django Views Use Control Flow + Functions

```python
# views.py — Django view (Day 20 preview)
from django.http import JsonResponse

def user_profile(request, user_id: int):
    # Control flow to handle different HTTP methods
    if request.method == "GET":
        user = get_user_or_none(user_id)
        if user is None:
            return JsonResponse({"error": "User not found"}, status=404)
        return JsonResponse({"name": user.name, "email": user.email})

    elif request.method == "DELETE":
        # ... delete logic
        pass

    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


def get_user_or_none(user_id: int):
    """Helper using early return pattern."""
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
```

### Comprehensions in ORM Queries

```python
# Transform Django queryset with comprehension (Day 21 preview)
from myapp.models import Product

def get_active_product_names() -> list[str]:
    return [p.name for p in Product.objects.filter(is_active=True)]

def get_price_map() -> dict[str, float]:
    return {p.name: p.price for p in Product.objects.all()}
```

### Higher-Order Functions as Middleware Pattern

```python
# Middleware pattern (Day 25 preview) — wraps functions with extra behavior
def require_auth(view_func):
    """HOF that adds authentication check to any view."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login")
        return view_func(request, *args, **kwargs)
    return wrapper

@require_auth
def dashboard(request):
    return render(request, "dashboard.html")
```

### 🔭 Connection to Upcoming Days
- **Day 3:** File I/O — uses functions, loops, and comprehensions to process file data
- **Day 4:** OOP — methods are functions; understanding `self` needs LEGB
- **Day 8:** Decorators — directly built on closures and HOFs learned today
- **Day 20:** Django views — every URL maps to a Python function

---

## 8. Quick Revision Summary

### Key Terms

| Term | One-line Definition |
|------|---------------------|
| Ternary operator | Inline `if/else` expression: `val_if_true if condition else val_if_false` |
| Loop `else` | Runs only if loop ended naturally (no `break`) |
| `break` | Immediately exits the enclosing loop |
| `continue` | Skips current iteration, continues to next |
| `pass` | No-op placeholder — does nothing |
| `match/case` | Python 3.10+ structural pattern matching |
| Comprehension | Concise syntax to create list/dict/set from an iterable |
| Generator expression | Lazy comprehension that yields values one at a time |
| `*args` | Captures extra positional arguments as a tuple |
| `**kwargs` | Captures extra keyword arguments as a dict |
| Pure function | Function with no side effects — output depends only on input |
| First-class function | Functions treated as values (assignable, passable, returnable) |
| Lambda | Anonymous single-expression function |
| LEGB | Scope lookup order: Local → Enclosing → Global → Built-in |
| Closure | Inner function that remembers its enclosing scope's variables |
| `nonlocal` | Keyword to modify a variable in the enclosing (non-global) scope |
| Type hint | PEP 484 annotation for parameter and return types |

---

### Core Syntax Cheat Sheet

```python
# Ternary
result = "yes" if condition else "no"

# Loop else
for x in iterable:
    if condition: break
else:
    # runs if no break

# match/case (3.10+)
match value:
    case pattern: ...
    case _: ...          # wildcard

# Comprehensions
[expr for x in it if cond]         # list
{k: v for k, v in it}              # dict
{expr for x in it}                 # set
(expr for x in it)                 # generator

# Function signatures
def f(pos, /, normal, *, kw_only): ...
def f(*args, **kwargs): ...

# Type hints
def f(x: int, y: str = "a") -> bool: ...

# Lambda
fn = lambda x, y: x + y

# LEGB modifiers
global var_name
nonlocal var_name

# Closure
def outer():
    x = 10
    def inner(): return x   # captures x
    return inner
```

---

### 5 MCQ Recap Questions

**Q1.** When does the `else` clause of a `for` loop execute?
- A) When the loop body is empty
- B) When the loop runs zero iterations
- **C) When the loop completes without hitting a `break`** ✅
- D) Always, after the loop

**Q2.** What does `*args` capture inside a function?
- A) A dictionary of keyword arguments
- **B) A tuple of extra positional arguments** ✅
- C) A list of all arguments
- D) Nothing — it's syntax sugar

**Q3.** In the LEGB rule, which scope is searched LAST?
- A) Local
- B) Global
- C) Enclosing
- **D) Built-in** ✅

**Q4.** What is the key characteristic of a closure?
- A) It uses the `global` keyword
- B) It's defined inside a class
- **C) It remembers variables from its enclosing scope after the outer function returns** ✅
- D) It has no return value

**Q5.** What is the difference between a list comprehension and a generator expression?
- A) No difference — they produce the same result
- B) Generator expressions use square brackets
- **C) List comprehensions produce all values at once; generators are lazy and yield values on demand** ✅
- D) Generators are slower than list comprehensions

---

## 9. Instructor Notes

### 📌 Anticipated Student Questions

| Question | Suggested Answer |
|----------|-----------------|
| "When should I use `for/else` vs a flag variable?" | `for/else` is cleaner and more Pythonic for "search and report not found" patterns. Flag variables add noise. |
| "Is `match/case` the same as a switch statement?" | Similar purpose, but far more powerful — it matches *structure* (types, shapes, sequences), not just values. |
| "Why use generators over list comprehensions?" | Memory efficiency — generators produce values one at a time. Critical when processing millions of records. |
| "When should I use `lambda` vs `def`?" | Lambda for short, throwaway one-liners (sort keys, map/filter). `def` for anything with logic, multiple statements, or that needs a name. |
| "What's the point of `nonlocal`?" | Without it, you can *read* an enclosing variable but can't *reassign* it. `nonlocal` grants write access. |
| "Does Python optimize tail recursion?" | No. Python has a fixed recursion limit (~1000). Use iteration or `functools.lru_cache` instead of deep recursion. |
| "What are type hints good for if Python ignores them?" | IDE support (autocompletion, errors), `mypy` static analysis, documentation, and Django REST Framework serializers use them. |

---

### 🖊️ Whiteboard Diagrams to Draw

1. **LEGB Scope Diagram:** Four nested boxes labeled B (outermost), G, E, L (innermost). Arrow from L searching outward to B.
2. **Closure Memory Model:** Draw `make_counter()` on the stack, then show the returned `counter` function with an arrow to the captured `count` cell still alive on the heap.
3. **for/else Flow:** Draw a flowchart — loop body → condition → break? → if yes: skip else; if no: continue; when done: run else.
4. **Argument Order:** Linear diagram: `positional → *args → keyword-only → **kwargs`
5. **Generator vs List:** Two diagrams — list creates a full box of values at once; generator shows a tap producing one value at a time on demand.
6. **HOF concept:** Box labeled "outer function" → produces → box labeled "inner function" → which has a pointer back to outer scope.

---

### ⏱️ Timing Guide (3 Hours)

| Time | Activity |
|------|----------|
| 0:00 – 0:10 | Day 1 quick recap quiz (3 questions), setup check |
| 0:10 – 0:30 | Control flow: if/elif/else, ternary, loop else + whiteboard |
| 0:30 – 0:45 | break/continue/pass + match/case live demo |
| 0:45 – 1:05 | Comprehensions — list, dict, set, generator |
| 1:05 – 1:15 | ☕ Break |
| 1:15 – 1:35 | Functions: argument patterns (*args, **kwargs), return values |
| 1:35 – 1:55 | First-class functions, lambda, type hints |
| 1:55 – 2:15 | LEGB rule, global/nonlocal, closures + whiteboard |
| 2:15 – 2:35 | Guided exercises 1 & 2 (instructor-led) |
| 2:35 – 2:50 | Common mistakes walkthrough + Q&A |
| 2:50 – 3:00 | MCQ recap, assignment briefing, Day 3 preview |

> 💡 **Tip:** The closure + LEGB section often needs extra time — budget 5 minutes flex here.
> 💡 **Demo tip:** Use [Python Tutor](https://pythontutor.com) live to show LEGB lookup and closure variable capture visually.

---

### 📚 Resources & Further Reading

- [PEP 8 — Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [PEP 634 — Structural Pattern Matching](https://peps.python.org/pep-0634/)
- [Real Python — Closures](https://realpython.com/inner-functions-what-are-they-good-for/)
- [Real Python — Comprehensions](https://realpython.com/list-comprehension-python/)
- [Python Docs — functools](https://docs.python.org/3/library/functools.html)
- [Python Tutor — Visualizer](https://pythontutor.com/) ← live LEGB/closure demo tool
- [Fluent Python (Ch. 7) — Functions as First-Class Objects](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/)

---

### 📝 Assignment Brief (Take-Home)

**Build a Feature-Rich CLI Calculator:**

Requirements:
- Basic operations: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- Scientific functions using `math` module: `sin`, `cos`, `sqrt`
- Memory storage: `MS` (memory store), `MR` (memory recall), `MC` (memory clear)
- History tracking: last 10 operations
- Error handling: division by zero, invalid input, domain errors
- **Type hints on all functions**
- `match/case` for operation dispatch

```python
# Starter scaffold
import math
from typing import Optional

history: list[str] = []
memory: float = 0.0

def calculate(a: float, op: str, b: Optional[float] = None) -> float:
    """Dispatch calculation based on operator."""
    match op:
        case "+": return a + b
        case "-": return a - b
        # ... complete this
        case "sqrt": return math.sqrt(a)
        case _: raise ValueError(f"Unknown operator: {op}")

def add_to_history(expression: str, result: float) -> None:
    """Add to history, keep last 10."""
    # Your code here
    pass

def main() -> None:
    """Main REPL loop."""
    # Your code here
    pass

if __name__ == "__main__":
    main()
```