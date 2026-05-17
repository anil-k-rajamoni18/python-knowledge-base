# Python Exception Handling: 🛡️

## 1️⃣ What is an Exception?

An **exception** is a runtime error that disrupts the normal flow of a program. When Python encounters an error, it creates an exception object. If your program doesn't handle it, the program will crash and stop executing.

**Common examples that trigger exceptions:**

* **Dividing by zero** — mathematical impossibility
* **Accessing an invalid index** — trying to reach an element that doesn't exist
* **Opening a file that doesn't exist** — file system error
* **Converting invalid input** — type mismatch
* **Accessing a dictionary key that doesn't exist** — key not found
* **Calling a method on None** — attempting operations on null values

```python
print(10 / 0)   # ZeroDivisionError: division by zero
print([1, 2, 3][5])  # IndexError: list index out of range
int("hello")  # ValueError: invalid literal for int()
None.something()  # AttributeError: 'NoneType' object has no attribute 'something'
```

---

## 2️⃣ Why Exception Handling? 🤔

**Scenario Without Exception Handling:**
```python
# User inputs "0" when we ask for divisor
print("Enter a number to divide 10 by:")
number = int(input())
result = 10 / number  # CRASH if user enters 0
print(f"Result: {result}")
print("Thank you for using our calculator!")  # Never executes
```

If the user enters `0`, the program crashes with `ZeroDivisionError` and the "Thank you" message never prints.

**Benefits of Exception Handling:**

Without handling, your program crashes and users lose trust. With handling, the program continues safely, you control error messages, users see helpful feedback, and you can implement recovery strategies. This is essential for production applications, web servers, mobile apps, and any software users depend on.

```python
print("Enter a number to divide 10 by:")
try:
    number = int(input())
    result = 10 / number
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Error: Cannot divide by zero! Please try again.")
except ValueError:
    print("Error: Please enter a valid number!")
print("Thank you for using our calculator!")  # Always executes
```

Now if the user enters `0` or invalid text, the program handles it gracefully.

---

## 3️⃣ Basic `try` – `except` Block

The most fundamental exception handling structure consists of a `try` block where you place risky code, and an `except` block where you handle errors.

**Syntax:**
```python
try:
    risky_code_here
except ErrorType:
    code_to_handle_error
    can_have_multiple_lines
```

**How it works:**
1. Python executes code in the `try` block
2. If an exception of type `ErrorType` occurs, the `try` block stops immediately
3. Control jumps to the `except` block
4. The `except` block executes
5. Program continues after the try-except structure

**Example 1: Division Error**
```python
try:
    x = int(input("Enter a number: "))
    print(10 / x)
except ZeroDivisionError:
    print("Cannot divide by zero")

# Output if user enters 0:
# Cannot divide by zero
```

**Example 2: Type Conversion Error**
```python
try:
    age = int(input("Enter your age: "))
    print(f"Next year you'll be {age + 1}")
except ValueError:
    print("Invalid input! Age must be a number")

# Output if user enters "abc":
# Invalid input! Age must be a number
```

**Example 3: Index Out of Range**
```python
try:
    fruits = ["apple", "banana", "orange"]
    print(fruits[10])  # Only indices 0, 1, 2 exist
except IndexError:
    print("That fruit index doesn't exist!")

# Output:
# That fruit index doesn't exist!
```

---

## 4️⃣ Catching Multiple Exceptions 🎯

Different errors might occur in your `try` block, and you can handle each one differently.

**Example 1: Calculator with Multiple Errors**
```python
try:
    x = int(input("Enter first number: "))
    y = int(input("Enter second number: "))
    result = x / y
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Error: Division by zero is not allowed!")
except ValueError:
    print("Error: Invalid input! Please enter valid numbers")

# Scenario 1 - User enters "abc":
# Error: Invalid input! Please enter valid numbers

# Scenario 2 - User enters 0 for second number:
# Error: Division by zero is not allowed!
```

**Example 2: List Processing with Multiple Errors**
```python
try:
    user_data = input("Enter list index and operation (e.g., '0 * 2'): ")
    index, operation = user_data.split()
    index = int(index)
    
    numbers = [10, 20, 30]
    value = numbers[index]  # Can raise IndexError
    result = eval(f"{value} {operation}")  # Can raise various errors
    print(f"Result: {result}")
except ValueError:
    print("Error: Index must be a number!")
except IndexError:
    print("Error: Index out of range!")
except ZeroDivisionError:
    print("Error: Cannot perform division by zero!")
except Exception as e:
    print(f"Unexpected error: {e}")
```

**Example 3: File and Data Processing**
```python
try:
    filename = input("Enter filename: ")
    lines_to_read = int(input("How many lines? "))
    
    with open(filename) as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: File '{filename}' not found!")
except ValueError:
    print("Error: Number of lines must be an integer!")
except Exception as e:
    print(f"Unexpected error: {e}")
```

