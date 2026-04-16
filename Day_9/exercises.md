# Day 9 — Exercises: Python Exception Handling & Logging
### Python Full Stack Bootcamp | Hands-on Practice

---

> 📋 **Instructions:**
> - Complete exercises in order — each builds on the previous
> - Run your code after each step and verify the output
> - Write your own solution before looking at hints
> - All exercises should be saved in separate `.py` files

---

## Exercise 1 — Warm-Up: Reading the Traceback (10 min)

**Goal:** Get comfortable understanding Python error messages.

Run each snippet, read the traceback, and answer the questions below.

**Snippet A:**
```python
def greet(name):
    return "Hello, " + name

print(greet(42))
```
1. What exception is raised?
2. On which line does it occur?
3. What does the error message tell you?
4. How do you fix it?

---

**Snippet B:**
```python
data = {"name": "Alice", "age": 30}
print(data["email"])
```
1. What exception is raised?
2. What is the missing key?
3. Write a `try/except` block that prints `"Field not found"` instead of crashing.

---

**Snippet C:**
```python
numbers = [10, 20, 30]
print(numbers[5])
```
1. What exception is raised?
2. Fix it so the program prints `"Index out of range"` when the index doesn't exist.

---

**Snippet D — Predict the Output:**
```python
def risky():
    try:
        x = 10 / 0
    except ZeroDivisionError:
        print("Caught ZeroDivisionError")
        return "from except"
    finally:
        print("In finally")
        return "from finally"

print(risky())
```
Write your predicted output *before* running it. Then run it. Were you correct?

---

## Exercise 2 — try/except/else/finally Practice (20 min)

**File:** `ex02_safe_operations.py`

**Task:** Implement these four functions with proper exception handling.

### 2.1 — Safe Division
```python
def safe_divide(numerator, denominator):
    """
    Divide numerator by denominator safely.
    
    Returns:
        float: The result if successful
        None: If denominator is zero or inputs are not numbers
    
    Requirements:
        - Handle ZeroDivisionError
        - Handle TypeError (e.g., dividing by a string)
        - Print a descriptive error message for each case
    """
    # YOUR CODE HERE
    pass

# Test cases — all should print without crashing:
print(safe_divide(10, 2))      # Expected: 5.0
print(safe_divide(10, 0))      # Expected: None + error message
print(safe_divide(10, "abc"))  # Expected: None + error message
print(safe_divide("a", 2))     # Expected: None + error message
```

---

### 2.2 — Safe Dictionary Lookup
```python
def get_user_field(user_dict, field, default=None):
    """
    Safely get a field from a user dictionary.
    
    Returns:
        The field value if found
        default if field is missing (KeyError)
        default if user_dict is not a dict (TypeError/AttributeError)
    """
    # YOUR CODE HERE
    pass

# Test cases:
user = {"name": "Alice", "age": 25, "city": "Hyderabad"}
print(get_user_field(user, "name"))          # Alice
print(get_user_field(user, "email"))         # None
print(get_user_field(user, "email", "N/A"))  # N/A
print(get_user_field(None, "name"))          # None
print(get_user_field("not a dict", "name"))  # None
```

---

### 2.3 — File Reader with Cleanup Logging
```python
def read_file_safely(filepath):
    """
    Read a file and return its contents as a string.
    
    Requirements:
        - Use try/except/else/finally
        - Handle FileNotFoundError and PermissionError
        - In the else block, print "File read successfully: X bytes"
        - In the finally block, print "read_file_safely() finished"
        - Return None if any error occurs
    """
    # YOUR CODE HERE
    pass

# Create a test file first, then test:
# open("test.txt", "w").write("Hello World")
read_file_safely("test.txt")         # Should print success + finally
read_file_safely("nonexistent.txt")  # Should print error + finally
```

---

### 2.4 — Input Validator
```python
def get_positive_int(prompt_text, value):
    """
    Validate that value is a positive integer.
    
    Requirements:
        - Raise ValueError if value cannot be converted to int
        - Raise ValueError if the int is not positive (> 0)
        - Return the integer if valid
    
    Note: Do NOT use try/except here — just raise.
    """
    # YOUR CODE HERE
    pass

# Test it in a loop:
test_values = ["5", "-3", "0", "abc", "10"]
for v in test_values:
    try:
        result = get_positive_int("Enter number", v)
        print(f"Valid: {result}")
    except ValueError as e:
        print(f"Invalid: {e}")
```

