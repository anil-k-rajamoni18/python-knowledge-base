
# 🧠 DAY 5 — Python OOP 

**Object-Oriented Programming (OOP)** enables building modular, scalable, and maintainable systems. Python uses a flexible OOP model that supports:

  * **Class-based OOP**
  * **Multiple inheritance**
  * **Duck typing**
  * **Dynamic attributes**
  * **Metaprogramming**

This is why OOP in Python is widely used for:

  * **Enterprise software**
  * **REST APIs**
  * **Microservices**
  * **Finance/banking software**
  * **Machine learning pipelines**
  * **Automation frameworks**

-----

## 🟦 1. Classes, Objects & Methods — Deep Dive

### ✔ What is a Class?

A class is a **blueprint** that defines the structure and behavior of objects.

> Internally, Python classes are implemented using dictionaries storing attributes and methods.

```python
class Car:
    wheels = 4  # class attribute
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price
```

**💡 Python Internals**

  * Every class has a `__dict__` attribute storing methods/variables.
  * Every object also has its own `__dict__`, separate from the class.

<!-- end list -->

```python
c = Car("BMW", 50000)
print(c.__dict__)      # {'brand':'BMW', 'price':50000}
print(Car.__dict__)    # contains wheels, __init__, methods, metadata
```

### ✔ What is an Object?

An object is a **runtime instance** created from a class. Objects store state, and methods describe behavior.

### ✔ Instance Methods

Defined with `self`, representing the specific object the method is operating on.

```python
def start(self):
    print(f"{self.brand} engine started")
```

### ✔ Constructor (`__init__`)

Python doesn't have overloaded constructors—but you can achieve constructor flexibility using **default parameters**, `*args`, or `**kwargs`.

```python
def __init__(self, name="Guest", age=None):
    self.name = name
    self.age = age
```

### Real-Time Use Cases

| Use Case | Example Class | Purpose |
| :--- | :--- | :--- |
| **API Entities** | `User(id, name, role)` | Most common in industry for defining data structures returned by APIs. |
| **ML/AI Pipeline** | `Model(train(data), predict(x))` | Abstracting training and inference steps into reusable components. |
| **Financial Systems** | `Transaction(type, amount, timestamp)` | Formalizing data records and business logic. |

-----

## 🟩 2. Inheritance — Types, Internals, Industry Use

**Inheritance** allows a class to reuse another class’s properties and methods.

```python
class Animal:
    def speak(self):
        return "Unknown sound"

class Dog(Animal):
    def speak(self):
        # Overriding the parent method
        return "Bark"
```

### ✔ Python Supports 4 Types of Inheritance

1.  **Single**
2.  **Multiple**
3.  **Multilevel**
4.  **Hierarchical**

### ✔ Method Resolution Order (MRO)

Python follows **C3 linearization** for determining the order in which methods are searched in a class hierarchy, especially with multiple inheritance.

Check MRO via:

```python
print(Dog.mro())
```

### ✔ Real-Time Examples

  * 🚗 **Vehicle Hierarchy:** `Vehicle` $\rightarrow$ `Car` $\rightarrow$ `SportsCar`
  * 🧠 **AI Model Hierarchy:** `BaseModel` $\rightarrow$ `ClassificationModel` $\rightarrow$ `ImageClassificationModel`
  * 🧾 **Invoice & Tax System:** `Invoice` $\rightarrow$ `GSTInvoice` $\rightarrow$ `ExportInvoice`

-----

## 🟥 3. Polymorphism — Static (Duck Typing) vs Dynamic

**Polymorphism** allows different classes to have the same method name with different implementations.

### ✔ Python Polymorphism Works Through:

  * **Method overriding** (redefining a parent's method).
  * **Duck typing** ("if it quacks like a duck...").
  * Interfaces via abstract base classes (see Abstraction).

### ✔ Duck Typing Example

Duck typing is a core Pythonic concept that allows objects to be used interchangeably if they support the necessary method signatures, without requiring a formal shared parent class.

```python
class Dog:
    def speak(self):
        return "Bark"

class Human:
    def speak(self):
        return "Hello"

def make_sound(entity):
    # This function doesn't care about the type, only the 'speak' method
    print(entity.speak())
```

> **Used in:** logging frameworks, ML model `predict()` pipelines, adaptor patterns.

-----

## 🟪 4. Encapsulation — Python-Style (Not Like Java/C++)

Python does not strictly enforce access modifiers but uses naming conventions:

| Prefix | Meaning | Access Level |
| :--- | :--- | :--- |
| `name` | public | Accessed freely |
| `_name` | protected | Intended for internal use, but accessible |
| `__name` | private | **Name-mangled** (discourages direct access) |

### ✔ Name Mangling

The interpreter automatically rewrites attributes starting with two underscores (`__`) to include the class name, preventing simple accidental modification by subclasses or outside code.

> `__balance` becomes `_Account__balance` internally.

```python
class Account:
    def __init__(self):
        self.__balance = 1000
```

### ✔ Why Encapsulation Matters

  * Restricting direct access to sensitive data.
  * Data validation before modification (e.g., using properties).
  * Preventing accidental corruption.
  * Enforcing business rules (e.g., preventing negative withdrawal).

-----

## 🟨 5. Abstraction — Hiding Complexity

**Abstraction** means exposing only essential information to the user and hiding internal complexity.

Two ways in Python:

### ⭐ 1. Abstract Base Classes (ABC module)

Classes that cannot be instantiated and require derived classes to implement specific methods.

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self):
        # Must be implemented by subclasses
        pass