**Best Practice:** Order your exceptions from most specific to least specific:
```python
try:
    risky_code()
except ZeroDivisionError:  # Specific
    handle_zero_division()
except ValueError:  # Specific
    handle_value_error()
except Exception:  # Generic (catches everything else)
    handle_generic_error()
```

---

## 5️⃣ Generic `except` (Proceed with Caution) ⚠️

The `Exception` class catches most errors. Using it without specific error types can hide bugs.

**Example 1: Logging All Errors**
```python
try:
    print(10 / 0)
except Exception as e:
    print(f"Error occurred: {e}")
    # In real apps, log this to a file
    # logger.error(f"Exception: {e}")
```

**Example 2: What NOT to Do**
```python
try:
    user_input = int(input("Enter a number: "))
    result = 100 / user_input
except:  # BAD: catches ALL exceptions, including typos in code
    print("Something went wrong")
```

This catches `ZeroDivisionError`, `ValueError`, and even if you accidentally typed `resultt` instead of `result` (NameError). This makes debugging extremely difficult.

**Example 3: Proper Generic Handling**
```python
try:
    data = process_user_data(user_input)
except (ValueError, TypeError, KeyError) as e:  # Specific exceptions
    print(f"Data processing error: {e}")
except Exception as e:  # Fallback for unexpected errors
    print(f"Unexpected error: {e}")
    # Log this for debugging
```

**When to use generic except:**
* Logging errors in production
* Graceful degradation
* Last-resort error handling

**Never use empty `except:`:**
```python
# NEVER DO THIS:
try:
    dangerous_operation()
except:  # Catches everything silently
    pass  # Errors disappear without trace
```

---

## 6️⃣ `else` Block (Runs When NO Exception Occurs) ✨

The `else` block executes only if the `try` block succeeds without exceptions. This separates success logic from error handling.

**Example 1: File Processing**
```python
try:
    num = int(input("Enter a number: "))
    result = 100 / num
except ZeroDivisionError:
    print("Cannot divide by zero!")
except ValueError:
    print("Please enter a valid number!")
else:
    print(f"Success! The result is: {result}")
```

**Output scenarios:**
```
User enters "10":
Success! The result is: 10.0

User enters "0":
Cannot divide by zero!

User enters "abc":
Please enter a valid number!
```

**Example 2: Reading and Processing Files**
```python
filename = input("Enter filename: ")

try:
    file = open(filename, 'r')
    data = file.read()
except FileNotFoundError:
    print(f"Error: Cannot find {filename}")
else:
    lines = data.split('\n')
    print(f"File successfully read with {len(lines)} lines")
    file.close()
```

**Example 3: API Call Success Logic**
```python
try:
    response = requests.get("https://api.example.com/data")
    response.raise_for_status()  # Raises exception if status is not 200
except requests.ConnectionError:
    print("Network error: Cannot connect to server")
except requests.HTTPError as e:
    print(f"Server error: {e.response.status_code}")
else:
    data = response.json()
    print(f"Successfully fetched {len(data)} records")
```

**Why use `else`?**
* Keeps success code separate from error handling
* Makes code more readable
* Prevents putting too much code in the `try` block
* Only executes if everything goes right

---

## 7️⃣ `finally` Block (Always Executes) 🔒

The `finally` block always runs, regardless of whether an exception occurred. It's perfect for cleanup tasks.

**When to use `finally`:**
* Closing files
* Releasing database connections
* Cleaning up resources
* Resetting state
* Logging completion

**Example 1: File Handling**
```python
try:
    f = open("data.txt", 'r')
    content = f.read()
    print(content)
except FileNotFoundError:
    print("File not found!")
finally:
    print("Closing file...")
    f.close()  # This always runs, even if exception occurred
```

**Example 2: Database Operations**
```python
db = None
try:
    db = connect_to_database("localhost", "mydb")
    db.execute("SELECT * FROM users")
    print("Query successful")
except ConnectionError:
    print("Failed to connect to database")
except Exception as e:
    print(f"Query error: {e}")
finally:
    if db:
        print("Closing database connection...")
        db.close()
```

**Example 3: Resource Management**
```python
try:
    print("Starting operation...")
    result = perform_risky_operation()
    print(f"Operation result: {result}")
except TimeoutError:
    print("Operation timed out!")
except RuntimeError as e:
    print(f"Runtime error: {e}")
finally:
    print("Cleaning up resources...")
    cleanup_resources()
    print("Done!")
```

**Flow Visualization:**
```
try block executes
    ↓
If exception: except block runs
If no exception: else block runs (if present)
    ↓
finally block ALWAYS runs
    ↓
Program continues
```

**Example 4: Complete Flow**
```python
try:
    x = int(input("Enter number: "))
    result = 10 / x
    print(f"Calculation done")
except ZeroDivisionError:
    print("Cannot divide by zero")
except ValueError:
    print("Invalid number")
else:
    print(f"Result is: {result}")
finally:
    print("Cleanup complete")

# Possible outputs:
# User enters "5":
# Calculation done
# Result is: 2.0
# Cleanup complete

# User enters "0":
# Cannot divide by zero
# Cleanup complete

# User enters "abc":
# Invalid number
# Cleanup complete
```