---

## Exercise 3 — Custom Exceptions (30 min)

**File:** `ex03_custom_exceptions.py`

**Task:** Build a custom exception hierarchy for a library management system.

### Step 1 — Define the Exception Hierarchy

```python
"""
Create the following exception hierarchy:

LibraryError (base)
├── BookNotFoundError       — book ID doesn't exist
├── BookAlreadyCheckedOut   — book is unavailable
├── MemberNotFoundError     — member ID doesn't exist
└── OverdueFineError        — member has unpaid fines above limit
    └── MaxFinesExceededError — member has exceeded the fine limit

Requirements for each exception:
- Inherit correctly from parent
- Accept relevant parameters (e.g., book_id, member_id, fine_amount)
- Store parameters as instance attributes
- Call super().__init__() with a clear, descriptive message
- The message should include the relevant parameter values
"""

# YOUR CODE HERE
```

---

### Step 2 — Implement the Library Class

```python
class Library:
    def __init__(self):
        self.books = {
            "B001": {"title": "Python Crash Course", "available": True},
            "B002": {"title": "Clean Code", "available": False},   # Already checked out
            "B003": {"title": "The Pragmatic Programmer", "available": True},
        }
        self.members = {
            "M001": {"name": "Alice", "fines": 0.0, "checked_out": []},
            "M002": {"name": "Bob",   "fines": 150.0, "checked_out": ["B002"]},  # Has fines
        }
        self.MAX_FINE_LIMIT = 100.0
    
    def checkout_book(self, member_id: str, book_id: str):
        """
        Checkout a book to a member.
        
        Raise:
            MemberNotFoundError — if member_id not in members
            BookNotFoundError   — if book_id not in books
            OverdueFineError    — if member has fines > MAX_FINE_LIMIT
            BookAlreadyCheckedOut — if book is not available
        
        On success:
            - Mark book as unavailable
            - Add book_id to member's checked_out list
            - Print "'{title}' checked out to {name}"
        """
        # YOUR CODE HERE
        pass
    
    def return_book(self, member_id: str, book_id: str):
        """
        Return a book from a member.
        
        Raise:
            MemberNotFoundError — if member_id not in members
            BookNotFoundError   — if book_id not in books
            LibraryError        — if this member doesn't have this book checked out
        
        On success:
            - Mark book as available
            - Remove book_id from member's checked_out list
            - Print "'{title}' returned by {name}"
        """
        # YOUR CODE HERE
        pass
```

---

### Step 3 — Test Your Implementation

```python
library = Library()

# Test scenarios — each should print the appropriate error, not crash
test_cases = [
    ("M001", "B001"),   # ✅ Success
    ("M001", "B002"),   # ❌ BookAlreadyCheckedOut
    ("M001", "B999"),   # ❌ BookNotFoundError
    ("M999", "B003"),   # ❌ MemberNotFoundError
    ("M002", "B003"),   # ❌ OverdueFineError (Bob has ₹150 in fines)
]

for member_id, book_id in test_cases:
    try:
        library.checkout_book(member_id, book_id)
    except MaxFinesExceededError as e:
        print(f"[MAX FINES] {e}")
    except OverdueFineError as e:
        print(f"[FINE ERROR] {e}")
    except BookAlreadyCheckedOut as e:
        print(f"[UNAVAILABLE] {e}")
    except BookNotFoundError as e:
        print(f"[NOT FOUND] {e}")
    except MemberNotFoundError as e:
        print(f"[MEMBER ERROR] {e}")
    except LibraryError as e:
        print(f"[LIBRARY ERROR] {e}")
```

---

## Exercise 4 — Logging Setup (25 min)

**File:** `ex04_logging_setup.py`

**Task:** Set up a professional logging configuration for a web application.

### Step 1 — Basic Logger with Two Handlers

