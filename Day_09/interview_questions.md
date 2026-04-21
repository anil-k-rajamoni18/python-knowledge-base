# Day 9 — Interview Questions: Python Exception Handling & Logging
### Python Full Stack Bootcamp | Interview Prep Reference

---

> 💡 **How to use this file:** Questions are grouped by difficulty. Study the concept, then try answering before reading the model answer. For senior roles, be ready to write code on a whiteboard or in a shared editor.

---

## 🟢 Beginner Level (0–1 Year Experience)

---

**Q1. What is an exception in Python? How is it different from a syntax error?**

**Model Answer:**
An exception is a runtime error — it occurs while the program is executing, after it has already been parsed successfully. A syntax error, on the other hand, is caught by the Python parser *before* execution begins and prevents the program from running at all.

Examples:
- `SyntaxError`: `if x =  5:` — invalid Python grammar
- `RuntimeError/Exception`: `int("abc")` — valid syntax, but fails at runtime because `"abc"` can't be converted to an integer

Exceptions can be caught and handled using `try/except`; syntax errors cannot.

---

**Q2. Explain the purpose of each block: `try`, `except`, `else`, `finally`.**

**Model Answer:**
- **`try`** — wraps the code that might raise an exception. Always executed.
- **`except`** — runs only if an exception is raised in the `try` block. Can catch specific or multiple exception types.
- **`else`** — runs only if the `try` block completed *without* any exception being raised. Useful for code that should only run on success.
- **`finally`** — always runs, whether or not an exception occurred. Used for cleanup (closing files, releasing locks, closing DB connections).

```python
try:
    f = open("data.txt")
    data = f.read()
except FileNotFoundError:
    print("File missing")
else:
    print("File read OK:", len(data), "bytes")
finally:
    print("Done")  # Always prints
```

---

**Q3. What is the output of this code?**

```python
def test():
    try:
        return "try"
    finally:
        return "finally"

print(test())
```

**Model Answer:** `finally`

`finally` always executes before a `return` in `try` takes effect. Since `finally` also contains a `return`, it overrides the `try` return value. This behaviour is generally a code smell — avoid `return` in `finally`.

---

**Q4. What is the difference between `raise` and `raise e`?**

**Model Answer:**
- `raise` (bare) — re-raises the *current* active exception, preserving the original traceback. Use this when you've caught an exception, done something (like logging), and want to propagate it up.
- `raise e` — raises the exception object `e`, but the traceback is reset to the current line. The original stack trace is lost.

```python
try:
    int("abc")
except ValueError as e:
    logger.error("Failed: %s", e)
    raise        # ✅ Preserves original traceback
    # raise e    # ❌ Loses original traceback
```

---

**Q5. Name five common built-in exception types and when they occur.**

**Model Answer:**
| Exception | When It Occurs |
|---|---|
| `ValueError` | Right type, wrong value — `int("abc")` |
| `TypeError` | Wrong type passed — `"a" + 1` |
| `KeyError` | Dictionary key doesn't exist — `d["missing"]` |
| `IndexError` | List index out of range — `lst[99]` on a 3-element list |
| `FileNotFoundError` | File doesn't exist — `open("ghost.txt")` |
| `ZeroDivisionError` | Division by zero — `10 / 0` |
| `AttributeError` | Object doesn't have the attribute — `None.strip()` |

---

**Q6. What are the five logging levels in Python? What is the default level?**

**Model Answer:**
| Level | Numeric Value | Use Case |
|---|---|---|
| `DEBUG` | 10 | Detailed diagnostic information |
| `INFO` | 20 | Normal operational events |
| `WARNING` | 30 | Something unexpected but non-fatal |
| `ERROR` | 40 | A failure that needs attention |
| `CRITICAL` | 50 | Severe failure, application may crash |

The default level for the root logger is `WARNING` — meaning only `WARNING`, `ERROR`, and `CRITICAL` messages are shown unless you change it with `basicConfig(level=logging.DEBUG)`.

---

**Q7. What is the difference between `logger.error("msg")` and `logger.exception("msg")`?**

**Model Answer:**
Both log at `ERROR` level, but `logger.exception()` automatically includes the current exception's traceback information (equivalent to `logger.error("msg", exc_info=True)`). `logger.exception()` should only be called inside an `except` block.

