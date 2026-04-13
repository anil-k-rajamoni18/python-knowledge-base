# Day 2 Interview Preparation
# Topic: Control Flow & Functions
---

## 🟢 Beginner Level Questions

---

### Q1. What are the three loop control keywords in Python and what does each do?

**Answer:**
- `break` — immediately exits the enclosing loop, skipping any remaining iterations and the `else` clause
- `continue` — skips the rest of the current iteration and jumps to the next one
- `pass` — does nothing; a syntactic placeholder for empty blocks

```python
for i in range(10):
    if i == 3:
        continue    # skip 3
    if i == 7:
        break       # stop at 7
    print(i, end=" ")
# Output: 0 1 2 4 5 6
```

---

### Q2. What is a list comprehension? How is it different from a `for` loop?

**Answer:**
A list comprehension is a concise, single-expression syntax for creating a new list by transforming or filtering an iterable.

```python
# For loop
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x**2)

# Equivalent list comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
```

**Differences:**
- Comprehensions are faster (optimized C loop in CPython)
- Comprehensions return a value (the new list); loops modify state as a side effect
- Comprehensions are more readable for simple transformations; loops are clearer for complex logic

---

### Q3. What is the purpose of `*args` and `**kwargs`?

**Answer:**
- `*args` allows a function to accept any number of **positional** arguments, captured as a **tuple**
- `**kwargs` allows a function to accept any number of **keyword** arguments, captured as a **dict**

```python
def describe(*args, **kwargs):
    print("Positional:", args)
    print("Keyword:", kwargs)

describe(1, 2, 3, name="Alice", role="dev")
# Positional: (1, 2, 3)
# Keyword: {'name': 'Alice', 'role': 'dev'}
```

---

### Q4. What does Python return if a function has no `return` statement?

**Answer:**
Python implicitly returns `None`.

```python
def do_nothing():
    x = 42      # does some work but never returns

result = do_nothing()
print(result)           # None
print(type(result))     # <class 'NoneType'>
```

---

### Q5. What is a lambda function? When would you use one?

**Answer:**
A lambda is an anonymous, single-expression function defined with the `lambda` keyword.

```python
# Named function
def square(x): return x**2

# Equivalent lambda
square = lambda x: x**2
```

**When to use:** Short, throwaway functions — primarily as arguments to `sorted()`, `map()`, `filter()`, or any higher-order function where a full `def` would be verbose.

```python
names = ["Charlie", "Alice", "Bob"]
names.sort(key=lambda name: len(name))   # sort by length
print(names)    # ['Bob', 'Alice', 'Charlie']
```

**When NOT to use:** When the function needs more than one expression, has complex logic, or needs to be reused — use `def` instead.

---

### Q6. What are type hints in Python? Do they affect runtime behavior?

**Answer:**
Type hints (PEP 484) are annotations that specify the expected types of function parameters and return values.

```python
def greet(name: str, times: int = 1) -> str:
    return (name + " ") * times
```

**They do NOT affect runtime** — Python ignores them during execution. Their value is:
- IDE autocompletion and inline error detection
- Static analysis tools like `mypy`
- Improved code documentation
- Framework integrations (e.g., FastAPI, Django REST Framework use them for validation)

---

## 🟡 Intermediate Level Questions

---

### Q7. Explain the LEGB rule with an example.

**Answer:**
LEGB is the order Python searches for a name when it's referenced:

1. **L**ocal — current function scope
2. **E**nclosing — any enclosing function scopes (for closures)
3. **G**lobal — module-level scope
4. **B**uilt-in — Python's pre-defined names (`len`, `print`, `range`, etc.)

```python
x = "global"            # G

def outer():
    x = "enclosing"     # E

    def inner():
        x = "local"     # L
        print(x)        # → "local"

    inner()
    print(x)            # → "enclosing"

outer()
print(x)                # → "global"
print(len)              # → built-in len function (B)
```

Python stops at the first scope where the name is found.

---

### Q8. What is the pitfall of mutable default arguments? How do you fix it?

**Answer:**
Default argument values are evaluated **once at function definition time**, not on each call. If the default is a mutable object (list, dict, set), it persists and accumulates state across calls.

