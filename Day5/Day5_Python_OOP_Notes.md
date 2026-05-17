# 🐍 DAY 5 — Python OOP: Object-Oriented Programming 

---

## 📌 Table of Contents

1. [Why OOP? The Big Picture](#why-oop)
2. [Classes, Objects & Methods](#classes-objects)
3. [The Four Pillars — Overview](#four-pillars)
4. [Inheritance — Types, MRO, super()](#inheritance)
5. [Polymorphism — Duck Typing & Overriding](#polymorphism)
6. [Encapsulation — Python Style](#encapsulation)
7. [Abstraction — ABCs & Interfaces](#abstraction)
8. [Class vs Instance Variables](#class-vs-instance)
9. [Dunder / Magic Methods](#dunder-methods)
10. [Properties — @property & Setters](#properties)
11. [Class Methods & Static Methods](#class-static-methods)
12. [Real-World OOP Architecture Patterns](#patterns)
13. [Hands-On Exercises](#exercises)
14. [Mini Project — Bank Management System](#mini-project)

---

## 🗺️ 1. Why OOP? The Big Picture {#why-oop}

Before writing a single class, understand what problem OOP actually solves.

```
PROCEDURAL APPROACH                  OOP APPROACH
─────────────────────────────────    ──────────────────────────────────────
Functions + global data              Data + behaviour bundled in objects
Hard to scale past ~500 lines        Scales to millions of lines (Django, etc.)
Hard to model real-world domains     Maps naturally: User, Order, Payment
Change breaks unrelated code         Change is localised inside a class
Hard to test in isolation            Each class testable independently
```

### Where Python OOP Is Used in Industry

```
┌───────────────────────────────────────────────────────────────┐
│                  Python OOP in the Wild                       │
│                                                               │
│  REST APIs         → Django Models, DRF Serializers           │
│  ML Pipelines      → sklearn Estimators, PyTorch Modules      │
│  Finance/Banking   → Account, Transaction, Portfolio classes  │
│  Automation/DevOps → Fabric tasks, Ansible modules            │
│  Game Engines      → Sprite, Scene, Player classes            │
│  ORMs              → SQLAlchemy Model, Django ORM             │
│  GUI Apps          → tkinter Widget, PyQt QWidget             │
└───────────────────────────────────────────────────────────────┘
```

---

## 🟦 2. Classes, Objects & Methods {#classes-objects}

### What is a Class?

A class is a **blueprint** — it defines what data (attributes) an object will hold and what actions (methods) it can perform. No memory is allocated until you create an object from it.

```python
class Car:
    wheels = 4              # class attribute — shared by ALL Cars

    def __init__(self, brand, price):
        self.brand = price  # instance attribute — unique to THIS car
        self.price = price

    def start(self):
        print(f"{self.brand} engine started 🚗")

    def __str__(self):
        return f"Car({self.brand}, ₹{self.price:,})"
```

### What is an Object?

An object is a **runtime instance** of a class. Creating one allocates memory and calls `__init__`:

```python
bmw   = Car("BMW", 5_000_000)
honda = Car("Honda", 1_200_000)

bmw.start()         # BMW engine started 🚗
print(bmw)          # Car(BMW, ₹50,00,000)

# Every object has its own __dict__
print(bmw.__dict__)   # {'brand': 'BMW', 'price': 5000000}
print(Car.__dict__)   # contains wheels, __init__, start, __str__ ...
```

### Python Internals — How Objects Are Stored

```
             Class: Car
            ┌───────────────────────┐
            │ wheels = 4            │  ← shared by all instances
            │ __init__ = <function> │
            │ start   = <function>  │
            └──────────┬────────────┘
                       │  (each object points back to its class)
          ┌────────────┴──────────────────┐
          ▼                               ▼
  Object: bmw                    Object: honda
  ┌─────────────────┐             ┌─────────────────┐
  │ brand = "BMW"   │             │ brand = "Honda" │
  │ price = 5000000 │             │ price = 1200000 │
  └─────────────────┘             └─────────────────┘
```

> **Key insight:** When you access `bmw.wheels`, Python first checks `bmw.__dict__` (not found), then checks `Car.__dict__` (found: 4). This attribute lookup chain is how Python works.

### Constructor Flexibility

Python has one `__init__`, but you can mimic multiple constructors using default arguments, `*args`/`**kwargs`, or `@classmethod` factory methods:

```python
class Employee:
    def __init__(self, name, dept="General", salary=0):
        self.name   = name
        self.dept   = dept
        self.salary = salary

    @classmethod
    def from_dict(cls, data: dict):
        """Create an Employee from a dictionary (e.g., API response)."""
        return cls(data["name"], data.get("dept", "General"), data.get("salary", 0))

    @classmethod
    def from_csv_row(cls, row: str):
        """Create an Employee from a CSV line."""
        name, dept, salary = row.strip().split(",")
        return cls(name, dept, float(salary))

# Usage
emp1 = Employee("Ravi", "Engineering", 85000)
emp2 = Employee.from_dict({"name": "Priya", "dept": "HR", "salary": 72000})
emp3 = Employee.from_csv_row("Kiran,Finance,91000")
```

### Real-Time Class Examples

```python
# API Entity — most common use in backends
class User:
    def __init__(self, user_id, name, email, role="user"):
        self.user_id = user_id
        self.name    = name
        self.email   = email
        self.role    = role
        self.active  = True

    def to_dict(self):
        """Serialize to JSON-safe dict (for API responses)."""
        return {
            "id":     self.user_id,
            "name":   self.name,
            "email":  self.email,
            "role":   self.role,
            "active": self.active,
        }

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name!r})"
```

---

## 🏛️ 3. The Four Pillars — Overview {#four-pillars}

```
┌──────────────────────────────────────────────────────────────────┐
│                   THE FOUR PILLARS OF OOP                        │
│                                                                  │
│  1. ENCAPSULATION   — Bundle data + methods; control access      │
│     "What data does this object own, and who can touch it?"      │
│                                                                  │
│  2. INHERITANCE     — Reuse and extend existing classes          │
│     "This class IS-A more specific version of that class."       │
│                                                                  │
│  3. POLYMORPHISM    — Same interface, different behaviour        │
│     "Call the same method on different objects; each responds    │
│      appropriately."                                             │
│                                                                  │
│  4. ABSTRACTION     — Hide complexity; expose only essentials    │
│     "I know what it does. I don't need to know how."             │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🟩 4. Inheritance {#inheritance}

Inheritance lets a child class **reuse** everything from a parent class and **extend or override** what it needs. This eliminates duplication and models natural hierarchies.

### Basic Single Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"


class Dog(Animal):
    def speak(self):             # override parent method
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"


dog = Dog("Bruno")
cat = Cat("Whiskers")

print(dog.speak())    # Woof!
print(cat.name)       # Whiskers  — inherited from Animal
print(dog)            # Dog(name='Bruno')  — inherited __str__
```

### The Four Types of Inheritance in Python

**1. Single Inheritance** — one parent, one child

```python
class Vehicle:
    pass

class Car(Vehicle):
    pass
```

**2. Multilevel Inheritance** — grandparent → parent → child

```python
class Vehicle:
    def fuel_type(self):
        return "Unknown"

class Car(Vehicle):
    def fuel_type(self):
        return "Petrol"

class ElectricCar(Car):
    def fuel_type(self):
        return "Electric"

tesla = ElectricCar()
print(tesla.fuel_type())    # Electric
```

**3. Multiple Inheritance** — child inherits from two or more parents

```python
class Flyable:
    def fly(self):
        return "Flying..."

class Swimmable:
    def swim(self):
        return "Swimming..."

class Duck(Flyable, Swimmable):
    pass

d = Duck()
d.fly()     # Flying...
d.swim()    # Swimming...
```

**4. Hierarchical Inheritance** — one parent, multiple children

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        import math
        return math.pi * self.r ** 2

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h
```

### `super()` — Calling the Parent

`super()` gives you a proxy to the parent class. Essential when overriding methods but still needing the parent's logic:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age  = age

class Employee(Person):
    def __init__(self, name, age, company, salary):
        super().__init__(name, age)     # call Person.__init__
        self.company = company
        self.salary  = salary

class Manager(Employee):
    def __init__(self, name, age, company, salary, team_size):
        super().__init__(name, age, company, salary)  # call Employee.__init__
        self.team_size = team_size

mgr = Manager("Anil", 35, "TechCorp", 150000, 8)
print(mgr.name, mgr.salary, mgr.team_size)
```

### Method Resolution Order (MRO)

With multiple inheritance, Python uses **C3 linearization** to decide which class's method runs when the same method exists in multiple parents.

```python
class A:
    def hello(self): return "A"

class B(A):
    def hello(self): return "B"

class C(A):
    def hello(self): return "C"

class D(B, C):
    pass

print(D().hello())     # "B"  — follows MRO
print(D.mro())
# [D, B, C, A, object]
```

```
MRO for D:   D → B → C → A → object
             (left-to-right, depth-first, no repetition)
```

> **Rule of thumb:** Python reads the MRO list left to right and picks the first class that defines the method. Always check `.mro()` when debugging unexpected method calls in multiple inheritance.

### Real-World Inheritance Examples

```python
# Django-style ORM model
class BaseModel:
    def save(self):    print("Saving to DB...")
    def delete(self):  print("Deleting from DB...")
    def __repr__(self): return f"<{self.__class__.__name__}>"

class UserModel(BaseModel):
    def __init__(self, username, email):
        self.username = username
        self.email    = email

class PostModel(BaseModel):
    def __init__(self, title, content, author):
        self.title   = title
        self.content = content
        self.author  = author   # UserModel instance

# sklearn-style ML model hierarchy
class BaseEstimator:
    def fit(self, X, y):   raise NotImplementedError
    def predict(self, X):  raise NotImplementedError
    def score(self, X, y): ...

class LinearRegression(BaseEstimator):
    def fit(self, X, y):
        # actual training logic
        return self
    def predict(self, X):
        # return predictions
        return []
```

---

## 🟥 5. Polymorphism {#polymorphism}

Polymorphism means "many forms" — the same operation behaves differently depending on the object it's applied to.

### Method Overriding

```python
class Notification:
    def send(self, message):
        raise NotImplementedError("Subclasses must implement send()")

class EmailNotification(Notification):
    def send(self, message):
        print(f"📧 Email: {message}")

class SMSNotification(Notification):
    def send(self, message):
        print(f"📱 SMS: {message}")

class PushNotification(Notification):
    def send(self, message):
        print(f"🔔 Push: {message}")

# Polymorphic usage — caller doesn't care about the concrete type
def notify_user(notifier: Notification, msg: str):
    notifier.send(msg)

channels = [EmailNotification(), SMSNotification(), PushNotification()]
for channel in channels:
    notify_user(channel, "Your order has been shipped!")
```

### Duck Typing — Python's Preferred Polymorphism

In Python, you don't need a shared parent class. If an object has the right method, it works:

```python
class PDFExporter:
    def export(self, data):
        print(f"Exporting {len(data)} records to PDF...")

class CSVExporter:
    def export(self, data):
        print(f"Exporting {len(data)} records to CSV...")

class JSONExporter:
    def export(self, data):
        print(f"Exporting {len(data)} records to JSON...")

# None of these share a parent — duck typing in action
def run_export(exporter, data):
    exporter.export(data)     # just needs an .export() method

records = [1, 2, 3, 4, 5]
for exporter in [PDFExporter(), CSVExporter(), JSONExporter()]:
    run_export(exporter, records)
```

> **Observation:** Duck typing is why Python doesn't need Java-style `interface` declarations. It's more flexible — but also means you need good tests to catch type errors that a compiler would catch in statically-typed languages.

### Operator Overloading (a form of polymorphism)

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)       # Vector(4, 6)
print(v1 * 3)        # Vector(3, 6)
print(v1 == v2)      # False
```

---

## 🟪 6. Encapsulation {#encapsulation}

Encapsulation bundles data and the methods that operate on it into a single unit, and controls access to that data. Python uses naming conventions rather than strict access modifiers.

### Access Levels

| Convention | Example | Meaning |
|------------|---------|---------|
| `name` | `self.balance` | Public — anyone can access |
| `_name` | `self._cache` | Protected — "internal use, be careful" |
| `__name` | `self.__password` | Private — name-mangled by Python |

### Name Mangling in Detail

```python
class Account:
    def __init__(self, owner, balance):
        self.owner    = owner        # public
        self._log     = []           # protected — internal use
        self.__balance = balance     # private — name mangled

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
        self._log.append(f"Deposited ₹{amount}")

    def get_balance(self):
        return self.__balance        # controlled read access


acc = Account("Priya", 10000)
acc.deposit(5000)

print(acc.owner)           # "Priya"         — works fine
print(acc._log)            # works (protected, not enforced)
# print(acc.__balance)     # AttributeError!
print(acc._Account__balance)  # 15000  — mangled name, still accessible if needed
```

> **Python Philosophy:** Python trusts developers. There's no hard enforcement — `__name` discourages accidental access, not deliberate access. The convention communicates intent to the reader.

### Why Encapsulation Matters

```
Without encapsulation:               With encapsulation:
────────────────────────────────     ──────────────────────────────────────
acc.balance = -99999  # valid 😱     acc.deposit(-99)  → ValueError raised
No validation on writes              Invariants enforced in methods
Scattered business logic             Logic lives with the data
Refactoring breaks callers           Internal storage can change freely
```

---

## 🟨 7. Abstraction {#abstraction}

Abstraction means hiding the *how* and exposing only the *what*. You interact with a `PaymentGateway.pay()` without knowing whether it talks to Razorpay, Stripe, or UPI underneath.

### Abstract Base Classes (ABC)

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    """Abstract interface for all payment gateways."""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process a payment. Returns True on success."""
        ...

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Issue a refund. Returns True on success."""
        ...

    def receipt(self, amount):
        """Non-abstract — shared implementation."""
        print(f"Receipt: ₹{amount} processed via {self.__class__.__name__}")


# Concrete implementations
class RazorpayGateway(PaymentGateway):
    def pay(self, amount):
        print(f"Processing ₹{amount} via Razorpay API...")
        return True

    def refund(self, txn_id):
        print(f"Refunding {txn_id} via Razorpay...")
        return True


class StripeGateway(PaymentGateway):
    def pay(self, amount):
        print(f"Charging ${amount} via Stripe API...")
        return True

    def refund(self, txn_id):
        print(f"Refunding {txn_id} via Stripe...")
        return True


# PaymentGateway()  → TypeError: Can't instantiate abstract class
gateway = RazorpayGateway()
gateway.pay(1500)
gateway.receipt(1500)
```

### ABC for ML Pipelines (Real Pattern)

```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def fit(self, X, y):
        ...

    @abstractmethod
    def predict(self, X):
        ...

    def fit_predict(self, X, y):
        """Template method — uses abstract methods."""
        self.fit(X, y)
        return self.predict(X)


class MyLinearModel(BaseModel):
    def fit(self, X, y):
        self.coeffs = [0.5, 1.2]   # simplified
        return self

    def predict(self, X):
        return [sum(x * c for x, c in zip(row, self.coeffs)) for row in X]
```

### Abstract Properties

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @property
    @abstractmethod
    def area(self) -> float:
        ...

    @property
    @abstractmethod
    def perimeter(self) -> float:
        ...

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        import math
        return math.pi * self.radius ** 2

    @property
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius

c = Circle(5)
print(f"Area: {c.area:.2f}")         # Area: 78.54
print(f"Perimeter: {c.perimeter:.2f}")  # Perimeter: 31.42
```

---

## 🟧 8. Class Variables vs Instance Variables {#class-vs-instance}

### The Core Distinction

```python
class Employee:
    company     = "TechCorp"     # class variable — ALL employees share this
    _headcount  = 0              # class variable — tracks total employees

    def __init__(self, name, salary):
        self.name   = name       # instance variable — unique to each employee
        self.salary = salary
        Employee._headcount += 1

    @classmethod
    def get_headcount(cls):
        return cls._headcount

    def __del__(self):
        Employee._headcount -= 1


emp1 = Employee("Ravi",  85000)
emp2 = Employee("Priya", 92000)
print(Employee.get_headcount())    # 2
print(emp1.company)                # "TechCorp"  — reads class variable
```

### The Danger — Accidental Shadowing

```python
emp1.company = "StartupXYZ"   # creates an INSTANCE variable, shadows class variable
print(emp1.company)            # "StartupXYZ"  — reads instance variable
print(emp2.company)            # "TechCorp"    — still reads class variable
print(Employee.company)        # "TechCorp"    — class variable unchanged
```

> **Observation:** Assigning to `instance.class_var` creates a new instance variable that shadows the class variable for that object only. The class variable itself is untouched. This is a frequent source of confusion.

### When to Use Which

| Class Variable | Instance Variable |
|----------------|-------------------|
| Bank-wide interest rate | Account balance |
| App-wide config | Per-user preferences |
| Object counter | Object's name/ID |
| Default tax rate | Order total |
| Shared connection pool | Per-request session |

---

## 🔮 9. Dunder / Magic Methods {#dunder-methods}

Dunder methods let your objects participate naturally in Python's built-in operations — `print()`, `len()`, `+`, `==`, `in`, `for`, `with`, and more.

### Object Lifecycle

```python
class Resource:
    def __new__(cls, *args, **kwargs):
        """Called BEFORE __init__ — controls object creation."""
        print(f"Creating {cls.__name__} instance...")
        instance = super().__new__(cls)
        return instance

    def __init__(self, name):
        self.name = name
        print(f"Initialising {self.name}")

    def __del__(self):
        """Called when object is garbage collected."""
        print(f"Destroying {self.name}")
```

### String Representation

```python
class Product:
    def __init__(self, name, price, stock):
        self.name  = name
        self.price = price
        self.stock = stock

    def __str__(self):
        """User-friendly — for print() and str()"""
        return f"{self.name} — ₹{self.price:,} ({self.stock} in stock)"

    def __repr__(self):
        """Developer-friendly — for debugging, logs, repr()"""
        return f"Product(name={self.name!r}, price={self.price}, stock={self.stock})"

p = Product("Laptop", 65000, 12)
print(p)        # Laptop — ₹65,000 (12 in stock)
print(repr(p))  # Product(name='Laptop', price=65000, stock=12)
```

> **Rule:** Always implement `__repr__`. It's used in debuggers, logs, and the REPL. `__str__` is optional — if absent, Python falls back to `__repr__`.

### Comparison Operators

```python
from functools import total_ordering

@total_ordering     # auto-generates missing comparison methods from __eq__ and __lt__
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa  = gpa

    def __eq__(self, other):
        return self.gpa == other.gpa

    def __lt__(self, other):
        return self.gpa < other.gpa

    def __repr__(self):
        return f"Student({self.name!r}, GPA={self.gpa})"

students = [Student("Ravi", 8.5), Student("Priya", 9.2), Student("Kiran", 7.8)]
print(sorted(students))
# [Student('Kiran', GPA=7.8), Student('Ravi', GPA=8.5), Student('Priya', GPA=9.2)]
```

### Container & Sequence Methods

```python
class Playlist:
    def __init__(self, name):
        self.name   = name
        self._songs = []

    def add(self, song):
        self._songs.append(song)

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index):
        return self._songs[index]

    def __contains__(self, song):
        return song in self._songs

    def __iter__(self):
        return iter(self._songs)

    def __repr__(self):
        return f"Playlist({self.name!r}, {len(self)} songs)"


pl = Playlist("Chill Vibes")
pl.add("Song A")
pl.add("Song B")

print(len(pl))            # 2
print(pl[0])              # "Song A"
print("Song B" in pl)     # True
for song in pl:
    print(song)
```

### Callable Objects — `__call__`

```python
class TaxCalculator:
    def __init__(self, rate):
        self.rate = rate

    def __call__(self, amount):
        return amount * (1 + self.rate / 100)

gst_18 = TaxCalculator(18)
print(gst_18(1000))    # 1180.0  — called like a function!

# Used heavily in ML: model(x) calls model.__call__(x) in PyTorch
```

### Context Manager — `__enter__` / `__exit__`

```python
class DatabaseConnection:
    def __init__(self, dsn):
        self.dsn  = dsn
        self.conn = None

    def __enter__(self):
        print(f"Connecting to {self.dsn}...")
        self.conn = f"<Connection to {self.dsn}>"
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection...")
        self.conn = None
        # return True to suppress exceptions, False (or None) to propagate
        return False

with DatabaseConnection("postgresql://localhost/myapp") as conn:
    print(f"Using {conn}")
# Connecting to postgresql://localhost/myapp...
# Using <Connection to postgresql://localhost/myapp>
# Closing connection...
```

### Complete Dunder Reference

| Method | Triggered by | Use case |
|--------|-------------|----------|
| `__init__` | `MyClass()` | Initialise instance |
| `__new__` | Before `__init__` | Singleton, flyweight patterns |
| `__del__` | Garbage collected | Resource cleanup |
| `__str__` | `print(obj)`, `str(obj)` | Human-readable display |
| `__repr__` | `repr(obj)`, REPL, logs | Debugging representation |
| `__len__` | `len(obj)` | Custom container size |
| `__getitem__` | `obj[key]` | Index/key access |
| `__setitem__` | `obj[key] = val` | Index/key assignment |
| `__contains__` | `x in obj` | Membership test |
| `__iter__` | `for x in obj` | Make iterable |
| `__next__` | `next(obj)` | Iterator protocol |
| `__eq__` | `==` | Equality check |
| `__lt__` | `<` | Less-than comparison |
| `__add__` | `+` | Addition operator |
| `__call__` | `obj()` | Callable object |
| `__enter__` | `with obj:` | Context manager entry |
| `__exit__` | End of `with` block | Context manager exit |

---

## 🏠 10. Properties — @property & Setters {#properties}

Properties give you **getter/setter behaviour** with attribute-style access. No more `get_balance()` / `set_balance()` — just `account.balance`.

```python
class BankAccount:
    def __init__(self, owner, initial_balance=0):
        self.owner    = owner
        self._balance = initial_balance   # _protected convention

    @property
    def balance(self):
        """Read-only access to balance."""
        return self._balance

    @balance.setter
    def balance(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Balance must be numeric")
        if amount < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = amount

    @balance.deleter
    def balance(self):
        raise AttributeError("Cannot delete balance")

    @property
    def balance_str(self):
        """Computed property — no setter needed."""
        return f"₹{self._balance:,.2f}"


acc = BankAccount("Priya", 10000)
print(acc.balance)         # 10000    — calls getter
acc.balance = 15000        # calls setter
# acc.balance = -500       # ValueError
print(acc.balance_str)     # ₹15,000.00
```

> **Why properties?** The `balance` attribute *looks* like a plain attribute to callers (`acc.balance = 5000`), but behind the scenes, validation runs. You can refactor internal storage later without breaking any calling code.

---

## 📌 11. Class Methods & Static Methods {#class-static-methods}

Python has three kinds of methods inside a class:

```
┌────────────────┬──────────────────┬───────────────────────────────────┐
│ Method Type    │ First Parameter  │ When to Use                       │
├────────────────┼──────────────────┼───────────────────────────────────┤
│ Instance method│ self             │ Needs access to instance data     │
│ @classmethod   │ cls              │ Needs class (factory methods)     │
│ @staticmethod  │ (none)           │ Utility — no instance/class needed│
└────────────────┴──────────────────┴───────────────────────────────────┘
```

```python
class DateParser:
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, year, month, day):
        self.year  = year
        self.month = month
        self.day   = day

    # Instance method — needs self
    def to_string(self):
        return f"{self.year:04d}-{self.month:02d}-{self.day:02d}"

    # Class method — alternative constructor
    @classmethod
    def from_string(cls, date_str):
        """Factory: DateParser.from_string('2025-08-15')"""
        from datetime import datetime
        dt = datetime.strptime(date_str, cls.DATE_FORMAT)
        return cls(dt.year, dt.month, dt.day)

    # Static method — utility, no instance/class context needed
    @staticmethod
    def is_valid(date_str):
        """Validate format without creating an object."""
        from datetime import datetime
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False


d1 = DateParser(2025, 8, 15)
d2 = DateParser.from_string("2025-12-01")

print(d1.to_string())               # 2025-08-15
print(DateParser.is_valid("2025-13-01"))  # False  — invalid month
```

---

## 🏗️ 12. Real-World OOP Architecture Patterns {#patterns}

### Repository Pattern

Abstracts data access behind a clean interface. Business logic never touches raw SQL or file paths.

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int): ...

    @abstractmethod
    def save(self, user): ...

    @abstractmethod
    def delete(self, user_id: int): ...


class InMemoryUserRepository(UserRepository):
    """For testing — no real DB needed."""
    def __init__(self):
        self._store = {}

    def get_by_id(self, user_id):
        return self._store.get(user_id)

    def save(self, user):
        self._store[user.user_id] = user

    def delete(self, user_id):
        self._store.pop(user_id, None)


class PostgresUserRepository(UserRepository):
    """Production — talks to real DB."""
    def get_by_id(self, user_id):
        # cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        pass

    def save(self, user):
        # cursor.execute("INSERT INTO users ...")
        pass

    def delete(self, user_id):
        # cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        pass
```

### Service Layer Pattern

Contains business logic, sits between the API layer and the repository layer:

```python
class OrderService:
    def __init__(self, order_repo, product_repo, payment_gateway):
        self.orders   = order_repo
        self.products = product_repo
        self.payments = payment_gateway

    def place_order(self, user_id, items):
        # 1. Validate items and stock
        for item in items:
            product = self.products.get_by_id(item["product_id"])
            if product.stock < item["quantity"]:
                raise ValueError(f"Insufficient stock for {product.name}")

        # 2. Calculate total
        total = sum(
            self.products.get_by_id(i["product_id"]).price * i["quantity"]
            for i in items
        )

        # 3. Process payment
        if not self.payments.pay(total):
            raise RuntimeError("Payment failed")

        # 4. Save order
        order = Order(user_id, items, total)
        self.orders.save(order)
        return order
```

### Strategy Pattern

Define a family of algorithms, encapsulate each one, make them interchangeable:

```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...

class BubbleSort(SortStrategy):
    def sort(self, data):
        data = data.copy()
        for i in range(len(data)):
            for j in range(len(data) - 1 - i):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

class QuickSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1: return data
        pivot = data[len(data) // 2]
        return (self.sort([x for x in data if x < pivot])
                + [x for x in data if x == pivot]
                + self.sort([x for x in data if x > pivot]))

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def sort(self, data):
        return self.strategy.sort(data)

data = [5, 3, 8, 1, 2]
print(Sorter(QuickSort()).sort(data))    # [1,2,3,5,8]
print(Sorter(BubbleSort()).sort(data))   # [1,2,3,5,8]
```

### Factory Pattern

Decide *which* object to create at runtime based on input:

```python
class NotificationFactory:
    _registry = {}

    @classmethod
    def register(cls, channel, klass):
        cls._registry[channel] = klass

    @classmethod
    def create(cls, channel, **kwargs):
        if channel not in cls._registry:
            raise ValueError(f"Unknown channel: {channel}")
        return cls._registry[channel](**kwargs)

NotificationFactory.register("email", EmailNotification)
NotificationFactory.register("sms",   SMSNotification)
NotificationFactory.register("push",  PushNotification)

notifier = NotificationFactory.create("email")
notifier.send("Welcome!")
```

---

## 🧪 13. Hands-On Exercises {#exercises}

### Exercise 1: Payment Processing System

```python
from abc import ABC, abstractmethod

class PaymentFailedError(Exception):
    def __init__(self, method, reason):
        super().__init__(f"{method} payment failed: {reason}")

class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool: ...

    def __str__(self):
        return self.__class__.__name__

class UPI(Payment):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def pay(self, amount):
        if amount > 100000:
            raise PaymentFailedError("UPI", "Limit exceeded ₹1,00,000")
        print(f"✅ ₹{amount} paid via UPI ({self.upi_id})")
        return True

class Card(Payment):
    def __init__(self, last4):
        self.last4 = last4

    def pay(self, amount):
        print(f"✅ ₹{amount} charged to card ending {self.last4}")
        return True

class NetBanking(Payment):
    def __init__(self, bank):
        self.bank = bank

    def pay(self, amount):
        print(f"✅ ₹{amount} transferred via {self.bank} NetBanking")
        return True

# Polymorphic checkout
def checkout(payment: Payment, amount: float):
    try:
        return payment.pay(amount)
    except PaymentFailedError as e:
        print(f"❌ {e}")
        return False

checkout(UPI("ravi@upi"), 5000)
checkout(Card("4242"), 15000)
checkout(UPI("ravi@upi"), 200000)   # will fail — limit exceeded
```

### Exercise 2: University System

```python
class Person:
    def __init__(self, name, age, email):
        self.name  = name
        self.age   = age
        self.email = email

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} (age {self.age})"

class Student(Person):
    def __init__(self, name, age, email, student_id, marks=None):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.marks      = marks or {}

    def add_mark(self, subject, score):
        self.marks[subject] = score

    @property
    def gpa(self):
        if not self.marks:
            return 0.0
        return sum(self.marks.values()) / len(self.marks) / 10

    def __str__(self):
        return f"Student: {self.name} | GPA: {self.gpa:.1f} | ID: {self.student_id}"

class Teacher(Person):
    def __init__(self, name, age, email, employee_id, subjects=None):
        super().__init__(name, age, email)
        self.employee_id = employee_id
        self.subjects    = subjects or []

    def assign_subject(self, subject):
        self.subjects.append(subject)

    def __str__(self):
        return f"Teacher: {self.name} | Subjects: {', '.join(self.subjects)}"

t = Teacher("Dr. Sharma", 45, "sharma@uni.edu", "T001")
t.assign_subject("Algorithms")
t.assign_subject("Data Structures")

s = Student("Priya", 20, "priya@uni.edu", "S2025001")
s.add_mark("Maths", 92)
s.add_mark("CS", 88)

print(t)   # Teacher: Dr. Sharma | Subjects: Algorithms, Data Structures
print(s)   # Student: Priya | GPA: 9.0 | ID: S2025001
```

### Exercise 3: ATM Simulation

```python
from datetime import datetime

class InsufficientFundsError(Exception):
    def __init__(self, requested, available):
        super().__init__(
            f"Cannot withdraw ₹{requested:,}. Available balance: ₹{available:,}"
        )

class Transaction:
    def __init__(self, txn_type, amount):
        self.txn_type  = txn_type
        self.amount    = amount
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"[{self.timestamp}] {self.txn_type:<10} ₹{self.amount:>10,.2f}"

class ATM:
    DAILY_LIMIT = 50000

    def __init__(self, account_holder, initial_balance):
        self.account_holder  = account_holder
        self.__balance       = initial_balance
        self.__transactions  = []
        self.__daily_withdrawn = 0

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
        self.__transactions.append(Transaction("DEPOSIT", amount))
        print(f"✅ Deposited ₹{amount:,}. New balance: ₹{self.__balance:,}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise InsufficientFundsError(amount, self.__balance)
        if self.__daily_withdrawn + amount > self.DAILY_LIMIT:
            raise ValueError(f"Daily ATM limit of ₹{self.DAILY_LIMIT:,} exceeded")
        self.__balance       -= amount
        self.__daily_withdrawn += amount
        self.__transactions.append(Transaction("WITHDRAWAL", amount))
        print(f"✅ Withdrew ₹{amount:,}. Remaining balance: ₹{self.__balance:,}")

    def print_statement(self):
        print(f"\n{'─'*45}")
        print(f"  Account: {self.account_holder}")
        print(f"{'─'*45}")
        for txn in self.__transactions:
            print(f"  {txn}")
        print(f"{'─'*45}")
        print(f"  Current Balance: ₹{self.__balance:,.2f}")
        print(f"{'─'*45}\n")

atm = ATM("Priya Sharma", 20000)
atm.deposit(5000)
atm.withdraw(3000)
atm.print_statement()
```

---

## 🏦 14. Mini Project — Bank Management System {#mini-project}

### Project Structure

```
bank_system/
├── exceptions.py     ← Custom exception hierarchy
├── models.py         ← Transaction, Account classes
├── bank.py           ← Bank class (manages accounts)
└── main.py           ← CLI interface
```

### Exceptions

```python
# exceptions.py

class BankError(Exception):
    """Base exception for all bank errors."""
    pass

class InsufficientBalanceError(BankError):
    def __init__(self, requested, available):
        super().__init__(
            f"Insufficient balance. Requested: ₹{requested:,}, Available: ₹{available:,}"
        )

class InvalidAmountError(BankError):
    def __init__(self, amount):
        super().__init__(f"Invalid amount: ₹{amount}. Must be a positive number.")

class AccountNotFoundError(BankError):
    def __init__(self, account_id):
        super().__init__(f"Account '{account_id}' not found.")

class DuplicateAccountError(BankError):
    def __init__(self, account_id):
        super().__init__(f"Account '{account_id}' already exists.")
```

### Models

```python
# models.py
from datetime import datetime
from exceptions import (InsufficientBalanceError, InvalidAmountError)

class Transaction:
    def __init__(self, txn_type: str, amount: float, balance_after: float):
        self.txn_type      = txn_type
        self.amount        = amount
        self.balance_after = balance_after
        self.timestamp     = datetime.now()

    def __str__(self):
        ts = self.timestamp.strftime("%d-%b-%Y %H:%M")
        return (f"[{ts}] {self.txn_type:<12} "
                f"₹{self.amount:>10,.2f}   "
                f"Balance: ₹{self.balance_after:>12,.2f}")


class Account:
    interest_rate = 3.5    # class variable — bank-wide rate

    def __init__(self, account_id: str, holder_name: str,
                 account_type: str = "savings", initial_deposit: float = 0):
        self.account_id   = account_id
        self.holder_name  = holder_name
        self.account_type = account_type
        self.__balance    = 0.0
        self.__history    = []

        if initial_deposit > 0:
            self.deposit(initial_deposit)

    @property
    def balance(self):
        return self.__balance

    def _validate_amount(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise InvalidAmountError(amount)

    def deposit(self, amount: float):
        self._validate_amount(amount)
        self.__balance += amount
        self.__history.append(Transaction("CREDIT", amount, self.__balance))
        return self.__balance

    def withdraw(self, amount: float):
        self._validate_amount(amount)
        if amount > self.__balance:
            raise InsufficientBalanceError(amount, self.__balance)
        self.__balance -= amount
        self.__history.append(Transaction("DEBIT", amount, self.__balance))
        return self.__balance

    def apply_interest(self):
        interest = self.__balance * (Account.interest_rate / 100)
        self.__balance += interest
        self.__history.append(Transaction("INTEREST", interest, self.__balance))
        return interest

    def get_statement(self) -> list:
        return list(self.__history)

    def __str__(self):
        return (f"Account[{self.account_id}] "
                f"{self.holder_name} ({self.account_type}) "
                f"— Balance: ₹{self.__balance:,.2f}")

    def __repr__(self):
        return f"Account(id={self.account_id!r}, holder={self.holder_name!r})"
```

### Bank Class

```python
# bank.py
from models import Account
from exceptions import AccountNotFoundError, DuplicateAccountError

class Bank:
    def __init__(self, name: str):
        self.name      = name
        self.__accounts = {}

    def create_account(self, account_id, holder_name,
                       account_type="savings", initial_deposit=0):
        if account_id in self.__accounts:
            raise DuplicateAccountError(account_id)
        acc = Account(account_id, holder_name, account_type, initial_deposit)
        self.__accounts[account_id] = acc
        print(f"✅ Account created: {acc}")
        return acc

    def get_account(self, account_id) -> Account:
        if account_id not in self.__accounts:
            raise AccountNotFoundError(account_id)
        return self.__accounts[account_id]

    def transfer(self, from_id, to_id, amount):
        sender   = self.get_account(from_id)
        receiver = self.get_account(to_id)
        sender.withdraw(amount)
        receiver.deposit(amount)
        print(f"✅ Transferred ₹{amount:,} from {from_id} to {to_id}")

    def apply_interest_all(self):
        for acc in self.__accounts.values():
            interest = acc.apply_interest()
            print(f"  {acc.holder_name}: +₹{interest:,.2f} interest")

    def print_statement(self, account_id):
        acc = self.get_account(account_id)
        print(f"\n{'═'*60}")
        print(f"  {self.name} — Account Statement")
        print(f"  {acc}")
        print(f"{'─'*60}")
        history = acc.get_statement()
        if not history:
            print("  No transactions yet.")
        for txn in history:
            print(f"  {txn}")
        print(f"{'═'*60}\n")

    def __str__(self):
        return f"{self.name} ({len(self.__accounts)} accounts)"
```

### CLI / Main

```python
# main.py
from bank import Bank
from exceptions import BankError

def main():
    bank = Bank("Hyderabad National Bank")
    print(f"Welcome to {bank.name}\n")

    while True:
        print("1. Create Account  2. Deposit  3. Withdraw")
        print("4. Transfer        5. Statement 6. Interest  0. Exit")
        choice = input("Choice: ").strip()

        try:
            if choice == "1":
                aid   = input("Account ID: ")
                name  = input("Holder Name: ")
                atype = input("Type (savings/current) [savings]: ") or "savings"
                dep   = float(input("Initial Deposit [0]: ") or 0)
                bank.create_account(aid, name, atype, dep)

            elif choice == "2":
                aid = input("Account ID: ")
                amt = float(input("Amount: "))
                bal = bank.get_account(aid).deposit(amt)
                print(f"New balance: ₹{bal:,}")

            elif choice == "3":
                aid = input("Account ID: ")
                amt = float(input("Amount: "))
                bal = bank.get_account(aid).withdraw(amt)
                print(f"Remaining: ₹{bal:,}")

            elif choice == "4":
                src = input("From Account: ")
                dst = input("To Account: ")
                amt = float(input("Amount: "))
                bank.transfer(src, dst, amt)

            elif choice == "5":
                bank.print_statement(input("Account ID: "))

            elif choice == "6":
                print("Applying interest to all accounts...")
                bank.apply_interest_all()

            elif choice == "0":
                print("Thank you for banking with us. Goodbye!")
                break

        except BankError as e:
            print(f"⚠️  {e}")
        except ValueError as e:
            print(f"⚠️  Invalid input: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
```

### Concepts Used — Breakdown

```
┌─────────────────────────────┬──────────────────────────────────────────────┐
│ OOP Concept                 │ Where Applied                                │
├─────────────────────────────┼──────────────────────────────────────────────┤
│ Classes & Objects           │ Account, Transaction, Bank                   │
│ __init__ & constructors     │ All classes                                  │
│ Instance methods            │ deposit, withdraw, transfer                  │
│ Class variables             │ Account.interest_rate                        │
│ Encapsulation               │ __balance, __history, __accounts (private)   │
│ @property                   │ balance — controlled read access             │
│ Abstraction                 │ Bank hides account storage details           │
│ Inheritance                 │ BankError → Specific error subclasses        │
│ Polymorphism                │ All exceptions handled via BankError         │
│ __str__ / __repr__          │ Account, Transaction                         │
│ @classmethod pattern        │ account_type factory approach                │
│ Custom exceptions           │ Full hierarchy in exceptions.py              │
│ Error handling              │ CLI loop with try/except/BankError           │
└─────────────────────────────┴──────────────────────────────────────────────┘
```

---

## 📝 Quick Recap Cheatsheet

```
CLASS ANATOMY
  class Name(Parent):
      class_var = value          ← shared by all instances
      def __init__(self, ...):   ← constructor
          self.inst_var = val    ← unique per instance
      def method(self): ...      ← instance method
      @classmethod
      def factory(cls): ...      ← alternative constructor
      @staticmethod
      def utility(): ...         ← no self/cls needed
      @property
      def computed(self): ...    ← getter

FOUR PILLARS
  Encapsulation  → __private, _protected, @property
  Inheritance    → class Child(Parent): + super().__init__()
  Polymorphism   → method overriding + duck typing
  Abstraction    → ABC + @abstractmethod

MRO (multiple inheritance)
  ClassName.mro()  →  [Child, Parent1, Parent2, ..., object]
  Python uses C3 linearization — left to right, no repeat

KEY DUNDER METHODS
  __str__      → print(obj)        — user-friendly string
  __repr__     → repr(obj), REPL   — developer string (always implement this)
  __len__      → len(obj)
  __eq__       → obj1 == obj2
  __add__      → obj1 + obj2
  __call__     → obj()             — callable object
  __enter__    → with obj:         — context manager
  __iter__     → for x in obj:

GOLDEN RULES
  ✔ Favour composition over deep inheritance hierarchies
  ✔ Always implement __repr__ for debuggability
  ✔ Use @property instead of get_x() / set_x() methods
  ✔ Keep classes focused — Single Responsibility Principle
  ✔ Use ABCs to enforce contracts across a class family
  ✔ Prefix private with __ only when sub-classing is a real concern
  ✔ @classmethod for alternative constructors (from_dict, from_csv)
  ✔ @staticmethod for utility functions that logically belong to a class
```

---
