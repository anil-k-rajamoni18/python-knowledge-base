# Day 9 — Python Exception Handling & Logging
### Python Full Stack Bootcamp | Session Duration: 3 Hours
## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, students will be able to:
- Understand Python's exception hierarchy and confidently use `try/except/else/finally` to handle errors gracefully
- Write and raise custom exceptions with meaningful messages and attributes
- Apply the EAFP coding philosophy and distinguish it from LBYL
- Configure Python's `logging` module with handlers, formatters, and log rotation for production-grade apps
- Integrate exception handling and structured logging into a real-world banking simulation project


## 2. Concept Explanation

### 2.1 What is an Exception?
**Real-world analogy:** Think of a Python program like a car journey. Exceptions are road incidents — a flat tyre (FileNotFoundError), running out of fuel (MemoryError), or a wrong turn (ValueError). Exception handling is the plan you have *before* you start driving: "If I get a flat, I'll pull over and call for help — I won't just crash into the ditch."

Exceptions are **not bugs** — they are Python's structured way of signalling that something went wrong at runtime. Without handling them, your program crashes and users see ugly tracebacks.

### 2.2 The Exception Hierarchy
Python exceptions form a tree. All exceptions inherit from `BaseException`. Understanding this tree lets you catch the right level — not too broad, not too specific.

```
BaseException
├── SystemExit              ← raised by sys.exit()
├── KeyboardInterrupt       ← Ctrl+C
├── GeneratorExit
└── Exception               ← Almost everything you'll ever catch
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── ValueError
    ├── TypeError
    ├── AttributeError
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── OSError
    │   ├── FileNotFoundError
    │   └── PermissionError
    ├── RuntimeError
    └── StopIteration
```
**Rule of thumb:** Always catch the most *specific* exception you expect. Catch `Exception` only as a last resort.

### 2.3 The try/except/else/finally Structure
| Block | Runs when... |
|---|---|
| `try` | Always — contains risky code |
| `except` | Only when an exception is raised |
| `else` | Only when NO exception occurred |
| `finally` | Always — whether or not exception occurred |

### 2.4 EAFP vs LBYL
| Style | Stands For | Approach |
|---|---|---|
| **LBYL** | Look Before You Leap | Check conditions *before* performing an action |
| **EAFP** | Easier to Ask Forgiveness than Permission | Try first, handle failure |

Python *prefers* EAFP — it leads to cleaner, faster, and more Pythonic code.

### 2.5 Custom Exceptions — The "Why"
Built-in exceptions are generic. `ValueError` tells you *a value was wrong*, but not *which value* or *why* in your domain. Custom exceptions let you express **business logic errors** clearly: `InsufficientFundsError` is instantly understandable to any developer on your team.

### 2.6 The Logging Module — The "Why"
`print()` is for development. `logging` is for production. Logging gives you:
- **Severity levels** to filter noise
- **Timestamps and metadata** automatically
- **Multiple output destinations** (file, terminal, network) simultaneously
- **Log rotation** so disk space doesn't fill up
- **Configurable without changing code**

---

## 3. Syntax & Code Examples

### 3.1 Basic try/except/else/finally


```python
# Basic structure — all four blocks
def read_config(filename):
    try:
        file = open(filename, "r")          # Risky operation
        content = file.read()
    except FileNotFoundError:
        print(f"Config file '{filename}' not found. Using defaults.")
        content = ""
    except PermissionError:
        print(f"No permission to read '{filename}'.")
        content = ""
    else:
        # Only runs if NO exception was raised
        print("Config loaded successfully.")
        file.close()
    finally:
        # ALWAYS runs — perfect for cleanup
        print("read_config() completed.")
    
    return content

# Expected Output (file missing):
# Config file 'app.cfg' not found. Using defaults.
# read_config() completed.

# Expected Output (file exists):
# Config loaded successfully.
# read_config() completed.
```

### 3.2 Multiple except Blocks + Catching Multiple Exceptions

