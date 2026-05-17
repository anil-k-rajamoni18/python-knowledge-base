# Python Functions📚

## 1️⃣ What is a Function?

A **function** is a reusable block of code that performs a specific task. Functions help you organize code, eliminate repetition, and make programs easier to maintain and understand.

**Key Benefits:**
* **Reusability** — Write once, use many times
* **Modularity** — Break complex problems into smaller pieces
* **Maintainability** — Easier to update and debug
* **Readability** — Clear code structure and intent
* **Testing** — Test individual components separately

**Real-World Analogy:**
A function is like a recipe. You define the steps once, then you can make the dish multiple times without rewriting the recipe. You can also share the recipe with others.

```python
# Without functions (repetitive)
print(10 + 5)
print(20 + 5)
print(30 + 5)

# With function (clean and reusable)
def add_five(number):
    return number + 5

print(add_five(10))  # 15
print(add_five(20))  # 25
print(add_five(30))  # 35
```

---

## 2️⃣ Function Basics: Structure & Syntax

**Anatomy of a Function:**

```python
def function_name(parameter1, parameter2):
    """Docstring - describes what function does"""
    # Function body - code to execute
    result = parameter1 + parameter2
    return result  # Optional - return a value
```

**Components Explained:**

| Component | Purpose | Example |
|-----------|---------|---------|
| `def` | Keyword to define a function | `def` calculate(a, b): |
| `function_name` | Name of the function (snake_case) | `calculate_age` |
| `()` | Parameter list | `(year_born, current_year)` |
| `:` | Marks start of function block | Needed for indentation |
| Docstring | Multi-line description | `"""Calculate person's age"""` |
| Body | Code that executes | Variables, calculations, loops |
| `return` | Send value back to caller | `return age` |

**Example 1: Simple Function**
```python
def greet(name):
    """Greet a person by name"""
    message = f"Hello, {name}!"
    return message

result = greet("Alice")
print(result)  # Hello, Alice!
```

**Example 2: Function with Multiple Parameters**
```python
def calculate_gpa(math_grade, english_grade, science_grade):
    """Calculate average GPA"""
    total = math_grade + english_grade + science_grade
    average = total / 3
    return average

gpa = calculate_gpa(85, 90, 88)
print(f"GPA: {gpa:.2f}")  # GPA: 87.67
```

**Example 3: Function with No Return Value**
```python
def print_separator():
    """Print a line separator"""
    print("-" * 50)

print_separator()
print("Content here")
print_separator()
```

---

## 3️⃣ Parameters vs Arguments

**Parameter** — Variable in function definition
**Argument** — Actual value passed to function

```python
def add(a, b):  # a and b are PARAMETERS
    return a + b

result = add(5, 3)  # 5 and 3 are ARGUMENTS
```

**Types of Parameters:**

1. **Positional Parameters**
```python
def introduce(name, age, city):
    print(f"{name} is {age} years old and lives in {city}")

# Arguments must be in same order
introduce("John", 25, "NYC")  # Correct
introduce(25, "John", "NYC")  # Wrong - age is string, name is int
introduce("John", "NYC", 25)  # Wrong - city is int, age is string
```

2. **Default Parameters**
```python
def greet(name, greeting="Hello"):
    """Greet with custom message"""
    return f"{greeting}, {name}!"

print(greet("Alice"))  # Hello, Alice!
print(greet("Bob", "Hi"))  # Hi, Bob!
print(greet("Charlie", greeting="Hey"))  # Hey, Charlie!
```
3. **Keyword Arguments**
```python
def create_profile(name, age, city, profession):
    profile = {
        "name": name,
        "age": age,
        "city": city,
        "profession": profession
    }
    return profile

# Positional order
profile1 = create_profile("Alice", 25, "NYC", "Engineer")

# Keyword order (can be any order)
profile2 = create_profile(
    profession="Engineer",
    name="Alice",
    city="NYC",
    age=25
)

# Mix positional and keyword
profile3 = create_profile("Alice", 25, profession="Engineer", city="NYC")
```

4. *args (Variable-Length Positional Arguments)**
```python
def sum_all(*numbers):
    """Sum any number of arguments"""
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3))  # 6
print(sum_all(1, 2, 3, 4, 5))  # 15
print(sum_all(10))  # 10
```