```python
import logging
from logging.handlers import RotatingFileHandler

def create_app_logger(app_name: str, log_file: str) -> logging.Logger:
    """
    Create a logger with:
    1. A StreamHandler (console) at INFO level
    2. A RotatingFileHandler at DEBUG level
       - Max file size: 1 MB
       - Keep 2 backup files
    3. Format: "YYYY-MM-DD HH:MM:SS | LEVEL    | module:line | message"
    4. Logger level set to DEBUG
    
    Returns the configured logger.
    """
    # YOUR CODE HERE
    pass

# Test it:
logger = create_app_logger("webapp", "webapp.log")

logger.debug("App starting up...")           # Only in file
logger.info("Server listening on port 5000") # Console + file
logger.warning("Config file not found, using defaults")
logger.error("Database connection failed")
logger.critical("Out of memory!")
```

---

### Step 2 — Module-Level Loggers

```python
# Create three separate loggers for different modules of an app:
# "webapp.auth", "webapp.payments", "webapp.api"
# Each should:
# - Use the same format as above
# - Have propagate = False (so messages don't go to root logger too)
# - Write to a separate log file per module

auth_logger     = create_app_logger("webapp.auth",     "auth.log")
payments_logger = create_app_logger("webapp.payments", "payments.log")
api_logger      = create_app_logger("webapp.api",      "api.log")

# Simulate events:
auth_logger.info("User 'alice' logged in successfully.")
auth_logger.warning("Failed login attempt for user 'hacker' — 3rd attempt.")

payments_logger.info("Payment ₹500 processed for user 'alice'.")
payments_logger.error("Payment gateway timeout after 30s.", exc_info=False)

api_logger.debug("GET /api/v1/users?page=1 — 23 records returned.")
api_logger.info("POST /api/v1/orders — Order #1042 created.")
```

---

### Step 3 — Logging Exceptions Properly

```python
import json

logger = create_app_logger("parser", "parser.log")

def parse_json_config(json_string: str) -> dict:
    """
    Parse a JSON string into a dictionary.
    Log appropriately:
    - DEBUG when starting the parse
    - INFO when successful (log number of keys)
    - ERROR when parsing fails (use logger.exception for traceback)
    - WARNING when result is an empty dict
    
    Raise ValueError on parse failure.
    """
    # YOUR CODE HERE
    pass

# Test cases:
test_inputs = [
    '{"host": "localhost", "port": 5432, "db": "myapp"}',   # Valid
    '{}',                                                    # Empty (warning)
    'not valid json {{{',                                    # Invalid JSON
    None,                                                    # TypeError
]

for inp in test_inputs:
    try:
        config = parse_json_config(inp)
        if config:
            print(f"Parsed OK: {list(config.keys())}")
    except (ValueError, TypeError) as e:
        print(f"Failed: {e}")
```

---

## Exercise 5 — Full Integration: Banking System (40 min)

**File:** `ex05_banking_system.py`

**Task:** Build a complete banking module combining everything from today.

### Requirements

**Custom Exceptions:**
- `BankingError` (base)
  - `InvalidAccountError(account_id)`
  - `InsufficientFundsError(balance, requested_amount)`
  - `NegativeAmountError(amount)`
  - `DailyLimitExceededError(daily_limit, attempted_amount)`
  - `AccountFrozenError(account_id, reason)`

**`BankAccount` class:**
```
Attributes:
  - account_id: str
  - holder_name: str
  - balance: float
  - is_frozen: bool
  - freeze_reason: str
  - daily_withdrawal_limit: float (default: 10_000)
  - _daily_withdrawn: float (tracks today's withdrawals)

Methods:
  - deposit(amount) → None
  - withdraw(amount) → None
  - transfer_to(target_account, amount) → None
  - freeze(reason) → None
  - unfreeze() → None
  - get_statement() → str (formatted balance + status)
```

**Validation rules:**
- `deposit`: amount must be positive
- `withdraw`: amount positive, not exceeding balance, not exceeding daily limit, account not frozen
- `transfer_to`: same as withdraw + target account must not be frozen

**Logging requirements:**
- One logger per module: `logging.getLogger("banking.account")`
- DEBUG: each deposit/withdraw amount and resulting balance
- INFO: each successful transaction with account ID and new balance
- WARNING: when balance drops below ₹500 after a withdrawal
- ERROR: every exception raised (log before raising)
- RotatingFileHandler → `banking.log` (1 MB, 2 backups)
- StreamHandler → console (INFO and above only)

