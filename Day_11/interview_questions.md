# Day 11 — Interview Questions: Python Decorators
### Python Full Stack Bootcamp | Interview Prep Reference

---

> 💡 **How to use this file:** Read each question, formulate your answer mentally, then compare with the model answer. For senior-level questions, practice writing the code live before reading the solution.

---

## 🟢 Beginner Level (0–1 Year Experience)

---

**Q1. What is a decorator in Python? Explain it in simple terms.**

**Model Answer:**
A decorator is a function that takes another function as input, adds some extra behaviour to it, and returns the modified function. It's a clean, reusable way to extend functionality without changing the original function's code.

The `@decorator_name` syntax placed above a function definition is shorthand for `function = decorator_name(function)`.

```python
import functools

def shout(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

@shout
def greet(name):
    return f"hello, {name}"

print(greet("alice"))   # HELLO, ALICE
# Same as: greet = shout(greet)
```

---

**Q2. What are first-class functions? Why do they matter for decorators?**

**Model Answer:**
A "first-class" function means the language treats functions as values — just like integers or strings. You can:
- Assign a function to a variable: `f = my_func`
- Pass a function as an argument: `apply(my_func, data)`
- Return a function from a function: `return inner_func`
- Store functions in a list or dict

Decorators **require** first-class functions because a decorator:
1. **Receives** the original function as an argument
2. **Creates** a new wrapper function (a function inside a function)
3. **Returns** the wrapper function

Without first-class functions, none of these operations would be possible.

---

**Q3. What is a closure? Give a simple example.**

**Model Answer:**
A closure is an inner function that *remembers* (captures) variables from its enclosing function's scope, even after the outer function has finished executing.

```python
def make_adder(x):
    def add(y):
        return x + y      # 'x' is captured from the enclosing scope
    return add

add_5 = make_adder(5)     # make_adder finishes, but 'x=5' lives in closure
print(add_5(10))          # 15  — add still knows x=5
print(add_5(3))           # 8

# Closures are what make decorators "remember" the original function
```

---

**Q4. What does `functools.wraps` do and why is it important?**

**Model Answer:**
`functools.wraps(func)` is itself a decorator applied to the wrapper function. It copies key attributes from the original function to the wrapper:
- `__name__` — function name
- `__doc__` — docstring
- `__module__` — module where defined
- `__qualname__` — qualified name
- `__annotations__` — type hints
- `__wrapped__` — reference to the original function

Without it, the wrapper masquerades as a different function, which breaks debugging, documentation tools (`help()`), and frameworks like Flask that use `__name__` to register routes (causing "duplicate endpoint" errors).

```python
import functools

# Without functools.wraps:
def bad_dec(func):
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    return wrapper

@bad_dec
def greet(): """Says hello."""
print(greet.__name__)  # 'wrapper'  ← Wrong!
print(greet.__doc__)   # None       ← Lost!

# With functools.wraps:
def good_dec(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs): return func(*args, **kwargs)
    return wrapper

@good_dec
def greet(): """Says hello."""
print(greet.__name__)  # 'greet'      ✅
print(greet.__doc__)   # 'Says hello.' ✅
```

---

**Q5. Explain the order of decorator application when multiple decorators are stacked.**

**Model Answer:**
Decorators are applied **bottom-up** (innermost first) but execute **top-down** (outermost first).

```python
@A   # Applied 3rd (outermost) — its wrapper runs first on each call
@B   # Applied 2nd (middle)
@C   # Applied 1st (innermost, closest to the function)
def f():
    pass

# Equivalent to:
f = A(B(C(f)))

# Call sequence when f() is called:
# A's wrapper → B's wrapper → C's wrapper → original f
```

Practical implication: put authentication *before* rate limiting so unauthenticated users don't consume rate-limit quota.

---

**Q6. What is `*args` and `**kwargs` in a wrapper function? Why must you include them?**

**Model Answer:**
`*args` captures any number of positional arguments as a tuple; `**kwargs` captures any number of keyword arguments as a dict. In a wrapper function, they are essential because:

1. **The decorator doesn't know** what arguments the wrapped function expects at decoration time
2. Without them, the wrapper would only work for functions with a specific, hard-coded signature
3. They allow the decorator to be applied universally to *any* function

