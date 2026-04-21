# Day 11 — Python Decorators
### Python Full Stack Bootcamp | Session Duration: 3 Hours

---

## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, students will be able to:
- Explain first-class functions and closures, and use them to build decorator functions from scratch
- Write decorators using the `@` syntax with `functools.wraps` to preserve function metadata
- Create parameterized decorator factories that accept their own arguments
- Apply real-world decorators for timing, logging, authentication, caching, and retry logic
- Stack multiple decorators correctly and explain the order of application

### 📚 Prerequisites (Days 1–10)
- Functions, `*args`, `**kwargs`, scope (Day 6)
- OOP — classes, `__call__`, dunder methods (Days 7–8)
- Exception handling — `try/except` (Day 9)
- Closures and generator concepts (Day 10)


## 2. Concept Explanation

### 2.1 Functions as First-Class Objects — The Foundation

**Real-world analogy:** In most languages, functions are like appliances — fixed in place, you go to them. In Python, functions are like objects you can pick up, carry around, put in a box, hand to someone else, and even modify before handing back. They are **first-class citizens**.

"First-class" means a function can be:
- Assigned to a variable
- Passed as an argument to another function
- Returned from a function
- Stored in a data structure

This is the *entire* foundation of decorators. Without first-class functions, decorators don't exist.

### 2.2 Closures — The Memory That Functions Have

**Real-world analogy:** Imagine a backpack. When a function is defined inside another function, it gets a backpack containing all the variables from the outer function's scope. Even after the outer function finishes, the inner function still has its backpack — with those variables inside. That backpack is the **closure**.

A closure is an inner function that **remembers** the variables from its enclosing scope, even after that scope has exited.

### 2.3 The Wrapper Pattern — What Decorators Actually Do

A decorator is a function that:
1. **Takes** a function as input
2. **Defines** a new (wrapper) function that calls the original
3. **Returns** the wrapper function

It's like gift-wrapping a present. The original function (the gift) is still inside — but it now has extra paper around it (the wrapper) that can do something before or after you open it. The `@` syntax is just Python's way of doing the gift-wrapping automatically.

### 2.4 The `@` Syntax — Syntactic Sugar

`@decorator` placed above a function definition is *exactly* equivalent to writing `func = decorator(func)` after the function. It's purely cosmetic convenience.

### 2.5 Parameterized Decorators — Decorators with Arguments

When a decorator itself needs to accept arguments (e.g., `@retry(max_attempts=3)`), you add one more layer of nesting: a **decorator factory** that returns the actual decorator. This is a function that returns a function that returns a function — three levels deep.

### 2.6 Class-Based Decorators

Any callable object can be a decorator — not just functions. A class with `__call__` implemented can wrap functions too. This is useful when the decorator needs to maintain complex state between calls.

### 2.7 Stacking Decorators — Order Matters

When you stack multiple decorators, they are applied **bottom-up** (closest to the function first) but **execute top-down**. Visualise them as layers of an onion — outermost layer is the first decorator, innermost is the function itself.

---

## 3. Syntax & Code Examples

### 3.1 First-Class Functions — The Building Blocks

```python
# ── Functions assigned to variables ───────────────────────────────────────────
def greet(name):
    return f"Hello, {name}!"

say_hello = greet          # No () — we're assigning the function itself, not calling it
print(say_hello("Alice"))  # Hello, Alice!
print(greet is say_hello)  # True — same object

# ── Functions passed as arguments ─────────────────────────────────────────────
def apply_twice(func, value):
    """Call func(value) twice, returning the result of the second call."""
    return func(func(value))

def double(x):
    return x * 2

print(apply_twice(double, 3))   # 12  — double(double(3)) = double(6) = 12

# ── Functions returned from functions ─────────────────────────────────────────
def make_multiplier(factor):
    """Returns a NEW function that multiplies by factor."""
    def multiplier(x):
        return x * factor     # 'factor' comes from the outer scope
    return multiplier         # Return the function object, not its result

triple = make_multiplier(3)
print(triple(10))             # 30
print(triple(7))              # 21
print(type(triple))           # <class 'function'>

# ── Functions stored in data structures ───────────────────────────────────────
operations = {
    "add":      lambda x, y: x + y,
    "subtract": lambda x, y: x - y,
    "multiply": lambda x, y: x * y,
}
print(operations["add"](5, 3))  # 8
```

---

### 3.2 Closures — Inner Functions with Memory

```python
def make_counter(start=0):
    """
    Returns a counter function that remembers its own count.
    Each call to make_counter() creates a SEPARATE, independent counter.
    """
    count = start    # This variable lives in the closure
    
    def increment(step=1):
        nonlocal count       # Declare we want to MODIFY the outer variable
        count += step
        return count
    
    return increment

# Two independent counters — separate closures, separate 'count' variables
counter_a = make_counter(0)
counter_b = make_counter(100)

print(counter_a())     # 1
print(counter_a())     # 2
print(counter_b())     # 101
print(counter_a(5))    # 7   — step=5
print(counter_b())     # 102 — completely independent of counter_a

# Inspecting the closure
print(counter_a.__closure__)           # tuple of cell objects
print(counter_a.__closure__[0].cell_contents)   # 7 — current value of 'count'
```