```

### ⭐ 2. Interfaces via Duck Typing

Python often relies on **duck typing** for implicit interfaces, meaning abstraction is achieved simply by ensuring all necessary components implement the same method (e.g., all database drivers implement a `connect()` method).

> **Real-world uses:** Payment Gateways, Machine Learning Pipeline Steps, Database Wrappers.

-----

## 🟧 6. Class Variables vs Instance Variables (Deep Level)

### ✔ Instance Variables

  * Created inside `__init__`.
  * **Unique** to each specific object (instance).
  * Stored in the object's `__dict__`.

### ✔ Class Variables

  * **Shared** across all objects of the class.
  * Stored in the class's `__dict__`, not the object's `__dict__`.

<!-- end list -->

```python
class Employee:
    company = "Infosys"    # class variable
    def __init__(self, name):
        self.name = name    # instance variable
```

### ✔ Real-Time Usage

| Class Variable | Instance Variable |
| :--- | :--- |
| Global configuration | Account balance |
| Logging prefix | Username/password |
| Counter for objects | Per-user preferences |
| Interest rate for all accounts | Specific user ID |

-----

## 🟥 7. Dunder (Magic) Methods — Most Useful Ones

**Dunder** (double-underscore) methods enable Pythonic behavior and allow custom objects to interact with built-in functions and operators.

### ✔ Object Initialization

  * `__init__`: Standard constructor.
  * `__new__`: Called **before** `__init__` to control object creation.

### ✔ Representation

  * `__str__`: **User-friendly** string representation (for `print()`).
  * `__repr__`: **Developer-friendly** string representation (for debugging/console).

### ✔ Comparison Operators

`__eq__` (`==`), `__lt__` (`<`), `__gt__` (`>`), `__le__` (`<=`), `__ge__` (`>=`)

### ✔ Arithmetic Operators

`__add__` (`+`), `__sub__` (`-`), `__mul__` (`*`), etc.

### ✔ Iterable Methods

  * `__iter__`: Returns an iterator object.
  * `__next__`: Returns the next item in the iteration.

### ✔ Callable Objects

Makes an object behave like a function (e.g., you can call `instance()`).

```python
class Fun:
    def __call__(self):
        print("Object called!")
```

> **Used for:** ML models (`model(x)`), configuration objects, or decorators.

-----

## 🧱 8. Real-Time OOP Architecture Patterns (Industry)

These patterns formalize the interaction between different layers of an application.

  * **Repository Pattern** (Used in Django/Flask Backends): Abstracts the data storage layer.

    ```python
    class UserRepository:
        def get_user(self, id): pass
    ```

  * **Service Layer Pattern**: Contains the core business logic, decoupled from I/O.

    ```python
    class PaymentService:
        def process_payment(self): pass
    ```

  * **Factory Pattern**: Provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.

    ```python
    class ConnectionFactory:
        def get_connection(self, type): pass
    ```

  * **Strategy Pattern** (Polymorphism): Defines a family of algorithms, encapsulates each one, and makes them interchangeable.

    ```python
    class PaymentStrategy: pass
    class UPI(PaymentStrategy): pass
    class Card(PaymentStrategy): pass
    ```

-----

## 🧪 Hands-On OOP Exercises (Real-Time Inspired)

1.  **Payment Processing System**
      * **Implement:** Base class: `Payment`. Derived classes: `UPI`, `Card`, `NetBanking`.
      * **Behavior:** Polymorphic `pay()` method.
      * **Error:** Custom exception: `PaymentFailed`.
2.  **University System**
      * **Create:** `Person` $\rightarrow$ `Student`, `Teacher`.
      * **Attributes:** Teacher has subjects, Student has marks.
      * **Magic:** Override `__str__` for clean representation.
3.  **Smart Home Device Controller**
      * **Classes:** `BaseDevice`, `LightBulb`, `Thermostat`, `Fan`.
      * **Concepts:** Use inheritance, abstract classes (ABC), and polymorphism.
4.  **Order Management (E-commerce Mini Model)**
      * **Classes:** `Product`, `Order`, `Cart`.
      * **Behavior:** Operator overloading (`__add__` to merge carts).
5.  **ATM Simulation**
      * **Ensure:** Private balance (`__balance`).
      * **Rules:** Withdrawal rules.
      * **Logs:** Logs transactions using a separate `Transaction` class.
      * **Error:** Custom error: `InsufficientFunds`.

-----

## 🧩 Mini Project — Bank Management System (OOP, Realistic)

### ✔ Classes to Build

  * `Account`
  * `Bank`
  * `Transaction`

### ✔ Custom Exceptions

  * `InsufficientBalanceError`
  * `InvalidAmountError`

### ✔ Behaviors

  * `deposit()`
  * `withdraw()`
  * `view_balance()`
  * Transaction history logging.
  * Automatic timestamp generation.
  * Class variable for bank-wide interest rate.

### ✔ Concepts Used

  * **Encapsulation** (`__balance`)
  * **Abstraction** (Base methods for transactions)
  * **Polymorphism** (Handling different transaction types)
  * Class vs. instance variables
  * Magic methods (`__str__`, `__repr__`)

