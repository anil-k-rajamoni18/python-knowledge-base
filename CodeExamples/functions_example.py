## What is a function in Python?
# A function is a reusable block of code that performs a specific task. 
# It allows you to organize your code into logical sections, making it easier to read and maintain. Functions can take input parameters, perform operations, and return output.

# Example of a simple function
def greet(name):
    return f"Hello, {name}!"

# Calling the function
print(greet("Surya"))  # Output: Hello, Surya!

# print(greet())  # Error: missing 1 required positional argument: 'name'

## Types of Functions in Python
# 1. Built-in Functions: These are functions that are provided by Python and are always available for use. 
# Examples include print(), len(), type(), etc.

# 2. User-Defined Functions: These are functions that you create yourself to perform specific tasks.
def add(a, b):
    return a + b

# Calling the user-defined function
print(add(5, 3))  # Output: 8


## Function Parameters and Arguments
# Parameters are the variables that are defined in the function definition, while arguments are the actual values that are passed to the function when it is called.

# 1. Postional Arguments
def subtract(a, b):
    return a - b

print(subtract(10, 4))  # Output: 6
# print(subtract(4))  # Error: missing 1 required positional argument: 'b'


# 2. Keyword Arguments
def divide(a, b):
    return a / b

print(divide(a=20, b=5))  # Output: 4.0
print(divide(b=5, a=20))  # Output: 4.0

# 3. Default Arguments
def power(base, exponent=2):
    return base ** exponent

print(power(5))  # Output: 25 (default exponent is 2)
print(power(5, 3))  # Output: 125 (exponent is overridden

# 4. Variable-Length Arguments
def sum_all(*args):
    print("Arguments received:", args)
    print("Type of args:", type(args))
    return sum(args)

print(sum_all(1, 2, 3, 4))  # Output: 10


# 5. Kwargs (Keyword Variable-Length Arguments)
def print_info(**kwargs):
    print("Keyword Arguments received:", kwargs)
    print("Type of kwargs:", type(kwargs))
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="New York")


# 6. Keyword-Only Arguments
def print_info(name, age, *, city): # The * indicates that city is a keyword-only argument
    print("Name:", name)
    print("Age:", age)
    print("City:", city)

print_info("Alice", 30, city="New York")

# 7. Positional-Only Arguments with Default Values
def print_info(name, age, city="Unknown"):
    print("Name:", name)
    print("Age:", age)
    print("City:", city)

print_info("Alice", 30)  # City will use default value "Unknown"
print_info("Alice", 30, "New York")  # City will be overridden to "New York"

# Error scenario: Positional-Only Arguments with Default Values
# def print_info(city="Unknown", name, age):
#     print("Name:", name)
#     print("Age:", age)
#     print("City:", city)


## Returning Values from Functions
def calculate_area(radius):
    import math
    area = math.pi * radius ** 2
    return area

print(calculate_area(5))  # Output: 78.53981633974483

# Multiple Return Values
def get_user_info():
    name = "Alice"
    age = 30
    city = "New York"
    return name, age, city

user_data = get_user_info()
print("User Data:", user_data)  # Output: ('Alice', 30, 'New York')

# No Return Value (returns None by default)
def print_greeting(name):
    print(f"Hello, {name}!")

result = print_greeting("Bob")  # Output: Hello, Bob!
print("Result of print_greeting:", result)  # Output: Result of print_greeting


## Nested Functions

def say_hello(name):
    print(f"Hello, {name}!")

greet = say_hello  # Assigning the function to a variable
print(say_hello)
print(greet)
say_hello("Alice")  # Output: Hello, Alice!
greet("Bob")  # Output: Hello, Bob!


def calculator(operation):
    def add(a, b):
        return a + b
    
    def subtract(a, b):
        return a - b
    
    if operation == "add":
        return add
    elif operation == "subtract":
        return subtract
    else:
        raise ValueError("Invalid operation")
    

add_function = calculator("add")
subtract_function = calculator("subtract")

print(add_function(5, 3))  # Output: 8
print(subtract_function(5, 3))  # Output: 2


# Closures
def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

closure_example = outer_function(10)
print(closure_example(5))  # Output: 15

# Realtime Example of Closures
def make_multiplier(multiplier):
    def multiplier_function(x):
        return x * multiplier
    return multiplier_function


double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # Output: 10
print(triple(5))  # Output: 15


# Lambda Functions
# Lambda functions are anonymous functions that are defined using the lambda keyword.
#  They are often used for short, simple functions that are not reused elsewhere in the code.

# Syntax: lambda arguments: expression

# regular function
def square(x):
    return x ** 2

# lambda function
square_lambda = lambda x: x ** 2
print(square(5))  # Output: 25
print(square_lambda(5))  # Output: 25

# Lambda functions with multiple arguments
add = lambda a, b: a + b
print(add(3, 4))  # Output: 7

# Lambda functions with no arguments
greet = lambda: "Hello, World!"
print(greet())  # Output: Hello, World!

# Lambda with conditional expression
max_value = lambda a, b: a if a > b else b
print(max_value(10, 20))  # Output: 20

