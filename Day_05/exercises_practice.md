# Python Full Stack — Day 5 Exercise & Practice File
# Topic: OOP Fundamentals — Classes, Objects, Methods & the Four Pillars

> **Instructions:** Work through sections in order. Write your predictions before running. Attempt every problem before checking the answer key. Many problems build on each other.

---

## 📋 Setup Check

```python
# Run this first
import sys
print(f"Python version: {sys.version}")

# Quick OOP sanity check
class TestClass:
    class_var = "shared"
    def __init__(self, value):
        self.instance_var = value

t = TestClass("hello")
print(f"class_var: {t.class_var}")
print(f"instance_var: {t.instance_var}")
print("✅ Setup OK!")
```

---

## Section A — Predict the Output (No Running Allowed!)

### A1. Instance vs Class Variables

```python
class Dog:
    species = "Canis lupus familiaris"  # class variable
    count = 0

    def __init__(self, name: str):
        Dog.count += 1
        self.name = name

d1 = Dog("Rex")
d2 = Dog("Buddy")
d3 = Dog("Max")

print(d1.species)           # Line 1
print(Dog.species)          # Line 2
print(d1.count)             # Line 3
print(Dog.count)            # Line 4
print(d1.name, d2.name)     # Line 5

d1.species = "Wolf"         # What does this do?
print(d1.species)           # Line 6
print(d2.species)           # Line 7
print(Dog.species)          # Line 8
```

**Predictions:**
```
Line 1: ______
Line 2: ______
Line 3: ______
Line 4: ______
Line 5: ______
Line 6: ______
Line 7: ______
Line 8: ______
```

---

### A2. Method Types

```python
class Calculator:
    brand = "CalcPro"
    _calc_count = 0

    def __init__(self, model: str):
        self.model = model
        Calculator._calc_count += 1

    def add(self, a, b):
        return a + b

    @classmethod
    def get_brand(cls):
        return cls.brand

    @classmethod
    def total_made(cls):
        return cls._calc_count

    @staticmethod
    def is_positive(n):
        return n > 0

c1 = Calculator("X100")
c2 = Calculator("X200")

print(c1.add(3, 4))             # Line 1
print(Calculator.get_brand())   # Line 2
print(c1.get_brand())           # Line 3 — calling classmethod on instance
print(Calculator.total_made())  # Line 4
print(Calculator.is_positive(-5))  # Line 5
print(c1.is_positive(10))          # Line 6 — static method on instance
```

**Predictions:**
```
Line 1: ___
Line 2: ______
Line 3: ______
Line 4: ___
Line 5: ___
Line 6: ___
```

---

### A3. `__init__` and `__str__` / `__repr__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

p1 = Point(3, 4)
p2 = Point(0, 0)

print(p1)               # Line 1
print(repr(p1))         # Line 2
print(str(p1))          # Line 3
print([p1, p2])         # Line 4 — what does a list use?
print(f"Point: {p1}")   # Line 5 — f-strings use which?
```

**Predictions:**
```
Line 1: ______
Line 2: ______
Line 3: ______
Line 4: ______
Line 5: ______
```

---

### A4. The Mutable Class Variable Trap

```python
class Team:
    members = []        # ← class variable

    def __init__(self, name):
        self.name = name

    def add_member(self, member):
        self.members.append(member)

team_a = Team("Alpha")
team_b = Team("Beta")

team_a.add_member("Alice")
team_a.add_member("Bob")
team_b.add_member("Carol")

print(team_a.members)   # Line 1
print(team_b.members)   # Line 2
print(Team.members)     # Line 3
print(len(Team.members))# Line 4
```

**Predictions:**
```
Line 1: ______________________________
Line 2: ______________________________
Line 3: ______________________________
Line 4: ___
```

**Explain what you observe and why:**
```
_______________________________________________
_______________________________________________
```

---

### A5. `__dict__` Inspection

```python
class Config:
    debug = False
    version = "1.0"

    def __init__(self, env):
        self.env = env

c = Config("production")
c.debug = True          # shadowing