**Real Example with *args:**
```python
def print_info(title, *items):
    """Print title followed by items"""
    print(f"=== {title} ===")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")

print_info("Fruits", "Apple", "Banana", "Orange")
# Output:
# === Fruits ===
# 1. Apple
# 2. Banana
# 3. Orange
```

5. **kwargs (Variable-Length Keyword Arguments)**
```python
def create_user(name, **details):
    """Create user with flexible details"""
    user = {"name": name}
    user.update(details)
    return user

user = create_user(
    name="John",
    age=25,
    email="john@example.com",
    city="NYC",
    job="Engineer"
)

print(user)
# {'name': 'John', 'age': 25, 'email': 'john@example.com', 'city': 'NYC', 'job': 'Engineer'}
```

**Real Example with **kwargs:**
```python
def create_html_tag(tag_name, content="", **attributes):
    """Create HTML tag with dynamic attributes"""
    attrs = " ".join([f'{key}="{value}"' for key, value in attributes.items()])
    if attrs:
        return f"<{tag_name} {attrs}>{content}</{tag_name}>"
    return f"<{tag_name}>{content}</{tag_name}>"

# Usage
button = create_html_tag("button", "Click me", id="btn1", class_="primary", onclick="submit()")
print(button)
# <button id="btn1" class_="primary" onclick="submit()">Click me</button>
```

6. **Combining All Parameter Types**
```python
def process_data(required, default="value", *args, **kwargs):
    """Function with all parameter types"""
    print(f"Required: {required}")
    print(f"Default: {default}")
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

process_data(
    "essential",
    "custom_default",
    "extra1",
    "extra2",
    option1="data1",
    option2="data2"
)

# Output:
# Required: essential
# Default: custom_default
# Args: ('extra1', 'extra2')
# Kwargs: {'option1': 'data1', 'option2': 'data2'}
```

**Order Rule:** `positional`, `default`, `*args`, `**kwargs`

---

## 4️⃣ Return Values

Functions can return data back to the caller.

**Example 1: Single Return Value**
```python
def square(number):
    """Calculate square of a number"""
    return number ** 2

result = square(5)
print(result)  # 25
```

**Example 2: Multiple Return Values**
```python
def get_min_max(numbers):
    """Return minimum and maximum from list"""
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([3, 7, 2, 8, 1])
print(f"Min: {minimum}, Max: {maximum}")  # Min: 1, Max: 8
```

**Example 3: Return Dictionary (Common in Real Apps)**
```python
def login_user(username, password):
    """Attempt login, return status and message"""
    if len(password) < 8:
        return {
            "success": False,
            "message": "Password too short"
        }
    if username in ["admin", "root"]:
        return {
            "success": True,
            "user_id": 1,
            "message": "Login successful"
        }
    return {
        "success": False,
        "message": "Invalid credentials"
    }

result = login_user("admin", "password123")
if result["success"]:
    print(f"Welcome user {result['user_id']}")
else:
    print(f"Error: {result['message']}")
```

**Example 4: Early Return**
```python
def find_user(users, user_id):
    """Find user, return early if found"""
    for user in users:
        if user["id"] == user_id:
            return user  # Return immediately
    
    return None  # Not found

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]

user = find_user(users, 2)
print(user)  # {'id': 2, 'name': 'Bob'}
```

**Example 5: No Return (Implicit None)**
```python
def print_data(data):
    """Print data, no return value"""
    for item in data:
        print(item)

result = print_data([1, 2, 3])
print(result)  # None (no return statement)
```

---

## 5️⃣ Function Scope & Variables

**Scope** determines where a variable can be accessed.

**Example 1: Local Scope**
```python
def calculate():
    x = 10  # LOCAL variable - exists only in function
    y = 20
    return x + y

calculate()
print(x)  # NameError: name 'x' is not defined
```

**Example 2: Global Scope**
```python
x = 10  # GLOBAL variable - accessible everywhere

def show_x():
    print(x)  # Can read global variable

show_x()  # 10
print(x)  # 10
```