```python
# ❌ Bug
def append_item(item, lst=[]):
    lst.append(item)
    return lst

print(append_item("a"))     # ['a']
print(append_item("b"))     # ['a', 'b'] ← bug — same list object!

# ✅ Fix — use None as sentinel
def append_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(append_item("a"))     # ['a']
print(append_item("b"))     # ['b'] ← correct
```

**Why it happens:** Default values are stored on the function object itself (check `append_item.__defaults__`). The same mutable object is reused every time.

---

### Q9. What is a closure? Provide a real-world use case.

**Answer:**
A closure is an inner function that **captures and remembers variables from its enclosing scope**, even after the outer function has returned.

Three conditions for a closure:
1. Nested function exists
2. Inner function references a variable from the outer scope
3. Outer function returns the inner function

```python
def make_multiplier(factor: int):
    def multiply(x: int) -> int:
        return x * factor   # 'factor' is captured from enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))    # 10
print(triple(5))    # 15
```

**Real-world use cases:**
- **Decorator pattern** — wrapping functions with logging, authentication, caching
- **Factory functions** — creating specialized functions from a template
- **Callback configuration** — event handlers that need context
- **Django middleware** — wraps views with extra behavior

```python
# Practical closure: configurable logger
def make_logger(prefix: str):
    def log(message: str) -> None:
        print(f"[{prefix}] {message}")
    return log

error_log = make_logger("ERROR")
info_log = make_logger("INFO")

error_log("Database connection failed")     # [ERROR] Database connection failed
info_log("Server started on port 8000")    # [INFO] Server started on port 8000
```

---

### Q10. What is the difference between `*args` and `**kwargs`? Can you use both in the same function?

**Answer:**

| | `*args` | `**kwargs` |
|--|---------|------------|
| Captures | Extra positional arguments | Extra keyword arguments |
| Type inside function | `tuple` | `dict` |
| Syntax in call | `f(1, 2, 3)` | `f(a=1, b=2)` |
| Unpacking usage | `f(*my_list)` | `f(**my_dict)` |

Yes, you can use both — but order matters: `positional → *args → keyword-only → **kwargs`

```python
def full_function(a, b, *args, keyword_only="default", **kwargs):
    print(f"a={a}, b={b}")
    print(f"extra positional: {args}")
    print(f"keyword_only: {keyword_only}")
    print(f"extra keyword: {kwargs}")

full_function(1, 2, 3, 4, keyword_only="custom", x=10, y=20)
# a=1, b=2
# extra positional: (3, 4)
# keyword_only: custom
# extra keyword: {'x': 10, 'y': 20}
```

---

### Q11. When should you use a `lambda` vs `def`?

**Answer:**

| Scenario | Use |
|----------|-----|
| Short, single-expression function as an argument | `lambda` |
| Function with multiple statements | `def` |
| Function that needs a docstring | `def` |
| Reusable, named function | `def` |
| Sort key, map/filter argument | `lambda` |
| Complex business logic | `def` |

```python
# ✅ Good lambda use
data.sort(key=lambda item: (item.category, item.price))

# ❌ Bad lambda use — too complex, unreadable
process = lambda x: x**2 if x > 0 else (-x + 10) if x < -5 else 0

# ✅ Better as def
def process(x: int) -> int:
    if x > 0: return x**2
    if x < -5: return -x + 10
    return 0
```

**PEP 8 explicitly discourages** assigning lambdas to names — if you're naming it, use `def`.

---

### Q12. What is a generator expression and when would you prefer it over a list comprehension?

**Answer:**
A generator expression uses `()` instead of `[]` and produces values **lazily** — one at a time, on demand — rather than building the entire list in memory.

```python
# List comprehension — all values in memory at once
squares_list = [x**2 for x in range(1_000_000)]    # ~8MB in memory

# Generator expression — one value at a time, tiny memory footprint
squares_gen = (x**2 for x in range(1_000_000))     # ~200 bytes

# Both work the same way for iteration
total = sum(x**2 for x in range(1_000_000))         # generator inside sum
```

**When to prefer generators:**
- Processing large files line by line
- Streaming API responses
- Pipeline data processing
- When you only need to iterate once and don't need indexing