```python
def safe_divide(a, b):
    try:
        result = int(a) / int(b)
    except ZeroDivisionError:
        print("Error: Cannot divide by zero.")
        return None
    except ValueError:
        print("Error: Both arguments must be numbers.")
        return None
    except (TypeError, AttributeError):    # Catching multiple types in one block
        print("Error: Invalid input types.")
        return None
    else:
        return result

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # Error: Cannot divide by zero. → None
print(safe_divide(10, "x"))  # Error: Both arguments must be numbers. → None
```

### 3.3 Accessing Exception Details with `as`

```python
def load_user(user_id):
    users = {1: "Alice", 2: "Bob"}
    try:
        user = users[user_id]
        age = int("not_a_number")           # Simulate bad data
    except KeyError as e:
        print(f"User not found. Key: {e}")  # e holds the missing key
    except ValueError as e:
        print(f"Data conversion failed: {e}")
    
    return None

load_user(99)    # User not found. Key: 99
load_user(1)     # Data conversion failed: invalid literal for int() ...
```

### 3.4 Raising Exceptions

```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"Age must be an integer, got {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValueError(f"Age {age} is outside valid range (0–150)")
    return age

# Re-raising an exception (preserve original traceback)
def process_payment(amount):
    try:
        result = make_transfer(amount)
    except ConnectionError as e:
        log_error(e)          # Log it...
        raise                 # ...then re-raise to caller
```

### 3.5 Exception Chaining with `raise ... from`

```python
# raise X from Y — explicitly chains exceptions
# The original cause is stored in __cause__

def fetch_user_from_db(user_id):
    try:
        # Simulating a low-level DB error
        raise ConnectionError("DB connection refused on port 5432")
    except ConnectionError as e:
        raise RuntimeError(
            f"Failed to fetch user {user_id} from database"
        ) from e    # 'from e' attaches the original error as the cause

try:
    fetch_user_from_db(42)
except RuntimeError as e:
    print(f"High-level error: {e}")
    print(f"Caused by: {e.__cause__}")

# Output:
# High-level error: Failed to fetch user 42 from database
# Caused by: DB connection refused on port 5432
```

### 3.6 Custom Exceptions

```python
# ─── Custom Exception Hierarchy ───────────────────────────────────────────────

class BankingError(Exception):
    """Base class for all banking-related errors."""
    pass

class InvalidAccountError(BankingError):
    """Raised when an account number is invalid or not found."""
    
    def __init__(self, account_number, message=None):
        self.account_number = account_number
        self.message = message or f"Account '{account_number}' does not exist."
        super().__init__(self.message)   # Always call parent __init__

class InsufficientFundsError(BankingError):
    """Raised when a withdrawal exceeds the available balance."""
    
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.shortfall = amount - balance
        super().__init__(
            f"Insufficient funds: tried to withdraw ₹{amount}, "
            f"but balance is only ₹{balance} (shortfall: ₹{self.shortfall})"
        )

# ─── Using Custom Exceptions ──────────────────────────────────────────────────

class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        return self.balance

account = BankAccount("ACC001", balance=1000)

try:
    account.withdraw(1500)
except InsufficientFundsError as e:
    print(e)
    print(f"Shortfall: ₹{e.shortfall}")

# Output:
# Insufficient funds: tried to withdraw ₹1500, but balance is only ₹1000 (shortfall: ₹500)
# Shortfall: ₹500
```

### 3.7 EAFP vs LBYL — Side by Side

```python
import os

# ─── LBYL (Look Before You Leap) ──────────────────────────────────────────────
# Problem: Race condition between check and action; verbose
def read_file_lbyl(path):
    if os.path.exists(path):          # Check
        if os.access(path, os.R_OK):  # Check again
            with open(path) as f:
                return f.read()
    return None

# ─── EAFP (Easier to Ask Forgiveness than Permission) ─────────────────────────
# Pythonic, cleaner, handles race conditions correctly
def read_file_eafp(path):
    try:
        with open(path) as f:
            return f.read()
    except (FileNotFoundError, PermissionError):
        return None
```