```python
def universal_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):   # Catch everything
        return func(*args, **kwargs)   # Pass everything through
    return wrapper

@universal_decorator
def add(a, b): return a + b           # 2 positional args

@universal_decorator
def greet(name, greeting="Hello"):    # 1 positional, 1 keyword
    return f"{greeting}, {name}!"

# Both work — wrapper is transparent
print(add(3, 4))              # 7
print(greet("Alice"))         # Hello, Alice!
print(greet("Bob", greeting="Hi"))   # Hi, Bob!
```

---

**Q7. What is the difference between `@lru_cache` and a manually written memoize decorator?**

**Model Answer:**

| Feature | Manual `memoize` | `@lru_cache` |
|---|---|---|
| Cache size | Unlimited (unbounded dict) | Configurable `maxsize` |
| Eviction policy | None | LRU (Least Recently Used) |
| Cache statistics | Must implement yourself | Built-in `.cache_info()` |
| Cache clearing | Must implement yourself | Built-in `.cache_clear()` |
| Implementation | Pure Python | C extension (faster) |
| Thread safety | Not guaranteed | Thread-safe |

`@lru_cache(maxsize=128)` is the production-grade choice. Use a manual memoize decorator only for learning or when you need custom caching logic.

---

## 🟡 Intermediate Level (1–2 Years Experience)

---

**Q8. How do you write a parameterized decorator? Walk through the three layers.**

**Model Answer:**
A parameterized decorator requires three layers:

1. **Decorator factory** — accepts the decorator's own arguments, returns a decorator
2. **Decorator** — accepts the function to wrap, returns a wrapper
3. **Wrapper** — accepts the function's call arguments, calls the original

```python
import functools
import time

# Layer 1: FACTORY — accepts decorator arguments
def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    
    # Layer 2: DECORATOR — accepts the function
    def decorator(func):
        
        # Layer 3: WRAPPER — accepts the function's arguments
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exc
        
        return wrapper       # factory returns decorator
    return decorator         # decorator returns wrapper

# Usage — factory is called with arguments:
@retry(max_attempts=4, delay=0.5, exceptions=(ConnectionError,))
def fetch(url):
    ...
# Same as: fetch = retry(max_attempts=4, delay=0.5, exceptions=(ConnectionError,))(fetch)
```

---

**Q9. What is a class-based decorator? When would you prefer it over a function decorator?**

**Model Answer:**
A class-based decorator uses a class with `__init__` (to receive the function) and `__call__` (to act as the wrapper). 

Prefer class-based decorators when:
1. **You need persistent state** — a class instance naturally holds state (`self.call_count`, `self.cache`, `self.call_times`)
2. **You need to expose methods** on the decorated function (`greet.reset()`, `greet.cache_clear()`)
3. **The decorator logic is complex** — a class is more readable than deeply nested closures

```python
import functools

class Throttle:
    """Rate-limit decorator: limits calls per time window."""
    
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.call_times = []
        self.blocked_count = 0
    
    def __call__(self, *args, **kwargs):
        import time
        now = time.time()
        self.call_times = [t for t in self.call_times if t > now - 60]
        if len(self.call_times) >= 5:
            self.blocked_count += 1
            raise RuntimeError("Rate limit: 5 calls/min")
        self.call_times.append(now)
        return self.func(*args, **kwargs)
    
    def stats(self):
        return {"blocked": self.blocked_count, "window_calls": len(self.call_times)}

@Throttle
def send_notification(msg):
    print(f"Notif: {msg}")

send_notification("hello")
print(send_notification.stats())   # {'blocked': 0, 'window_calls': 1}
```

---

**Q10. How would you write a decorator that can optionally take arguments — i.e., works both as `@decorator` and `@decorator(arg=val)`?**

**Model Answer:**
This is called an "optional-argument decorator" — one of the trickier patterns. The key is checking whether the first argument is a callable (the function) or not.

```python
import functools

def maybe_parameterized(func=None, *, prefix="[LOG]"):
    """
    Works as:
      @maybe_parameterized               — no arguments
      @maybe_parameterized(prefix=">>") — with arguments
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            print(f"{prefix} Calling {fn.__name__}")
            return fn(*args, **kwargs)
        return wrapper
    
    if func is not None:
        # Called as @maybe_parameterized (no parentheses) — func is the decorated function
        return decorator(func)
    else:
        # Called as @maybe_parameterized(prefix=">>") — return the decorator
        return decorator

@maybe_parameterized
def func_a(): return "a"

@maybe_parameterized(prefix=">>>")
def func_b(): return "b"

func_a()   # [LOG] Calling func_a
func_b()   # >>> Calling func_b
```