```python
try:
    int("abc")
except ValueError:
    logger.error("Failed")       # Logs "Failed" at ERROR, no traceback
    logger.exception("Failed")   # Logs "Failed" at ERROR + full traceback
```

---

## 🟡 Intermediate Level (1–2 Years Experience)

---

**Q8. What is exception chaining? What does `raise X from Y` do?**

**Model Answer:**
Exception chaining links a new exception to its original cause. `raise X from Y` stores `Y` as `X.__cause__`, making the causal relationship explicit when the traceback is displayed. This is used when you want to translate a low-level error into a higher-level domain error without losing the original cause.

```python
def get_config(key):
    config = {"host": "localhost"}
    try:
        return config[key]
    except KeyError as e:
        raise ValueError(f"Configuration key '{key}' is required") from e

try:
    get_config("port")
except ValueError as e:
    print(e)           # Configuration key 'port' is required
    print(e.__cause__) # 'port'
```

`raise X from None` suppresses the original exception chain completely.

---

**Q9. What is the difference between EAFP and LBYL? Which does Python prefer and why?**

**Model Answer:**
- **LBYL (Look Before You Leap):** Check preconditions before acting.
  ```python
  if key in dictionary:
      value = dictionary[key]
  ```
- **EAFP (Easier to Ask Forgiveness than Permission):** Try the action; handle failure.
  ```python
  try:
      value = dictionary[key]
  except KeyError:
      handle_missing()
  ```

Python *prefers EAFP* because:
1. It avoids race conditions (the check and the action are separate; state can change between them)
2. It's often more readable and concise
3. It follows Python's duck-typing philosophy — don't check types, just try
4. It's faster when success is the common case (no double lookup)

---

**Q10. How do you create a custom exception hierarchy? Why would you do this?**

**Model Answer:**
You create a base exception for your module/domain and have specific exceptions inherit from it. This allows callers to catch all errors from your module with one `except` clause, or catch specific errors individually.

```python
class AppError(Exception):
    """Base for all application errors."""
    pass

class DatabaseError(AppError):
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field = field
        super().__init__(f"Validation failed on '{field}': {message}")

class NotFoundError(AppError):
    def __init__(self, resource, identifier):
        super().__init__(f"{resource} with id={identifier} not found.")

# Caller can catch all app errors:
try:
    process()
except AppError as e:
    handle(e)

# Or specific ones:
try:
    process()
except ValidationError as e:
    return 400, str(e)
except NotFoundError as e:
    return 404, str(e)
```

---

**Q11. What is a `RotatingFileHandler` and why is it important in production?**

**Model Answer:**
`RotatingFileHandler` automatically creates a new log file when the current one reaches a specified size (`maxBytes`), and keeps a configurable number of backup files (`backupCount`). For example, with `maxBytes=5MB` and `backupCount=3`, you'd have `app.log`, `app.log.1`, `app.log.2`, `app.log.3` — the oldest is deleted when a new rotation occurs.

This is critical in production because:
- Without rotation, log files grow unboundedly and fill up disk space, potentially crashing the server
- It provides a predictable, bounded disk footprint
- Old logs are preserved for a configurable retention period

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=5 * 1024 * 1024,   # 5 MB
    backupCount=3
)
```

---

**Q12. What is logger propagation? How do you prevent it?**

**Model Answer:**
By default, when a logger handles a message, it also passes it up to its parent logger (the root logger). This is called propagation. If both a child logger and the root logger have handlers, the message gets logged twice.

```python
# Problem: message logged twice
child_logger = logging.getLogger("myapp.module")
child_logger.addHandler(file_handler)
# Message goes to file_handler AND root logger's handler

# Solution: disable propagation
child_logger.propagate = False
```

In practice, set `propagate = False` on named loggers that have their own handlers, to avoid duplicate log entries.

---

**Q13. Why should you use `logger.info("User %s logged in", username)` instead of `logger.info(f"User {username} logged in")`?**

**Model Answer:**
With f-strings, Python evaluates the string *immediately*, before calling the logger. If the message would be filtered out (e.g., the level is set to WARNING), the string was still built — wasting CPU and memory.

With `%s` style, the string is only formatted *if the message will actually be emitted* — Python checks the level first. For high-volume applications logging millions of DEBUG messages, this makes a significant performance difference.

```python
# Wasteful — always builds the string even if DEBUG is filtered
logger.debug(f"Processing record: {json.dumps(large_object)}")