---

### Starter Code

```python
import logging
from logging.handlers import RotatingFileHandler
from datetime import date

# ── Set up logger ─────────────────────────────────────────────────────────────
# YOUR CODE HERE

# ── Custom Exceptions ─────────────────────────────────────────────────────────
# YOUR CODE HERE

# ── BankAccount Class ─────────────────────────────────────────────────────────
class BankAccount:
    LOW_BALANCE_THRESHOLD = 500.0
    
    def __init__(self, account_id: str, holder_name: str,
                 initial_balance: float = 0.0,
                 daily_withdrawal_limit: float = 10_000.0):
        # YOUR CODE HERE
        pass
    
    def deposit(self, amount: float) -> None:
        # YOUR CODE HERE
        pass
    
    def withdraw(self, amount: float) -> None:
        # YOUR CODE HERE
        pass
    
    def transfer_to(self, target: "BankAccount", amount: float) -> None:
        # YOUR CODE HERE
        pass
    
    def freeze(self, reason: str) -> None:
        # YOUR CODE HERE
        pass
    
    def unfreeze(self) -> None:
        # YOUR CODE HERE
        pass
    
    def get_statement(self) -> str:
        status = "FROZEN" if self.is_frozen else "ACTIVE"
        return (
            f"Account: {self.account_id} | Holder: {self.holder_name}\n"
            f"Balance: ₹{self.balance:.2f} | Status: {status}\n"
            f"Daily withdrawn: ₹{self._daily_withdrawn:.2f} / ₹{self.daily_withdrawal_limit:.2f}"
        )
    
    def __repr__(self):
        return f"BankAccount({self.account_id}, {self.holder_name}, ₹{self.balance:.2f})"
```

---

### Test Script

```python
# Run this after implementing BankAccount:

if __name__ == "__main__":
    # Create accounts
    alice = BankAccount("ACC001", "Alice",  initial_balance=5000.0)
    bob   = BankAccount("ACC002", "Bob",    initial_balance=1000.0)
    
    print("=== Initial Statements ===")
    print(alice.get_statement())
    print()
    print(bob.get_statement())
    print()
    
    print("=== Transactions ===")
    
    # Test 1: Successful deposit
    alice.deposit(2000)
    
    # Test 2: Successful withdrawal
    alice.withdraw(1000)
    
    # Test 3: Transfer
    alice.transfer_to(bob, 500)
    
    # Test 4: InsufficientFundsError
    try:
        bob.withdraw(10000)
    except InsufficientFundsError as e:
        print(f"[EXPECTED] {e}")
    
    # Test 5: NegativeAmountError
    try:
        alice.deposit(-100)
    except NegativeAmountError as e:
        print(f"[EXPECTED] {e}")
    
    # Test 6: DailyLimitExceededError
    try:
        alice.withdraw(15000)
    except DailyLimitExceededError as e:
        print(f"[EXPECTED] {e}")
    
    # Test 7: Freeze and attempt transaction
    alice.freeze("Suspicious activity detected")
    try:
        alice.withdraw(100)
    except AccountFrozenError as e:
        print(f"[EXPECTED] {e}")
    
    alice.unfreeze()
    alice.withdraw(100)  # Should work now
    
    print("\n=== Final Statements ===")
    print(alice.get_statement())
    print()
    print(bob.get_statement())
```

---

## Exercise 6 — Challenge: Retry Decorator with Exponential Backoff (Stretch Goal)

**File:** `ex06_retry_decorator.py`

**Task:** Implement a production-grade `@retry` decorator.

### Requirements