### 3.8 Context Managers for Resource Cleanup

```python
# The 'with' statement is the Pythonic way to ensure cleanup
# It calls __exit__ even if an exception occurs

# ─── Without context manager (fragile) ────────────────────────────────────────
f = open("data.txt")
try:
    data = f.read()
finally:
    f.close()   # Must manually close

# ─── With context manager (Pythonic) ──────────────────────────────────────────
with open("data.txt") as f:
    data = f.read()
# File is automatically closed here, even if an exception occurs inside
```

---

### 3.9 The Logging Module

#### Basic Setup with basicConfig

```python
import logging

# Configure the root logger
logging.basicConfig(
    level=logging.DEBUG,                          # Show all levels DEBUG and above
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)   # Best practice: use module name

# The five levels (lowest → highest severity)
logger.debug("Variable x = %s", 42)           # Development details
logger.info("User 'alice' logged in.")         # Normal events
logger.warning("Disk space below 10%%.")       # Something unexpected
logger.error("Payment processing failed.")     # Error, program continues
logger.critical("Database connection lost!")   # Severe, app may not recover

# Output (example):
# 2024-01-15 10:23:45 | DEBUG    | __main__ | Variable x = 42
# 2024-01-15 10:23:45 | INFO     | __main__ | User 'alice' logged in.
# 2024-01-15 10:23:45 | WARNING  | __main__ | Disk space below 10%.
```

#### Handlers — Multiple Output Destinations

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str) -> logging.Logger:
    """Create a logger that writes to both console and a rotating file."""
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)   # Master switch: allow all levels
    
    # ── Formatter ──────────────────────────────────────────────────────────────
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # ── Console Handler (INFO and above only) ──────────────────────────────────
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)    # Filter: only INFO+ to console
    console_handler.setFormatter(formatter)
    
    # ── File Handler with Rotation ─────────────────────────────────────────────
    # maxBytes=5MB, keep last 3 backup files: app.log, app.log.1, app.log.2
    file_handler = RotatingFileHandler(
        filename="app.log",
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)      # Filter: DEBUG+ to file
    file_handler.setFormatter(formatter)
    
    # ── Attach handlers ────────────────────────────────────────────────────────
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Usage — one logger per module
logger = setup_logger(__name__)
logger.info("Application started.")
logger.debug("Debug info only goes to file, not console.")
```

#### dictConfig — Production-Grade Configuration

```python
import logging
import logging.config

