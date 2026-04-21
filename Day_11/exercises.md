# Day 11 — Exercises: Python Decorators
### Python Full Stack Bootcamp | Hands-on Practice

---

> 📋 **Instructions:**
> - Work through exercises in order — each builds on previous concepts
> - Write your solution *before* reading hints
> - Test every code block and verify the expected output
> - Save each exercise as a separate `.py` file

---

## Exercise 1 — Warm-Up: First-Class Functions & Closures (15 min)

**File:** `ex01_foundations.py`

**Goal:** Build the mental model for decorators before writing any decorator syntax.

### Part A — Spot the Difference

```python
def greet(name):
    return f"Hello, {name}!"

# What does each of these lines do? Answer in comments.
a = greet           # a is: ___________________
b = greet("Alice")  # b is: ___________________
c = greet           # Is c the same object as greet? ___

print(a("Bob"))     # Output: ___
print(b)            # Output: ___
print(a is greet)   # Output: ___
```

---

### Part B — Build a Closure

```python
"""
Complete this closure factory.
make_greeting(greeting) should return a function that prepends
the given greeting to any name.
"""

def make_greeting(greeting):
    # YOUR CODE HERE — define an inner function that uses 'greeting'
    pass

hello = make_greeting("Hello")
hi    = make_greeting("Hi there")
namaste = make_greeting("Namaste")

print(hello("Alice"))    # Hello, Alice!
print(hi("Bob"))         # Hi there, Bob!
print(namaste("Carol"))  # Namaste, Carol!

# Both functions remember their own greeting independently
print(hello("Dave"))     # Hello, Dave!   — not affected by hi
```

---

### Part C — The Wrapper Pattern (No @ yet)

```python
"""
Write a decorator function called 'loud' that:
1. Takes a function as argument
2. Defines a wrapper function
3. The wrapper calls the original function and returns its result IN UPPERCASE
4. Returns the wrapper

Do NOT use @ syntax yet — apply it manually.
"""

def loud(func):
    # YOUR CODE HERE
    pass

def whisper(name):
    return f"hello, {name}"

# Apply manually
loud_whisper = loud(whisper)

print(loud_whisper("alice"))    # HELLO, ALICE
print(loud_whisper("bob"))      # HELLO, BOB

# The original should be unchanged
print(whisper("carol"))         # hello, carol
```

---

### Part D — Rewrite Part C Using @ Syntax

```python
# Rewrite Part C using the @ decorator syntax
# The behaviour should be identical

def loud(func):
    # YOUR CODE HERE (same as Part C)
    pass

@loud
def whisper(name):
    return f"hello, {name}"

print(whisper("alice"))   # HELLO, ALICE
print(whisper("bob"))     # HELLO, BOB
```

---

## Exercise 2 — Basic Decorators with functools.wraps (25 min)

**File:** `ex02_basic_decorators.py`

```python
import functools
import time
```

### 2.1 — Timing Decorator

```python
def timing(func):
    """
    Decorator that prints how long the function took to run.
    
    Requirements:
    - Use time.perf_counter() for precision
    - Print: "[TIMING] function_name() took X.XXXXs"
    - Must use @functools.wraps
    - Must return the function's original return value
    """
    # YOUR CODE HERE
    pass

# Tests:
@timing
def slow_operation():
    time.sleep(0.5)
    return "done"

@timing
def fast_sum(n):
    return sum(range(n))

result = slow_operation()
print(f"Result: {result}")
# [TIMING] slow_operation() took 0.5001s
# Result: done

result = fast_sum(1_000_000)
print(f"Sum: {result}")
# [TIMING] fast_sum() took 0.0XXXs
# Sum: 499999500000

# Verify metadata preserved:
print(slow_operation.__name__)   # slow_operation (NOT 'wrapper')
print(fast_sum.__name__)         # fast_sum
```

---

### 2.2 — Call Counter Decorator