**Example 3: Global Modification (Not Recommended)**
```python
counter = 0  # Global variable

def increment():
    global counter  # Tell Python to use global counter
    counter += 1

increment()
increment()
print(counter)  # 2
```

**Example 4: Local vs Global**
```python
x = "global"

def my_function():
    x = "local"  # Creates NEW local variable
    print(x)  # Prints local x

my_function()  # local
print(x)  # global (global x unchanged)
```

**Example 5: Complex Scope Example**
```python
def outer():
    x = "outer"
    
    def inner():
        x = "inner"  # Local to inner
        print(x)
    
    inner()  # Prints "inner"
    print(x)  # Prints "outer"

outer()

# Output:
# inner
# outer
```

**Best Practice:** Minimize global variables. Pass data through parameters instead.

```python
# ❌ BAD: Uses global
count = 0
def increment():
    global count
    count += 1

# ✅ GOOD: Uses parameters
def increment(count):
    return count + 1

count = 0
count = increment(count)
```

---

## 6️⃣ Docstrings & Documentation

**Docstrings** document what functions do, their parameters, return values, and examples.

**Example 1: Simple Docstring**
```python
def add(a, b):
    """Add two numbers and return the result."""
    return a + b
```

**Example 2: Comprehensive Docstring (Google Style)**
```python
def calculate_discount(price, discount_percent):
    """
    Calculate final price after applying discount.
    
    Args:
        price (float): Original price in dollars
        discount_percent (float): Discount percentage (0-100)
    
    Returns:
        float: Final price after discount
    
    Raises:
        ValueError: If price is negative or discount > 100
    
    Examples:
        >>> calculate_discount(100, 20)
        80.0
        >>> calculate_discount(50, 10)
        45.0
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount
```

**Example 3: Using Docstrings**
```python
def greet(name, greeting="Hello"):
    """
    Greet a person with a custom message.
    
    Args:
        name: Person's name
        greeting: Custom greeting (default: "Hello")
    
    Returns:
        Formatted greeting string
    """
    return f"{greeting}, {name}!"

# Access docstring
print(greet.__doc__)
help(greet)  # Also shows docstring
```

---

## 7️⃣ Function Types

**1. Void Functions (No Return)**
```python
def save_file(filename, content):
    """Save content to file"""
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Saved to {filename}")

save_file("data.txt", "Hello World")
```

**2. Value-Returning Functions**
```python
def calculate_area(radius):
    """Calculate circle area"""
    import math
    return math.pi * radius ** 2

area = calculate_area(5)
print(f"Area: {area:.2f}")
```

**3. Predicate Functions (Return Boolean)**
```python
def is_even(number):
    """Check if number is even"""
    return number % 2 == 0

print(is_even(4))   # True
print(is_even(7))   # False
```

**4. Factory Functions (Create Objects)**
```python
def create_user(name, email, role="user"):
    """Create user dictionary"""
    return {
        "id": None,  # Will be assigned by database
        "name": name,
        "email": email,
        "role": role,
        "created_at": None
    }

user1 = create_user("Alice", "alice@example.com")
user2 = create_user("Bob", "bob@example.com", role="admin")
```

**5. Higher-Order Functions (Accept/Return Functions)**
```python
def multiply_by(factor):
    """Return a function that multiplies by factor"""
    def multiplier(number):
        return number * factor
    return multiplier

# Create specialized functions
double = multiply_by(2)
triple = multiply_by(3)

print(double(5))  # 10
print(triple(5))  # 15
```

---

## 8️⃣ Practical Function Examples

**Example 1: User Registration**
```python
import re

def register_user(username, email, password):
    """
    Register new user with validation.
    
    Returns:
        dict: Result with status and message
    """
    errors = []
    
    # Validate username
    if len(username) < 3:
        errors.append("Username must be at least 3 characters")
    
    # Validate email
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
        errors.append("Invalid email format")
    
    # Validate password
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        errors.append("Password must contain uppercase letter")
    
    if errors:
        return {"success": False, "errors": errors}
    
    return {
        "success": True,
        "user": {
            "username": username,
            "email": email,
            "created_at": "2024-01-01"
        }
    }

# Test
result = register_user("alice", "alice@example.com", "Password123")
print(result)
```