# Efficient — only builds the string if DEBUG is enabled
logger.debug("Processing record: %s", large_object)
```

---

## 🔴 Advanced Level (2+ Years / Senior Roles)

---

**Q14. Explain the logging module's hierarchy and how it interacts with propagation.**

**Model Answer:**
Python loggers are organized in a namespace hierarchy using dots as separators, mirroring the module structure. `logging.getLogger("banking.accounts")` is a child of `logging.getLogger("banking")`, which is a child of the root logger.

When a message is logged:
1. The logger checks if the message's level meets its own threshold
2. If yes, the message is passed to all of the logger's handlers
3. If `propagate=True` (default), the message is then passed to the parent logger — and so on up the chain to the root

This allows hierarchical configuration: set `logging.getLogger("banking").setLevel(logging.DEBUG)` to enable verbose logging for the entire banking subsystem without affecting other modules.

```
Root Logger (WARNING)
└── banking (DEBUG)     ← matches all banking.* loggers
    ├── banking.accounts (inherits DEBUG)
    └── banking.payments (inherits DEBUG)
```

---

**Q15. How would you implement structured logging in Python? Why is it preferred in microservices?**

**Model Answer:**
Structured logging outputs log records as machine-readable JSON instead of human-readable text. This makes logs easily searchable, filterable, and parseable by log aggregation tools like Elasticsearch, Datadog, or CloudWatch.

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
        }
        # Include exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        # Include any extra fields
        for key, value in record.__dict__.items():
            if key not in ("msg", "args", "exc_info", "exc_text", "stack_info",
                           "lineno", "funcName", "created", "msecs", "relativeCreated",
                           "thread", "threadName", "processName", "process",
                           "name", "levelname", "levelno", "pathname", "filename",
                           "module", "getMessage"):
                if not key.startswith("_"):
                    log_entry[key] = value
        return json.dumps(log_entry)

# Usage
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("api")
logger.addHandler(handler)

# Add context to log entries
logger.info("Payment processed", extra={
    "user_id": "user_123",
    "amount": 500.00,
    "currency": "INR",
    "transaction_id": "txn_abc123"
})
# Output: {"timestamp": "2024-01-15T10:23:45Z", "level": "INFO", "message": "Payment processed", "user_id": "user_123", ...}
```

In microservices, JSON logs can be shipped to a central aggregator (ELK Stack, Splunk) and queried like a database: `level:ERROR AND service:payment AND user_id:user_123`.

---

**Q16. What are Exception Groups (Python 3.11+)? When would you use them?**

**Model Answer:**
Exception Groups (`ExceptionGroup`) allow multiple exceptions to be raised and handled simultaneously. They are useful in concurrent or parallel code where multiple tasks can fail independently and you want to report all failures rather than just the first.

```python
# Python 3.11+
import asyncio

async def fetch(url):
    if "bad" in url:
        raise ValueError(f"Bad URL: {url}")
    return f"data from {url}"

async def fetch_all(urls):
    results = []
    exceptions = []
    for url in urls:
        try:
            results.append(await fetch(url))
        except ValueError as e:
            exceptions.append(e)
    if exceptions:
        raise ExceptionGroup("Fetch errors", exceptions)
    return results

# Handling with except*
try:
    asyncio.run(fetch_all(["http://good.com", "http://bad.com", "http://bad2.com"]))
except* ValueError as eg:
    print(f"Got {len(eg.exceptions)} ValueError(s):")
    for e in eg.exceptions:
        print(f"  - {e}")
```

`except*` (with asterisk) is a new syntax specifically for `ExceptionGroup` — it matches all exceptions of the specified type within the group and lets the rest propagate.

---

**Q17. You have a Flask API and you want ALL unhandled exceptions to be logged with context (user ID, request path, timestamp) and return a clean JSON error response. How do you design this?**

**Model Answer:**
Use Flask's `@app.errorhandler(Exception)` combined with a structured logging setup and request context injection.