```python
def count_calls(func):
    """
    Decorator that counts how many times the function has been called.
    
    Requirements:
    - Track call count in the closure
    - After each call, print: "[COUNTER] function_name has been called N time(s)"
    - Expose the counter via func.call_count attribute on the wrapper
    - Expose a reset via func.reset_count() on the wrapper
    - Must use @functools.wraps
    """
    # YOUR CODE HERE
    pass

@count_calls
def send_email(to, subject):
    return f"Sent to {to}: {subject}"

send_email("alice@example.com", "Welcome!")
# [COUNTER] send_email has been called 1 time(s)
send_email("bob@example.com", "Newsletter")
# [COUNTER] send_email has been called 2 time(s)
send_email("carol@example.com", "Invoice")
# [COUNTER] send_email has been called 3 time(s)

print(f"Total emails: {send_email.call_count}")   # Total emails: 3
send_email.reset_count()
print(f"After reset: {send_email.call_count}")    # After reset: 0
send_email("dave@example.com", "Reminder")
# [COUNTER] send_email has been called 1 time(s)
```

---

### 2.3 — Exception Logger Decorator

```python
def log_exceptions(func):
    """
    Decorator that logs any exception raised by the function.
    
    Requirements:
    - Use Python's logging module at ERROR level
    - Log: "Exception in function_name(): ExceptionType: message"
    - Include the full traceback (exc_info=True)
    - Always RE-RAISE the exception after logging
    - Must use @functools.wraps
    """
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.ERROR,
                        format="%(levelname)s | %(message)s")
    # YOUR CODE HERE
    pass

@log_exceptions
def divide(a, b):
    return a / b

@log_exceptions
def get_item(lst, index):
    return lst[index]

# Test 1: Normal call — no logging
print(divide(10, 2))    # 5.0

# Test 2: Exception — should log then re-raise
try:
    divide(10, 0)
except ZeroDivisionError:
    print("Caught ZeroDivisionError (re-raised correctly)")

# Test 3: Another exception type
try:
    get_item([1, 2, 3], 10)
except IndexError:
    print("Caught IndexError (re-raised correctly)")
```

---

## Exercise 3 — Parameterized Decorators (30 min)

**File:** `ex03_parameterized_decorators.py`

```python
import functools
import time
```

### 3.1 — Configurable Logger

```python
def log_calls(level="INFO", include_args=True, include_result=False):
    """
    Parameterized decorator that logs function calls.
    
    Parameters:
        level         — logging level string: "DEBUG", "INFO", "WARNING", "ERROR"
        include_args  — if True, log the arguments passed
        include_result — if True, log the return value
    
    Log format:
        "[LEVEL] function_name called" 
        "[LEVEL] function_name args: (args,) kwargs: {kwargs}" (if include_args=True)
        "[LEVEL] function_name returned: result" (if include_result=True)
    """
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format="%(levelname)-8s | %(message)s")
    # YOUR CODE HERE — remember: 3 levels!
    pass

# Test 1: DEBUG with args only
@log_calls(level="DEBUG", include_args=True)
def add(a, b):
    return a + b

add(3, 4)
# DEBUG    | add called
# DEBUG    | add args: (3, 4) kwargs: {}

# Test 2: INFO with result
@log_calls(level="INFO", include_args=True, include_result=True)
def multiply(x, y):
    return x * y

multiply(6, 7)
# INFO     | multiply called
# INFO     | multiply args: (6, 7) kwargs: {}
# INFO     | multiply returned: 42

# Test 3: WARNING, no args
@log_calls(level="WARNING", include_args=False, include_result=False)
def risky_operation(data):
    return data[::-1]

risky_operation("hello")
# WARNING  | risky_operation called
```

---

### 3.2 — Retry with Exponential Backoff