**Example 2: Data Filtering**
```python
def filter_products(products, min_price=0, max_price=float('inf'), category=None):
    """
    Filter products by price and category.
    """
    filtered = products
    
    # Filter by price
    filtered = [p for p in filtered if min_price <= p['price'] <= max_price]
    
    # Filter by category
    if category:
        filtered = [p for p in filtered if p['category'] == category]
    
    return filtered

# Test data
products = [
    {"name": "Laptop", "price": 1200, "category": "Electronics"},
    {"name": "Mouse", "price": 25, "category": "Electronics"},
    {"name": "Desk", "price": 300, "category": "Furniture"},
    {"name": "Chair", "price": 150, "category": "Furniture"},
]

# Usage
cheap_electronics = filter_products(products, max_price=200, category="Electronics")
print(cheap_electronics)
# [{'name': 'Mouse', 'price': 25, 'category': 'Electronics'}]
```

**Example 3: Text Processing**
```python
def count_words(text):
    """Count words in text"""
    words = text.split()
    return len(words)

def summarize_text(text, word_limit=50):
    """Summarize text to specific word count"""
    words = text.split()
    summary = " ".join(words[:word_limit])
    if len(words) > word_limit:
        summary += "..."
    return summary

text = "Python is a powerful programming language. " * 10
print(f"Total words: {count_words(text)}")
print(f"Summary: {summarize_text(text, 20)}")
```

**Example 4: Data Analysis**
```python
def analyze_grades(grades):
    """
    Analyze student grades.
    
    Returns:
        dict: Statistics about grades
    """
    if not grades:
        return {"error": "No grades provided"}
    
    return {
        "total": len(grades),
        "average": sum(grades) / len(grades),
        "highest": max(grades),
        "lowest": min(grades),
        "passed": sum(1 for g in grades if g >= 60),
        "pass_rate": sum(1 for g in grades if g >= 60) / len(grades) * 100
    }

grades = [85, 90, 78, 92, 88, 76, 95]
stats = analyze_grades(grades)

for key, value in stats.items():
    print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")
```

**Example 5: File Operations**
```python
def read_csv_file(filename):
    """Read CSV file and return as list of dictionaries"""
    data = []
    try:
        with open(filename, 'r') as f:
            headers = f.readline().strip().split(',')
            for line in f:
                values = line.strip().split(',')
                row = dict(zip(headers, values))
                data.append(row)
        return data
    except FileNotFoundError:
        return {"error": f"File '{filename}' not found"}

def save_csv_file(filename, data):
    """Save list of dictionaries to CSV file"""
    if not data:
        print("No data to save")
        return
    
    try:
        headers = data[0].keys()
        with open(filename, 'w') as f:
            f.write(','.join(headers) + '\n')
            for row in data:
                values = [str(row.get(h, '')) for h in headers]
                f.write(','.join(values) + '\n')
        print(f"Saved {len(data)} rows to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")
```

---

## 9️⃣ Recursion

**Recursion** is when a function calls itself. It needs a base case to stop.

**Example 1: Factorial**
```python
def factorial(n):
    """Calculate factorial recursively"""
    if n <= 1:  # BASE CASE
        return 1
    return n * factorial(n - 1)  # RECURSIVE CALL

print(factorial(5))  # 5 * 4 * 3 * 2 * 1 = 120
```

**Execution trace for factorial(3):**
```
factorial(3)
├─ 3 * factorial(2)
│  ├─ 2 * factorial(1)
│  │  └─ 1 (base case)
│  └─ 2 * 1 = 2
└─ 3 * 2 = 6
```

**Example 2: Fibonacci**
```python
def fibonacci(n):
    """Calculate nth Fibonacci number"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(6))  # 8
```

**Example 3: Sum List**
```python
def sum_list(numbers):
    """Sum list using recursion"""
    if not numbers:  # BASE CASE
        return 0
    return numbers[0] + sum_list(numbers[1:])

print(sum_list([1, 2, 3, 4, 5]))  # 15
```