print(c.__dict__)               # Line 1
print(Config.__dict__.get("debug"))  # Line 2
print(c.debug)                  # Line 3
print(Config.debug)             # Line 4
```

**Predictions:**
```
Line 1: ______________________________
Line 2: ___
Line 3: ___
Line 4: ___
```

---

## Section B — Fill in the Blanks

### B1. Complete the Class

```python
class Rectangle:
    # 1. Class variable tracking total rectangles created
    ______ = 0

    # 2. Constructor with width and height
    def ______(self, width: float, height: float):
        Rectangle.total += 1
        self.______ = width
        self.______ = height

    # 3. Instance method returning area
    def area(______) -> float:
        return self.______ * self.______

    # 4. Instance method returning perimeter
    def perimeter(self) -> ______:
        return 2 * (self.width + self.height)

    # 5. Class method — creates a square (all sides equal)
    @______
    def create_square(______, side: float) -> "Rectangle":
        return ______(side, side)

    # 6. Static method — checks if dimensions are valid
    @______
    def is_valid(width: float, height: float) -> bool:
        return width > 0 and height > 0

    # 7. __str__ representation
    def ______(self):
        return f"Rectangle({self.width}x{self.height})"
```

---

### B2. Fix the Method Types

```python
class Temperature:
    absolute_zero = -273.15     # class variable

    def __init__(self, celsius):
        self.celsius = celsius

    # BUG: This should be a @staticmethod — fix it
    @classmethod
    def is_valid(cls, value):
        return value >= Temperature.absolute_zero

    # BUG: This should be a @classmethod factory method — fix it
    @staticmethod
    def from_fahrenheit(f):
        return Temperature((f - 32) * 5 / 9)   # can't support subclasses!

    # BUG: This should be an instance method — fix it
    @staticmethod
    def to_fahrenheit():
        return self.celsius * 9 / 5 + 32        # NameError: self not defined
```

**Write the corrected version of each method:**
```python
# Fixed is_valid:
______________________
______________________

# Fixed from_fahrenheit:
______________________
______________________

# Fixed to_fahrenheit:
______________________
______________________
```

---

### B3. Complete the `__init__` with Validation

```python
class BankAccount:
    MINIMUM_BALANCE = 0.0

    def __init__(self, owner: str, initial_balance: float = 0.0):
        # 1. Validate owner is non-empty string
        if not ______ or not ______:
            raise ______("Owner must be a non-empty string")

        # 2. Validate balance is not negative
        if initial_balance ______:
            raise ValueError(f"Balance cannot be negative, got {initial_balance}")

        # 3. Set instance variables
        self.______ = owner.strip()
        self.______ = initial_balance
        self.______ = []    # transaction history
```

---

## Section C — Debugging Exercises

### C1. The Missing `self`

```python
class Counter:
    count = 0

    def increment():          # Bug is here
        count += 1            # Another bug here

    def get_count(self):
        return self.count

c = Counter()
c.increment()
print(c.get_count())
```

**Identify both bugs and fix:**
```python
class Counter:
    count = 0

    def increment(______):    # Fix 1
        ______.______ += 1    # Fix 2

    def get_count(self):
        return self.count
```

---

### C2. The Broken Factory Method

```python
class Shape:
    def __init__(self, color="red"):
        self.color = color

    def describe(self):
        return f"A {self.color} {self.__class__.__name__}"

class Circle(Shape):
    def __init__(self, radius, color="red"):
        super().__init__(color)
        self.radius = radius

    @staticmethod           # Bug: should be @classmethod
    def create_blue():
        return Shape(color="blue")  # Bug: hardcoded Shape, not Circle

c = Circle.create_blue()
print(type(c).__name__)     # Prints "Shape" — should print "Circle"
print(c.describe())         # Missing radius!
```

**Fix both bugs:**
```python
class Circle(Shape):
    def __init__(self, radius, color="red"):
        super().__init__(color)
        self.radius = radius

    @______
    def create_blue(______):
        return ______(radius=5, color="blue")