---

### 3.3 The Wrapper Pattern — Building a Decorator by Hand

```python
# ── Step 1: Write a basic wrapper manually ────────────────────────────────────
def shout(func):
    """A decorator that makes any function's return value UPPERCASE."""
    
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)          # Call the original function
        return result.upper()                   # Transform the result
    
    return wrapper                              # Return the wrapper, not the result

def greet(name):
    return f"hello, {name}"

# Apply the decorator manually (the old way)
greet = shout(greet)     # greet is now the wrapper function
print(greet("alice"))    # HELLO, ALICE

# ── Step 2: The same thing using @ syntax ────────────────────────────────────
def shout(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

@shout                   # Equivalent to: greet = shout(greet)
def greet(name):
    return f"hello, {name}"

print(greet("bob"))      # HELLO, BOB

# ── Verify: @ syntax is exactly equal to manual application ──────────────────
def no_op(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@no_op
def add(a, b):
    return a + b

# This is IDENTICAL to: add = no_op(add)
print(add(3, 4))   # 7
```

---

### 3.4 `functools.wraps` — Preserving Function Identity

```python
import functools

# ── Without wraps — function identity is broken ───────────────────────────────
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def important_function():
    """This docstring is important."""
    pass

print(important_function.__name__)   # 'wrapper'   ← WRONG!
print(important_function.__doc__)    # None         ← WRONG!

# ── With functools.wraps — identity preserved ─────────────────────────────────
def good_decorator(func):
    @functools.wraps(func)           # ← Copies __name__, __doc__, __module__ etc.
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def important_function():
    """This docstring is important."""
    pass

print(important_function.__name__)   # 'important_function' ✅
print(important_function.__doc__)    # 'This docstring is important.' ✅
```

---

### 3.5 Real-World Decorator 1 — Timing / Profiling

```python
import functools
import time

def timing(func):
    """Measures and prints the execution time of the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()          # High-resolution timer
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMING] {func.__name__}() took {elapsed:.4f}s")
        return result
    return wrapper

@timing
def slow_function():
    time.sleep(1)
    return "done"

@timing
def fast_function(n):
    return sum(range(n))

slow_function()          # [TIMING] slow_function() took 1.0012s
fast_function(1_000_000) # [TIMING] fast_function() took 0.0423s
```

---

### 3.6 Real-World Decorator 2 — Logging

```python
import functools
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)s | %(message)s")

def log_calls(func):
    """Logs every call to the function, including arguments and return value."""
    logger = logging.getLogger(func.__module__)
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(
            "Calling %s | args=%s | kwargs=%s",
            func.__name__, args, kwargs
        )
        try:
            result = func(*args, **kwargs)
            logger.debug("  %s returned: %s", func.__name__, result)
            return result
        except Exception as e:
            logger.error("  %s raised %s: %s", func.__name__, type(e).__name__, e)
            raise    # Re-raise — don't swallow exceptions
    
    return wrapper

@log_calls
def divide(a, b):
    return a / b

divide(10, 2)   # Logs the call and result
divide(10, 0)   # Logs the exception, then re-raises ZeroDivisionError

# Output:
# 2024-01-15 10:00:00 | DEBUG | Calling divide | args=(10, 2) | kwargs={}
# 2024-01-15 10:00:00 | DEBUG |   divide returned: 5.0
# 2024-01-15 10:00:00 | DEBUG | Calling divide | args=(10, 0) | kwargs={}
# 2024-01-15 10:00:00 | ERROR |   divide raised ZeroDivisionError: division by zero
```

---

### 3.7 Parameterized Decorators — Decorator Factories

```python
import functools
import logging

# ── Three levels of nesting ───────────────────────────────────────────────────
# Level 1: decorator FACTORY (accepts decorator arguments)
# Level 2: actual DECORATOR (accepts the function)
# Level 3: WRAPPER (accepts the function's arguments)

def log_with_level(level="INFO"):
    """
    Decorator FACTORY — call it with a level to get the actual decorator.
    Usage: @log_with_level("DEBUG") or @log_with_level("ERROR")
    """
    def decorator(func):                     # Level 2: actual decorator
        @functools.wraps(func)
        def wrapper(*args, **kwargs):         # Level 3: wrapper
            log_func = getattr(logging, level.lower())
            log_func(f"Calling {func.__name__}()")
            result = func(*args, **kwargs)
            log_func(f"{func.__name__}() completed.")
            return result
        return wrapper
    return decorator                         # Return the decorator, not the wrapper

# Using the decorator factory with arguments:
@log_with_level("DEBUG")
def compute_tax(amount, rate=0.18):
    return amount * rate

@log_with_level("INFO")
def process_payment(order_id):
    return f"Payment processed for {order_id}"

@log_with_level("WARNING")
def deprecated_function():
    return "old result"

compute_tax(1000, rate=0.18)    # Logs at DEBUG level
process_payment("ORD-001")      # Logs at INFO level
```

---

### 3.8 Real-World Decorator 3 — Authentication Simulator