```python
import functools
import time
import logging
import random

logger = logging.getLogger(__name__)

def retry(max_attempts=3, base_delay=1.0, backoff_factor=2.0,
          exceptions=(Exception,), on_failure=None):
    """
    Decorator factory that retries a function on specified exceptions.
    
    Parameters:
        max_attempts  — total number of attempts (including first)
        base_delay    — initial delay in seconds between retries
        backoff_factor — multiply delay by this after each failure
                         (exponential backoff: 1s, 2s, 4s, 8s...)
        exceptions    — tuple of exception types to retry on
        on_failure    — optional callback(exception, attempt_number) called on each failure
    
    Logging:
        - DEBUG: "Attempt {n}/{max} for {func_name}()"
        - WARNING: "Attempt {n} failed: {error}. Retrying in {delay}s..."
        - ERROR: "All {max} attempts failed for {func_name}(). Final error: {error}"
        - INFO: "{func_name}() succeeded on attempt {n}"
    
    Behaviour:
        - Retry only on exceptions listed in `exceptions`
        - Use exponential backoff: delay * (backoff_factor ** (attempt - 1))
        - After max_attempts, re-raise the last exception
        - If on_failure is provided, call it after each failed attempt
        - Preserve function name and docstring (use functools.wraps)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # YOUR CODE HERE
            pass
        return wrapper
    return decorator


# ── Test It ───────────────────────────────────────────────────────────────────

# Simulated flaky function — succeeds on 3rd call
call_count = 0

@retry(max_attempts=4, base_delay=0.1, backoff_factor=2.0,
       exceptions=(ConnectionError, TimeoutError))
def flaky_api_call(endpoint: str):
    """Fetch data from a flaky API endpoint."""
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError(f"Connection refused to {endpoint}")
    return {"data": "success", "attempt": call_count}

# Test 1: Should succeed on attempt 3
call_count = 0
result = flaky_api_call("https://api.example.com/data")
print(f"Result: {result}")

# Test 2: Always fails — should re-raise after max_attempts
@retry(max_attempts=3, base_delay=0.1)
def always_fails():
    raise ValueError("This always fails")

try:
    always_fails()
except ValueError as e:
    print(f"Expected failure: {e}")

# Test 3: Non-retryable exception — should fail immediately
@retry(max_attempts=3, base_delay=0.1, exceptions=(ConnectionError,))
def wrong_type_error():
    raise ValueError("Not a ConnectionError — should NOT retry")

try:
    wrong_type_error()
except ValueError as e:
    print(f"Non-retryable: {e}")
```

---

## ✅ Exercise Checklist

| Exercise | What You Practised | Done? |
|---|---|---|
| Ex 1 — Traceback Reading | Understanding error messages | ⬜ |
| Ex 2 — Safe Operations | try/except/else/finally patterns | ⬜ |
| Ex 3 — Custom Exceptions | Exception hierarchy, custom attributes | ⬜ |
| Ex 4 — Logging Setup | Handlers, formatters, levels, exc_info | ⬜ |
| Ex 5 — Banking System | Full integration of exceptions + logging | ⬜ |
| Ex 6 — Retry Decorator | Decorators, backoff, advanced patterns | ⬜ |

---

## 💡 Hints & Tips

### Exercise 2 Hints
- For `safe_divide`: catch `ZeroDivisionError` and `TypeError` separately
- For `get_user_field`: `None.get()` raises `AttributeError`, not `TypeError`
- For `read_file_safely`: open the file before the try block, or handle the case where `f` may not be defined in finally

### Exercise 3 Hints
- `BookAlreadyCheckedOut.__init__` should take `book_id` and `title`
- In `checkout_book`, check member → book → fines → availability (in this order)
- Use `raise LibraryError(...)` not `raise LibraryError` (without instantiation)

### Exercise 4 Hints
- `logger.addHandler()` can be called multiple times — once per handler
- Set `logger.propagate = False` when you don't want messages going to root logger
- `exc_info=True` in `logger.error()` is equivalent to calling `logger.exception()`

### Exercise 5 Hints
- `_daily_withdrawn` should reset each new day — use `date.today()` and store the last reset date
- In `transfer_to`, call `self.withdraw(amount)` then `target.deposit(amount)` — handle the exception if withdraw fails
- The WARNING for low balance should be checked *after* updating the balance

### Exercise 6 Hints
- The delay for attempt N is: `base_delay * (backoff_factor ** (N - 1))`
- Use `time.sleep(delay)` between attempts
- Only retry if `isinstance(exception, exceptions)` — otherwise re-raise immediately
- Return the function result when an attempt succeeds