---

## 8️⃣ Common Built-in Exceptions 📚

Understanding common exceptions helps you write better error handling.

| Exception | When It Occurs | Example |
|-----------|---|---|
| **ZeroDivisionError** | Divide by zero | `10 / 0` |
| **ValueError** | Wrong type conversion | `int("abc")` |
| **TypeError** | Invalid operation between types | `"text" + 5` |
| **IndexError** | Invalid list/tuple index | `[1, 2, 3][10]` |
| **KeyError** | Missing dictionary key | `{"a": 1}["b"]` |
| **FileNotFoundError** | File doesn't exist | `open("missing.txt")` |
| **ImportError** | Module not found | `import nonexistent_module` |
| **AttributeError** | Missing attribute/method | `None.something()` |
| **NameError** | Undefined variable | `print(undefined_var)` |
| **RuntimeError** | Generic runtime error | Various situations |

**Detailed Examples:**

```python
# ZeroDivisionError
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")

# ValueError - type conversion
try:
    age = int("twenty-five")
except ValueError:
    print("Age must be a number!")

# TypeError - wrong operation type
try:
    result = "hello" + 5
except TypeError:
    print("Cannot add string and integer!")

# IndexError
try:
    numbers = [1, 2, 3]
    print(numbers[100])
except IndexError:
    print("Index out of range!")

# KeyError
try:
    user = {"name": "John", "age": 25}
    print(user["email"])
except KeyError:
    print("Email key not found in user data!")

# FileNotFoundError
try:
    with open("settings.json") as f:
        config = json.load(f)
except FileNotFoundError:
    print("Configuration file not found!")
    config = {}

# AttributeError
try:
    data = None
    print(data.something())
except AttributeError:
    print("Cannot access attribute on None!")

# ImportError
try:
    import pandas_advanced  # Doesn't exist
except ImportError:
    print("Required module not installed!")
    print("Install it with: pip install pandas")
```

---

## 9️⃣ Real-World Example: List Processing 🔄

Processing data while handling multiple possible errors:

```python
numbers = ["10", "20", "abc", "30", "zero", "40"]

print("Processing numbers...")
processed = []
errors = []

for i, n in enumerate(numbers):
    try:
        value = int(n)
        result = 100 / value
        processed.append(result)
        print(f"✓ Index {i}: {n} → Result: {result}")
    except ValueError:
        errors.append(f"Index {i}: '{n}' is not a number")
        print(f"✗ Index {i}: '{n}' is not a valid number")
    except ZeroDivisionError:
        errors.append(f"Index {i}: Cannot divide by {n}")
        print(f"✗ Index {i}: Cannot divide by {n}")

print(f"\nProcessed {len(processed)} items successfully")
if errors:
    print(f"\nErrors encountered ({len(errors)}):")
    for error in errors:
        print(f"  - {error}")

# Output:
# Processing numbers...
# ✓ Index 0: 10 → Result: 10.0
# ✓ Index 1: 20 → Result: 5.0
# ✗ Index 2: 'abc' is not a valid number
# ✓ Index 3: 30 → Result: 3.3333...
# ✗ Index 4: 'zero' is not a valid number
# ✓ Index 5: 40 → Result: 2.5
# 
# Processed 4 items successfully
# 
# Errors encountered (2):
#   - Index 2: 'abc' is not a number
#   - Index 4: 'zero' is not a number
```

**Another Example: Data Validation Pipeline**
```python
def process_user_records(records):
    valid = []
    invalid = []
    
    for i, record in enumerate(records):
        try:
            # Try to convert age
            age = int(record.get("age", ""))
            
            # Validate email exists
            if "email" not in record:
                raise KeyError("email field missing")
            
            # Validate age range
            if age < 18 or age > 120:
                raise ValueError(f"Age {age} out of valid range")
            
            valid.append(record)
            
        except ValueError as e:
            invalid.append({"index": i, "error": f"Invalid value: {e}"})
        except KeyError as e:
            invalid.append({"index": i, "error": f"Missing field: {e}"})
        except Exception as e:
            invalid.append({"index": i, "error": f"Unknown error: {e}"})
    
    return valid, invalid

# Test
records = [
    {"name": "John", "age": "25", "email": "john@email.com"},
    {"name": "Jane", "age": "abc", "email": "jane@email.com"},  # Invalid age
    {"name": "Bob", "age": "30"},  # Missing email
    {"name": "Alice", "age": "150", "email": "alice@email.com"},  # Age out of range
]

valid, invalid = process_user_records(records)
print(f"Valid records: {len(valid)}")
print(f"Invalid records: {len(invalid)}")
for inv in invalid:
    print(f"  Record {inv['index']}: {inv['error']}")
```

---

## 🔟 Nested `try-except` Blocks 🎁

You can place `try-except` blocks inside other `try-except` blocks. Use sparingly as it can reduce readability.