```python
import logging
import traceback
from flask import Flask, request, jsonify, g
import uuid

app = Flask(__name__)
logger = logging.getLogger("api")

# Middleware: inject request ID for tracing
@app.before_request
def inject_request_id():
    g.request_id = str(uuid.uuid4())[:8]

# Global exception handler
@app.errorhandler(Exception)
def handle_unexpected_error(error):
    logger.error(
        "Unhandled exception | request_id=%s | path=%s | method=%s | user=%s | error=%s",
        g.get("request_id", "N/A"),
        request.path,
        request.method,
        g.get("user_id", "anonymous"),
        str(error),
        exc_info=True   # Includes full traceback
    )
    return jsonify({
        "error": "Internal server error",
        "request_id": g.get("request_id")  # Return request_id for support tickets
    }), 500

# Domain-specific handler
class ResourceNotFoundError(Exception):
    pass

@app.errorhandler(ResourceNotFoundError)
def handle_not_found(error):
    logger.warning("Resource not found: %s | path=%s", error, request.path)
    return jsonify({"error": str(error)}), 404
```

Key design principles:
1. Log the full traceback (`exc_info=True`) for unexpected errors
2. Return a clean, user-safe error message (don't expose internal details)
3. Include a `request_id` in both the log and the response so you can correlate them
4. Use separate handlers for expected domain errors vs unexpected exceptions

---

**Q18. What is the difference between `logging.warning()` and `logging.getLogger(__name__).warning()`? Which should you use in a library?**

**Model Answer:**
`logging.warning()` logs to the **root logger** — a global, shared object. In a library, this is dangerous because:
- You may interfere with the application's logging configuration
- All library messages appear under the root logger, not namespaced to your library
- The application developer has no way to selectively control your library's logging level

`logging.getLogger(__name__)` creates (or retrieves) a logger named after your module (e.g., `mylib.utils`). This is the correct approach in library code because:
- Messages are namespaced — the application can do `logging.getLogger("mylib").setLevel(logging.ERROR)` to silence your library
- The library adds no handlers — it just logs; the application decides where those logs go
- Follows the "configure once, at the top" principle

**Rule:** In *applications*, configure the root logger once. In *libraries*, never configure the root logger — only use `getLogger(__name__)`.

---

## 🎯 Rapid-Fire Questions

**Q. Can you have multiple `except` blocks?** → Yes, as many as needed. Most specific first.

**Q. What does `except Exception as e: pass` do?** → Silently swallows all exceptions. Almost always wrong.

**Q. What exception does `sys.exit()` raise?** → `SystemExit` (subclass of `BaseException`, not `Exception`).

**Q. How do you log to multiple destinations simultaneously?** → Add multiple Handlers to the same Logger.

**Q. What is `__cause__` vs `__context__` in exceptions?** → `__cause__` is set by `raise X from Y` (explicit chain); `__context__` is set automatically when an exception is raised during handling of another (implicit chain).

**Q. What is `logging.NullHandler()`?** → A handler that does nothing. Best practice in libraries: add it to prevent "No handlers could be found" warnings if the application hasn't configured logging.

**Q. What's the difference between `WARNING` and `ERROR` log levels?** → `WARNING`: something unexpected happened but the operation succeeded. `ERROR`: the operation failed.

**Q. Can `finally` block suppress an exception?** → Yes, if `finally` contains a `return` or `break` statement — those swallow the exception. Generally avoid this.

---

## 📝 Coding Interview Questions

**CI-1.** Write a function `safe_int(value)` that tries to convert `value` to an integer. Return the integer on success, `None` on failure. Log a warning if conversion fails.

**CI-2.** Implement a `retry` decorator that retries a function up to N times with a delay, only on `ConnectionError`. Log each retry attempt.

**CI-3.** Create a `TransactionError` custom exception with attributes `transaction_id`, `reason`, and `timestamp`. Make it printable with all three values.

**CI-4.** You have a `process_records(records)` function. Write it so that if a single record fails processing, it logs the error and continues with the rest (not crashing the whole batch). Return a summary `{"processed": N, "failed": M}`.

**CI-5.** Explain what this code does and what's wrong with it:
```python
try:
    result = risky()
except Exception:
    pass
```
*Answer: Silently swallows all exceptions including bugs in your own code. Should at minimum log the error: `logger.exception("risky() failed")`*