**Example 4: Search in Nested Lists**
```python
def find_value(data, target):
    """Search for value in nested lists"""
    for item in data:
        if item == target:
            return True
        if isinstance(item, list):
            if find_value(item, target):
                return True
    return False

nested = [1, [2, 3, [4, 5]], 6]
print(find_value(nested, 4))  # True
print(find_value(nested, 10)) # False
```

**When to Use Recursion:**
* Tree/graph traversal
* Divide-and-conquer algorithms
* Mathematical sequences
* File system navigation

**When NOT to Use:**
* Large datasets (stack overflow risk)
* Performance-critical code
* When iteration is simpler

---

## 🔟 Decorators

**Decorators** modify or enhance function behavior without changing the function itself.

**Example 1: Simple Decorator**
```python
def my_decorator(func):
    """Decorator that prints function name and arguments"""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        print(f"Arguments: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Returned: {result}")
        return result
    return wrapper

@my_decorator
def add(a, b):
    """Add two numbers"""
    return a + b

add(5, 3)
# Output:
# Calling add
# Arguments: (5, 3), {}
# Returned: 8
```

**Example 2: Timer Decorator**
```python
import time

def timer_decorator(func):
    """Measure execution time of function"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer_decorator
def slow_function():
    """Simulate slow operation"""
    time.sleep(2)
    return "Done"

slow_function()
# slow_function took 2.0023 seconds
```

**Example 3: Authentication Decorator**
```python
def require_admin(func):
    """Check if user is admin before executing"""
    def wrapper(user, *args, **kwargs):
        if user.get("role") != "admin":
            return "Access Denied: Admin only"
        return func(user, *args, **kwargs)
    return wrapper

@require_admin
def delete_user(user, user_id):
    return f"User {user_id} deleted by {user['name']}"

# Test
admin_user = {"name": "Alice", "role": "admin"}
regular_user = {"name": "Bob", "role": "user"}

print(delete_user(admin_user, 123))  # User 123 deleted by Alice
print(delete_user(regular_user, 123))  # Access Denied: Admin only
```

---

## 1️⃣1️⃣ Lambda Functions

**Lambda** functions are small, anonymous functions defined with `lambda` keyword.

**Syntax:** `lambda parameters: expression`

**Example 1: Simple Lambda**
```python
square = lambda x: x ** 2
print(square(5))  # 25
```

**Example 2: Lambda with Multiple Parameters**
```python
add = lambda x, y: x + y
print(add(5, 3))  # 8
```

**Example 3: Lambda with map()**
```python
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]
```

**Example 4: Lambda with filter()**
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6, 8, 10]
```

**Example 5: Lambda with sort()**
```python
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78}
]

# Sort by grade
sorted_students = sorted(students, key=lambda s: s["grade"], reverse=True)
print(sorted_students)
# [{'name': 'Bob', 'grade': 92}, {'name': 'Alice', 'grade': 85}, {'name': 'Charlie', 'grade': 78}]
```

**When to Use Lambda:**
* Short, one-line operations
* With map(), filter(), sorted()
* As callback functions

**When NOT to Use:**
* Complex logic (use `def` instead)
* Code that needs comments
* Reusable code

---

## 1️⃣2️⃣ Built-in Functions

Python provides many useful built-in functions.

**String Functions:**
```python
# len() - length
print(len("hello"))  # 5

# str() - convert to string
print(str(123))  # "123"

# upper(), lower() - case conversion
print("Hello".upper())  # "HELLO"

# strip() - remove whitespace
print("  hello  ".strip())  # "hello"

# split() - split string
print("a,b,c".split(","))  # ['a', 'b', 'c']

# join() - join list
print("-".join(["a", "b", "c"]))  # "a-b-c"
```

**List Functions:**
```python
# len() - length
print(len([1, 2, 3]))  # 3

# min(), max() - find extremes
print(min([3, 1, 4, 1, 5]))  # 1
print(max([3, 1, 4, 1, 5]))  # 5

# sum() - sum elements
print(sum([1, 2, 3, 4]))  # 10

# sorted() - sort
print(sorted([3, 1, 4, 1, 5]))  # [1, 1, 3, 4, 5]

# reversed() - reverse
print(list(reversed([1, 2, 3])))  # [3, 2, 1]
```

**Map, Filter, Reduce:**
```python
# map() - apply function to all items
numbers = [1, 2, 3, 4]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)  # [2, 4, 6, 8]