c = Circle.create_blue()
print(type(c).__name__)     # Should print: Circle
```

---

### C3. The Shared Mutable State Bug

```python
class Student:
    # Bug is on the next line
    subjects = []

    def __init__(self, name):
        self.name = name

    def enroll(self, subject):
        self.subjects.append(subject)

alice = Student("Alice")
bob = Student("Bob")

alice.enroll("Math")
alice.enroll("Physics")
bob.enroll("History")

print(f"Alice: {alice.subjects}")
print(f"Bob: {bob.subjects}")
# Both show the same list! Bug!
```

**Fix the bug:**
```python
class Student:
    def __init__(self, name):
        self.name = name
        self.subjects = ______    # Fix here
```

---

### C4. The Broken Property

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius    # Bug: should be self._radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius must be non-negative")
        self._radius = value
```

**What happens when you run `c = Circle(5)` with this code?**
```
Error description: _______________________________
Why: _____________________________________________
```

**The code is actually correct as written — explain why `self.radius = radius` in `__init__` works properly:**
```
_______________________________________________
_______________________________________________
```

---

### C5. The Wrong `__repr__`

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        # Bug: this should be __str__ behavior, and __repr__ should be unambiguous
        return f"{self.name}: ${self.price}"

p = Product("Widget", 9.99)
products = [p, Product("Gadget", 19.99)]
print(products)     # Hard to debug — not clear how to recreate
```

**Write both `__str__` and a proper `__repr__`:**
```python
def __str__(self):
    return ______

def __repr__(self):
    return ______

# Test:
# print(p)          → "Widget: $9.99"
# print(repr(p))    → "Product(name='Widget', price=9.99)"
# print([p])        → [Product(name='Widget', price=9.99)]
```

---

## Section D — Write the Code

### D1. BankAccount — Full Implementation

Implement the complete `BankAccount` class with all features discussed in theory:

```python
from datetime import datetime
from typing import Optional


class BankAccount:
    """
    Complete bank account implementation.

    Class variables:
    - bank_name: str = "Python National Bank"
    - interest_rate: float = 0.035
    - _account_counter: int = 0

    Instance variables:
    - account_number (auto-assigned)
    - owner: str
    - balance: float
    - account_type: str
    - _transaction_history: list[dict]
    - _is_active: bool

    Instance methods:
    - deposit(amount) → float: new balance
    - withdraw(amount) → float: new balance
    - get_balance() → float
    - apply_interest() → float: interest earned
    - get_statement() → str: formatted statement
    - close_account() → None

    Class methods:
    - create_savings_account(owner, balance) → BankAccount
    - create_joint_account(owner1, owner2, balance) → BankAccount
    - get_total_accounts() → int
    - update_interest_rate(rate) → None

    Static methods:
    - validate_account_number(num) → bool
    - format_currency(amount, currency="USD") → str
    - calculate_compound_interest(principal, rate, years) → float

    Dunder methods:
    - __str__: "Account #N | Owner | $Balance | Type"
    - __repr__: "BankAccount(owner='...', balance=..., type='...')"
    """

    # Your complete implementation here
    pass


# ── Test Suite ──────────────────────────────────────────────────────────────
def test_bank_account():
    # Test 1: Basic account creation
    alice = BankAccount("Alice", 1000.0)
    bob = BankAccount("Bob", 500.0)
    assert alice.account_number != bob.account_number
    assert BankAccount.get_total_accounts() >= 2

    # Test 2: Deposit and withdraw
    alice.deposit(500)
    assert alice.get_balance() == 1500.0
    alice.withdraw(200)
    assert alice.get_balance() == 1300.0

    # Test 3: Interest
    interest = alice.apply_interest()
    assert interest > 0
    assert alice.balance > 1300.0

    # Test 4: Class methods
    savings = BankAccount.create_savings_account("Carol", 5000)
    assert savings.account_type == "savings"

    joint = BankAccount.create_joint_account("Diana", "Eve", 2000)
    assert "Diana" in joint.owner and "Eve" in joint.owner

    # Test 5: Static methods
    assert BankAccount.validate_account_number(1) == True
    assert BankAccount.validate_account_number(-1) == False
    assert "$" in BankAccount.format_currency(100)

    # Test 6: Error handling
    try:
        alice.withdraw(999999)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # Test 7: Statement
    statement = alice.get_statement()
    assert "Alice" in statement
    assert "Python National Bank" in statement

    print("✅ All BankAccount tests passed!")

