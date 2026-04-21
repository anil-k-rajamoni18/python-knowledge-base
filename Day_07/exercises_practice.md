# 💪 Python Full Stack — Day 7 Exercise & Practice File
# Topic: Encapsulation & Abstraction

> **Instructions:** Work in order. Write predictions before running. Never peek at answers until you've genuinely attempted the problem. The property exercises are the most important — master them.

---

## 📋 Setup Check

```python
from abc import ABC, abstractmethod

# Quick sanity test
class TestABC(ABC):
    @abstractmethod
    def method(self): ...

class Concrete(TestABC):
    def method(self): return "implemented"

try:
    TestABC()               # should raise TypeError
except TypeError:
    print("✅ ABC working")

c = Concrete()
print(c.method())           # implemented
print("✅ Setup complete!")
```

---

## Section A — Predict the Output (No Running Allowed!)

### A1. Name Mangling

```python
class Vehicle:
    def __init__(self, brand, serial):
        self.brand = brand
        self._model = "unknown"
        self.__serial = serial

    def get_serial(self):
        return self.__serial

class Car(Vehicle):
    def __init__(self, brand, serial, doors):
        super().__init__(brand, serial)
        self.__serial = f"CAR-{serial}"   # different from parent's __serial!
        self.doors = doors

    def info(self):
        return f"{self.brand} | {self.__serial} | {self.get_serial()}"

v = Vehicle("Toyota", "V001")
c = Car("Honda", "C002", 4)

print(v.brand)              # Line 1
print(v._model)             # Line 2
print(v.get_serial())       # Line 3

try:
    print(v.__serial)       # Line 4
except AttributeError as e:
    print(f"Error: {e}")

print(c.info())             # Line 5
print(c.__dict__)           # Line 6 — list the keys
```

**Predictions:**
```
Line 1: ______
Line 2: ______
Line 3: ______
Line 4: ______
Line 5: ______
Line 6 keys: ______________________________
```

---

### A2. Property Behavior

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width      # calls setter
        self.height = height    # calls setter

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value

    @property
    def area(self):
        return self._width * self._height

r = Rectangle(4, 5)

print(r.width)          # Line 1
print(r.area)           # Line 2

r.width = 10
print(r.area)           # Line 3

try:
    r.width = -1        # Line 4 — what happens?
except ValueError as e:
    print(f"Error: {e}")

try:
    r.area = 100        # Line 5 — what happens?
except AttributeError as e:
    print(f"Error: {e}")

print(r.__dict__)       # Line 6 — what attributes are stored?
```

**Predictions:**
```
Line 1: ___
Line 2: ___
Line 3: ___
Line 4: ______________________________
Line 5: ______________________________
Line 6: ______________________________
```

---

### A3. Abstract Class Rules

```python
from abc import ABC, abstractmethod

class Appliance(ABC):
    def __init__(self, brand):
        self.brand = brand

    @abstractmethod
    def turn_on(self): ...

    @abstractmethod
    def turn_off(self): ...

    def status(self):
        return f"{self.brand} appliance"

class Washer(Appliance):
    def turn_on(self): return "Washer spinning..."
    # turn_off not implemented!

class Fridge(Appliance):
    def turn_on(self): return "Fridge cooling..."
    def turn_off(self): return "Fridge off."

# Predict what each line does:
try:
    a = Appliance("Generic")    # Line 1
except TypeError as e:
    print(f"1: {type(e).__name__}")

try:
    w = Washer("Samsung")       # Line 2
except TypeError as e:
    print(f"2: {type(e).__name__}")

f = Fridge("LG")                # Line 3 — this works
print(f.turn_on())              # Line 4
print(f.status())               # Line 5
print(isinstance(f, Appliance)) # Line 6
```

**Predictions:**
```
Line 1: ______
Line 2: ______
Line 3: (no error? or error?) ______
Line 4: ______
Line 5: ______
Line 6: ______
```

---

### A4. `@property` in `__init__`

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius    # this goes through setter!

    @property
    def celsius(self): return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value

# Predict:
t1 = Temperature(25)
print(t1._celsius)          # Line 1

try:
    t2 = Temperature(-300)  # Line 2
except ValueError as e:
    print(f"Error: {e}")

t1.celsius = 100
print(t1._celsius)          # Line 3
print(t1.celsius)           # Line 4 — same as Line 3?
```

**Predictions:**
```
Line 1: ___
Line 2: ______________________________
Line 3: ___
Line 4: ___
```