# Dictionary-based config is preferred for complex setups
# Easy to store in a config file or environment variables

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "detailed": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(funcName)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "app.log",
            "maxBytes": 5242880,   # 5 MB
            "backupCount": 3
        }
    },
    "loggers": {
        "banking": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False   # Don't pass to root logger
        }
    },
    "root": {
        "level": "WARNING",
        "handlers": ["console"]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("banking")
logger.info("Logging configured via dictConfig.")
```

#### Logging Exceptions

```python
logger = logging.getLogger(__name__)

def process_transaction(data):
    try:
        amount = float(data["amount"])
        account_id = data["account_id"]
        # ... process ...
    except KeyError as e:
        # exc_info=True attaches full traceback to the log
        logger.error("Missing required field: %s", e, exc_info=True)
    except ValueError as e:
        logger.error("Invalid data format: %s", e, exc_info=True)
    except Exception as e:
        # Use logger.exception() — it auto-includes exc_info=True
        logger.exception("Unexpected error during transaction: %s", e)
        raise   # Re-raise after logging
```

---

## 4. Common Mistakes & Gotchas

### Mistake 1 — Catching `Exception` (or `BaseException`) Blindly

```python
# ❌ WRONG — swallows ALL errors including programming bugs
def bad_handler():
    try:
        result = do_something()
    except Exception:
        pass   # Silent failure — nightmare to debug!

# ✅ CORRECT — catch only what you expect and can handle
def good_handler():
    try:
        result = do_something()
    except (ValueError, KeyError) as e:
        logger.error("Expected error: %s", e)
        result = default_value
```

### Mistake 2 — Wrong Order of except Blocks

```python
# ❌ WRONG — broader exception catches first; specific block never runs
try:
    x = int("abc")
except Exception as e:       # Too broad — catches ValueError before it reaches below
    print("Generic error")
except ValueError as e:      # DEAD CODE — never reached!
    print("Value error")

# ✅ CORRECT — specific exceptions first, general last
try:
    x = int("abc")
except ValueError as e:
    print(f"Value error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Mistake 3 — Using `print()` Instead of `logging`

```python
# ❌ WRONG — no timestamps, no severity, no file output, not configurable
def process(data):
    try:
        result = parse(data)
    except ValueError:
        print("ERROR: Invalid data")   # Lost forever in production

# ✅ CORRECT — structured, persistent, filterable
logger = logging.getLogger(__name__)

def process(data):
    try:
        result = parse(data)
    except ValueError as e:
        logger.error("Invalid data received: %s | Input: %s", e, data)
```

### Mistake 4 — Not Calling `super().__init__()` in Custom Exceptions

```python
# ❌ WRONG — exception message won't display correctly
class BadError(Exception):
    def __init__(self, code):
        self.code = code
        # Forgot super().__init__() !

# ✅ CORRECT — always call parent __init__ with the message
class GoodError(Exception):
    def __init__(self, code, message=""):
        self.code = code
        super().__init__(message or f"Error code: {code}")
```

### Mistake 5 — Resource Leak (Forgetting finally / context manager)

```python
# ❌ WRONG — if an exception occurs, file is never closed
def bad_file_read(path):
    f = open(path)
    data = f.read()     # What if this raises?
    f.close()           # This line is skipped!
    return data

# ✅ CORRECT — context manager guarantees cleanup
def good_file_read(path):
    with open(path) as f:
        return f.read()
```

---

## 5. Hands-on Exercises

### Guided Exercise 1 — Safe User Input with Exception Handling (30 min)

**Goal:** Build an input-validation function for a student grade entry system.

**Step 1:** Create the base function
```python
def get_student_grade(name, score_str):
    """
    Validates and returns a grade for a student.
    score_str should be a string that can be converted to float (0–100).
    """
    try:
        score = float(score_str)
    except ValueError:
        raise ValueError(f"Invalid score '{score_str}' for student '{name}'. Must be a number.")
    
    if not (0 <= score <= 100):
        raise ValueError(f"Score {score} for '{name}' must be between 0 and 100.")
    
    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "F"
    
    return {"name": name, "score": score, "grade": grade}
```

**Step 2:** Add logging
```python
import logging
logger = logging.getLogger(__name__)

def get_student_grade(name, score_str):
    logger.debug("Processing grade for student: %s, raw score: %s", name, score_str)
    try:
        score = float(score_str)
    except ValueError:
        logger.warning("Invalid score input for '%s': %s", name, score_str)
        raise ValueError(f"Invalid score '{score_str}' for '{name}'.")
    
    if not (0 <= score <= 100):
        logger.warning("Score out of range for '%s': %s", name, score)
        raise ValueError(f"Score {score} is out of range (0–100).")
    
    grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "F"
    logger.info("Grade assigned: %s → %s (%.1f)", name, grade, score)
    return {"name": name, "score": score, "grade": grade}
```

**Step 3:** Process a batch with exception handling
```python
students = [("Alice", "87"), ("Bob", "abc"), ("Carol", "105"), ("David", "72")]

results = []
for name, score in students:
    try:
        result = get_student_grade(name, score)
        results.append(result)
    except ValueError as e:
        print(f"Skipping {name}: {e}")

print("\nValid results:")
for r in results:
    print(f"  {r['name']}: {r['grade']} ({r['score']})")
```

---

### Guided Exercise 2 — Banking System with Custom Exceptions (30 min)

**Goal:** Build a mini banking module with custom exception hierarchy and logging.

```python
import logging
from logging.handlers import RotatingFileHandler

# ── Logger Setup ──────────────────────────────────────────────────────────────
def get_banking_logger():
    logger = logging.getLogger("banking")
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler("banking.log", maxBytes=1_000_000, backupCount=2)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())  # Also print to console
    return logger

logger = get_banking_logger()

# ── Custom Exceptions ─────────────────────────────────────────────────────────
class BankingError(Exception):
    pass

class InvalidAccountError(BankingError):
    def __init__(self, account_id):
        self.account_id = account_id
        super().__init__(f"Account '{account_id}' not found.")

class InsufficientFundsError(BankingError):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(
            f"Cannot withdraw ₹{amount}. Available balance: ₹{balance}."
        )

class NegativeAmountError(BankingError):
    def __init__(self, amount):
        super().__init__(f"Amount must be positive. Got: ₹{amount}")

# ── Bank Class ────────────────────────────────────────────────────────────────
class Bank:
    def __init__(self):
        self._accounts = {}
    
    def create_account(self, account_id: str, initial_balance: float = 0):
        if account_id in self._accounts:
            raise ValueError(f"Account '{account_id}' already exists.")
        self._accounts[account_id] = initial_balance
        logger.info("Account created: %s | Balance: ₹%.2f", account_id, initial_balance)
    
    def get_balance(self, account_id: str) -> float:
        if account_id not in self._accounts:
            raise InvalidAccountError(account_id)
        return self._accounts[account_id]
    
    def deposit(self, account_id: str, amount: float):
        if amount <= 0:
            raise NegativeAmountError(amount)
        if account_id not in self._accounts:
            raise InvalidAccountError(account_id)
        self._accounts[account_id] += amount
        logger.info("Deposit: %s | ₹%.2f | New balance: ₹%.2f",
                    account_id, amount, self._accounts[account_id])
    
    def withdraw(self, account_id: str, amount: float):
        if amount <= 0:
            raise NegativeAmountError(amount)
        balance = self.get_balance(account_id)   # Raises InvalidAccountError if missing
        if amount > balance:
            raise InsufficientFundsError(balance, amount)
        self._accounts[account_id] -= amount
        logger.info("Withdrawal: %s | ₹%.2f | New balance: ₹%.2f",
                    account_id, amount, self._accounts[account_id])
    
    def transfer(self, from_id: str, to_id: str, amount: float):
        logger.debug("Transfer initiated: %s → %s | ₹%.2f", from_id, to_id, amount)
        try:
            self.withdraw(from_id, amount)
            self.deposit(to_id, amount)
            logger.info("Transfer complete: %s → %s | ₹%.2f", from_id, to_id, amount)
        except BankingError as e:
            logger.error("Transfer failed: %s", e)
            raise   # Re-raise to caller

# ── Test it ───────────────────────────────────────────────────────────────────
bank = Bank()
bank.create_account("ACC001", 5000)
bank.create_account("ACC002", 1000)

operations = [
    ("deposit",   "ACC001", 500),
    ("withdraw",  "ACC001", 200),
    ("withdraw",  "ACC001", 10000),   # Should raise InsufficientFundsError
    ("transfer",  "ACC001", "ACC002", 300),
    ("withdraw",  "GHOST",  100),     # Should raise InvalidAccountError
]

for op in operations:
    try:
        if op[0] == "deposit":
            bank.deposit(op[1], op[2])
        elif op[0] == "withdraw":
            bank.withdraw(op[1], op[2])
        elif op[0] == "transfer":
            bank.transfer(op[1], op[2], op[3])
    except InsufficientFundsError as e:
        print(f"[FUNDS ERROR] {e}")
    except InvalidAccountError as e:
        print(f"[ACCOUNT ERROR] {e}")
    except NegativeAmountError as e:
        print(f"[INPUT ERROR] {e}")
```

---

### Independent Practice 1 — Temperature Converter (20 min)

**Task:** Write a `convert_temperature(value, from_unit, to_unit)` function that:
- Raises `ValueError` for non-numeric input
- Raises a custom `UnsupportedUnitError` for unknown units (e.g., "Kelvin" should work; "Rankine" should not)
- Logs each conversion at INFO level
- Returns the converted value

**Hint:** Supported units: `"C"`, `"F"`, `"K"`. Conversion: C→F: `(C * 9/5) + 32`, C→K: `C + 273.15`

---

### Independent Practice 2 — File Processing with Logging (20 min)

**Task:** Write a function `process_csv(filepath)` that:
- Uses `try/except` to handle `FileNotFoundError` and `csv.Error`
- Logs DEBUG for each row processed, INFO for completion, ERROR for failures
- Uses a `RotatingFileHandler` outputting to `processing.log`
- Returns a list of valid rows (skipping and logging any malformed ones)

---

### 🏆 Challenge Problem — Retry Decorator with Logging (Stretch Goal)

**Task:** Create a `@retry(max_attempts=3, delay=1, exceptions=(Exception,))` decorator that:
- Retries the decorated function up to `max_attempts` times on failure
- Waits `delay` seconds between retries
- Logs each attempt and failure at WARNING level
- Raises the final exception if all attempts fail
- Logs SUCCESS at INFO level when an attempt succeeds

```python
# Expected usage:
@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError,))
def fetch_data(url):
    # ... makes a network request that may fail
    pass
```

**Hint:** Use `functools.wraps`, `time.sleep`, and a loop.

---

## 6. Best Practices & Industry Standards

### Exception Handling
1. **Be specific:** Always catch the most specific exception you can. Broad catches hide bugs.
2. **Never silence exceptions:** `except Exception: pass` is almost always wrong. Log it, at minimum.
3. **Use `finally` for cleanup** when you can't use a context manager.
4. **Use context managers** (`with`) for any resource that needs cleanup (files, DB connections, locks).
5. **Re-raise with context:** Use `raise X from Y` to preserve the chain of causation.
6. **Custom exceptions for domain errors:** Any error specific to your application's logic deserves its own exception class.

### Logging
1. **One logger per module:** `logger = logging.getLogger(__name__)` — never use the root logger directly in library code.
2. **Use lazy formatting:** `logger.info("User %s logged in", username)` — not `logger.info(f"User {username} logged in")`. The f-string is evaluated even if the level is filtered out.
3. **Log at the right level:**
   - `DEBUG` — detailed diagnostic info (only in development)
   - `INFO` — normal operational events (user actions, startup/shutdown)
   - `WARNING` — something unexpected that didn't cause failure
   - `ERROR` — a failure that needs attention
   - `CRITICAL` — system-level failure, immediate attention required
4. **Never log sensitive data:** Passwords, tokens, credit card numbers — never in logs.
5. **Use `exc_info=True` or `logger.exception()`** when logging inside an except block — it attaches the full traceback.
6. **Configure logging once** at application entry point (`main.py` or `app.py`), not in library modules.

---

## 7. Real-World Application

### Where is This Used?

| Context | Exception/Logging Use |
|---|---|
| **Django/Flask views** | `try/except` around DB queries; custom `APIException` classes; logging requests |
| **REST APIs** | Map custom exceptions to HTTP status codes (404, 400, 500) |
| **Data pipelines** | Skip bad rows with exception handling; log row counts and errors |
| **Payment systems** | `InsufficientFundsError`, `CardDeclinedError` etc. — precise business logic |
| **Deployment (Gunicorn)** | Production log files analyzed by tools like Datadog, ELK Stack |

### Mini Project Snippet — Flask Error Handler

```python
# In a Flask app (Day 14 preview), custom exceptions map to HTTP responses:
from flask import Flask, jsonify

app = Flask(__name__)

class ResourceNotFoundError(Exception):
    def __init__(self, resource_type, resource_id):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type} with id {resource_id} not found.")

@app.errorhandler(ResourceNotFoundError)
def handle_not_found(error):
    # This is registered as a Flask error handler
    return jsonify({"error": str(error)}), 404

@app.route("/users/<int:user_id>")
def get_user(user_id):
    user = db.find_user(user_id)
    if not user:
        raise ResourceNotFoundError("User", user_id)   # Automatically returns 404 JSON
    return jsonify(user)
```

### Connection to Upcoming Days
- **Day 10 (File I/O):** All file operations wrapped in `try/except`; logging file processing stats
- **Day 11 (Databases):** `try/except` around `sqlite3` operations; transaction rollback in `finally`
- **Day 14–16 (Flask):** Exception → HTTP status code mapping; structured access logs
- **Day 28–30 (Deployment):** Log shipping to CloudWatch/Datadog; alerting on ERROR/CRITICAL

---

## 8. Quick Revision Summary

### Key Terms
| Term | Definition |
|---|---|
| **Exception** | A signal that an error condition has occurred at runtime |
| **Traceback** | The call stack display showing where an exception originated |
| **try/except** | Block structure to catch and handle exceptions |
| **finally** | Block that runs regardless of exception occurrence |
| **raise** | Keyword to manually trigger an exception |
| **Custom Exception** | A user-defined class inheriting from `Exception` |
| **EAFP** | Code style: try the action, handle failure after |
| **LBYL** | Code style: check preconditions before acting |
| **Logger** | Named object that issues log messages |
| **Handler** | Destination for log output (console, file, network) |
| **Formatter** | Defines the text layout of log messages |
| **Log Level** | Severity category: DEBUG / INFO / WARNING / ERROR / CRITICAL |
| **RotatingFileHandler** | Handler that creates new log file when size limit is reached |
| **exc_info** | Logger parameter that attaches traceback to log entry |

### Core Syntax Cheat Sheet

```python
# Exception handling
try:
    risky_code()
except SpecificError as e:
    handle(e)
except (TypeError, ValueError) as e:
    handle_multiple(e)
else:
    ran_without_error()
finally:
    always_runs()

# Raise / Re-raise / Chain
raise ValueError("message")
raise                                  # re-raise current exception
raise RuntimeError("high") from e      # chain exceptions

# Custom exception
class MyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

# Basic logging
import logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
logger.info("msg %s", var)             # lazy formatting
logger.exception("msg")               # auto-includes traceback

# Rotating file handler
from logging.handlers import RotatingFileHandler
h = RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=3)
```

### 5 MCQ Recap Questions

**Q1.** Which block in a `try` statement is guaranteed to run whether or not an exception occurs?
- A) `try`
- B) `except`
- C) `else`
- **D) `finally` ✅**