---

**Q11. How does `@property` work as a decorator? What problem does it solve?**

**Model Answer:**
`@property` converts a method into a "managed attribute" — it's accessed like an attribute (no `()`) but calls the underlying method. It solves the problem of providing getter/setter validation without changing the public API.

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance    # Private — managed by property
    
    @property
    def balance(self):
        """Getter — called when you READ account.balance"""
        return self._balance
    
    @balance.setter
    def balance(self, value):
        """Setter — called when you WRITE account.balance = x"""
        if value < 0:
            raise ValueError(f"Balance cannot be negative: {value}")
        self._balance = value
    
    @balance.deleter
    def balance(self):
        """Deleter — called when you DEL account.balance"""
        del self._balance

acc = BankAccount(1000)
print(acc.balance)      # 1000  — calls getter, no ()
acc.balance = 500       # calls setter — validates
acc.balance = -100      # raises ValueError
```

---

**Q12. What is `functools.cached_property`? How does it differ from `@property`?**

**Model Answer:**
`@functools.cached_property` computes the property value on first access and then stores it as an instance attribute, bypassing the descriptor on subsequent accesses. It's a read-only property that caches its result.

```python
import functools
import time

class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    @property
    def stats(self):
        """Recomputed EVERY time stats is accessed."""
        time.sleep(0.5)   # Simulate expensive computation
        return {"mean": sum(self.data) / len(self.data), "count": len(self.data)}
    
    @functools.cached_property
    def cached_stats(self):
        """Computed ONCE, then stored directly on the instance."""
        time.sleep(0.5)
        return {"mean": sum(self.data) / len(self.data), "count": len(self.data)}

p = DataProcessor([1, 2, 3, 4, 5])
p.stats          # 0.5s — computed
p.stats          # 0.5s — computed again (not cached!)
p.cached_stats   # 0.5s — computed once
p.cached_stats   # instant — reads from p.__dict__["cached_stats"]
```

Key difference: `@property` uses Python's descriptor protocol every access; `@cached_property` stores the result directly in the instance's `__dict__`, which shadows the class-level descriptor on subsequent accesses.

---

**Q13. What is the `__wrapped__` attribute? How do you use it in testing?**

**Model Answer:**
When `@functools.wraps(func)` is applied, it sets `wrapper.__wrapped__ = func`. This creates a chain — if multiple decorators are stacked, each wrapper's `__wrapped__` points to the next layer.

In testing, this allows you to bypass decorators and test the original function in isolation:

```python
import functools
import time

def timing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"[TIMING] {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

@timing
def add(a, b):
    return a + b

# Normal call — triggers timing side effect
add(3, 4)   # [TIMING] 0.0001s

# In tests — bypass the decorator
original_add = add.__wrapped__
result = original_add(3, 4)   # No timing output
assert result == 7   # Test the pure logic
```

For multiple stacked decorators:
```python
@timing       # __wrapped__ → logging wrapper
@log_calls    # __wrapped__ → original function
def my_func(): pass

original = my_func.__wrapped__.__wrapped__   # Unwrap all layers
```

---

## 🔴 Advanced Level (2+ Years / Senior Roles)

---

**Q14. Design a `@circuit_breaker` decorator. Explain the Circuit Breaker pattern and implement it.**

**Model Answer:**
The Circuit Breaker pattern prevents cascading failures in distributed systems. Like a household fuse, it "trips" (opens) after a threshold of failures and temporarily blocks all calls, giving the downstream service time to recover.

States:
- **Closed** — normal operation, calls go through
- **Open** — failures exceeded threshold, calls blocked immediately
- **Half-Open** — after cooldown, one test call is allowed; if it succeeds, closes; if it fails, opens again

```python
import functools
import time