test_bank_account()
```

---

### D2. Library Book System

```python
class Book:
    """
    Library book management system.

    Class variables:
    - library_name: str = "City Public Library"
    - _total_books: int = 0

    Instance variables:
    - title: str
    - author: str
    - isbn: str
    - is_available: bool = True
    - borrow_count: int = 0
    - _book_id: int (auto-assigned)

    Instance methods:
    - borrow() → None: mark unavailable, increment borrow_count
      raises RuntimeError if already borrowed
    - return_book() → None: mark available
      raises RuntimeError if not borrowed
    - get_info() → str: formatted book info
    - __str__, __repr__

    Class methods:
    - from_isbn(cls, isbn, title, author) → Book: factory method
    - get_total_books(cls) → int

    Static methods:
    - is_valid_isbn(isbn: str) → bool
      ISBN-13: exactly 13 digits, all numeric
    - format_isbn(isbn: str) → str
      formats as: 978-1-59327-928-8 (split at positions 3,4,10,12)
    """

    # Your implementation here
    pass


# Test
def test_book():
    b1 = Book("Python Crash Course", "Eric Matthes", "9781593279288")
    b2 = Book("Clean Code", "Robert Martin", "9780132350884")

    print(b1.get_info())
    assert Book.get_total_books() == 2

    b1.borrow()
    assert b1.is_available == False
    assert b1.borrow_count == 1

    try:
        b1.borrow()             # already borrowed!
        assert False
    except RuntimeError:
        pass

    b1.return_book()
    assert b1.is_available == True

    assert Book.is_valid_isbn("9781593279288") == True
    assert Book.is_valid_isbn("123") == False
    assert Book.is_valid_isbn("978159327928X") == False   # contains letter

    b3 = Book.from_isbn("9780201633610", "Design Patterns", "GoF")
    assert b3.title == "Design Patterns"
    assert Book.get_total_books() == 3

    print("✅ All Book tests passed!")

test_book()
```

---

### D3. Temperature Class with Properties

```python
class Temperature:
    """
    Temperature with multi-unit support.

    Stores internally in Celsius.
    Properties: celsius, fahrenheit, kelvin (computed)
    Class methods: from_fahrenheit, from_kelvin
    Static methods: is_valid_celsius
    Dunder: __str__, __repr__, __eq__, __lt__, __le__, __gt__, __ge__
    """

    ABSOLUTE_ZERO = -273.15

    def __init__(self, celsius: float):
        # Use the property setter for validation
        self.celsius = celsius  # triggers @celsius.setter

    @property
    def celsius(self) -> float:
        # Your implementation
        pass

    @celsius.setter
    def celsius(self, value: float) -> None:
        # Validate: must be >= ABSOLUTE_ZERO
        # Your implementation
        pass

    @property
    def fahrenheit(self) -> float:
        # C × 9/5 + 32
        pass

    @property
    def kelvin(self) -> float:
        # C + 273.15
        pass

    @classmethod
    def from_fahrenheit(cls, f: float) -> "Temperature":
        # (F - 32) × 5/9
        pass

    @classmethod
    def from_kelvin(cls, k: float) -> "Temperature":
        # K - 273.15
        pass

    @staticmethod
    def is_valid_celsius(value: float) -> bool:
        pass

    def __str__(self):
        return f"{self.celsius:.2f}°C / {self.fahrenheit:.2f}°F / {self.kelvin:.2f}K"

    def __repr__(self):
        return f"Temperature(celsius={self.celsius})"

    def __eq__(self, other):
        if isinstance(other, Temperature):
            return abs(self.celsius - other.celsius) < 1e-9
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Temperature):
            return self.celsius < other.celsius
        return NotImplemented