# filter() - keep items that match condition
numbers = [1, 2, 3, 4, 5]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# reduce() - combine all items
from functools import reduce
numbers = [1, 2, 3, 4]
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 24
```

**Iteration Functions:**
```python
# enumerate() - get index and value
for i, value in enumerate(["a", "b", "c"]):
    print(f"{i}: {value}")

# zip() - pair elements from lists
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age}")

# range() - generate sequence
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4
```

---

## 1️⃣3️⃣ Best Practices

**1. Follow Naming Conventions**
```python
# ❌ BAD
def CALCULATE(X, Y):
    pass

def a():
    pass

# ✅ GOOD
def calculate_total(price, tax_rate):
    pass

def get_user_age():
    pass
```

**2. Keep Functions Small**
```python
# ❌ BAD: Too much in one function
def process_user_data(data):
    # validate
    # calculate
    # save
    # email
    # log
    pass

# ✅ GOOD: Single responsibility
def validate_user_data(data):
    pass

def calculate_stats(data):
    pass

def save_user(data):
    pass
```

**3. Use Type Hints**
```python
# ❌ Without type hints
def add(x, y):
    return x + y

# ✅ With type hints
def add(x: int, y: int) -> int:
    """Add two integers and return result"""
    return x + y
```

**4. Provide Default Values for Optional Parameters**
```python
# ❌ BAD
def create_user(username, password, email, city, country):
    pass

# ✅ GOOD
def create_user(username, password, email="", city="", country=""):
    pass
```

**5. Document Your Functions**
```python
def calculate_discount(price: float, discount: float) -> float:
    """
    Calculate discounted price.
    
    Args:
        price: Original price
        discount: Discount percentage (0-100)
    
    Returns:
        Final price after discount
    """
    return price * (1 - discount / 100)
```

**6. Handle Edge Cases**
```python
def divide(a: int, b: int) -> float:
    """Divide a by b, handle zero division"""
    if b == 0:
        return None  # or raise ValueError
    return a / b
```

**7. Avoid Side Effects**
```python
# ❌ BAD: Modifies global state
global_list = []

def add_item(item):
    global_list.append(item)  # Side effect

# ✅ GOOD: Pure function
def add_item(items, item):
    new_items = items.copy()
    new_items.append(item)
    return new_items
```

**8. Use *args and **kwargs Sparingly**
```python
# ❌ Hard to understand
def process(*args, **kwargs):
    pass

# ✅ Clear parameters
def process(name, age, email=None, phone=None):
    pass
```

---

## 1️⃣4️⃣ Common Patterns

**Pattern 1: Function Composition**
```python
def add(x, y):
    return x + y

def multiply(x, y):
    return x * y

def square(x):
    return x ** 2

# Chain operations
result = square(multiply(add(2, 3), 4))
print(result)  # (5 * 4)^2 = 400
```

**Pattern 2: Memoization**
```python
def fibonacci_memo(n, memo={}):
    """Fibonacci with memoization"""
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memo(n-1, memo) + fibonacci_memo(n-2, memo)
    return memo[n]

print(fibonacci_memo(10))  # Much faster than naive recursion
```

**Pattern 3: Callback Functions**
```python
def process_data(data, on_success, on_error):
    """Process data with callbacks"""
    try:
        result = validate_and_process(data)
        on_success(result)
    except Exception as e:
        on_error(str(e))

def success_handler(result):
    print(f"Success: {result}")

def error_handler(error):
    print(f"Error: {error}")

process_data(some_data, success_handler, error_handler)
```

**Pattern 4: Factory Pattern**
```python
def create_animal(animal_type):
    """Factory function to create animals"""
    if animal_type == "dog":
        return {"type": "dog", "sound": "woof"}
    elif animal_type == "cat":
        return {"type": "cat", "sound": "meow"}
    else:
        return None

dog = create_animal("dog")
cat = create_animal("cat")
```

---

## 1️⃣5️⃣ Real-World Examples

**Example 1: Credit Card Validator**
```python
def validate_credit_card(card_number):
    """Validate credit card using Luhn algorithm"""
    digits = [int(d) for d in str(card_number)]
    
    # Double every second digit from right
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    
    # Sum all digits
    total = sum(digits)
    
    return total % 10 == 0