**Example 1: Nested File and Data Processing**
```python
try:
    filename = input("Enter filename: ")
    file = open(filename)
    
    try:
        content = file.read()
        lines = content.split('\n')
        
        # Process each line
        for i, line in enumerate(lines):
            try:
                value = int(line)
                print(f"Line {i}: {value}")
            except ValueError:
                print(f"Line {i}: Not a number, skipping")
                
    except Exception as e:
        print(f"Error reading file: {e}")
    finally:
        file.close()
        
except FileNotFoundError:
    print(f"File '{filename}' not found!")
```

**Example 2: API Call with Nested Error Handling**
```python
try:
    api_key = input("Enter API key: ")
    endpoint = input("Enter endpoint: ")
    
    try:
        response = requests.get(
            f"https://api.example.com/{endpoint}",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        try:
            data = response.json()
            print(f"Data received: {len(data)} records")
        except json.JSONDecodeError:
            print("Response is not valid JSON")
            
    except requests.ConnectionError:
        print("Network connection failed")
    except requests.Timeout:
        print("Request timed out")
        
except KeyboardInterrupt:
    print("User cancelled operation")
```

**Better Alternative: Use function decomposition instead of nesting**
```python
def read_and_process_file(filename):
    try:
        with open(filename) as f:
            return process_content(f.read())
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
        return None

def process_content(content):
    results = []
    for line in content.split('\n'):
        try:
            results.append(int(line))
        except ValueError:
            pass  # Skip invalid lines
    return results

# Cleaner and easier to read
data = read_and_process_file("numbers.txt")
```

---

## 1️⃣1️⃣ Raising Exceptions (`raise`) 🚀

Raise exceptions when you detect invalid conditions. This lets you control program flow and provide meaningful errors.

**Example 1: Age Validation**
```python
def check_age(age):
    try:
        age = int(age)
        if age < 0:
            raise ValueError("Age cannot be negative")
        if age < 18:
            raise ValueError("Age must be 18 or above to access")
        if age > 120:
            raise ValueError("Age seems unrealistic")
        print(f"Access granted for age {age}")
    except ValueError as e:
        print(f"Error: {e}")

check_age(-5)      # Error: Age cannot be negative
check_age(15)      # Error: Age must be 18 or above to access
check_age(150)     # Error: Age seems unrealistic
check_age(25)      # Access granted for age 25
```

**Example 2: Password Validation**
```python
def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    return True

try:
    pwd = input("Enter password: ")
    validate_password(pwd)
    print("✓ Password is valid!")
except ValueError as e:
    print(f"✗ {e}")
```

**Example 3: Bank Transaction**
```python
def withdraw(account, amount):
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")
    if amount > account.balance:
        raise ValueError(f"Insufficient funds. Balance: ${account.balance}")
    if amount > 5000:
        raise ValueError("Daily withdrawal limit is $5000")
    
    account.balance -= amount
    return account.balance

class Account:
    def __init__(self, balance):
        self.balance = balance

account = Account(1000)

try:
    withdraw(account, -100)  # Error: negative amount
except ValueError as e:
    print(f"Transaction failed: {e}")

try:
    withdraw(account, 2000)  # Error: insufficient funds
except ValueError as e:
    print(f"Transaction failed: {e}")

try:
    withdraw(account, 500)   # Success
    print(f"Withdrawal successful. New balance: ${account.balance}")
except ValueError as e:
    print(f"Transaction failed: {e}")
```

**Example 4: Re-raising Exceptions**
```python
def process_user_data(data):
    try:
        user_id = int(data["id"])
        email = data["email"]
        
        if "@" not in email:
            raise ValueError("Invalid email format")
            
        return {"id": user_id, "email": email}
        
    except KeyError as e:
        print(f"Missing required field: {e}")
        raise  # Re-raise the same exception
    except ValueError as e:
        print(f"Invalid data: {e}")
        raise  # Re-raise so caller knows it failed

try:
    result = process_user_data({"id": "abc"})
except (KeyError, ValueError) as e:
    print(f"Processing failed: {e}")
```

---

## 1️⃣2️⃣ Custom Exceptions (Very Interview-Friendly!) 💼

Create your own exception classes for specific error conditions. This makes code more professional and maintainable.

**Example 1: Bank Exception**
```python
class InsufficientBalanceError(Exception):
    """Raised when trying to withdraw more than available balance"""
    pass

class DailyLimitExceededError(Exception):
    """Raised when daily withdrawal limit is exceeded"""
    pass

def withdraw_money(balance, amount):
    if amount > balance:
        raise InsufficientBalanceError(
            f"Trying to withdraw ${amount} but balance is ${balance}"
        )
    if amount > 5000:
        raise DailyLimitExceededError(
            f"Daily limit is $5000, trying to withdraw ${amount}"
        )
    return balance - amount

# Usage
try:
    new_balance = withdraw_money(1000, 1500)
except InsufficientBalanceError as e:
    print(f"❌ {e}")
except DailyLimitExceededError as e:
    print(f"⚠️ {e}")

# Output: ❌ Trying to withdraw $1500 but balance is $1000
```