# Tests
def test_temperature():
    t1 = Temperature(100)
    assert t1.fahrenheit == 212.0
    assert t1.kelvin == 373.15
    print(str(t1))     # 100.00°C / 212.00°F / 373.15K

    t2 = Temperature.from_fahrenheit(32)
    assert t2.celsius == 0.0

    t3 = Temperature.from_kelvin(0)
    assert abs(t3.celsius - (-273.15)) < 0.01

    assert Temperature.is_valid_celsius(-273.15) == True
    assert Temperature.is_valid_celsius(-274) == False

    try:
        Temperature(-300)       # below absolute zero
        assert False
    except ValueError:
        pass

    assert Temperature(100) > Temperature(0)
    assert Temperature(0) == Temperature.from_fahrenheit(32)
    sorted_temps = sorted([Temperature(100), Temperature(0), Temperature(37)])
    print([str(t) for t in sorted_temps])

    print("✅ All Temperature tests passed!")

test_temperature()
```

---

### D4. Vehicle Hierarchy Starter (Preview for Day 6)

```python
"""
Build a vehicle system using OOP fundamentals (no inheritance yet).
Use class variables for shared specs, instance methods for behavior.
"""

class Vehicle:
    """
    Represents any vehicle.

    Class variables:
    - max_speed_limit: int = 120 (km/h — legal limit)
    - _total_vehicles: int = 0

    Instance variables:
    - make: str
    - model: str
    - year: int
    - _current_speed: float = 0
    - _mileage: float = 0
    - _fuel: float (starts at max capacity)
    - fuel_capacity: float
    - fuel_efficiency: float (km per liter)

    Properties:
    - current_speed: float (read-only)
    - mileage: float (read-only)
    - fuel_level: float (read-only)
    - fuel_percentage: float (0-100, read-only)

    Instance methods:
    - accelerate(amount: float) → None: increase speed up to max_speed_limit
    - brake(amount: float) → None: decrease speed, floor at 0
    - drive(distance: float) → dict: simulate driving
      - calculate fuel consumed
      - update mileage
      - return {"distance": ..., "fuel_used": ..., "fuel_remaining": ...}
      - raises ValueError if not enough fuel or speed == 0
    - refuel(liters: float) → float: add fuel, return new level
    - get_status() → str: formatted current status

    Class methods:
    - get_total_vehicles() → int

    Static methods:
    - speed_in_mph(kmh: float) → float: convert km/h to mph
    - is_vintage(year: int) → bool: True if more than 25 years old

    Dunder: __str__, __repr__
    """
    pass


# Test
car = Vehicle("Toyota", "Camry", 2020, fuel_capacity=50, fuel_efficiency=15)
car.accelerate(60)
result = car.drive(30)
print(result)           # {'distance': 30, 'fuel_used': 2.0, 'fuel_remaining': 48.0}
car.brake(30)
print(car.current_speed)    # 30

print(Vehicle.speed_in_mph(100))     # 62.14
print(Vehicle.is_vintage(1995))      # True
print(Vehicle.get_total_vehicles())  # 1
print(car.get_status())
```

---

## Section E — Class Observation Experiments

### E1. `__dict__` Explorer

```python
# Run this and study the output carefully
class Person:
    species = "Homo sapiens"
    population = 0

    def __init__(self, name, age):
        Person.population += 1
        self.name = name
        self.age = age

p1 = Person("Alice", 30)
p2 = Person("Bob", 25)

print("=== Instance __dict__ ===")
print(f"p1.__dict__ = {p1.__dict__}")
print(f"p2.__dict__ = {p2.__dict__}")

print("\n=== Class __dict__ (selected) ===")
print(f"species:    {Person.__dict__['species']}")
print(f"population: {Person.__dict__['population']}")

print("\n=== Shadowing experiment ===")
p1.species = "Human"   # creates instance var
print(f"p1.species:     {p1.species}")
print(f"p2.species:     {p2.species}")
print(f"Person.species: {Person.species}")
print(f"p1.__dict__:    {p1.__dict__}")  # species now in p1's dict