---

### A5. Protected vs Private in Practice

```python
class Config:
    _max_retries = 3        # protected class var

    def __init__(self, host):
        self.host = host
        self._timeout = 30
        self.__secret_key = "abc123"

class DBConfig(Config):
    def __init__(self, host, port):
        super().__init__(host)
        self.port = port

    def connection_string(self):
        # Which of these work?
        return (f"{self.host}:{self.port}"         # a
                f"?timeout={self._timeout}"         # b
                f"?retries={self._max_retries}")    # c
                # f"&key={self.__secret_key}")      # d — intentionally commented

db = DBConfig("localhost", 5432)
print(db.connection_string())    # Line 1

# From OUTSIDE the class hierarchy:
print(db.host)              # Line 2
print(db._timeout)          # Line 3
print(db._max_retries)      # Line 4

try:
    print(db.__secret_key)  # Line 5
except AttributeError as e:
    print(f"Error: {e}")

print(db._Config__secret_key)   # Line 6 — name mangled access
```

**Predictions:**
```
Line 1: ______________________________
Line 2: ______
Line 3: ___
Line 4: ___
Line 5: ______________________________
Line 6: ______
```

---

## Section B — Fill in the Blanks

### B1. Complete the Property

```python
class Circle:
    def __init__(self, radius: float):
        ______ = radius        # 1. use the property setter via __init__

    @______
    def radius(self) -> float:    # 2. define the getter decorator
        return self.______        # 3. return from private storage

    @______.______                # 4. define the setter decorator
    def radius(self, value: float) -> None:
        if value ______:          # 5. validation: must be > 0
            raise ValueError("Radius must be positive")
        self.______ = value       # 6. store in private attribute

    @property
    def area(self) -> float:
        import math
        return math.pi * ______   # 7. compute from private radius

    @property
    def diameter(self) -> float:
        return ______             # 8. use self.radius (the property)

# Test:
c = Circle(5)
print(c.radius)      # 5
print(c.diameter)    # 10
print(c.area)        # 78.54
```

---

### B2. Complete the Abstract Class

```python
from abc import ______, ______      # 1. import ABC and abstractmethod

class Notification(______):          # 2. inherit from ABC
    def __init__(self, sender: str):
        self.sender = sender
        self._log = []

    @______                          # 3. mark as abstract
    def send(self, recipient: str, message: str) -> bool:
        ...

    @property
    @______                          # 4. mark as abstract property
    def channel(self) -> str:
        ...

    def log_send(self, recipient, message, status):   # 5. concrete method
        self._log.append({
            "to": recipient,
            "msg": message,
            "status": status,
            "channel": ______        # 6. use the abstract property
        })

class EmailNotification(Notification):
    @property
    def channel(self) -> str:
        return ______               # 7. return "email"

    def send(self, recipient, message) -> bool:
        print(f"Email to {recipient}: {message}")
        ______.log_send(recipient, message, "sent")  # 8. call concrete method
        return True
```

---

### B3. Fix the Name Mangling Access

```python
class BankAccount:
    def __init__(self, owner, balance, pin):
        self.owner = owner
        self.__balance = balance
        self.__pin = pin

    def get_balance(self):
        return self.__balance

acc = BankAccount("Alice", 1000, 1234)

# Fix each line to correctly access the private attributes:
# (hint: use name mangling syntax)

# 1. Access balance directly (for testing only):
print(acc.______)           # should print 1000

# 2. Access pin directly (for testing only):
print(acc.______)           # should print 1234

# 3. What are the mangled attribute names?
print(acc.______)           # prints the __dict__ with mangled names
```

---

## Section C — Debugging Exercises

### C1. The Recursion Bomb

```python
# Bug: This causes infinite recursion
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price   # Bug is here!

    @property
    def price(self):
        return self.price    # Bug!

    @price.setter
    def price(self, value):
        self.price = value   # Bug!

p = Product("Widget", 9.99)
print(p.price)
# RecursionError!
```

**Identify both bugs and fix:**
```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def price(self):
        return ______    # Fix 1

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        ______ = value   # Fix 2
```

---

### C2. The Missing Abstract Method