```python
import functools

# Simulated session store
_current_user = {"id": None, "role": None}

def set_user(user_id, role):
    _current_user["id"]   = user_id
    _current_user["role"] = role

def clear_user():
    _current_user["id"]   = None
    _current_user["role"] = None

# ── Basic authentication decorator ───────────────────────────────────────────
def require_auth(func):
    """Blocks access if no user is logged in."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if _current_user["id"] is None:
            raise PermissionError("Authentication required. Please log in.")
        return func(*args, **kwargs)
    return wrapper

# ── Role-based authorization (parameterized) ─────────────────────────────────
def require_role(*allowed_roles):
    """Blocks access unless user has one of the allowed roles."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if _current_user["id"] is None:
                raise PermissionError("Authentication required.")
            if _current_user["role"] not in allowed_roles:
                raise PermissionError(
                    f"Role '{_current_user['role']}' not authorised. "
                    f"Required: {allowed_roles}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ── Protected endpoints ───────────────────────────────────────────────────────
@require_auth
def get_profile():
    return f"Profile for user {_current_user['id']}"

@require_role("admin", "superuser")
def delete_user(user_id):
    return f"User {user_id} deleted."

@require_role("admin")
def view_all_orders():
    return "All orders: [order1, order2, ...]"

# ── Tests ─────────────────────────────────────────────────────────────────────
# No user logged in
try:
    get_profile()
except PermissionError as e:
    print(f"[BLOCKED] {e}")

# Log in as regular user
set_user(user_id=42, role="user")
print(get_profile())           # ✅ Works — authenticated
try:
    delete_user(99)            # ❌ Role not allowed
except PermissionError as e:
    print(f"[BLOCKED] {e}")

# Log in as admin
set_user(user_id=1, role="admin")
print(delete_user(99))         # ✅ Admin can delete

# Output:
# [BLOCKED] Authentication required. Please log in.
# Profile for user 42
# [BLOCKED] Role 'user' not authorised. Required: ('admin', 'superuser')
# User 99 deleted.
```

---

### 3.9 Real-World Decorator 4 — Retry Logic

```python
import functools
import time
import logging

logger = logging.getLogger(__name__)

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """
    Decorator factory: retries the function on specified exceptions.
    
    Args:
        max_attempts: Total number of attempts (including the first)
        delay:        Seconds to wait between attempts
        exceptions:   Tuple of exception types to retry on
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)      # Try the function
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            "%s failed (attempt %d/%d): %s. Retrying in %.1fs...",
                            func.__name__, attempt, max_attempts, e, delay
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            "%s failed after %d attempts.",
                            func.__name__, max_attempts
                        )
            raise last_exception    # Re-raise the last exception
        return wrapper
    return decorator

# ── Usage ─────────────────────────────────────────────────────────────────────
import random

@retry(max_attempts=4, delay=0.1, exceptions=(ConnectionError, TimeoutError))
def fetch_from_api(url):
    """Simulates an unreliable network call."""
    if random.random() < 0.7:   # 70% chance of failure
        raise ConnectionError(f"Connection refused: {url}")
    return {"data": "success"}

try:
    result = fetch_from_api("https://api.example.com/data")
    print(f"Success: {result}")
except ConnectionError as e:
    print(f"All attempts failed: {e}")
```

---

### 3.10 Real-World Decorator 5 — Memoization / Caching

```python
import functools
import time

# ── Manual memoization decorator ─────────────────────────────────────────────
def memoize(func):
    """Caches function results based on arguments. Simple version."""
    cache = {}    # Lives in the closure — persists across calls
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a hashable key from all arguments
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)    # Compute and cache
        else:
            print(f"  [CACHE HIT] {func.__name__}{args}")
        return cache[key]
    
    wrapper.cache = cache           # Expose cache for inspection/clearing
    wrapper.cache_clear = cache.clear
    return wrapper

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Without memoization, fibonacci(35) would make ~29M recursive calls
start = time.perf_counter()
print(fibonacci(35))    # 9227465 — computed instantly with cache
print(f"Time: {time.perf_counter() - start:.4f}s")

# ── Built-in: functools.lru_cache ────────────────────────────────────────────
@functools.lru_cache(maxsize=128)    # Cache up to 128 unique argument sets
def expensive_calculation(n):
    """Simulates an expensive computation."""
    time.sleep(0.1)    # Simulate work
    return n ** 2

# First call: computed
print(expensive_calculation(10))    # 100 (takes 0.1s)
# Second call: from cache
print(expensive_calculation(10))    # 100 (instant)

# Cache statistics
print(expensive_calculation.cache_info())
# CacheInfo(hits=1, misses=1, maxsize=128, currsize=1)

# ── functools.cache (Python 3.9+) ─────────────────────────────────────────────
@functools.cache    # Unbounded cache — equivalent to lru_cache(maxsize=None)
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

print(factorial(10))   # 3628800
```

---

### 3.11 Stacking Multiple Decorators