print("\n=== vars() is same as __dict__ ===")
print(vars(p1) == p1.__dict__)   # True
```

**Questions to answer after running:**
```
1. What's in p1.__dict__ initially? ______________________
2. After p1.species = "Human", what's in p1.__dict__? ______
3. Does modifying p1.species affect Person.species? ______
4. Does modifying p1.species affect p2.species? ______
```

---

### E2. Method Calling Equivalents

```python
class Greeter:
    greeting = "Hello"

    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"{self.greeting}, {self.name}!"

    @classmethod
    def formal_greeting(cls):
        return f"Good day from {cls.__name__}"

    @staticmethod
    def random_greeting():
        return "Howdy!"

g = Greeter("Alice")

# Test that these are equivalent
print(g.greet())                    # normal call
print(Greeter.greet(g))             # unbound call — same result?

print(g.formal_greeting())          # instance calling classmethod
print(Greeter.formal_greeting())    # class calling classmethod — same?

print(g.random_greeting())          # instance calling staticmethod
print(Greeter.random_greeting())    # class calling staticmethod — same?
```

**Record what you observe:**
```
g.greet() == Greeter.greet(g)?      ______
g.formal_greeting() == Greeter.formal_greeting()?  ______
g.random_greeting() == Greeter.random_greeting()?  ______

What does this tell you about how Python methods work internally?
_______________________________________________
```

---

### E3. The Class Variable Counter Pattern

```python
# Build and test this pattern carefully
class Tracked:
    _instances = 0

    def __init__(self, label):
        Tracked._instances += 1
        self.label = label
        self.id = Tracked._instances

    @classmethod
    def count(cls):
        return cls._instances

    def __del__(self):
        Tracked._instances -= 1

# Create instances
a = Tracked("alpha")
b = Tracked("beta")
c = Tracked("gamma")
print(f"After creating 3: {Tracked.count()}")   # 3

del b
print(f"After deleting b: {Tracked.count()}")   # 2

d = Tracked("delta")
print(f"After adding d:   {Tracked.count()}")   # 3

# What is a.id? b.id (before deletion)? c.id? d.id?
print(f"a.id={a.id}, c.id={c.id}, d.id={d.id}")
```

**Questions:**
```
After creating a, b, c: count = ___
After del b: count = ___
After adding d: count = ___
a.id = ___, c.id = ___, d.id = ___
Is __del__ guaranteed to be called immediately on del? ______
```

---

## Section F — Mini Project: Complete Inventory System

```python
"""
Inventory Management System

Two classes: Product and Inventory

Product:
- Class var: category_tax = {"electronics": 0.18, "food": 0.05, "clothing": 0.12}
- Class var: _total_products = 0
- Instance vars: name, sku, price, quantity, category
- Properties: total_value, price_with_tax
- Instance methods: apply_discount(pct), add_stock(qty), sell(qty) → returns sold qty
  sell raises ValueError if qty > stock
- Class method: from_dict(data: dict) → Product
- Static method: generate_sku(name, category) → str (e.g., "ELEC-0001")
- __str__, __repr__

Inventory:
- Instance vars: name, _products = {}
- Instance methods:
  - add_product(product)
  - remove_product(sku) → bool
  - get_product(sku) → Optional[Product]
  - search(query) → list[Product]: name contains query (case-insensitive)
  - low_stock(threshold=5) → list[Product]
  - total_value() → float
  - category_summary() → dict: category → total value
  - restock_report() → str: formatted list of low stock items
- __len__, __str__
"""

from typing import Optional


class Product:
    category_tax = {
        "electronics": 0.18,
        "food": 0.05,
        "clothing": 0.12,
        "general": 0.08
    }
    _total_products = 0

    def __init__(self, name: str, price: float, quantity: int, category: str = "general"):
        # Your implementation
        pass

    @property
    def total_value(self) -> float:
        """Price × quantity"""
        pass

    @property
    def price_with_tax(self) -> float:
        """Price including category tax"""
        pass

    def apply_discount(self, percent: float) -> None:
        """Reduce price by percent%"""
        pass

    def add_stock(self, qty: int) -> None:
        pass

    def sell(self, qty: int) -> int:
        """Sell qty units. Returns actual sold quantity."""
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        pass

    @staticmethod
    def generate_sku(name: str, category: str) -> str:
        """e.g., 'Laptop Pro' + 'electronics' → 'ELEC-0001'"""
        # Use first 4 letters of category + sequential number
        pass

    def __str__(self):
        return f"{self.name} | {self.sku} | ₹{self.price:.2f} | Qty: {self.quantity}"

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, qty={self.quantity})"