class CircuitBreaker:
    def __init__(self, func, failure_threshold=5, recovery_timeout=60):
        functools.update_wrapper(self, func)
        self.func = func
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        
        self._failure_count = 0
        self._last_failure_time = None
        self._state = "closed"   # closed, open, half-open
    
    def __call__(self, *args, **kwargs):
        if self._state == "open":
            if time.time() - self._last_failure_time > self.recovery_timeout:
                self._state = "half-open"
                print(f"[CB] {self.func.__name__}: half-open, testing...")
            else:
                raise RuntimeError(
                    f"[CB] {self.func.__name__}: circuit OPEN "
                    f"(recovering for {self.recovery_timeout}s)"
                )
        
        try:
            result = self.func(*args, **kwargs)
            if self._state == "half-open":
                self._reset()
                print(f"[CB] {self.func.__name__}: recovered, circuit CLOSED")
            return result
        except Exception as e:
            self._record_failure()
            raise
    
    def _record_failure(self):
        self._failure_count += 1
        self._last_failure_time = time.time()
        if self._failure_count >= self.failure_threshold:
            self._state = "open"
            print(f"[CB] {self.func.__name__}: OPEN after {self._failure_count} failures")
    
    def _reset(self):
        self._failure_count = 0
        self._last_failure_time = None
        self._state = "closed"
    
    @property
    def state(self):
        return self._state

def circuit_breaker(failure_threshold=5, recovery_timeout=60):
    """Decorator factory for the circuit breaker pattern."""
    def decorator(func):
        return CircuitBreaker(func, failure_threshold, recovery_timeout)
    return decorator

@circuit_breaker(failure_threshold=3, recovery_timeout=5)
def call_payment_service(amount):
    import random
    if random.random() < 0.8:   # 80% failure rate
        raise ConnectionError("Payment service unavailable")
    return f"Payment of ₹{amount} processed"
```

---

**Q15. How would you implement a `@singleton` decorator that ensures only one instance of a class is ever created?**

**Model Answer:**
```python
import functools
import threading

def singleton(cls):
    """
    Decorator that ensures a class has at most one instance.
    Thread-safe using a lock.
    """
    instances = {}
    lock = threading.Lock()
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:          # Double-checked locking for thread safety
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    # Expose a way to reset (useful in tests)
    get_instance.reset = lambda: instances.pop(cls, None)
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self, host="localhost", port=5432):
        self.host = host
        self.port = port
        print(f"Creating DB connection to {host}:{port}")
    
    def execute(self, query):
        return f"Executing on {self.host}: {query}"

# Multiple calls return the same instance
db1 = DatabaseConnection()           # Creating DB connection to localhost:5432
db2 = DatabaseConnection()           # No output — same instance returned
db3 = DatabaseConnection(host="prod-server")   # Still same instance!

print(db1 is db2)   # True
print(db1 is db3)   # True
print(db1.host)     # localhost — first args used

# In tests, reset the singleton
DatabaseConnection.reset()
db_fresh = DatabaseConnection(host="test-db")   # New instance created
```

---

**Q16. Explain the difference between a decorator, a context manager, and a mixin. When would you choose each?**

**Model Answer:**

| Pattern | Applied At | Scope | Best For |
|---|---|---|---|
| **Decorator** | Function/class definition | Function call | Cross-cutting concerns applied per-function: auth, logging, timing, caching |
| **Context Manager** | Runtime, `with` block | Code block | Resource lifecycle: open/close, lock/unlock, transaction begin/commit |
| **Mixin** | Class definition | All methods of a class | Shared behaviour across class hierarchies: serialization, validation, event emission |

```python
# DECORATOR — applied to a specific function, per-call concern
@require_auth
def get_profile(user_id): ...

# CONTEXT MANAGER — wraps a block, resource acquisition/release
with database.transaction():
    update_balance(user_id, amount)
    record_transaction(user_id, amount)
    # Rolls back automatically if exception occurs

# MIXIN — adds methods to a class, structural concern
class TimestampMixin:
    def touch(self): self.updated_at = datetime.now()

class Post(TimestampMixin, Base):
    ...
```

Choose decorators for **per-function** cross-cutting concerns. Choose context managers for **resource cleanup** that must happen regardless of exceptions. Choose mixins for **shared class behaviour** without deep inheritance.

---

**Q17. In a Django or Flask project, what problems can arise from incorrect decorator usage, and how do you avoid them?**

**Model Answer:**

**Problem 1 — Missing `functools.wraps` in Flask → Duplicate endpoint error:**
```python
# ❌ Both routes get named 'wrapper' — Flask raises AssertionError
@app.route("/users")
@require_auth         # No functools.wraps inside → __name__ = 'wrapper'
def get_users(): ...