```python
from abc import ABC, abstractmethod

class Serializer(ABC):
    @abstractmethod
    def serialize(self, data) -> str: ...

    @abstractmethod
    def deserialize(self, text: str): ...

class JSONSerializer(Serializer):
    import json

    def serialize(self, data) -> str:
        return json.dumps(data)
    # Bug: deserialize not implemented!

# What error happens and when?
s = JSONSerializer()   # Error here? Or later?
result = s.serialize({"key": "value"})
print(result)
```

**Predict the error:**
```
Error type: ______
When it occurs: ______________________________
Error message: ______________________________
```

**Fix:**
```python
class JSONSerializer(Serializer):
    import json

    def serialize(self, data) -> str:
        return json.dumps(data)

    def deserialize(self, text: str):
        return ______    # implement this
```

---

### C3. Wrong Decorator Order for Abstract Property

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    # Bug: decorators in wrong order
    @abstractmethod
    @property
    def area(self) -> float: ...
```

**Explain what's wrong and fix:**
```
Wrong order causes: ______________________________

Correct order:
@______     # first (outer decorator)
@______     # second (inner decorator)
def area(self) -> float: ...
```

---

### C4. Protected vs Private Confusion

```python
class Animal:
    def __init__(self, name):
        self.__name = name   # private

class Dog(Animal):
    def speak(self):
        return f"{self.__name} says Woof!"   # Bug!

d = Dog("Rex")
d.speak()   # AttributeError!
```

**Explain why this fails:**
```
_____________________________________________
```

**Fix (two options):**
```python
# Option 1: Change Animal to use protected
class Animal:
    def __init__(self, name):
        self.______ = name   # protected — subclasses can access

# Option 2: Expose via property in Animal
class Animal:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self): return ______  # provide access through property

# Dog can then use self.name in both options
```

---

### C5. Read-Only Property Violation

```python
class Circle:
    def __init__(self, radius):
        self._r = radius

    @property
    def area(self):
        import math
        return math.pi * self._r ** 2

c = Circle(5)
print(c.area)       # 78.54 — this works

# Bug: trying to assign a computed property
c.area = 100        # should raise AttributeError
# But the developer wants to "set" the area — how should they do it?
```

**Answer the design question:**
```
Why can't you set area directly?
_________________________________________

If the user wants to set area and have radius auto-calculated, how would you implement this?
(write the setter for area)
@area.setter
def area(self, value: float) -> None:
    import math
    self._r = ______    # back-calculate radius from area
```

---

## Section D — Write the Code

### D1. Secure BankAccount — Full Implementation

```python
"""
Build a complete SecureBankAccount class:

Private attributes:
- __owner: str
- __balance: float
- __pin: int (4-digit)
- __transaction_log: list
- __failed_attempts: int
- __locked: bool

Properties:
- owner: str — read-only
- balance: float — read-only
- is_locked: bool — read-only computed
- annual_interest: float — computed (balance × 0.035)

Private methods:
- __verify_pin(pin) → None: raises ValueError/RuntimeError
- __log(type, amount) → None

Public methods:
- deposit(amount) → float: no PIN needed
- withdraw(amount, pin) → float: requires PIN
- change_pin(current, new) → None: validates both
- get_statement(pin) → str: requires PIN

Class variable:
- interest_rate = 0.035

Validation:
- PIN must be 4-digit integer (1000-9999)
- balance never goes negative
- Lock after 3 failed PIN attempts
"""

class SecureBankAccount:
    interest_rate = 0.035

    def __init__(self, owner: str, balance: float, pin: int):
        # Your implementation
        pass

    # Your properties and methods here


# Test suite
def test_secure_account():
    acc = SecureBankAccount("Alice", 5000, 1234)

    # Properties
    assert acc.owner == "Alice"
    assert acc.balance == 5000.0
    assert acc.is_locked == False
    assert acc.annual_interest == 5000 * 0.035

    # Cannot set balance directly
    try:
        acc.balance = 9999
        assert False, "Should raise AttributeError"
    except AttributeError:
        pass

    # Deposit (no PIN)
    acc.deposit(1000)
    assert acc.balance == 6000.0

    # Withdraw with correct PIN
    acc.withdraw(500, 1234)
    assert acc.balance == 5500.0

    # Withdraw with wrong PIN — 3 attempts lock the account
    for i in range(2):
        try:
            acc.withdraw(100, 9999)
        except ValueError:
            pass

    try:
        acc.withdraw(100, 9999)  # 3rd failed attempt
    except RuntimeError as e:
        assert "locked" in str(e).lower()

    assert acc.is_locked == True

    # PIN change
    acc2 = SecureBankAccount("Bob", 2000, 5678)
    acc2.change_pin(5678, 9999)
    acc2.withdraw(100, 9999)    # new PIN works
    assert acc2.balance == 1900.0

    # Invalid PIN format
    try:
        acc2.change_pin(9999, 12)   # too short
        assert False
    except ValueError:
        pass

    # Statement requires PIN
    statement = acc2.get_statement(9999)
    assert "Bob" in statement

    print("✅ All SecureBankAccount tests passed!")