class Inventory:
    def __init__(self, name: str):
        self.name = name
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        self._products[product.sku] = product

    def remove_product(self, sku: str) -> bool:
        return self._products.pop(sku, None) is not None

    def get_product(self, sku: str) -> Optional[Product]:
        return self._products.get(sku)

    def search(self, query: str) -> list[Product]:
        q = query.lower()
        return [p for p in self._products.values() if q in p.name.lower()]

    def low_stock(self, threshold: int = 5) -> list[Product]:
        return [p for p in self._products.values() if p.quantity <= threshold]

    def total_value(self) -> float:
        return sum(p.total_value for p in self._products.values())

    def category_summary(self) -> dict[str, float]:
        from collections import defaultdict
        summary = defaultdict(float)
        for p in self._products.values():
            summary[p.category] += p.total_value
        return dict(summary)

    def restock_report(self) -> str:
        low = self.low_stock()
        if not low:
            return "✅ All products adequately stocked."
        lines = ["⚠️  Restock Required:", "-" * 40]
        for p in sorted(low, key=lambda x: x.quantity):
            lines.append(f"  {p.name:<25} Qty: {p.quantity:>4}")
        return "\n".join(lines)

    def __len__(self):
        return len(self._products)

    def __str__(self):
        return f"Inventory: {self.name} ({len(self)} products, ₹{self.total_value():,.2f} total)"


# ── Test ────────────────────────────────────────────────────────────────────
def run_inventory_demo():
    inv = Inventory("Main Warehouse")

    # Add products
    laptop = Product("Laptop Pro", 75000, 10, "electronics")
    phone = Product("Smartphone X", 45000, 3, "electronics")
    rice = Product("Rice 5kg", 250, 100, "food")
    shirt = Product("Cotton Shirt", 599, 50, "clothing")
    pen = Product("Ball Pen Pack", 45, 4, "general")

    for p in [laptop, phone, rice, shirt, pen]:
        inv.add_product(p)

    print(inv)
    print()

    # Test operations
    laptop.sell(2)
    laptop.apply_discount(10)
    print(f"Laptop after 10% discount: ₹{laptop.price:.2f}")
    print(f"Laptop with tax: ₹{laptop.price_with_tax:.2f}")

    # Search
    results = inv.search("pro")
    print(f"\nSearch 'pro': {[p.name for p in results]}")

    # Low stock
    print(f"\nLow stock (≤5): {[p.name for p in inv.low_stock()]}")
    print()
    print(inv.restock_report())
    print()

    # Category summary
    print("Category Summary:")
    for cat, val in sorted(inv.category_summary().items()):
        print(f"  {cat:<15}: ₹{val:>12,.2f}")

    # From dict
    tablet = Product.from_dict({
        "name": "Tablet Mini",
        "price": 25000,
        "quantity": 8,
        "category": "electronics"
    })
    inv.add_product(tablet)
    print(f"\nAfter adding tablet: {inv}")

if __name__ == "__main__":
    run_inventory_demo()