```python
def retry(max_attempts=3, base_delay=1.0, backoff=2.0,
          exceptions=(Exception,), on_failure=None):
    """
    Retry decorator with exponential backoff.
    
    Parameters:
        max_attempts  — maximum number of attempts (default: 3)
        base_delay    — initial delay in seconds (default: 1.0)
        backoff       — multiply delay by this after each failure (default: 2.0)
        exceptions    — tuple of exception types to retry on
        on_failure    — optional callback(attempt_number, exception) called on each failure
    
    Behaviour:
        - Attempt 1: try immediately
        - Attempt 2: wait base_delay * backoff^0 = base_delay
        - Attempt 3: wait base_delay * backoff^1
        - ...
        - After max_attempts: re-raise the last exception
    
    Print: "Attempt N/max_attempts failed: error. Retrying in Xs..."
    Print: "All N attempts failed for function_name."
    Print: "function_name succeeded on attempt N."
    """
    # YOUR CODE HERE
    pass

# ── Test 1: Succeeds after 2 failures ────────────────────────────────────────
attempt_num = 0

@retry(max_attempts=4, base_delay=0.1, backoff=2.0,
       exceptions=(ValueError,))
def sometimes_fails():
    global attempt_num
    attempt_num += 1
    if attempt_num < 3:
        raise ValueError(f"Not ready yet (attempt {attempt_num})")
    return f"Success on attempt {attempt_num}"

attempt_num = 0
result = sometimes_fails()
print(result)
# Attempt 1/4 failed: Not ready yet (attempt 1). Retrying in 0.1s...
# Attempt 2/4 failed: Not ready yet (attempt 2). Retrying in 0.2s...
# sometimes_fails succeeded on attempt 3.
# Success on attempt 3

# ── Test 2: Always fails ──────────────────────────────────────────────────────
@retry(max_attempts=3, base_delay=0.05)
def always_fails():
    raise ConnectionError("Server down")

try:
    always_fails()
except ConnectionError as e:
    print(f"Final error: {e}")
# Attempt 1/3 failed: Server down. Retrying in 0.05s...
# Attempt 2/3 failed: Server down. Retrying in 0.1s...
# All 3 attempts failed for always_fails.
# Final error: Server down

# ── Test 3: Non-retryable exception stops immediately ─────────────────────────
@retry(max_attempts=5, exceptions=(ConnectionError,))
def wrong_error():
    raise ValueError("Wrong error type")

try:
    wrong_error()
except ValueError as e:
    print(f"Non-retryable (no retry): {e}")
```

---

### 3.3 — Input Validator

```python
def require_positive(*param_names):
    """
    Decorator factory: validates that specified numeric parameters are positive (> 0).
    
    Usage: @require_positive("amount", "quantity")
    
    Requirements:
    - Use inspect.signature to get parameter names
    - Check only the named parameters listed in param_names
    - Raise ValueError with message: "Parameter 'name' must be positive, got: value"
    - Non-specified parameters are not checked
    """
    import inspect
    # YOUR CODE HERE
    pass

@require_positive("amount", "quantity")
def add_to_cart(item_name, amount, quantity, discount=0):
    return f"Added {quantity}x {item_name} @ ₹{amount} each"

# Valid calls:
print(add_to_cart("Apple", 50.0, 3))
# Added 3x Apple @ ₹50.0 each

print(add_to_cart("Banana", 30.0, quantity=2, discount=-5))   # discount not checked
# Added 2x Banana @ ₹30.0 each

# Invalid calls:
try:
    add_to_cart("Cherry", -10.0, 5)   # amount is negative
except ValueError as e:
    print(f"[ERROR] {e}")
# [ERROR] Parameter 'amount' must be positive, got: -10.0

try:
    add_to_cart("Date", 20.0, 0)      # quantity is zero (not positive)
except ValueError as e:
    print(f"[ERROR] {e}")
# [ERROR] Parameter 'quantity' must be positive, got: 0
```

---

## Exercise 4 — Authentication & Authorization Stack (30 min)

**File:** `ex04_auth_stack.py`

**Goal:** Build a complete authentication/authorization decorator system.

### Step 1 — Session Management

```python
import functools
from datetime import datetime

# Simple in-memory session store
_sessions = {}   # {session_token: user_dict}

def create_session(user):
    """Create a session for the given user dict. Return token."""
    import uuid
    token = str(uuid.uuid4())[:8]
    _sessions[token] = {**user, "created_at": datetime.now()}
    return token

def get_current_user(token):
    """Return user dict for token, or None if not found."""
    return _sessions.get(token)

def clear_session(token):
    """Remove session."""
    _sessions.pop(token, None)
```

---

### Step 2 — Implement the Decorators

```python
def require_auth(func):
    """
    Block access if no valid session token in kwargs.
    Expects: function called with token="..." keyword argument.
    On failure: return {"error": 401, "message": "Authentication required"}
    On success: inject user dict into kwargs as user=user_dict, then call func
    """
    # YOUR CODE HERE
    pass

def require_permission(*permissions):
    """
    Block access if user doesn't have required permissions.
    User dict has a "permissions" key containing a list of permission strings.
    On failure: return {"error": 403, "message": "Permission denied: need [permissions]"}
    """
    # YOUR CODE HERE
    pass

def audit_log(action):
    """
    Log every call with the action name, user id, timestamp, and result status.
    Format: "[AUDIT] {timestamp} | action={action} | user={user_id} | status={ok|error}"
    """
    # YOUR CODE HERE
    pass
```