**Example 2: Game Exception**
```python
class GameOverException(Exception):
    """Game has ended"""
    def __init__(self, score):
        self.score = score
        super().__init__(f"Game Over! Final Score: {self.score}")

class InvalidMoveException(Exception):
    """Player attempted an invalid move"""
    pass

def play_game(moves):
    score = 0
    for move in moves:
        if move == "quit":
            raise GameOverException(score)
        if move not in ["up", "down", "left", "right"]:
            raise InvalidMoveException(f"'{move}' is not a valid move")
        score += 10
    return score

# Usage
try:
    play_game(["up", "down", "invalid"])
except InvalidMoveException as e:
    print(f"Error: {e}")
except GameOverException as e:
    print(f"Result: {e}")

# Output: Error: 'invalid' is not a valid move
```

**Example 3: API Exception Hierarchy**
```python
class APIException(Exception):
    """Base exception for API errors"""
    pass

class AuthenticationError(APIException):
    """User authentication failed"""
    pass

class RateLimitError(APIException):
    """Too many requests"""
    pass

class ServerError(APIException):
    """Server-side error"""
    pass

def api_call(endpoint, api_key, requests_count):
    if not api_key:
        raise AuthenticationError("API key is required")
    
    if requests_count > 100:
        raise RateLimitError("Rate limit exceeded: max 100 requests/hour")
    
    if endpoint == "/admin":
        raise ServerError("Internal server error (500)")
    
    return {"status": "success"}

# Usage
try:
    result = api_call("/data", "", 50)
except AuthenticationError as e:
    print(f"Auth Error: {e}")
except RateLimitError as e:
    print(f"Rate Limit: {e}")
except APIException as e:  # Catches all API exceptions
    print(f"API Error: {e}")

# Output: Auth Error: API key is required
```

**Example 4: Validation Exception**
```python
class ValidationError(Exception):
    """Data validation failed"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"Validation error in '{field}': {message}")

def validate_user_registration(data):
    try:
        if not data.get("username") or len(data["username"]) < 3:
            raise ValidationError("username", "must be at least 3 characters")
        
        if not data.get("email") or "@" not in data["email"]:
            raise ValidationError("email", "must be a valid email")
        
        if not data.get("password") or len(data["password"]) < 8:
            raise ValidationError("password", "must be at least 8 characters")
        
        return True
        
    except ValidationError as e:
        print(f"❌ {e}")
        return False

# Usage
validate_user_registration({"username": "ab", "email": "john", "password": "123"})
# Output: ❌ Validation error in 'username': must be at least 3 characters
```

---

## 1️⃣3️⃣ Exception Handling with Functions 📞

Functions should handle exceptions gracefully and communicate results clearly.

**Example 1: Calculator Function**
```python
def divide(a, b):
    """Divide two numbers safely"""
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Arguments must be numbers"

print(divide(10, 2))      # 5.0
print(divide(10, 0))      # Error: Cannot divide by zero
print(divide(10, "text")) # Error: Arguments must be numbers
```

**Example 2: Function with Return Codes**
```python
def parse_int(value):
    """Parse integer and return (success, result)"""
    try:
        return True, int(value)
    except ValueError:
        return False, None

success, result = parse_int("42")
if success:
    print(f"Parsed: {result}")
else:
    print("Failed to parse")
```

**Example 3: Function with Logging**
```python
import logging

def risky_operation(data):
    """Perform operation with proper error logging"""
    try:
        # Simulate risky operation
        if data < 0:
            raise ValueError("Data cannot be negative")
        result = 100 / data
        logging.info(f"Operation successful: {result}")
        return result
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        return None
    except ZeroDivisionError:
        logging.error("Division by zero attempted")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None
    finally:
        logging.info("Operation completed")

risky_operation(10)  # Success
risky_operation(0)   # Division by zero error
risky_operation(-5)  # Validation error
```

**Example 4: Decorator for Exception Handling**
```python
import functools

def handle_exceptions(func):
    """Decorator to handle exceptions in any function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {e}"
        except ZeroDivisionError:
            return "Cannot divide by zero"
        except Exception as e:
            return f"Unexpected error: {e}"
    return wrapper

@handle_exceptions
def divide_nums(a, b):
    return a / b

@handle_exceptions
def convert_int(value):
    return int(value)

print(divide_nums(10, 2))       # 5.0
print(divide_nums(10, 0))       # Cannot divide by zero
print(convert_int("abc"))       # ValueError: invalid literal for int()
```

---

## 1️⃣4️⃣ Real-World Scenario: API & Input Validation 🌐

Complete example combining multiple exception handling concepts:

**Example 1: User Registration API**
```python
import re

class EmailInvalidError(Exception):
    pass

class PasswordTooWeakError(Exception):
    pass

class UsernameTakenError(Exception):
    pass

def create_user(data):
    """Create user with comprehensive validation"""
    try:
        # Extract and validate email
        if "email" not in data:
            raise KeyError("email field is required")
        
        email = data["email"]
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise EmailInvalidError(f"'{email}' is not a valid email")
        
        # Extract and validate password
        if "password" not in data:
            raise KeyError("password field is required")
        
        password = data["password"]
        if len(password) < 8:
            raise PasswordTooWeakError("Password must be at least 8 characters")
        
        # Extract and validate username
        if "username" not in data:
            raise KeyError("username field is required")
        
        username = data["username"]
        if username in ["admin", "root", "system"]:  # Simulate checking taken usernames
            raise UsernameTakenError(f"Username '{username}' is already taken")
        
        # If we get here, all validations passed
        return {
            "status": "success",
            "message": f"User '{username}' created successfully",
            "user": {
                "username": username,
                "email": email
            }
        }
        
    except KeyError as e:
        return {
            "status": "error",
            "message": f"Missing required field: {e}",
            "code": "MISSING_FIELD"
        }
    except EmailInvalidError as e:
        return {
            "status": "error",
            "message": str(e),
            "code": "INVALID_EMAIL"
        }
    except PasswordTooWeakError as e:
        return {
            "status": "error",
            "message": str(e),
            "code": "WEAK_PASSWORD"
        }
    except UsernameTakenError as e:
        return {
            "status": "error",
            "message": str(e),
            "code": "USERNAME_TAKEN"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {e}",
            "code": "UNKNOWN_ERROR"
        }

# Test cases
print(create_user({"username": "john", "email": "john@example.com", "password": "SecurePass123"}))
# Output: status: success

print(create_user({"username": "admin", "email": "admin@example.com", "password": "SecurePass123"}))
# Output: status: error, code: USERNAME_TAKEN

print(create_user({"username": "jane", "password": "SecurePass123"}))
# Output: status: error, code: MISSING_FIELD
```

**Example 2: Data Processing Pipeline**
```python
def process_csv_data(filename):
    """Read and process CSV file with multiple error checks"""
    data = []
    errors = []
    
    try:
        # Try to open file
        with open(filename, 'r') as f:
            try:
                # Try to parse CSV
                import csv
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Try to process each row
                        processed = {
                            "name": row["name"],
                            "age": int(row["age"]),
                            "salary": float(row["salary"])
                        }
                        data.append(processed)
                    except ValueError as e:
                        errors.append(f"Row {row_num}: Invalid data - {e}")
                    except KeyError as e:
                        errors.append(f"Row {row_num}: Missing column - {e}")
                        
            except csv.Error as e:
                return {"status": "error", "message": f"CSV parsing error: {e}"}
                
    except FileNotFoundError:
        return {"status": "error", "message": f"File '{filename}' not found"}
    except IOError as e:
        return {"status": "error", "message": f"Cannot read file: {e}"}
    
    return {
        "status": "success",
        "total_rows": len(data),
        "processed_rows": len(data),
        "errors": errors,
        "data": data
    }

# Usage
result = process_csv_data("users.csv")
print(f"Processed {result['processed_rows']} rows")
if result['errors']:
    for error in result['errors']:
        print(f"  ⚠️ {error}")
```

---

## 1️⃣5️⃣ Best Practices (Exam + Industry) ✅

**1. Catch Specific Exceptions**
```python
# ❌ BAD: Too generic
try:
    user = get_user(user_id)
except:
    print("Error")

# ✅ GOOD: Specific exceptions
try:
    user = get_user(user_id)
except UserNotFoundError:
    print("User not found")
except DatabaseError as e:
    logging.error(f"Database error: {e}")
```

**2. Provide Context in Error Messages**
```python
# ❌ BAD: No context
except ValueError:
    print("Error")

# ✅ GOOD: Clear context
except ValueError as e:
    print(f"Failed to parse age '{age}': {e}")
```

**3. Use `else` for Success Logic**
```python
# ❌ BAD: Too much in try
try:
    value = int(user_input)
    success_count += 1
    print(f"Processed: {value}")
except ValueError:
    print("Invalid input")

# ✅ GOOD: Separated concerns
try:
    value = int(user_input)
except ValueError:
    print("Invalid input")
else:
    success_count += 1
    print(f"Processed: {value}")
```

**4. Use `finally` for Cleanup**
```python
# ❌ BAD: Might not clean up if exception
file = open("data.txt")
try:
    process(file)
except Exception:
    print("Error")
file.close()

# ✅ GOOD: Guaranteed cleanup
try:
    file = open("data.txt")
    process(file)
except Exception:
    print("Error")
finally:
    file.close()

# ✅ BEST: Use context managers
with open("data.txt") as file:
    process(file)  # Auto-closes
```

**5. Don't Use Empty `except:`**
```python
# ❌ NEVER DO THIS
try:
    dangerous_operation()
except:
    pass  # Silently swallows errors

# ✅ GOOD: Specific handling
try:
    dangerous_operation()
except SpecificError as e:
    handle_error(e)
except Exception as e:
    logging.error(f"Unexpected: {e}")
    raise  # Re-raise if necessary
```