test_secure_account()
```

---

### D2. Abstract Payment System — Full Build

```python
"""
Build the complete abstract payment system:

PaymentProcessor (ABC):
- __init__(processor_name: str)
- @abstractmethod process_payment(amount, recipient) → bool
- @abstractmethod refund(transaction_id) → bool
- @abstractproperty payment_type → str
- @abstractproperty transaction_fee → float (decimal, e.g. 0.025)
- Concrete: log_transaction(tx_id, amount, recipient, status) → None
- Concrete: get_fee(amount) → float (amount × fee)
- Concrete: get_history() → list[dict]
- Concrete: __str__ → processor name + type

Three implementations:
1. CreditCardProcessor
   - payment_type: "credit_card"
   - fee: 2.5%
   - process_payment: generates tx ID, logs, returns True
   - refund: logs refund, returns True

2. UPIProcessor(upi_id: str)
   - payment_type: "upi"
   - fee: 0%
   - process_payment: validates amount ≤ 100000, logs
   - refund: simulates 2-3 day return

3. CryptoProcessor(wallet: str)
   - payment_type: "cryptocurrency"
   - fee: 1%
   - process_payment: logs as "pending"
   - refund: returns False (immutable blockchain)

Polymorphic functions:
- checkout(processor, amount, merchant) → None
  (prints summary, calls process_payment, prints result)
- cheapest_processor(processors, amount) → PaymentProcessor
  (returns processor with lowest fee for that amount)
"""

from abc import ABC, abstractmethod
from datetime import datetime

class PaymentProcessor(ABC):
    # Your implementation
    pass

class CreditCardProcessor(PaymentProcessor):
    # Your implementation
    pass

class UPIProcessor(PaymentProcessor):
    # Your implementation
    pass

class CryptoProcessor(PaymentProcessor):
    # Your implementation
    pass


# Test
def test_payment_system():
    processors = [
        CreditCardProcessor(),
        UPIProcessor("alice@upi"),
        CryptoProcessor("0xABCD1234"),
    ]

    # Cannot instantiate ABC
    try:
        PaymentProcessor("test")
        assert False
    except TypeError:
        pass

    # All processors work with checkout()
    for proc in processors:
        checkout(proc, 500, "TechStore")

    # Fee comparison
    cheap = cheapest_processor(processors, 1000)
    print(f"Cheapest for ₹1000: {cheap.payment_type}")
    # Should be UPI (0% fee)

    # UPI limit
    upi = UPIProcessor("bob@upi")
    result = upi.process_payment(200000, "Expensive Store")
    assert result == False   # over limit

    print("✅ All PaymentProcessor tests passed!")

test_payment_system()
```

---

### D3. Student with Validated Properties

```python
"""
Student class:

Private storage:
- __name: str
- __grades: list[float]
- __student_id: str (auto-generated, read-only)

Properties:
- name: str — read-only (set once)
- student_id: str — read-only
- grades: list — returns COPY (not original)
- average: float — computed (0.0 if no grades)
- letter_grade: str — computed from average:
    90+ → A, 80+ → B, 70+ → C, 60+ → D, below → F

Methods:
- add_grade(grade: float): validates 0–100
- remove_last_grade() → float: raises IndexError if empty
- get_report() → str: formatted summary
- clear_grades() → None

Static method:
- generate_id() → str: returns "STU-{6 random digits}"

Demonstrate:
- grades returns a copy (modifying returned list doesn't affect student)
- letter_grade updates automatically with grades
- Attempting to set grades list directly → AttributeError
"""

import random

class Student:
    # Your implementation
    pass