---

### Step 3 — Define Protected Endpoints

```python
@audit_log("view_dashboard")
@require_auth
def view_dashboard(token=None, user=None):
    """Any authenticated user can view dashboard."""
    return {"status": "ok", "data": f"Dashboard for {user['name']}"}

@audit_log("admin_panel")
@require_auth
@require_permission("admin")
def admin_panel(token=None, user=None):
    """Admin-only panel."""
    return {"status": "ok", "data": "Admin panel content"}

@audit_log("manage_billing")
@require_auth
@require_permission("admin", "billing_manager")
def manage_billing(token=None, user=None):
    """Accessible to admins and billing managers."""
    return {"status": "ok", "data": "Billing management interface"}

@audit_log("delete_record")
@require_auth
@require_permission("admin", "superuser")
def delete_record(record_id, token=None, user=None):
    """Only superusers and admins can delete."""
    return {"status": "ok", "data": f"Record {record_id} deleted"}
```

---

### Step 4 — Test the System

```python
# Create test users
admin_token   = create_session({"id": 1, "name": "Admin Alice",
                                 "permissions": ["admin", "billing_manager"]})
billing_token = create_session({"id": 2, "name": "Billing Bob",
                                 "permissions": ["billing_manager"]})
user_token    = create_session({"id": 3, "name": "Regular Carol",
                                 "permissions": []})

print("\n=== Dashboard (any authenticated user) ===")
print(view_dashboard(token=admin_token))        # ✅ ok
print(view_dashboard(token=user_token))         # ✅ ok
print(view_dashboard())                         # ❌ 401

print("\n=== Admin Panel (admin only) ===")
print(admin_panel(token=admin_token))           # ✅ ok
print(admin_panel(token=billing_token))         # ❌ 403
print(admin_panel(token=user_token))            # ❌ 403

print("\n=== Manage Billing (admin or billing_manager) ===")
print(manage_billing(token=admin_token))        # ✅ ok
print(manage_billing(token=billing_token))      # ✅ ok
print(manage_billing(token=user_token))         # ❌ 403

print("\n=== Delete Record (admin or superuser) ===")
print(delete_record("REC-001", token=admin_token))    # ✅ ok
print(delete_record("REC-002", token=billing_token))  # ❌ 403
```

---

## Exercise 5 — Memoization & Caching (20 min)

**File:** `ex05_caching.py`

### 5.1 — Manual Memoize with Cache Info

```python
import functools
import time

def memoize(func):
    """
    Memoization decorator with cache statistics.
    
    Requirements:
    - Cache results by argument tuple (handle *args only for simplicity)
    - On cache HIT: print "[CACHE HIT] function_name(args)"
    - On cache MISS: print "[CACHE MISS] function_name(args) — computing..."
    - Expose wrapper.cache — the underlying dict
    - Expose wrapper.hits — number of cache hits
    - Expose wrapper.misses — number of cache misses
    - Expose wrapper.cache_clear() — clears cache and resets stats
    """
    # YOUR CODE HERE
    pass

@memoize
def expensive_power(base, exponent):
    """Computes base^exponent — pretends it's expensive."""
    time.sleep(0.1)
    return base ** exponent

# First calls — all misses
print(expensive_power(2, 10))   # [CACHE MISS] expensive_power((2, 10)) — computing...
print(expensive_power(3, 5))    # [CACHE MISS] expensive_power((3, 5)) — computing...

# Repeat calls — all hits
print(expensive_power(2, 10))   # [CACHE HIT] expensive_power((2, 10))
print(expensive_power(2, 10))   # [CACHE HIT] expensive_power((2, 10))
print(expensive_power(3, 5))    # [CACHE HIT] expensive_power((3, 5))

print(f"\nStats: {expensive_power.hits} hits, {expensive_power.misses} misses")
print(f"Cache: {expensive_power.cache}")

expensive_power.cache_clear()
print(f"\nAfter clear: {expensive_power.hits} hits, {expensive_power.misses} misses")
print(f"Cache: {expensive_power.cache}")
```

---

### 5.2 — Timed Cache (TTL Cache)