**Q2.** What is the correct order when chaining multiple `except` blocks?
- A) General exceptions first, specific last
- **B) Specific exceptions first, general last ✅**
- C) Order doesn't matter
- D) Only one `except` block is allowed

**Q3.** What does `raise ValueError("bad") from original_error` accomplish?
- A) Replaces the original error entirely
- **B) Creates a chained exception linking the new error to its cause ✅**
- C) Suppresses the original error
- D) Logs the original error automatically

**Q4.** Which logging level should you use for "normal operational events, like a user logging in"?
- A) DEBUG
- **B) INFO ✅**
- C) WARNING
- D) ERROR

**Q5.** What is the advantage of `logger.info("User %s", name)` over `logger.info(f"User {name}")`?
- A) There is no difference
- B) f-strings don't work in logging
- **C) With `%s`, the string is only formatted if the message will actually be logged ✅**
- D) `%s` is safer for passwords

---


### Resources & Further Reading
- 📖 [Python Docs — Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)
- 📖 [Python Docs — logging HOWTO](https://docs.python.org/3/howto/logging.html)
- 📖 [Python Docs — logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- 📖 [PEP 3151 — Exception Hierarchy Reworking](https://peps.python.org/pep-3151/)
- 📺 [Corey Schafer — Python Logging Tutorial](https://www.youtube.com/watch?v=-ARI4Cz-awo)
- 📖 [Real Python — Python Exceptions: An Introduction](https://realpython.com/python-exceptions/)