```python
import functools

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

def underline(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<u>{func(*args, **kwargs)}</u>"
    return wrapper

# ── Stacking: decorators apply BOTTOM-UP, execute TOP-DOWN ───────────────────
@bold           # Applied 3rd (outermost) — executes 1st
@italic         # Applied 2nd (middle)    — executes 2nd
@underline      # Applied 1st (innermost) — executes 3rd
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
# Output: <b><i><u>Hello, Alice!</u></i></b>

# Equivalent to:
# greet = bold(italic(underline(greet)))
# Execution: bold wrapper → calls italic wrapper → calls underline wrapper → calls greet

# ── With timing and logging stacked ──────────────────────────────────────────
@timing          # Outer: measures total time including logging overhead
@log_calls       # Inner: logs the call
def process_data(data):
    """Processes the data."""
    return [x * 2 for x in data]

result = process_data([1, 2, 3, 4, 5])
# [TIMING] process_data() took 0.0002s
# [LOG] Calling process_data | args=([1,2,3,4,5],) | kwargs={}
```

---

### 3.12 Class-Based Decorators

```python
import functools

class CountCalls:
    """
    A class-based decorator that counts how many times a function is called.
    Uses __call__ to make instances callable.
    """
    
    def __init__(self, func):
        functools.update_wrapper(self, func)   # Like @functools.wraps
        self.func = func
        self.call_count = 0
    
    def __call__(self, *args, **kwargs):
        self.call_count += 1
        print(f"[{self.func.__name__}] Call #{self.call_count}")
        return self.func(*args, **kwargs)
    
    def reset(self):
        self.call_count = 0

@CountCalls    # CountCalls(greet) — creates a CountCalls instance
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))   # [greet] Call #1 → Hello, Alice!
print(greet("Bob"))     # [greet] Call #2 → Hello, Bob!
print(greet("Carol"))   # [greet] Call #3 → Hello, Carol!
print(f"Total calls: {greet.call_count}")   # Total calls: 3
greet.reset()
print(f"After reset: {greet.call_count}")   # After reset: 0
```

---

### 3.13 Decorator Classes (Parameterized)

```python
import functools
import time

class RateLimit:
    """
    Parameterized class-based decorator that limits call frequency.
    Usage: @RateLimit(calls=5, period=60)
    """
    
    def __init__(self, calls, period):
        self.max_calls = calls
        self.period    = period      # seconds
    
    def __call__(self, func):
        """Called when used as @RateLimit(...). Returns the actual decorator."""
        call_times = []              # List of recent call timestamps
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove timestamps older than the rate period
            while call_times and call_times[0] < now - self.period:
                call_times.pop(0)
            
            if len(call_times) >= self.max_calls:
                raise RuntimeError(
                    f"Rate limit exceeded: {self.max_calls} calls "
                    f"per {self.period}s. Try again later."
                )
            
            call_times.append(now)
            return func(*args, **kwargs)
        
        return wrapper

# 3 calls allowed per 10 seconds
@RateLimit(calls=3, period=10)
def send_email(to, subject):
    return f"Email sent to {to}: {subject}"

# Test it
for i in range(5):
    try:
        result = send_email(f"user{i}@example.com", f"Message {i}")
        print(result)
    except RuntimeError as e:
        print(f"[BLOCKED] {e}")

# Output:
# Email sent to user0@example.com: Message 0
# Email sent to user1@example.com: Message 1
# Email sent to user2@example.com: Message 2
# [BLOCKED] Rate limit exceeded: 3 calls per 10s. Try again later.
# [BLOCKED] Rate limit exceeded: 3 calls per 10s. Try again later.
```

---

### 3.14 Method Decorators — `@property`, `@classmethod`, `@staticmethod`

```python
class Temperature:
    """Demonstrates built-in method decorators."""
    
    def __init__(self, celsius):
        self._celsius = celsius     # Private backing attribute
    
    @property                        # Makes method act like an attribute
    def celsius(self):
        return self._celsius
    
    @celsius.setter                  # Setter for the celsius property
    def celsius(self, value):
        if value < -273.15:
            raise ValueError(f"Temperature {value}°C below absolute zero!")
        self._celsius = value
    
    @property                        # Computed property — no setter needed
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32
    
    @classmethod                     # Receives class, not instance
    def from_fahrenheit(cls, f):
        """Alternative constructor — creates Temperature from Fahrenheit."""
        return cls((f - 32) * 5/9)
    
    @staticmethod                    # No access to class or instance
    def is_valid(celsius):
        """Pure utility — doesn't need self or cls."""
        return celsius >= -273.15

t = Temperature(100)
print(t.celsius)           # 100   — property read
print(t.fahrenheit)        # 212.0 — computed property
t.celsius = 25             # property setter — validates
print(t.celsius)           # 25

t2 = Temperature.from_fahrenheit(98.6)   # classmethod
print(f"{t2.celsius:.1f}°C")             # 37.0°C

print(Temperature.is_valid(-300))         # False — staticmethod
```

---

## 4. Common Mistakes & Gotchas

### Mistake 1 — Calling the Function Instead of Passing It

```python
# ❌ WRONG — greet() is called immediately, None is passed to decorator
@shout
def greet():
    return "hello"

# vs accidentally written as:
def greet():
    return "hello"
shout(greet())   # greet() returns "hello", shout("hello") raises TypeError

# ✅ CORRECT — pass the function object, not its return value
shout(greet)     # greet is the function, shout wraps it
```