```python
def ttl_cache(seconds=60):
    """
    Decorator factory: cache results but expire them after 'seconds'.
    
    Requirements:
    - Store (result, expiry_timestamp) per argument set
    - On cache HIT (not expired): print "[TTL HIT] function_name(args)"
    - On cache MISS or EXPIRED: print "[TTL MISS/EXPIRED] function_name(args)"
    - Use time.time() for timestamps
    - Expose wrapper.cache_clear()
    """
    # YOUR CODE HERE
    pass

@ttl_cache(seconds=2)   # Cache expires after 2 seconds
def get_exchange_rate(currency):
    """Simulates fetching live exchange rate — expensive/slow."""
    import random
    rate = round(random.uniform(80, 85), 2)
    return {"currency": currency, "rate": rate, "fetched_at": time.time()}

# First call — miss
r1 = get_exchange_rate("USD")
print(f"Rate: {r1['rate']}")

# Immediate repeat — hit (same rate)
r2 = get_exchange_rate("USD")
print(f"Rate: {r2['rate']}")
print(f"Same result: {r1['rate'] == r2['rate']}")   # True

# Wait for expiry
print("Waiting 2.1 seconds...")
time.sleep(2.1)

# After expiry — miss (new rate)
r3 = get_exchange_rate("USD")
print(f"New rate: {r3['rate']}")
print(f"Rate changed: {r1['rate'] != r3['rate']}")   # Likely True
```

---

## Exercise 6 — Class-Based Decorators (25 min)

**File:** `ex06_class_decorators.py`

### 6.1 — CallLogger Class Decorator

```python
import functools

class CallLogger:
    """
    Class-based decorator that maintains a full call history.
    
    Requirements:
    - __init__ receives the function
    - __call__ acts as the wrapper
    - Store history as list of dicts: {args, kwargs, result, timestamp}
    - Expose .history — the list of call records
    - Expose .last_call — the most recent record (or None)
    - Expose .clear() — clears history
    - Handle exceptions: store {args, kwargs, error: str, timestamp}
    """
    import time   # class-level import
    
    def __init__(self, func):
        # YOUR CODE HERE
        pass
    
    def __call__(self, *args, **kwargs):
        # YOUR CODE HERE
        pass
    
    # Add .history, .last_call, .clear() below
    pass

@CallLogger
def calculate_discount(price, discount_pct):
    if discount_pct < 0 or discount_pct > 100:
        raise ValueError(f"Invalid discount: {discount_pct}%")
    return round(price * (1 - discount_pct / 100), 2)

# Run some calls
print(calculate_discount(1000, 20))   # 800.0
print(calculate_discount(500, 10))    # 450.0
try:
    calculate_discount(200, 150)       # Raises ValueError
except ValueError:
    pass

# Inspect history
print(f"\nCall history ({len(calculate_discount.history)} entries):")
for record in calculate_discount.history:
    if "error" in record:
        print(f"  ERROR: {record['error']} | args={record['args']}")
    else:
        print(f"  OK: {record['result']} | args={record['args']}")

print(f"\nLast call: {calculate_discount.last_call}")
calculate_discount.clear()
print(f"After clear: {len(calculate_discount.history)} entries")
```

---

### 6.2 — Singleton Decorator Class

```python
class Singleton:
    """
    Class decorator that enforces single-instance creation.
    
    Requirements:
    - Applied to a CLASS (not a function)
    - __call__ returns the existing instance if already created
    - First call creates the instance and stores it
    - Expose .instance — the current instance (or None if not created)
    - Expose .reset() — destroys the instance (useful for testing)
    - Must preserve the class name and docstring
    """
    
    def __init__(self, cls):
        # YOUR CODE HERE
        pass
    
    def __call__(self, *args, **kwargs):
        # YOUR CODE HERE
        pass
    
    @property
    def instance(self):
        # YOUR CODE HERE
        pass
    
    def reset(self):
        # YOUR CODE HERE
        pass

@Singleton
class AppConfig:
    """Application configuration — must be a singleton."""
    
    def __init__(self, debug=False, db_url="sqlite:///app.db"):
        self.debug  = debug
        self.db_url = db_url
        print(f"[AppConfig] Created: debug={debug}, db_url={db_url}")

# First call — creates instance
cfg1 = AppConfig(debug=True, db_url="postgresql://localhost/mydb")
# [AppConfig] Created: debug=True, db_url=postgresql://localhost/mydb

# Subsequent calls — same instance
cfg2 = AppConfig(debug=False, db_url="different://db")   # Args IGNORED
cfg3 = AppConfig()

print(cfg1 is cfg2)   # True
print(cfg1 is cfg3)   # True
print(cfg2.debug)     # True — same instance as cfg1

print(f"Instance: {AppConfig.instance}")

# Reset for testing
AppConfig.reset()
print(f"After reset: {AppConfig.instance}")   # None

cfg4 = AppConfig(debug=False)   # New instance created
# [AppConfig] Created: debug=False, ...
print(cfg4 is cfg1)   # False — fresh instance
```