is_even = lambda x: x % 2 == 0
print(is_even(4))  # Output: True
print(is_even(5))  # Output: False


# map(function, iterable)
# The map function applies a given function to each item of an iterable (like a list) and returns a map object (which is an iterator). 
# You can convert the map object to a list or other iterable type if needed.


# example-1

numbers = [1, 2, 3, 4, 5]
squared = map(lambda x: x ** 2, numbers)
print(squared)  # Output: <map object at 0x...>
print(list(squared))  # Output: [1, 4, 9, 16, 25]

# example-2
names = ["Alice", "Bob", "Charlie"]
greeted_names = map(lambda name: f"Hello, {name}!", names)
print(list(greeted_names))  # Output: ['Hello, Alice!', 'Hello, Bob!', 'Hello, Charlie!']

# example-3
ages = [25, 30, 35]
age_groups = map(lambda age: "Adult" if age >= 18 else "Minor", ages)
print(list(age_groups))  # Output: ['Adult', 'Adult', 'Adult']

# example-4
names = ["surRya ", "kriSHna ", "sita "]
normalized_names = map(lambda name: name.strip().lower(), names)
print(list(normalized_names))  # Output: ['surya', 'krishna', 'sita']


# filter(function, iterable)
# The filter function constructs an iterator from elements of an iterable for which a function returns true.

numbers = [1, 2, 3, 4, 5]
even_numbers = filter(lambda x: x % 2 == 0, numbers)
print(list(even_numbers))  # Output: [2, 4]


names = "surya krishna sita".split()
long_names = filter(lambda name: len(name) > 4, names)
print(list(long_names))  # Output: ['surya', 'krishna']

name = "vikram aditya"
vowel_names = filter(lambda name: name[0].lower() in 'aeiou', name.split())
print(list(vowel_names))  # Output: ['aditya']


# Reduce(function, iterable)
# The reduce function applies a rolling computation to sequential pairs of values in an iterable.
# How it works: It takes the first two elements of the iterable and applies the function to them, then takes the result and applies the function to it and the next element, and so on until all elements have been processed. The final result is a single value.

from functools import reduce

numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
print(product)  # Output: 120


# example-2
from operator import add
sum = reduce(add, numbers)
print(sum)  # Output: 15

# example-3 with strings
words = ["Hello", "World", "from", "Python"]
sentence = reduce(lambda x, y: x + " " + y, words)
print(sentence)  # Output: Hello World from Python


## Local Variables
# A local variable is declared inside a function and can only be used within that function.
def add():
    a = 10
    b = 20
    print(a + b)

add()

# Global Variables
# A global variable is declared outside all functions and can be accessed anywhere.
x = 100

def show():
    print(x)

show()

# Modifying Global Variable Inside Function
# -> By default, Python treats variables inside a function as local.
# -> To modify global variable → use global keyword.

count = 0

def increment():
    global count
    count = count + 1
    print(count)

increment()
print(count)


balance = 1000

def deposit(amount):
    global balance
    balance += amount

deposit(500)
print(balance)


# # LEGB Rule (Scope Resolution)
# L – Local
# E – Enclosing
# G – Global
# B – Built-in

x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)

    inner()

outer()

## Local Scope (Inside Inner Function)
def outer():
    def inner():
        x = 10
        print(x)
    inner()

outer()

## Enclosing Scope
def outer():
    x = 20

    def inner():
        print(x)

    inner()

outer()

# Global Scope with Nested Functions
x = 100

def outer():
    def inner():
        print(x)
    inner()

outer()

# Modifying Enclosing Variable → nonlocal
# -> If you want to modify a variable from the outer function, use nonlocal.
def outer():
    x = 10

    def inner():
        nonlocal x
        x = 20
        print("Inner:", x)

    inner()
    print("Outer:", x)

outer()


# Full Example
x = "Global"

def outer():
    x = "Enclosing"

    def inner():
        x = "Local"
        print(x)

    inner()
    print(x)

outer()
print(x)


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

result = login_user("surya", "hello123")
if result["success"]:
    print(f"Welcome user {result['user_id']}")
else:
    print(f"Error: {result['message']}")



###
import re
from datetime import date
import random
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
            "userId": "USR" + str(random.randint(1,100)),
            "username": username,
            "email": email,
            "created_at": date.today().strftime("%Y-%m-%d")
        }
    }

# Test
result = register_user("alice", "alice@example.com", "Password123")
print(result)

def sum_of_n_numbers(n):
    """Calculate sum of n numbers recursively"""
    if n <= 1:  # BASE CASE
        return 1
    return n + sum_of_n_numbers(n - 1)  # RECURSIVE CALL

n=100
print(f"sum of numbers of {n} = {sum_of_n_numbers(n)}")


## 

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

##
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
    # time.sleep(2)
    return "Done"

slow_function()

@timer_decorator
def sum_of_numbers(num: int) -> int:
    sum:int = 0
    for i in range(1, num+1):
        sum = sum + i
    return sum

num=5000000
print(f"Sum of N {num}s = {sum_of_numbers(num)}")