### Mistake 2 — Forgetting `functools.wraps` (Identity Loss)

```python
# ❌ WRONG — breaks debugging, documentation tools, and frameworks like Flask
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper   # wrapper has no memory of which function it wraps

@my_decorator
def my_view():
    """Serves the homepage."""
    pass

# Flask uses function.__name__ to route URLs — this BREAKS routing:
print(my_view.__name__)    # 'wrapper' ← Flask sees two routes both named 'wrapper'!
print(my_view.__doc__)     # None

# ✅ CORRECT — always use @functools.wraps
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Mistake 3 — Parameterized Decorator Missing a Layer

```python
# ❌ WRONG — forgetting the outer factory layer
def log_level(func, level="INFO"):   # level is the FUNCTION, not the level string!
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# @log_level("DEBUG")  ← This fails! "DEBUG" is passed as func, not as level

# ✅ CORRECT — three layers: factory → decorator → wrapper
def log_level(level="INFO"):         # Layer 1: receives the level string
    def decorator(func):             # Layer 2: receives the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs): # Layer 3: receives call arguments
            print(f"[{level}] calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_level("DEBUG")    # log_level("DEBUG") returns decorator, which wraps greet
def greet():
    pass
```

### Mistake 4 — Decorator Order Confusion

```python
# ❌ COMMON CONFUSION — thinking decorators execute in the order written (top-down)
@decorator_a    # Applied LAST (outermost)
@decorator_b    # Applied FIRST (innermost)
def my_func():
    pass

# Equivalent to: my_func = decorator_a(decorator_b(my_func))
# Execution order: decorator_a's wrapper → decorator_b's wrapper → my_func

# EXAMPLE: order matters for timing + authentication
@timing           # ❌ Times ONLY authentication check — misses function time
@require_auth
def get_data():
    time.sleep(1)

@require_auth     # ✅ Check auth first, then time the actual function
@timing
def get_data():
    time.sleep(1)
```

### Mistake 5 — Mutable Default in Closure (Cache Pollution)

```python
# ❌ WRONG — one shared cache for ALL decorated functions!
_global_cache = {}    # Defined at module level

def bad_memoize(func):
    @functools.wraps(func)
    def wrapper(*args):
        if args not in _global_cache:    # Shared with every decorated function!
            _global_cache[args] = func(*args)
        return _global_cache[args]
    return wrapper

@bad_memoize
def square(n): return n * n

@bad_memoize
def cube(n): return n * n * n

# square(3) and cube(3) both use key (3,) — one overwrites the other!

# ✅ CORRECT — each decorator call creates its OWN cache in the closure
def good_memoize(func):
    cache = {}    # Created fresh for EACH decorated function
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper
```

---

## 5. Hands-on Exercises

### Guided Exercise 1 — Build a Validation Decorator (25 min)

**Goal:** Create a `@validate_types` decorator factory that checks argument types at runtime.

**Step 1:** Basic structure
```python
import functools

def validate_types(**expected_types):
    """
    Decorator factory. Validates argument types match expected types.
    Usage: @validate_types(name=str, age=int, salary=float)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get the function's parameter names
            import inspect
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            # Check each argument's type
            for param_name, expected_type in expected_types.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Argument '{param_name}' expected {expected_type.__name__}, "
                            f"got {type(value).__name__} ({value!r})"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

**Step 2:** Apply to a banking function
```python
@validate_types(account_id=str, amount=float, description=str)
def make_deposit(account_id, amount, description=""):
    return f"Deposited ₹{amount:.2f} to {account_id}: {description}"

# Valid calls
print(make_deposit("ACC001", 500.0, "Salary"))
print(make_deposit("ACC002", 1000.0))

# Invalid calls — should raise TypeError with clear message
try:
    make_deposit(123, 500.0)           # account_id should be str
except TypeError as e:
    print(f"[TYPE ERROR] {e}")

try:
    make_deposit("ACC001", "five hundred")   # amount should be float
except TypeError as e:
    print(f"[TYPE ERROR] {e}")
```

**Step 3:** Stack with timing
```python
@timing
@validate_types(account_id=str, amount=float)
def make_deposit(account_id, amount, description=""):
    time.sleep(0.01)    # Simulate work
    return f"Deposited ₹{amount:.2f} to {account_id}"

make_deposit("ACC001", 250.0, "Test")
# [TYPE VALIDATE] All types valid for make_deposit
# [TIMING] make_deposit() took 0.0103s
```

---

### Guided Exercise 2 — Decorator Stack for a Flask-style Endpoint (30 min)

**Goal:** Simulate how Flask/Django decorate view functions.

```python
import functools
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# ── Decorators ────────────────────────────────────────────────────────────────
def require_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not kwargs.get("user"):
            return {"error": "401 Unauthorized", "message": "Login required."}
        return func(*args, **kwargs)
    return wrapper

def require_role(*roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user", {})
            if user.get("role") not in roles:
                return {"error": "403 Forbidden",
                        "message": f"Role {roles} required."}
            return func(*args, **kwargs)
        return wrapper
    return decorator

def rate_limit(max_per_minute=60):
    def decorator(func):
        calls = []
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [t for t in calls if t > now - 60]
            if len(calls) >= max_per_minute:
                return {"error": "429 Too Many Requests"}
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get("user", {}).get("id", "anonymous")
        logger.info("REQUEST | %s | user=%s", func.__name__, user_id)
        result = func(*args, **kwargs)
        logger.info("RESPONSE | %s | status=%s", func.__name__,
                    "error" if "error" in result else "ok")
        return result
    return wrapper

# ── Endpoint definitions (Django/Flask style) ─────────────────────────────────
@log_request
@rate_limit(max_per_minute=10)
@require_auth
@require_role("admin", "manager")
def get_all_users(user=None):
    """Returns all users — admin/manager only."""
    return {"status": "ok", "users": ["alice", "bob", "carol"]}

@log_request
@require_auth
def get_my_profile(user=None):
    """Returns the calling user's own profile."""
    return {"status": "ok", "profile": user}

# ── Tests ─────────────────────────────────────────────────────────────────────
admin_user  = {"id": 1, "name": "Admin", "role": "admin"}
normal_user = {"id": 2, "name": "Bob",   "role": "user"}

print("\n--- Test 1: Admin accesses all users ---")
print(get_all_users(user=admin_user))

print("\n--- Test 2: Normal user tries to access all users ---")
print(get_all_users(user=normal_user))

print("\n--- Test 3: Unauthenticated access ---")
print(get_all_users())

print("\n--- Test 4: Any authenticated user gets their profile ---")
print(get_my_profile(user=normal_user))
```

---

### Independent Practice 1 — Deprecation Warning Decorator (20 min)

**Task:** Write a `@deprecated(reason, alternative=None)` decorator factory that:
- Prints a `DeprecationWarning` every time the decorated function is called
- Includes the function name, the reason for deprecation, and optionally an alternative function name
- Still calls and returns the result of the original function
- Works with `warnings.warn()` (standard library)

```python
import warnings
import functools

def deprecated(reason, alternative=None):
    """
    Mark a function as deprecated.
    
    Usage:
        @deprecated("Use new_function() instead")
        def old_function(): ...
        
        @deprecated("Renamed", alternative="new_process")
        def process(): ...
    """
    # YOUR CODE HERE
    pass

# Test:
@deprecated("This function is slow. Use fast_compute() instead.",
            alternative="fast_compute")
def slow_compute(n):
    """Computes n squared slowly."""
    return n ** 2

result = slow_compute(10)
print(f"Result: {result}")
# Expected:
# DeprecationWarning: slow_compute is deprecated: This function is slow.
#   Use fast_compute() instead. → Use 'fast_compute' instead.
# Result: 100
```

**Hints:**
- Use `warnings.warn(message, DeprecationWarning, stacklevel=2)` — `stacklevel=2` makes the warning point to the *caller*, not to the decorator
- Build the message string from the `reason` and `alternative` parameters

---

### Independent Practice 2 — Input Sanitizer Decorator (20 min)

**Task:** Write a `@sanitize_strings` decorator that:
- Strips leading/trailing whitespace from all string arguments (positional and keyword)
- Converts them to lowercase if a `lowercase=True` parameter is passed to the decorator
- Does NOT modify non-string arguments

```python
def sanitize_strings(lowercase=False):
    """
    Strip whitespace (and optionally lowercase) all string arguments.
    
    Usage:
        @sanitize_strings()
        def search(query): ...
        
        @sanitize_strings(lowercase=True)
        def find_user(name, email): ...
    """
    # YOUR CODE HERE
    pass

# Tests:
@sanitize_strings(lowercase=True)
def find_user(name, email, active=True):
    return f"Looking for: name={name!r}, email={email!r}, active={active}"

print(find_user("  ALICE  ", "  ALICE@EXAMPLE.COM  "))
# Looking for: name='alice', email='alice@example.com', active=True

print(find_user("  BOB  ", email="  BOB@Example.com  ", active=False))
# Looking for: name='bob', email='bob@example.com', active=False

@sanitize_strings()   # No lowercase
def register(username, password):
    return f"Registering: {username!r} with password {password!r}"

print(register("  Admin  ", "  MyPassword123  "))
# Registering: 'Admin' with password 'MyPassword123'
```

---

### 🏆 Challenge Problem — A Decorator Registry (Stretch Goal)

**Task:** Build a `Registry` class that acts as a decorator factory, allowing functions to register themselves by name and be retrieved and called later.

```python
# Expected behaviour:
registry = Registry()

@registry.register("greet")
def hello(name):
    return f"Hello, {name}!"

@registry.register("farewell")
def goodbye(name):
    return f"Goodbye, {name}!"

# Retrieve and call by name
greet_func = registry.get("greet")
print(greet_func("Alice"))     # Hello, Alice!

# Call directly on registry
print(registry.call("farewell", "Bob"))   # Goodbye, Bob!

# List all registered functions
print(registry.list_all())     # ['greet', 'farewell']

# Raise error for unknown name
registry.get("unknown")        # raises KeyError: "No function registered as 'unknown'"
```

**Bonus:** Make the registry work as a decorator *without* a name — using the function's own `__name__` as the key.

---

## 6. Best Practices & Industry Standards

### Decorator Design Rules

1. **Always use `@functools.wraps(func)`** inside every decorator wrapper — without exception. It preserves `__name__`, `__doc__`, `__module__`, `__qualname__`, `__annotations__`, and `__wrapped__` (which lets you access the original function via `func.__wrapped__`).

2. **Use `*args, **kwargs` in wrappers** — never hard-code the expected arguments. This makes decorators universally applicable.

3. **Never swallow exceptions silently.** If your decorator catches an exception (e.g., for logging), always re-raise it unless your decorator's entire purpose is exception handling (like a retry decorator).

4. **Make decorators stackable.** Design each decorator to do exactly one thing — logging, timing, auth, caching. Stack them when you need multiple behaviours.

5. **Prefer decorator factories (parameterized decorators) over hard-coded behaviours.** `@retry(max_attempts=3)` is far more reusable than a `@retry` that always tries exactly 3 times.

6. **Access the unwrapped function with `func.__wrapped__`** for testing:
   ```python
   @timing
   @log_calls
   def my_func(): pass
   
   # In tests, bypass decorators:
   original = my_func.__wrapped__.__wrapped__
   ```

7. **Consider class-based decorators when you need state** (call counters, rate limiters, caches) — they're cleaner than closures with `nonlocal`.

8. **Use `functools.lru_cache` / `functools.cache`** for memoization — don't reinvent them.

### PEP 8 / Naming Conventions
- Decorator functions: use verbs or adjectives — `log_calls`, `require_auth`, `cached`, `timing`
- Wrapper functions inside decorators: always name them `wrapper` for consistency and readability
- Decorator factories: noun or adjective describing the behaviour — `retry`, `rate_limit`, `validate_types`

---

## 7. Real-World Application

### Where Are Decorators Used?

| Framework / Library | Decorator | Purpose |
|---|---|---|
| **Flask** | `@app.route("/")` | Register URL → function mapping |
| **Flask-Login** | `@login_required` | Redirect to login if not authenticated |
| **Django** | `@login_required` | Same — block unauthenticated access |
| **Django** | `@cache_page(60 * 15)` | Cache view response for 15 minutes |
| **Django REST** | `@api_view(["GET"])` | Mark function as a REST API view |
| **Celery** | `@app.task` | Register function as an async task |
| **pytest** | `@pytest.mark.parametrize` | Run test with multiple input sets |
| **dataclasses** | `@dataclass` | Auto-generate `__init__`, `__repr__` etc. |
| **click** | `@click.command()` | Register CLI command |

### Mini Project — Flask-Style Router Simulator

```python
import functools
from typing import Callable

class FlaskLikeApp:
    """Simulates Flask's routing and request lifecycle decorators."""
    
    def __init__(self, name):
        self.name = name
        self._routes: dict[str, Callable] = {}
        self._before_request_funcs: list[Callable] = []
        self._after_request_funcs: list[Callable] = []
    
    def route(self, path, methods=("GET",)):
        """Decorator that registers a function as a route handler."""
        def decorator(func):
            for method in methods:
                key = f"{method.upper()}:{path}"
                self._routes[key] = func
                print(f"[ROUTER] Registered {method} {path} → {func.__name__}")
            return func    # Return original — Flask doesn't wrap view functions
        return decorator
    
    def before_request(self, func):
        """Decorator that registers a function to run before every request."""
        self._before_request_funcs.append(func)
        return func
    
    def after_request(self, func):
        """Decorator that registers a function to run after every response."""
        self._after_request_funcs.append(func)
        return func
    
    def dispatch(self, method, path, **kwargs):
        """Simulate handling an HTTP request."""
        # Run before-request hooks
        for hook in self._before_request_funcs:
            hook()
        
        key = f"{method.upper()}:{path}"
        handler = self._routes.get(key)
        if not handler:
            response = {"status": 404, "body": "Not Found"}
        else:
            response = {"status": 200, "body": handler(**kwargs)}
        
        # Run after-request hooks
        for hook in self._after_request_funcs:
            hook(response)
        
        return response

# ── Using the app ─────────────────────────────────────────────────────────────
app = FlaskLikeApp("MyApp")

@app.before_request
def log_incoming():
    print("[MIDDLEWARE] Incoming request...")

@app.after_request
def add_headers(response):
    response["X-Powered-By"] = "MyApp"
    print(f"[MIDDLEWARE] Response status: {response['status']}")

@app.route("/")
def index():
    return "Welcome to MyApp!"

@app.route("/users", methods=["GET", "POST"])
def users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

# Dispatch requests
print(app.dispatch("GET", "/"))
print(app.dispatch("GET", "/users"))
print(app.dispatch("DELETE", "/users"))   # 404
```

### Connection to Upcoming Days
- **Day 12 (File I/O / Context Managers):** `contextlib.contextmanager` is itself a decorator
- **Day 13 (Comprehensions):** `@dataclass` auto-generates methods using decorator magic
- **Day 14–16 (Flask):** Every route, middleware, error handler uses `@` syntax you now understand deeply
- **Day 17–20 (Django):** `@login_required`, `@cache_page`, `@permission_required` — all decorator factories

---

## 8. Quick Revision Summary

### Key Terms

| Term | Definition |
|---|---|
| **First-class function** | A function that can be assigned, passed, and returned like any value |
| **Closure** | An inner function that remembers variables from its enclosing scope |
| **Decorator** | A function that takes a function and returns an enhanced version |
| **Wrapper** | The inner function inside a decorator that calls the original |
| **`@` syntax** | Shorthand for `func = decorator(func)` |
| **`functools.wraps`** | Decorator that copies metadata from wrapped function to wrapper |
| **Decorator factory** | A function that takes arguments and returns a decorator |
| **Parameterized decorator** | A decorator that itself accepts arguments via a factory |
| **`lru_cache`** | Built-in memoization decorator with a maximum cache size |
| **`nonlocal`** | Keyword to modify a variable in an enclosing (but not global) scope |
| **Stacking** | Applying multiple decorators to one function |
| **Class-based decorator** | A class with `__call__` used as a decorator |

### Core Syntax Cheat Sheet

```python
# Basic decorator
def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

@my_decorator
def my_function(): pass

# Parameterized decorator (factory)
def my_decorator(param1, param2="default"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use param1, param2 here
            return func(*args, **kwargs)
        return wrapper
    return decorator

@my_decorator(param1="value", param2="other")
def my_function(): pass

# Class-based decorator
class MyDecorator:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

# Built-in caching
@functools.lru_cache(maxsize=128)
def expensive(n): ...

@functools.cache    # Python 3.9+
def expensive(n): ...

# Stacking (bottom-up application, top-down execution)
@outer    # applied 2nd, runs 1st
@inner    # applied 1st, runs 2nd
def func(): pass
# Equivalent to: func = outer(inner(func))
```

### 5 MCQ Recap Questions

**Q1.** What does `@decorator` syntax above a function definition do?
- A) Calls the function immediately with the decorator as argument
- B) Replaces the function with the decorator itself
- **C) Applies the decorator: equivalent to `func = decorator(func)` ✅**
- D) Creates a copy of the function with decorator metadata

**Q2.** Why is `@functools.wraps(func)` important inside a decorator?
- A) It makes the decorator faster
- B) It allows the decorator to call the original function
- **C) It preserves the original function's `__name__`, `__doc__`, and other metadata ✅**
- D) It prevents infinite recursion

**Q3.** Given: `@A` / `@B` / `@C` / `def f(): pass` — which statement is correct?
- A) `f = A(B(C(f)))` and execution order is C→B→A
- **B) `f = A(B(C(f)))` and execution order is A→B→C ✅**
- C) `f = C(B(A(f)))` and execution order is A→B→C
- D) `f = C(B(A(f)))` and execution order is C→B→A

**Q4.** How many layers of nesting does a parameterized decorator like `@retry(max_attempts=3)` require?
- A) One — just the wrapper function
- B) Two — decorator + wrapper
- **C) Three — factory + decorator + wrapper ✅**
- D) Four — always needs an extra validation layer

**Q5.** What is the difference between `@functools.lru_cache(maxsize=128)` and `@functools.cache`?
- A) `lru_cache` is faster than `cache`
- **B) `lru_cache` has a bounded cache size; `cache` is unbounded ✅**
- C) `cache` requires Python 2 compatibility
- D) There is no difference — they are aliases

---

## 9. Instructor Notes

### Common Student Questions to Anticipate

| Question | Answer |
|---|---|
| "Why not just modify the function directly instead of wrapping it?" | Decorators follow the Open/Closed Principle — functions are open for extension, closed for modification. You don't want to modify every function to add timing. |
| "When do I use a class decorator vs a function decorator?" | Use class decorators when you need to maintain state (call count, rate limit cache) or expose additional methods on the decorated function. |
| "Does the decorator run every time the function is called?" | The decorator *factory* runs once (at definition time). The *wrapper* runs on every call. |
| "Can I remove a decorator once it's applied?" | Not directly — but you can access the original via `func.__wrapped__` (if using `functools.wraps`). For testing, import the original before decoration. |
| "What's `nonlocal` for?" | It allows a nested function to *modify* (not just read) a variable from the enclosing scope. Without it, you'd get `UnboundLocalError`. |
| "Why does Flask use `@app.route('/')` without parentheses sometimes?" | `@app.route('/')` always has parentheses — it's always a factory. The parentheses-free form (`@decorator`) is a different (simpler) pattern. |
| "Can I apply `@lru_cache` to a method?" | Not directly — `self` is not hashable. Use `@lru_cache` on a module-level function, or `@functools.cached_property` for instance-level caching. |


### Resources & Further Reading
- 📖 [Python Docs — functools](https://docs.python.org/3/library/functools.html)
- 📖 [PEP 318 — Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- 📖 [Real Python — Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)
- 📖 [Real Python — Python's functools Module](https://realpython.com/python-functools-module/)
- 📺 [Corey Schafer — Python Decorators](https://www.youtube.com/watch?v=FsAPt_9Bf3U)
- 📖 [Flask Docs — View Decorators](https://flask.palletsprojects.com/en/latest/views/)
- 📖 [Django Docs — View Decorators](https://docs.djangoproject.com/en/stable/topics/http/decorators/)