---

## Exercise 7 — Challenge: Full Decorator Toolkit (Stretch Goal)

**File:** `ex07_toolkit.py`

**Goal:** Build a reusable decorator toolkit module for a web API.

### Requirements

Implement ALL of the following decorators in a single module called `decorators.py`:

```python
"""
decorators.py — Reusable decorator toolkit for web API development

Decorators to implement:
1. @timing(verbose=True)         — log execution time
2. @retry(attempts, delay, excs) — retry on failure with backoff
3. @cache(ttl_seconds)           — TTL-based result caching
4. @require_auth                 — check 'token' kwarg
5. @require_role(*roles)         — check user role
6. @rate_limit(calls, period)    — limit calls per time window
7. @validate_input(**types)      — validate argument types
8. @deprecated(reason)           — warn on call
9. @once                         — run function at most once
10. @trace                       — print call tree with indentation
"""
```

### Starter Structure

```python
import functools
import time
import logging
import warnings
import inspect
from collections import deque

logger = logging.getLogger(__name__)

# ── 1. Timing ─────────────────────────────────────────────────────────────────
def timing(verbose=True):
    # YOUR CODE HERE
    pass

# ── 2. Retry ──────────────────────────────────────────────────────────────────
def retry(attempts=3, delay=1.0, exceptions=(Exception,)):
    # YOUR CODE HERE
    pass

# ── 3. TTL Cache ──────────────────────────────────────────────────────────────
def cache(ttl_seconds=60):
    # YOUR CODE HERE
    pass

# ── 4. Require Auth ───────────────────────────────────────────────────────────
def require_auth(func):
    # YOUR CODE HERE (non-factory version — applied directly)
    pass

# ── 5. Require Role ───────────────────────────────────────────────────────────
def require_role(*roles):
    # YOUR CODE HERE
    pass

# ── 6. Rate Limit ─────────────────────────────────────────────────────────────
def rate_limit(calls=100, period=60):
    # YOUR CODE HERE
    pass

# ── 7. Validate Input ─────────────────────────────────────────────────────────
def validate_input(**types):
    # YOUR CODE HERE
    pass

# ── 8. Deprecated ─────────────────────────────────────────────────────────────
def deprecated(reason, alternative=None):
    # YOUR CODE HERE
    pass

# ── 9. Once ───────────────────────────────────────────────────────────────────
def once(func):
    # YOUR CODE HERE (non-factory — applied directly)
    pass

# ── 10. Trace ─────────────────────────────────────────────────────────────────
def trace(func):
    """
    Print indented call tree showing nested function calls.
    
    Expected output for factorial(3):
    → factorial(3)
      → factorial(2)
        → factorial(1)
        ← factorial(1) = 1
      ← factorial(2) = 2
    ← factorial(3) = 6
    """
    # YOUR CODE HERE
    # Hint: use a mutable counter in the module to track depth level
    pass
```

### Test the Toolkit

```python
from decorators import (timing, retry, cache, require_auth, require_role,
                         rate_limit, validate_input, deprecated, once, trace)

# ── Combined decorators on one function ───────────────────────────────────────
_session = {}

@timing(verbose=True)
@rate_limit(calls=5, period=60)
@require_auth
@require_role("admin")
@validate_input(amount=float, currency=str)
def process_payment(amount, currency, token=None, user=None):
    """Process a payment transaction."""
    time.sleep(0.01)
    return {"status": "ok", "amount": amount, "currency": currency,
            "processed_by": user["name"]}

# Setup session
import uuid
token = str(uuid.uuid4())[:8]
_session[token] = {"id": 1, "name": "Admin", "role": "admin"}

# Import require_auth from decorators — it needs _session reference
# (In a real app, the session store would be in a shared module)

# Test: valid payment
try:
    result = process_payment(500.0, "INR", token=token)
    print(f"Payment result: {result}")
except Exception as e:
    print(f"Error: {e}")

# ── Test trace with recursive function ───────────────────────────────────────
@trace
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(4))
# → factorial(4)
#   → factorial(3)
#     → factorial(2)
#       → factorial(1)
#       ← factorial(1) = 1
#     ← factorial(2) = 2
#   ← factorial(3) = 6
# ← factorial(4) = 24
# 24

# ── Test once decorator ───────────────────────────────────────────────────────
@once
def initialize_database():
    print("Connecting to database...")
    return "connected"

initialize_database()   # Connects
initialize_database()   # No output — returns cached result
initialize_database()   # No output — returns cached result
```