```

---

## ✅ Answer Key

<details>
<summary>Click to reveal — attempt everything first!</summary>

### A1 Answers
```
Line 1: Canis lupus familiaris  (class variable)
Line 2: Canis lupus familiaris  (same class variable)
Line 3: 3  (count is class variable — shared across all)
Line 4: 3
Line 5: Rex Buddy
Line 6: Wolf  (d1's own instance variable — shadowing)
Line 7: Canis lupus familiaris  (d2 still uses class variable)
Line 8: Canis lupus familiaris  (class variable unchanged)
```

### A2 Answers
```
Line 1: 7
Line 2: CalcPro
Line 3: CalcPro  (classmethod works on instances too)
Line 4: 2
Line 5: False
Line 6: True  (staticmethod works on instances too)
```

### A3 Answers
```
Line 1: (3, 4)  ← __str__
Line 2: Point(x=3, y=4)  ← __repr__
Line 3: (3, 4)  ← str() calls __str__
Line 4: [Point(x=3, y=4), Point(x=0, y=0)]  ← lists use __repr__
Line 5: Point: (3, 4)  ← f-strings use __str__
```

### A4 Answers
```
Line 1: ['Alice', 'Bob', 'Carol']
Line 2: ['Alice', 'Bob', 'Carol']
Line 3: ['Alice', 'Bob', 'Carol']
Line 4: 3

Explanation: Team.members is a class variable — ONE list shared by all instances.
append() mutates the existing list (no assignment → no shadowing).
All instances and the class see the same list.
```

### A5 Answers
```
Line 1: {'env': 'production', 'debug': True}  (debug is now an instance var)
Line 2: False  (class-level debug is still False)
Line 3: True   (c's instance var shadows class var)
Line 4: False  (class var unchanged)
```

### B1 Answer
```python
class Rectangle:
    total = 0

    def __init__(self, width: float, height: float):
        Rectangle.total += 1
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    @classmethod
    def create_square(cls, side: float) -> "Rectangle":
        return cls(side, side)

    @staticmethod
    def is_valid(width: float, height: float) -> bool:
        return width > 0 and height > 0

    def __str__(self):
        return f"Rectangle({self.width}x{self.height})"
```

### B2 Fix
```python
@staticmethod
def is_valid(value):
    return value >= Temperature.absolute_zero

@classmethod
def from_fahrenheit(cls, f):
    return cls((f - 32) * 5 / 9)

def to_fahrenheit(self):
    return self.celsius * 9 / 5 + 32
```

### C1 Fix
```python
def increment(self):        # Fix 1: add self
    Counter.count += 1      # Fix 2: use Counter.count or self.count
```

### C2 Fix
```python
@classmethod
def create_blue(cls):
    return cls(radius=5, color="blue")  # cls = Circle when called on Circle
```

### C3 Fix
```python
def __init__(self, name):
    self.name = name
    self.subjects = []   # instance variable — each student gets their own
```

### C4 Explanation
```
self.radius = radius in __init__ triggers the @radius.setter because self.radius
is defined as a property. The setter then validates and assigns to self._radius.
This is correct and intended behavior — properties work through __init__ too.
```

### C5 Fix
```python
def __str__(self):
    return f"{self.name}: ${self.price:.2f}"

def __repr__(self):
    return f"Product(name={self.name!r}, price={self.price})"
```

</details>

---

## 📊 Self-Assessment Checklist

| Concept | ✅ Got it | 🔄 Need review | ❓ Confused |
|---------|-----------|---------------|------------|
| Class vs object (blueprint vs instance) | | | |
| `__init__` — when it's called and what it does | | | |
| `self` — why it's explicit and what it represents | | | |
| Instance variables — unique per object | | | |
| Class variables — shared across all instances | | | |
| Shadowing trap — `self.class_var = x` behavior | | | |
| Mutable class variable danger | | | |
| Instance methods — `self` parameter | | | |
| `@classmethod` — `cls`, factory methods | | | |
| `@staticmethod` — no self/cls, utility | | | |
| When to use each method type | | | |
| `__str__` vs `__repr__` | | | |
| `@property` getter/setter | | | |
| Four OOP pillars — definition + example | | | |
| `__dict__` — what it shows | | | |
| Private convention (`_` and `__`) | | | |

**Score:**
- 16/16 ✅ — Ready for Day 6 (Inheritance, `super()`, MRO, abstract classes)
- 11–15 ✅ — Review shadowing and method types — they're core to Django
- < 11 ✅ — Re-do Guided Exercises 1 & 2; run experiments in Section E live

---

*Day 5 Exercises Complete — Day 6: OOP Advanced — Inheritance, `super()`, MRO, Abstract Classes, Dataclasses*