@app.route("/posts")
@require_auth         # Same! Second 'wrapper' endpoint
def get_posts(): ...
# AssertionError: View function mapping is overwriting an existing endpoint function: wrapper

# ✅ Fix: Always use functools.wraps in your decorators
```

**Problem 2 — Decorator applied to class method, `self` swallowed:**
```python
# ❌ Wrong — 'self' gets captured as first positional arg, breaks method
class View:
    @log_calls   # log_calls doesn't know about 'self'
    def get(self, request): ...

# ✅ Fix: ensure wrapper passes through *args, **kwargs — which includes self
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):   # args[0] will be 'self' for methods
        return func(*args, **kwargs)
    return wrapper
```

**Problem 3 — `@lru_cache` on a method leaks memory:**
```python
# ❌ 'self' is part of the cache key — each instance is cached separately
# Cache holds references to 'self', preventing garbage collection
class Service:
    @functools.lru_cache(maxsize=128)   # Memory leak!
    def expensive(self, n): ...

# ✅ Fix: use @functools.cached_property for per-instance caching, or
# extract the pure computation to a module-level cached function
@functools.lru_cache(maxsize=128)
def _compute(n): return n ** 2

class Service:
    def expensive(self, n): return _compute(n)
```

---

## 🎯 Rapid-Fire Questions

**Q. What does `@staticmethod` do?** → Converts a method into a static function — it receives no implicit first argument (`self` or `cls`). It's just a regular function namespaced inside the class.

**Q. What does `@classmethod` do?** → Makes the method receive the class (`cls`) as the first argument instead of the instance (`self`). Used for alternative constructors and factory methods.

**Q. Can a decorator be applied to a class?** → Yes. `@dataclass`, `@singleton`, `@register` are class decorators. The decorator receives the class object and returns a modified or replacement class.

**Q. What is `functools.update_wrapper`?** → The function that `@functools.wraps` calls internally. Used directly in class-based decorators where you can't use the `@functools.wraps` syntax: `functools.update_wrapper(self, func)`.

**Q. Can you decorate a generator function?** → Yes, but the wrapper must also return a generator (or use `yield from`), otherwise the generator protocol breaks.

**Q. What is `@functools.singledispatch`?** → Creates a function that dispatches to different implementations based on the type of the first argument — a form of function overloading.

**Q. What happens if you decorate `__init__`?** → It works, but be careful — `__init__` must always return `None`, and the wrapper must not return the result of `func(*args, **kwargs)` if that's non-None.

**Q. What is `functools.partial`?** → Creates a new function with some arguments pre-filled. Not a decorator, but related: `double = functools.partial(multiply, factor=2)`.

---

## 📝 Coding Interview Questions

**CI-1.** Write a `@timer` decorator that measures execution time and raises a `TimeoutError` if the function takes longer than N seconds.
```python
@timer(max_seconds=2)
def slow_operation():
    time.sleep(3)
# Should raise TimeoutError after 2 seconds
```

**CI-2.** Implement a `@once` decorator that ensures a function runs at most once — all subsequent calls return the cached result from the first call.

**CI-3.** Write a `@trace` decorator that prints the function name, arguments, and return value in an indented format that shows nested calls:
```
→ factorial(5)
  → factorial(4)
    → factorial(3)
    ← factorial(3) = 6
  ← factorial(4) = 24
← factorial(5) = 120
```

**CI-4.** Create a `@validate_output(schema)` decorator that validates a function's return value against a simple schema dict:
```python
@validate_output({"name": str, "age": int, "active": bool})
def get_user(user_id):
    return {"name": "Alice", "age": 30, "active": True}
```

**CI-5.** Design and implement a `@observable` decorator that notifies registered observers whenever the decorated function is called. Observers should receive the function name, arguments, and return value.

**CI-6.** What is wrong with this code? Fix it:
```python
def memoize(func):
    cache = {}
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper

@memoize
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n - 1)   # Bug: calls original factorial, not memoized!

# Answer: Inside the function body, 'factorial' refers to the memoized version
# (after decoration), so the recursive call IS to the memoized version.
# The real bug: wrapper doesn't handle kwargs and doesn't have functools.wraps.
```