---

## ✅ Exercise Checklist

| Exercise | Topic | Difficulty | Done? |
|---|---|---|---|
| Ex 1 — Foundations | First-class functions, closures, wrapper pattern | ⭐ | ⬜ |
| Ex 2.1 — Timing | Basic decorator + functools.wraps | ⭐ | ⬜ |
| Ex 2.2 — Call Counter | Closure state + exposed attributes | ⭐⭐ | ⬜ |
| Ex 2.3 — Exception Logger | Exception handling in decorators | ⭐⭐ | ⬜ |
| Ex 3.1 — Config Logger | Parameterized decorator (3-layer) | ⭐⭐ | ⬜ |
| Ex 3.2 — Retry + Backoff | Complex parameterized decorator | ⭐⭐⭐ | ⬜ |
| Ex 3.3 — Input Validator | inspect module + validation | ⭐⭐⭐ | ⬜ |
| Ex 4 — Auth Stack | Full auth/permission system | ⭐⭐⭐ | ⬜ |
| Ex 5.1 — Memoize | Custom cache with stats | ⭐⭐ | ⬜ |
| Ex 5.2 — TTL Cache | Time-based cache expiry | ⭐⭐⭐ | ⬜ |
| Ex 6.1 — CallLogger | Class-based decorator with history | ⭐⭐⭐ | ⬜ |
| Ex 6.2 — Singleton | Class decorator pattern | ⭐⭐⭐ | ⬜ |
| Ex 7 — Full Toolkit | All patterns combined | ⭐⭐⭐⭐ | ⬜ |

---

## 💡 Hints & Tips

### Exercise 1
- Part B: The inner function should be `def greet(name): return f"{greeting}, {name}!"` — `greeting` from outer scope is the closure variable
- Part C: `def wrapper(*args, **kwargs): result = func(*args, **kwargs); return result.upper()`

### Exercise 2.2 (Call Counter)
- Use `nonlocal count` to modify the counter in the closure
- Expose attributes directly: `wrapper.call_count = count` won't work (count is a local). Instead, use a mutable object: `state = {"count": 0}` and `state["count"] += 1`

### Exercise 3.1 (Config Logger)
- Three levels: `def log_calls(level, include_args, include_result):` → `def decorator(func):` → `def wrapper(*args, **kwargs):`
- `getattr(logging, level.lower())` gives you `logging.debug`, `logging.info`, etc.

### Exercise 3.2 (Retry + Backoff)
- Delay formula: `current_delay = base_delay * (backoff ** (attempt - 1))`
- Only sleep if `attempt < max_attempts` — no sleep on the last attempt

### Exercise 4 (Auth Stack)
- `require_auth`: extract `token` from `kwargs`, look up `_sessions[token]`, inject `user` back into kwargs: `kwargs["user"] = user`
- `require_permission`: get user from `kwargs["user"]`, check `permissions` list

### Exercise 5.2 (TTL Cache)
- Cache structure: `{args_key: (result, expiry_time)}` where `expiry_time = time.time() + seconds`
- On lookup: `if key in cache and time.time() < cache[key][1]:` → hit

### Exercise 6.1 (CallLogger)
- `functools.update_wrapper(self, func)` in `__init__` — class-based equivalent of `@functools.wraps`
- History entry: `{"args": args, "kwargs": kwargs, "result": result, "timestamp": time.time()}`

### Exercise 7 (trace)
- Use a module-level `_depth = [0]` (a list so it's mutable from the closure)
- In wrapper: `indent = "  " * _depth[0]`, print `→`, increment `_depth[0]`, call func, decrement, print `←`