print(validate_credit_card(4532015112830366))  # True
```

**Example 2: Email Validation**
```python
import re

def is_valid_email(email):
    """Validate email address"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

print(is_valid_email("user@example.com"))  # True
print(is_valid_email("invalid.email"))  # False
```

**Example 3: Password Strength Checker**
```python
def check_password_strength(password):
    """Check password strength and return score"""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("At least one uppercase letter")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("At least one lowercase letter")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("At least one digit")
    
    if any(c in "!@#$%^&*" for c in password):
        score += 2
    else:
        feedback.append("At least one special character")
    
    strength = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"][min(score, 5)]
    
    return {"score": score, "strength": strength, "feedback": feedback}

result = check_password_strength("Pass123!")
print(result)
```

**Example 4: Unit Converter**
```python
def convert_temperature(value, from_unit, to_unit):
    """Convert between temperature units"""
    # Convert to Celsius first
    if from_unit == "F":
        celsius = (value - 32) * 5/9
    elif from_unit == "K":
        celsius = value - 273.15
    else:
        celsius = value
    
    # Convert to target unit
    if to_unit == "F":
        return celsius * 9/5 + 32
    elif to_unit == "K":
        return celsius + 273.15
    else:
        return celsius

print(convert_temperature(32, "F", "C"))  # 0
print(convert_temperature(0, "C", "F"))   # 32
```

**Example 5: Permutation Generator**
```python
def generate_permutations(items):
    """Generate all permutations of items"""
    if len(items) <= 1:
        return [items]
    
    perms = []
    for i, item in enumerate(items):
        remaining = items[:i] + items[i+1:]
        for perm in generate_permutations(remaining):
            perms.append([item] + perm)
    
    return perms

print(generate_permutations([1, 2, 3]))
```

---

## 1️⃣6️⃣ Hands-On Exercises

**Exercise 1: Simple Calculator**
```python
# Create functions for basic math operations
def add(a, b):
    pass

def subtract(a, b):
    pass

def multiply(a, b):
    pass

def divide(a, b):
    pass

# Test your functions
# Challenge: Make a calculator that takes operation as parameter
```

**Exercise 2: Password Validator**
```python
# Create function that validates passwords
# Requirements:
# - Minimum 8 characters
# - At least one uppercase letter
# - At least one digit
# - Returns True/False

def validate_password(password):
    pass

# Test: validate_password("Secure123")  # True
```

**Exercise 3: Student Grade Analyzer**
```python
# Create function that analyzes student grades
def analyze_grades(grades):
    """
    Analyze grades and return:
    - average
    - highest
    - lowest
    - letter grade (A/B/C/D/F)
    """
    pass

# Test
grades = [85, 90, 78, 92, 88]
result = analyze_grades(grades)
# Should return dict with stats
```

**Exercise 4: List Manipulation**
```python
# Create function to:
def remove_duplicates(items):
    """Remove duplicate items from list"""
    pass

def find_common(list1, list2):
    """Find common items between two lists"""
    pass

def flatten_list(nested_list):
    """Flatten nested list structure"""
    pass

# Test with your own data
```

**Exercise 5: Text Processing**
```python
# Create function for text processing
def word_frequency(text):
    """Count frequency of each word"""
    pass

def is_palindrome(text):
    """Check if text is palindrome"""
    pass

def reverse_words(text):
    """Reverse order of words in text"""
    pass
```

---

## 1️⃣7️⃣ Function Flow Diagram

```
Function Call
    ↓
Parameters Passed
    ↓
Function Executes
    ├─ Local variables created
    ├─ Code runs
    └─ Can call other functions
    ↓
Return Statement
    ↓
Return Value Sent Back
    ↓
Continue in Calling Code
```

**Variable Lifetime:**
```
Global Variable
├─ Created: Start of program
├─ Accessible: Anywhere
└─ Destroyed: End of program

Local Variable
├─ Created: Function called
├─ Accessible: Inside function only
└─ Destroyed: Function ends
```

---