---

### Q13. Explain `global` vs `nonlocal`. When would you use each?

**Answer:**

- `global`: Declares that a variable name refers to the **module-level (global)** variable, allowing assignment to it inside a function
- `nonlocal`: Declares that a variable name refers to the **nearest enclosing scope** (not global), allowing assignment to it inside a nested function

```python
counter = 0                 # global scope

def increment_global():
    global counter
    counter += 1            # modifies the global

def make_counter():
    count = 0               # enclosing scope

    def increment():
        nonlocal count
        count += 1          # modifies enclosing, not global
        return count

    return increment

# Without global/nonlocal, Python would create a new local variable
# instead of modifying the outer one — causing UnboundLocalError
```

**Industry note:** Prefer returning values over `global` — it makes functions easier to test and reason about.

---

## 🔴 Advanced / Senior Level Questions

---

### Q14. What is recursion? What are its pros, cons, and how do you handle its limitations in Python?

**Answer:**
Recursion is when a function calls itself to solve a smaller version of the same problem, until it reaches a base case.

```python
def factorial(n: int) -> int:
    if n <= 1:          # base case — must have one!
        return 1
    return n * factorial(n - 1)   # recursive case

print(factorial(5))     # 120
```

**Pros:**
- Elegant for naturally recursive problems (trees, graphs, divide-and-conquer)
- Code can mirror the mathematical definition of a problem
- Often shorter and more readable than iterative equivalents

**Cons:**
- Each call adds a frame to the call stack — stack overflow risk for deep recursion
- Python has a fixed recursion limit (default ~1000): `sys.getrecursionlimit()`
- No tail-call optimization in CPython — every call consumes stack space
- Usually slower than iteration due to function call overhead

**Handling limitations:**

```python
import sys
sys.setrecursionlimit(5000)     # increase limit (use with caution!)

# Better: convert to iteration with an explicit stack
def factorial_iterative(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Or use memoization to avoid redundant calls
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

---

### Q15. What is the closure variable capture trap in loops? How do you fix it?

**Answer:**
When creating closures inside a loop, all closures capture the **same variable** (the loop variable), not its value at each iteration. By the time any closure is called, the loop has finished and the variable holds its final value.

```python
# ❌ Bug — all functions return 4
funcs = [lambda: i for i in range(5)]
print([f() for f in funcs])    # [4, 4, 4, 4, 4]

# ✅ Fix 1: Default argument captures current value
funcs = [lambda i=i: i for i in range(5)]
print([f() for f in funcs])    # [0, 1, 2, 3, 4]

# ✅ Fix 2: Factory function creates a fresh scope per iteration
def make_func(i):
    return lambda: i

funcs = [make_func(i) for i in range(5)]
print([f() for f in funcs])    # [0, 1, 2, 3, 4]

# ✅ Fix 3: functools.partial
from functools import partial
identity = lambda x: x
funcs = [partial(identity, i) for i in range(5)]
print([f() for f in funcs])    # [0, 1, 2, 3, 4]
```

---

### Q16. What is `functools.partial` and when is it useful?

**Answer:**
`functools.partial` creates a new function from an existing one with some arguments pre-filled (partial application).

```python
from functools import partial

def power(base: float, exponent: float) -> float:
    return base ** exponent

# Create specialized versions
square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(4))    # 16.0
print(cube(3))      # 27.0

# Real-world: pre-configure a logging function
import logging
logging.basicConfig(level=logging.DEBUG)

debug = partial(logging.log, logging.DEBUG)
error = partial(logging.log, logging.ERROR)

debug("Starting application")
error("Database unreachable")
```

**Use cases:**
- Creating specialized functions from general ones
- Fixing arguments for callback functions that accept a specific signature
- Replacing closures when no internal state is needed

---

### Q17. How does Python's `match/case` differ from a traditional `switch` statement?

**Answer:**
Traditional switch (C, Java) only matches on **value equality**. Python's `match/case` does **structural pattern matching** — it can match on:
- Literal values
- Variable capture (binding matched values to names)
- Sequence structure (lists, tuples)
- Mapping structure (dicts)
- Class instances
- Guards (`if` conditions in patterns)
- OR patterns with `|`

```python
# Value matching
match command:
    case "quit": ...
    case "help": ...