# Test
def test_student():
    s = Student("Alice")
    print(s.student_id)     # STU-XXXXXX

    assert s.average == 0.0
    assert s.letter_grade == "F"

    s.add_grade(85)
    s.add_grade(92)
    s.add_grade(78)
    assert abs(s.average - 85.0) < 0.01
    assert s.letter_grade == "B"

    # Grades returns a copy
    grades_copy = s.grades
    grades_copy.append(999)   # modify the copy
    assert 999 not in s.grades  # original unchanged!

    # Cannot assign grades
    try:
        s.grades = [100, 100]
        assert False
    except AttributeError:
        pass

    # Validation
    try:
        s.add_grade(105)    # over 100
        assert False
    except ValueError:
        pass

    # remove_last
    removed = s.remove_last_grade()
    assert removed == 78

    print(s.get_report())
    print("✅ All Student tests passed!")

test_student()
```

---

### D4. Protocol vs ABC Comparison

```python
"""
Build the same interface two ways to see the difference:

WAY 1 — ABC approach:
    Drawable(ABC)
    - @abstractmethod draw() → str
    - @abstractproperty color → str
    - Concrete: display() (uses draw() + color)

WAY 2 — Protocol approach:
    DrawableProtocol(Protocol)
    - draw() → str
    - color property → str

Create classes for both:
    CircleABC(Drawable) — inherits from ABC
    CircleDuck — no inheritance, just has draw() and color property

Functions:
    render_abc(item: Drawable) → works with ABC instances
    render_protocol(item: DrawableProtocol) → works with either class!

Demonstrate:
    CircleABC works with both render functions
    CircleDuck works ONLY with render_protocol (not render_abc unless inheriting)
    isinstance check difference
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

class Drawable(ABC):
    # Your implementation
    pass

@runtime_checkable
class DrawableProtocol(Protocol):
    # Your implementation
    pass

class CircleABC(Drawable):
    # Your implementation
    pass

class CircleDuck:
    # No inheritance! Just has the right methods
    # Your implementation
    pass


# Demonstrate
abc_circle = CircleABC(5, "red")
duck_circle = CircleDuck(3, "blue")

print(isinstance(abc_circle, Drawable))       # True
print(isinstance(duck_circle, Drawable))      # False — no inheritance!

print(isinstance(abc_circle, DrawableProtocol))   # True — has the methods
print(isinstance(duck_circle, DrawableProtocol))  # True — has the methods!

# render_abc only works with proper inheritance
render_abc(abc_circle)      # works
try:
    render_abc(duck_circle) # may fail with type checker, but runs in Python
except TypeError:
    print("render_abc needs ABC inheritance")

# render_protocol works for both
render_protocol(abc_circle)     # works
render_protocol(duck_circle)    # also works!
```

---

## Section E — Property Experiments

### E1. Computed Properties Chain

```python
# Run this and observe how properties chain together
class Circle:
    def __init__(self, radius):
        self.radius = radius   # setter validates

    @property
    def radius(self): return self._r

    @radius.setter
    def radius(self, v):
        if v <= 0: raise ValueError("Must be positive")
        self._r = v

    @property
    def diameter(self): return self._r * 2

    @diameter.setter
    def diameter(self, v): self.radius = v / 2   # delegates to radius setter!

    @property
    def area(self):
        import math
        return math.pi * self._r ** 2

c = Circle(5)
print(f"r={c.radius}, d={c.diameter}, area={c.area:.2f}")

# Set via diameter — radius updates automatically
c.diameter = 20
print(f"r={c.radius}, d={c.diameter}, area={c.area:.2f}")

# Try invalid via diameter setter
try:
    c.diameter = -10    # negative diameter → negative radius → ValueError in setter!
except ValueError as e:
    print(f"Caught from diameter setter: {e}")
```

**Questions to answer:**
```
1. When you set c.diameter = 20, what does self.radius = v/2 actually call?
   _______________________________________________

2. Why does the validation in radius.setter protect diameter.setter too?
   _______________________________________________

3. What does c.__dict__ contain? (Only _r?)
   _______________________________________________
```

---

### E2. Name Mangling Proof

```python
# Run this experiment to fully understand name mangling
class Parent:
    def __init__(self):
        self.__data = "parent data"
        self._shared = "shared"

    def parent_view(self):
        return f"Parent sees: {self.__data}"

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__data = "child data"   # new attribute! not overwriting parent's!

    def child_view(self):
        return f"Child sees: {self.__data}"

obj = Child()
print("parent_view:", obj.parent_view())     # what does Parent's method see?
print("child_view:", obj.child_view())       # what does Child's method see?
print("__dict__:", obj.__dict__)              # see ALL attributes with their mangled names
print("_shared:", obj._shared)               # protected — accessible from anywhere
```

**Fill in expected output:**
```
parent_view: ______________________________
child_view:  ______________________________
__dict__ keys: ____________________________
_shared: ______
```

**Why Parent and Child each see different `__data`:**
```
_______________________________________________
_______________________________________________
```

---

## Section F — Mini Project: Secure Student Database

```python
"""
Build a secure student database system:

1. Student class (with encapsulation):
   - Private: __name, __grades, __student_id, __gpa
   - Properties: name (R/O), student_id (R/O), gpa (computed), 
                 grades (returns copy), letter_grade (computed)
   - Methods: add_grade(grade), remove_grade(index), get_report()
   - Validation: grades 0-100, name non-empty

2. Abstract GradeCalculator(ABC):
   - @abstractmethod calculate_gpa(grades: list) → float
   - @abstractproperty scale → float (4.0 or 10.0)
   - Concrete: letter_from_gpa(gpa) → str

3. Two implementations:
   - StandardGPA(GradeCalculator): 4.0 scale
   - IndianGPA(GradeCalculator): 10.0 scale (CGPA)

4. StudentDatabase class:
   - Private: __students dict (id → Student)
   - __calculator: GradeCalculator (injected)
   - Properties: student_count (R/O), calculator (R/O)
   - Methods:
     - add_student(name) → Student
     - get_student(student_id) → Student | None
     - remove_student(student_id) → bool
     - top_students(n=3) → list[Student] (by GPA)
     - class_summary() → str (formatted report)

Demonstrate:
- Students with validated grades
- Polymorphic GPA calculation (same method, different calculator)
- Name mangling verification
- Read-only properties preventing corruption
"""

from abc import ABC, abstractmethod
import random

class Student:
    def __init__(self, name: str):
        # Your implementation
        pass

class GradeCalculator(ABC):
    @abstractmethod
    def calculate_gpa(self, grades: list[float]) -> float: ...

    @property
    @abstractmethod
    def scale(self) -> float: ...

    def letter_from_gpa(self, gpa: float) -> str:
        ratio = gpa / self.scale
        if ratio >= 0.9: return "A"
        if ratio >= 0.8: return "B"
        if ratio >= 0.7: return "C"
        if ratio >= 0.6: return "D"
        return "F"

class StandardGPA(GradeCalculator):
    @property
    def scale(self) -> float: return 4.0

    def calculate_gpa(self, grades: list[float]) -> float:
        if not grades: return 0.0
        avg = sum(grades) / len(grades)
        return round(avg / 25, 2)  # 0-100 → 0-4.0

class IndianGPA(GradeCalculator):
    @property
    def scale(self) -> float: return 10.0

    def calculate_gpa(self, grades: list[float]) -> float:
        if not grades: return 0.0
        avg = sum(grades) / len(grades)
        return round(avg / 10, 1)  # 0-100 → 0-10.0

class StudentDatabase:
    def __init__(self, calculator: GradeCalculator):
        # Your implementation
        pass


def run_demo():
    print("=== Standard GPA System ===")
    std_db = StudentDatabase(StandardGPA())
    alice = std_db.add_student("Alice")
    bob = std_db.add_student("Bob")
    carol = std_db.add_student("Carol")

    for name, grades in [
        ("Alice", [92, 88, 95, 90]),
        ("Bob", [75, 70, 78, 72]),
        ("Carol", [85, 82, 88, 80]),
    ]:
        student = std_db.get_student(getattr(eval(name.lower()), "student_id", None))
        # (simplified — in real code you'd track by id properly)

    print(std_db.class_summary())

    print("\n=== Indian CGPA System ===")
    ind_db = StudentDatabase(IndianGPA())
    # Add same students, compare GPA outputs

if __name__ == "__main__":
    run_demo()
```

---

## ✅ Answer Key

<details>
<summary>Click to reveal — attempt everything first!</summary>

### A1 Answers
```
Line 1: Toyota
Line 2: unknown
Line 3: V001   (Vehicle's __serial, not Car's)
Line 4: Error: 'Vehicle' object has no attribute '__serial'
Line 5: Honda | CAR-C002 | C002
         (Car's __serial is CAR-C002, get_serial() uses Vehicle's __serial = C002)
Line 6 keys: brand, _model, _Vehicle__serial, doors, _Car__serial
```

### A2 Answers
```
Line 1: 4
Line 2: 20
Line 3: 50  (10 × 5)
Line 4: Error: Width must be positive
Line 5: Error: can't set attribute (no setter for area)
Line 6: {'_width': 10, '_height': 5}  (properties store in _width, _height)
```

### A3 Answers
```
Line 1: TypeError (Appliance is abstract — has unimplemented methods)
Line 2: TypeError (Washer is also abstract — turn_off not implemented!)
Line 3: Works — Fridge is fully concrete
Line 4: Fridge cooling...
Line 5: LG appliance
Line 6: True — isinstance recognizes ABC inheritance
```

### A4 Answers
```
Line 1: 25      (__init__ self.celsius=25 triggers setter, stores in _celsius)
Line 2: ValueError: Below absolute zero!
Line 3: 100
Line 4: 100  (same as Line 3 — celsius property reads _celsius)
```

### A5 Answers
```
Line 1: localhost:5432?timeout=30?retries=3
Line 2: localhost
Line 3: 30     (protected, accessible)
Line 4: 3      (protected class var, accessible)
Line 5: Error: 'DBConfig' object has no attribute '__secret_key'
         (would need _Config__secret_key)
Line 6: abc123  (name-mangled access)
```

### B1 Answers
```python
self.radius = radius          # 1. property setter called
@property                     # 2.
return self._radius           # 3.
@radius.setter                # 4.
if value <= 0:                # 5.
self._radius = value          # 6.
math.pi * self._radius ** 2   # 7.
return self.radius * 2        # 8. or self._radius * 2
```

### B2 Answers
```python
from abc import ABC, abstractmethod    # 1.
class Notification(ABC):               # 2.
@abstractmethod                        # 3.
@abstractmethod                        # 4.
self.channel                           # 6. (use abstract property)
return "email"                         # 7.
self.log_send(...)                     # 8. (use super() or self.)
```

### C1 Fix
```python
@property
def price(self): return self._price    # Fix 1: use _price

@price.setter
def price(self, value):
    if value < 0: raise ValueError(...)
    self._price = value                # Fix 2: store in _price
```

### C2
```
Error type: TypeError
When it occurs: At JSONSerializer() instantiation
Message: Can't instantiate abstract class JSONSerializer with abstract methods deserialize

Fix: def deserialize(self, text): return self.json.loads(text)
```

### C3 Fix
```
Correct order (read bottom-up for decorator stacking):
@property         # outer — makes it a property descriptor
@abstractmethod   # inner — marks as abstract
def area(self) -> float: ...
```

### C4 Fix
```
Why: self.__name in Dog's speak() looks for _Dog__name
     (name mangling uses the class where the code is written)
     But __name was set in Animal as _Animal__name — different attribute!

Fix 1: self._name = name (protected — accessible everywhere in hierarchy)
Fix 2: @property def name(self): return self._Animal__name
        (or expose via property)
```

### C5 Fix
```python
@area.setter
def area(self, value: float) -> None:
    import math
    self._r = math.sqrt(value / math.pi)  # back-calculate radius
```

</details>

---

## 📊 Self-Assessment Checklist

| Concept | ✅ Got it | 🔄 Need review | ❓ Confused |
|---------|-----------|---------------|------------|
| Three access levels (public/protected/private) | | | |
| Name mangling — what Python does to `__attr` | | | |
| Accessing mangled name via `_ClassName__attr` | | | |
| `@property` getter syntax and usage | | | |
| `@attr.setter` with validation | | | |
| `@attr.deleter` usage | | | |
| Recursion trap — storing in `_attr` not `attr` | | | |
| Computed (read-only) property — no setter | | | |
| `__init__` calling property setter automatically | | | |
| ABC — what it is and why it can't be instantiated | | | |
| `@abstractmethod` — what it forces | | | |
| Abstract property — `@property @abstractmethod` | | | |
| Concrete methods in ABC — shared by all subclasses | | | |
| Subclass must implement ALL abstract methods | | | |
| Duck typing vs ABC vs Protocol | | | |
| When to use `__private` vs `_protected` | | | |

**Score:**
- 16/16 ✅ — Excellent! Ready for Day 8 (Decorators — you'll see @property from a new angle)
- 10–15 ✅ — Good. Redo the property exercises — they appear in every Django project
- < 10 ✅ — Focus on `@property` first (most used), then ABC. Re-read Sections 3.3 and 3.5

---

*Day 7 Exercises Complete — Day 8: Decorators — function wrappers, `@functools.wraps`, class decorators, and building your own*