**6. Log Errors in Real Applications**
```python
import logging

try:
    process_transaction(amount)
except ValueError as e:
    logging.error(f"Invalid transaction amount: {amount}, error: {e}")
except DatabaseError as e:
    logging.critical(f"Database error during transaction: {e}")
    send_alert_to_admin(e)
```

**7. Create Meaningful Custom Exceptions**
```python
# ❌ BAD: Too generic
class MyError(Exception):
    pass

# ✅ GOOD: Specific and descriptive
class PaymentProcessingError(Exception):
    """Raised when payment processing fails"""
    def __init__(self, transaction_id, reason):
        self.transaction_id = transaction_id
        self.reason = reason
        super().__init__(f"Payment {transaction_id} failed: {reason}")
```

**8. Fail Fast with Clear Messages**
```python
def validate_input(data):
    if not data:
        raise ValueError("Data cannot be empty")
    if "id" not in data:
        raise KeyError("'id' field is required")
    if not isinstance(data["id"], int):
        raise TypeError("'id' must be an integer")
    return True

# Errors caught early with clear messages
```

**9. Document Expected Exceptions**
```python
def fetch_user(user_id):
    """
    Fetch user by ID.
    
    Args:
        user_id: Integer user ID
        
    Returns:
        dict: User data
        
    Raises:
        ValueError: If user_id is not an integer
        UserNotFoundError: If user doesn't exist
        DatabaseError: If database connection fails
    """
    if not isinstance(user_id, int):
        raise ValueError("user_id must be an integer")
    # ... rest of implementation
```

**10. Use Exception Chains**
```python
# Python 3.3+: Preserves original exception
try:
    file = open("data.json")
    data = json.load(file)
except json.JSONDecodeError as e:
    raise ValueError("Invalid JSON file") from e  # Shows original error too
```

---

## 1️⃣6️⃣ Hands-On Exercises 💪

**Exercise 1: Handle Invalid Index**
```python
# Challenge: Handle IndexError when accessing list
lst = [1, 2, 3]
user_input = input("Enter index to access: ")

# Write code to:
# 1. Convert user_input to integer
# 2. Access lst[index]
# 3. Handle ValueError if input is not a number
# 4. Handle IndexError if index is out of range
# 5. Print the value if successful

# Solution:
try:
    index = int(user_input)
    value = lst[index]
    print(f"Value at index {index}: {value}")
except ValueError:
    print("Please enter a valid integer")
except IndexError:
    print(f"Index out of range. List has {len(lst)} elements")
```

**Exercise 2: Read File Safely**
```python
# Challenge: Read file with multiple error checks
filename = input("Enter filename: ")
lines_to_read = input("How many lines to read: ")

# Write code to:
# 1. Convert lines_to_read to integer
# 2. Open the file
# 3. Read specified number of lines
# 4. Handle FileNotFoundError
# 5. Handle ValueError
# 6. Ensure file is closed

# Solution:
try:
    num_lines = int(lines_to_read)
    with open(filename) as f:
        for i in range(num_lines):
            line = f.readline()
            if not line:
                print(f"File has only {i} lines")
                break
            print(f"Line {i+1}: {line.rstrip()}")
except FileNotFoundError:
    print(f"File '{filename}' not found")
except ValueError:
    print("Number of lines must be an integer")
```

**Exercise 3: Validate Password**
```python
# Challenge: Create custom exception and validate password
# Requirements:
# - At least 8 characters
# - At least one uppercase letter
# - At least one digit
# - At least one special character (!@#$%^&*)

class PasswordTooWeakError(Exception):
    pass

password = input("Enter password: ")

try:
    # Add validation logic
    if len(password) < 8:
        raise PasswordTooWeakError("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        raise PasswordTooWeakError("Must contain uppercase letter")
    if not any(c.isdigit() for c in password):
        raise PasswordTooWeakError("Must contain digit")
    if not any(c in "!@#$%^&*" for c in password):
        raise PasswordTooWeakError("Must contain special character")
    
    print("✓ Password is valid!")
except PasswordTooWeakError as e:
    print(f"✗ {e}")
```

**Exercise 4: Process CSV Data**
```python
# Challenge: Create a function that processes CSV with multiple validation checks

def validate_and_process_csv(filename):
    """
    Read CSV and validate each row.
    Return list of valid records and list of errors.
    """
    valid = []
    errors = []
    
    try:
        with open(filename) as f:
            # Read lines and process
            for i, line in enumerate(f, 1):
                try:
                    parts = line.strip().split(",")
                    if len(parts) != 3:
                        raise ValueError(f"Expected 3 columns, got {len(parts)}")
                    
                    name, age, email = parts
                    age = int(age)  # Can raise ValueError
                    
                    if age < 0 or age > 150:
                        raise ValueError(f"Age {age} out of range")
                    
                    if "@" not in email:
                        raise ValueError(f"Invalid email: {email}")
                    
                    valid.append({"name": name, "age": age, "email": email})
                    
                except ValueError as e:
                    errors.append(f"Line {i}: {e}")
    
    except FileNotFoundError:
        return None, [f"File '{filename}' not found"]
    
    return valid, errors

# Test
valid, errors = validate_and_process_csv("users.csv")
print(f"Valid records: {len(valid)}")
for error in errors:
    print(f"  ⚠️  {error}")
```