# Sequence matching with capture
match point:
    case (0, 0): print("origin")
    case (x, 0): print(f"on x-axis at {x}")
    case (0, y): print(f"on y-axis at {y}")
    case (x, y): print(f"at ({x}, {y})")

# Class pattern matching
match event:
    case MouseEvent(button=1, position=(x, y)):
        print(f"Left click at {x}, {y}")
    case KeyEvent(key="Escape"):
        print("Escape pressed")

# Guard condition
match number:
    case n if n < 0: print("negative")
    case n if n == 0: print("zero")
    case n: print(f"positive: {n}")
```

---

### Q18. Explain first-class functions with a practical higher-order function example.

**Answer:**
In Python, functions are **first-class objects** — they can be:
- Assigned to variables
- Stored in data structures
- Passed as arguments
- Returned from other functions

A **higher-order function** either takes a function as an argument or returns a function (or both).

```python
from typing import Callable

# HOF that takes a function as argument
def apply_twice(func: Callable[[int], int], value: int) -> int:
    """Apply func to value twice."""
    return func(func(value))

double = lambda x: x * 2
print(apply_twice(double, 3))       # 12  (3 → 6 → 12)

# HOF that returns a function
def compose(f: Callable, g: Callable) -> Callable:
    """Returns a function that applies g then f."""
    def composed(*args, **kwargs):
        return f(g(*args, **kwargs))
    return composed

add_one = lambda x: x + 1
square = lambda x: x ** 2

square_then_add = compose(add_one, square)
print(square_then_add(4))           # 17  (4² + 1)

# Real-world: function dispatch table (replaces long if/elif chains)
operations = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b,
}

def calculate(op: str, a: float, b: float) -> float:
    handler = operations.get(op)
    if handler is None:
        raise ValueError(f"Unknown operation: {op}")
    return handler(a, b)

print(calculate("add", 3, 4))   # 7
print(calculate("mul", 3, 4))   # 12
```

---

## 📝 Quick-Fire Answers

| Question | Answer |
|----------|--------|
| What does `for/else` do that plain `for` doesn't? | Runs `else` only if the loop completed without a `break` |
| What is the default recursion limit in Python? | ~1000 (`sys.getrecursionlimit()`) |
| Does Python support tail call optimization? | No — every recursive call adds a stack frame |
| What type does `*args` produce inside a function? | `tuple` |
| What type does `**kwargs` produce inside a function? | `dict` |
| What does `pass` do? | Nothing — syntactic placeholder |
| What module provides `partial`, `reduce`, `lru_cache`? | `functools` |
| What is `__closure__` on a function object? | Tuple of cells containing captured variables |
| What PEP defines type hints? | PEP 484 |
| What Python version introduced `match/case`? | Python 3.10 |
| What does `nonlocal` allow? | Reassigning a variable in the nearest enclosing (non-global) scope |
| What is a pure function? | A function with no side effects whose output depends only on its inputs |

---

## 🧠 Behavioral / Scenario Questions

### "Describe a situation where a closure would be the right tool."
**Model answer:** "I used a closure to build a configurable retry decorator. The outer function accepts `max_retries` and `delay` parameters, and the inner function wraps the target function. This way I can create `@retry(max_retries=3)` without needing a class — the closure captures the configuration naturally."

### "How would you refactor a function with 10 parameters?"
**Model answer:** "I'd group related parameters into a dataclass or dict, use `**kwargs` with validation, consider the Builder pattern, or split the function into smaller functions with single responsibilities. I'd also ask whether the function is doing too much and should be split entirely."

### "What would you do if you hit Python's recursion limit?"
**Model answer:** "First, I'd consider converting to an iterative solution using an explicit stack (list). If the recursive logic is genuinely needed, I'd add memoization with `@lru_cache` to avoid redundant calls. As a last resort, I'd use `sys.setrecursionlimit()` with careful bounds checking — though this is usually a sign of a design problem."

---

*End of Day 2 Interview Prep — Day 3 will add: OOP, classes, inheritance, dunder methods*