**Exercise 5: Create a Robust Calculator**
```python
# Challenge: Create calculator that handles all error cases

class DivisionByZeroError(Exception):
    pass

def calculate(expression):
    """
    Safe calculator that handles:
    - ZeroDivisionError
    - ValueError (invalid input)
    - Invalid operators
    - Type errors
    """
    try:
        parts = expression.split()
        if len(parts) != 3:
            raise ValueError("Invalid expression format (e.g., '10 + 5')")
        
        try:
            a = float(parts[0])
            operator = parts[1]
            b = float(parts[2])
        except ValueError:
            raise ValueError("Numbers must be integers or decimals")
        
        if operator == "+":
            return a + b
        elif operator == "-":
            return a - b
        elif operator == "*":
            return a * b
        elif operator == "/":
            if b == 0:
                raise DivisionByZeroError("Cannot divide by zero")
            return a / b
        else:
            raise ValueError(f"Unknown operator: {operator}")
    
    except DivisionByZeroError as e:
        return f"Error: {e}"
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

# Test
print(calculate("10 + 5"))      # 15.0
print(calculate("10 / 0"))      # Error: Cannot divide by zero
print(calculate("abc + 5"))     # Error: Numbers must be...
print(calculate("10 % 5"))      # Error: Unknown operator: %
```

---

## 1️⃣7️⃣ Exception Handling Flow (Mental Model) 🔀

Understanding the flow of exception handling:

```
┌─ START EXECUTION ─┐
│                   │
│  try:             │
│  ├─ Code here     │
│  │                │
│  ├─ Exception?    ──→ NO → else:
│  │                          ├─ Success code
│  ├─ YES ─────────────→ except BlockType:
│  │                          ├─ Handle error
│  │                          │
│  └─────────────────────────→ finally:
│                              ├─ Cleanup code
│                              │ (ALWAYS runs)
│                              │
└───────────────────────────→ CONTINUE EXECUTION
```

**Step-by-Step Execution:**

1. **Execute `try` block** — Run the code
2. **Exception occurs?**
   - **YES** → Skip rest of `try`, jump to `except`
   - **NO** → Complete `try`, skip `except`, run `else` (if present)
3. **`except` block** — Handle the error
4. **`finally` block** (if present) — **ALWAYS** runs, whether exception happened or not
5. **Continue** — Program proceeds after the entire try-except-else-finally structure

**Example Execution Traces:**

```python
# Scenario 1: Normal execution
try:
    x = 10 / 2
    print("Step 1: Division done")
except ZeroDivisionError:
    print("Step 2: Error handler (NOT EXECUTED)")
else:
    print("Step 3: Success handler")
finally:
    print("Step 4: Cleanup")

# Output:
# Step 1: Division done
# Step 3: Success handler
# Step 4: Cleanup
```

```python
# Scenario 2: Exception occurs
try:
    x = 10 / 0
    print("Step 1: Division done (NOT EXECUTED)")
except ZeroDivisionError:
    print("Step 2: Error handler")
else:
    print("Step 3: Success handler (NOT EXECUTED)")
finally:
    print("Step 4: Cleanup")

# Output:
# Step 2: Error handler
# Step 4: Cleanup
```

```python
# Scenario 3: Wrong exception type
try:
    x = int("abc")
    print("Step 1: Conversion done (NOT EXECUTED)")
except ZeroDivisionError:  # Wrong exception type
    print("Step 2: Error handler (NOT EXECUTED - wrong type)")
else:
    print("Step 3: Success handler (NOT EXECUTED)")
finally:
    print("Step 4: Cleanup")

# Output:
# Step 4: Cleanup
# ValueError raised (not caught, program crashes)
```

**Exception Hierarchy Visualization:**

```
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
    ├── StopIteration
    ├── ArithmeticError
    │   ├── FloatingPointError
    │   ├── OverflowError
    │   └── ZeroDivisionError
    ├── AssertionError
    ├── AttributeError
    ├── BufferError
    ├── EOFError
    ├── ImportError
    │   └── ModuleNotFoundError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── NameError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── ConnectionError
    ├── RuntimeError
    ├── TypeError
    ├── ValueError
    └── ... (many more)
```

**Matching Exception Hierarchy:**

```python
# Specific exception caught
try:
    x = 1 / 0
except ZeroDivisionError:  # Catches ZeroDivisionError
    print("Handled")

# Parent exception caught
try:
    x = 1 / 0
except ArithmeticError:  # Parent class catches child
    print("Handled")

# Won't match
try:
    x = 1 / 0
except ValueError:  # Different exception type
    print("Won't execute - ValueError not raised")
# ZeroDivisionError escapes and crashes program
```

---