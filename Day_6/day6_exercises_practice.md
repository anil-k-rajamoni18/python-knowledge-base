# 💪 Python Full Stack — Day 6 Exercise & Practice File
# Topic: Inheritance & Polymorphism

> **Instructions:** Work through sections in order. Write your predictions before running. Attempt every problem genuinely before checking answers. All exercises build on the Account hierarchy from the theory notes.

---

## 📋 Setup Check

```python
# Verify your understanding before starting
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self): return "..."

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    def speak(self): return "Woof!"

d = Dog("Rex", "Labrador")
print(isinstance(d, Dog))       # True
print(isinstance(d, Animal))    # True
print(d.speak())                # Woof!
print(d.name)                   # Rex
print("✅ Setup OK — let's go!")
```

---

## Section A — Predict the Output (No Running Allowed!)

### A1. Inheritance Basics

```python
class Vehicle:
    wheels = 4

    def __init__(self, brand):
        self.brand = brand

    def describe(self):
        return f"{self.brand} with {self.wheels} wheels"

class Motorcycle(Vehicle):
    wheels = 2

    def __init__(self, brand, engine_cc):
        super().__init__(brand)
        self.engine_cc = engine_cc

class Truck(Vehicle):
    def __init__(self, brand, payload):
        super().__init__(brand)
        self.payload = payload

car = Vehicle("Toyota")
moto = Motorcycle("Honda", 600)
truck = Truck("Volvo", 10)

print(car.describe())           # Line 1
print(moto.describe())          # Line 2
print(truck.describe())         # Line 3
print(moto.wheels)              # Line 4
print(Vehicle.wheels)           # Line 5
print(isinstance(moto, Vehicle))# Line 6
print(issubclass(Truck, Motorcycle))  # Line 7
```

**Predictions:**
```
Line 1: ______________________________
Line 2: ______________________________
Line 3: ______________________________
Line 4: ___
Line 5: ___
Line 6: ___
Line 7: ___
```

---

### A2. `super()` Tracing

```python
class A:
    def __init__(self):
        print("A.__init__")
        self.a = "from_A"

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()
        self.b = "from_B"

class C(B):
    def __init__(self):
        print("C.__init__")
        super().__init__()
        self.c = "from_C"

obj = C()
print(obj.a, obj.b, obj.c)
```

**Predictions (in order of print statements):**
```
1st: ______
2nd: ______
3rd: ______
4th: ______
```

---

### A3. Method Overriding

```python
class Shape:
    def area(self):
        return 0

    def describe(self):
        return f"Shape with area {self.area():.2f}"

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

s = Square(4)
c = Circle(5)
base = Shape()

print(base.describe())      # Line 1
print(s.describe())         # Line 2
print(c.describe())         # Line 3
print(s.area())             # Line 4
```

**Key question:** In Line 2, `s.describe()` is called. Inside `describe()`, it calls `self.area()`. Whose `area()` is called — `Shape`'s or `Square`'s?

**Predictions:**
```
Line 1: ______________________________
Line 2: ______________________________
Line 3: ______________________________
Line 4: ___
```

**Answer to key question:**
```
_______________________________________
```

---

### A4. MRO

```python
class A:
    def who(self): return "A"

class B(A):
    def who(self): return f"B->{super().who()}"

class C(A):
    def who(self): return f"C->{super().who()}"

class D(B, C):
    pass

class E(D):
    def who(self): return f"E->{super().who()}"

print(E().who())            # Line 1
print(E.__mro__)            # Line 2 — list the classes in order
```

**Predictions:**
```
Line 1: ______________________________
Line 2 (class names only): E → ___ → ___ → ___ → ___ → object
```

---

### A5. Polymorphism with Duck Typing

```python
class Dog:
    def speak(self): return "Woof!"
    def move(self): return "runs"

class Cat:
    def speak(self): return "Meow!"
    def move(self): return "slinks"

class Robot:
    def speak(self): return "Beep!"
    # No move() method!

def animal_show(things):
    for thing in things:
        print(f"{thing.__class__.__name__}: {thing.speak()}")

def movement_show(things):
    for thing in things:
        try:
            print(f"{thing.__class__.__name__}: {thing.move()}")
        except AttributeError as e:
            print(f"{thing.__class__.__name__}: ERROR - {e}")

participants = [Dog(), Cat(), Robot()]
animal_show(participants)
print("---")
movement_show(participants)
```

**Predictions:**
```
animal_show output:
___________________________________________

movement_show output:
___________________________________________
```

---

## Section B — Fill in the Blanks

### B1. Complete the Inheritance Chain

```python
class Employee:
    company = "TechCorp"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def pay_details(self):
        return f"{self.name}: base ${self.salary:,.2f}"


class Developer(Employee):
    def __init__(self, name, salary, language):
        ______.__init__(name, salary)      # 1. call parent (use super())
        self.language = ______             # 2. set language

    def pay_details(self):
        base = ______.__init__(name, salary)    # BUG: fix this line using super()
        return f"{base} | Language: {self.language}"


class SeniorDeveloper(Developer):
    BONUS_RATE = 0.20

    def __init__(self, name, salary, language, years_exp):
        ______(name, salary, language)     # 3. call parent
        self.years_exp = years_exp

    def pay_details(self):
        base_details = ______              # 4. call Developer's pay_details()
        bonus = self.salary * self.BONUS_RATE
        return f"{base_details} | Bonus: ${bonus:,.2f}"
```

---

### B2. Fix the Override

```python
class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        self._transactions = []

    def deposit(self, amount):
        self.balance += amount
        self._transactions.append(("deposit", amount))
        return self.balance

class PremiumAccount(Account):
    CASHBACK_RATE = 0.02

    def deposit(self, amount):
        # BUG: This override completely duplicates parent code
        # and adds cashback. Fix it using super().
        self.balance += amount                              # duplicated!
        self._transactions.append(("deposit", amount))     # duplicated!
        cashback = amount * self.CASHBACK_RATE
        self.balance += cashback
        self._transactions.append(("cashback", cashback))  # new
        return self.balance

    # Fix the deposit method above using super():
    # def deposit(self, amount):
    #     ______________________________  # 1 line: call parent deposit
    #     cashback = ______
    #     self.balance += cashback
    #     self._transactions.append(________)
    #     return self.balance
```

---

### B3. Complete the MRO Prediction

```python
class Logger:
    def log(self, msg): print(f"LOG: {msg}")

class Validator:
    def validate(self, data): return True

class BaseView:
    def handle(self, request): return "response"

class ProductView(Logger, Validator, BaseView):
    pass

# Fill in the MRO order:
# ProductView → ___ → ___ → ___ → object

# What happens when you call:
pv = ProductView()
pv.log("test")          # From which class? ______
pv.validate({})         # From which class? ______
pv.handle("GET /")      # From which class? ______
```

---

## Section C — Debugging Exercises

### C1. The Forgotten `super()`

```python
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

class Car(Vehicle):
    def __init__(self, make, model, year, doors):
        # Bug: super().__init__ not called!
        self.doors = doors

car = Car("Toyota", "Camry", 2023, 4)
print(car.doors)    # 4 — this works
print(car.make)     # AttributeError! — make was never set
```

**Fix the `Car.__init__` method:**
```python
class Car(Vehicle):
    def __init__(self, make, model, year, doors):
        ______________________________   # Fix here
        self.doors = doors
```

---

### C2. The Broken Polymorphism

```python
# This code uses isinstance instead of polymorphism — fix it!

class Circle:
    def __init__(self, r): self.r = r

class Rectangle:
    def __init__(self, w, h): self.w = w; self.h = h

class Triangle:
    def __init__(self, b, h): self.b = b; self.h = h

def calculate_area(shape):
    # ❌ BAD: explicit type checking breaks polymorphism
    if isinstance(shape, Circle):
        return 3.14 * shape.r ** 2
    elif isinstance(shape, Rectangle):
        return shape.w * shape.h
    elif isinstance(shape, Triangle):
        return 0.5 * shape.b * shape.h
    else:
        raise ValueError("Unknown shape type")

# What's wrong with this design?
# How would you fix it using inheritance and polymorphism?
```

**Rewrite using proper OOP:**
```python
class Shape:
    def area(self): raise NotImplementedError

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): ______

class Rectangle(Shape):
    def __init__(self, w, h): ______
    def area(self): ______

class Triangle(Shape):
    def __init__(self, b, h): ______
    def area(self): ______

# Now calculate_area becomes:
def calculate_area(shape: Shape) -> float:
    return ______   # one line!
```

---

### C3. The Wrong Inheritance Relationship

```python
# This code has an IS-A vs HAS-A mistake — find and fix it

class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self):
        return f"Engine ({self.horsepower}hp) started!"

    def stop(self):
        return "Engine stopped."

class Car(Engine):      # ← BUG: Wrong! Car is not a type of Engine
    def __init__(self, brand, horsepower):
        super().__init__(horsepower)
        self.brand = brand

    def drive(self):
        return f"{self.brand} is driving with {self.horsepower}hp"

car = Car("BMW", 300)
print(car.start())   # Inherits Engine.start() — seems to work but IS wrong
print(car.drive())
```

**What's the correct design? Rewrite using composition:**
```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self): return f"Engine ({self.horsepower}hp) started!"
    def stop(self): return "Engine stopped."

class Car:                   # No longer inherits from Engine
    def __init__(self, brand, horsepower):
        self.brand = brand
        self.______ = ______  # HAS-AN Engine
        # Fix: composition

    def start_car(self):
        return self.______.______  # delegate to engine

    def drive(self):
        return f"{self.brand} driving at {self.engine.horsepower}hp"
```

---

### C4. The MRO Conflict

```python
# This code will raise a TypeError about inconsistent MRO
# Figure out why, then fix it

class A: pass
class B(A): pass
class C(A): pass

class D(A, B):   # ← causes TypeError
    pass
```

**Explain why this causes an error:**
```
_____________________________________________
_____________________________________________
```

**Fix it:**
```python
class D(______, ______):   # correct order
    pass
```

---

### C5. The Missing `super()` in Override

```python
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
        self._sound_count = 0

    def make_sound(self):
        self._sound_count += 1
        return f"{self.name} made a sound"

class Dog(Animal):
    def make_sound(self):
        # Bug: doesn't call super() — _sound_count never increments!
        return f"{self.name} says: Woof!"

dog = Dog("Rex", "Canis lupus")
print(dog.make_sound())
print(dog._sound_count)   # Expected 1, actual: 0 — BUG!
```

**Fix the `make_sound` method to also call the parent (incrementing the counter):**
```python
class Dog(Animal):
    def make_sound(self):
        ______                          # call parent first (increments counter)
        return f"{self.name} says: Woof!"
```

---

## Section D — Write the Code

### D1. Complete Account Hierarchy

Build the full Account hierarchy from scratch:

```python
"""
Account (base)
├── SavingsAccount(Account)
│   - interest_rate: float = 0.04
│   - MINIMUM_BALANCE: float = 1000
│   - MAX_WITHDRAWALS: int = 3
│   - _monthly_withdrawals: int = 0
│   - withdraw(): check min balance + withdrawal limit, then super()
│   - calculate_interest(): balance * rate, adds to balance
│   - reset_monthly_withdrawals(): resets counter
│
├── CurrentAccount(Account)
│   - overdraft_limit: float
│   - withdraw(): allows overdraft, warns when negative
│   - calculate_interest(): returns 0 (no interest)
│   - available_balance property: balance + overdraft_limit
│
└── FixedDepositAccount(Account)
    - lock_in_months: int
    - interest_rate: float = 0.075
    - maturity_date: date
    - withdraw(): blocks if before maturity
    - calculate_interest(): simple interest, marks as mature
    - get_maturity_value(): preview amount at maturity
"""

from datetime import date

class Account:
    bank_name = "Python National Bank"

    def __init__(self, owner: str, balance: float = 0.0):
        # Your implementation
        pass

    def deposit(self, amount: float) -> float:
        # Your implementation
        pass

    def withdraw(self, amount: float) -> float:
        # Your implementation
        pass

    def get_balance(self) -> float:
        return self.balance

    def calculate_interest(self) -> float:
        return 0.0

    def _log(self, tx_type: str, amount: float) -> None:
        # Your implementation
        pass

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.owner}: ${self.balance:,.2f}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(owner={self.owner!r}, balance={self.balance:.2f})"


class SavingsAccount(Account):
    # Your implementation
    pass


class CurrentAccount(Account):
    # Your implementation
    pass


class FixedDepositAccount(Account):
    # Your implementation
    pass


# ── Test suite ────────────────────────────────────────────────────────────
def test_accounts():
    print("=== Testing Account Hierarchy ===\n")

    # Savings tests
    s = SavingsAccount("Alice", 10000)
    s.deposit(5000)
    assert s.get_balance() == 15000, "deposit failed"
    s.withdraw(2000)
    assert s.get_balance() == 13000, "withdraw failed"

    # Test minimum balance
    try:
        s.withdraw(12500)   # would leave only 500 — below minimum
        assert False, "Should raise ValueError"
    except ValueError as e:
        print(f"✅ Min balance check: {e}")

    # Test interest
    old_balance = s.get_balance()
    interest = s.calculate_interest()
    assert s.get_balance() > old_balance, "interest not applied"
    print(f"✅ Interest earned: ${interest:.2f}")

    # Current account tests
    c = CurrentAccount("Bob", 5000, overdraft_limit=3000)
    c.withdraw(7000)   # uses overdraft: 5000 + 3000 available
    print(f"✅ Overdraft used: balance = ${c.get_balance():,.2f}")
    assert c.get_balance() == -2000, "overdraft calculation wrong"

    try:
        c.withdraw(2000)  # would exceed overdraft limit
        assert False
    except ValueError as e:
        print(f"✅ Overdraft limit enforced: {e}")

    # Fixed deposit tests
    fd = FixedDepositAccount("Carol", 50000, lock_in_months=12)
    try:
        fd.withdraw(1000)   # locked!
        assert False
    except ValueError as e:
        print(f"✅ FD lock enforced: {e}")
    print(f"✅ FD maturity value preview: ${fd.get_maturity_value():,.2f}")

    # Polymorphism test
    print("\n=== Polymorphism Test ===")
    accounts = [s, c, fd]
    for acc in accounts:
        print(acc)

    print("\n✅ All tests passed!")

test_accounts()
```

---

### D2. Polymorphic `process_monthly_interest`

```python
def process_monthly_interest(accounts: list) -> dict:
    """
    Polymorphic function — works for any Account subtype.

    For each account:
    1. Call calculate_interest() (each type implements differently)
    2. Track total interest paid out

    Returns: dict with {owner: interest_earned}
    """
    # Your implementation here
    pass


# Test
savings = SavingsAccount("Alice", 50000)
current = CurrentAccount("Bob", 10000, overdraft_limit=5000)
fixed = FixedDepositAccount("Carol", 100000, lock_in_months=12)

result = process_monthly_interest([savings, current, fixed])
print(result)
# Expected: {'Alice': <positive float>, 'Bob': 0.0, 'Carol': 0.0}

# Notice: the function didn't need to know the types of accounts!
# It called the same method on all — polymorphism handles the rest.
```

---

### D3. Shape Hierarchy with ABC

```python
"""
Use Abstract Base Classes to enforce the contract.

Shape (ABC)
├── @abstractmethod area() -> float
├── @abstractmethod perimeter() -> float
├── describe() -> str (concrete — shared)
├── is_larger_than(other: Shape) -> bool (concrete — uses area())
│
├── Circle(Shape)
│   - __init__(radius: float)
│   - area(), perimeter()
│
├── Rectangle(Shape)
│   - __init__(width: float, height: float)
│   - area(), perimeter()
│   - is_square() -> bool
│
└── Triangle(Shape)
    - __init__(base: float, height: float, s1: float, s2: float)
    - area(), perimeter()

Functions:
- largest_shape(shapes: list) -> Shape
- sort_by_area(shapes: list) -> list[Shape] (sorted ascending)
- shapes_larger_than(shapes: list, threshold: float) -> list[Shape]
"""

from abc import ABC, abstractmethod
import math

class Shape(ABC):
    # Your implementation
    pass

class Circle(Shape):
    # Your implementation
    pass

class Rectangle(Shape):
    # Your implementation
    pass

class Triangle(Shape):
    # Your implementation
    pass


# Test
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 4, 5, 5),
    Rectangle(6, 6),
    Circle(2),
]

print("All shapes:")
for s in shapes:
    print(f"  {s.describe()}")

print(f"\nLargest: {largest_shape(shapes).describe()}")
print(f"\nSorted by area:")
for s in sort_by_area(shapes):
    print(f"  {s.describe()}")

print(f"\nShapes larger than area 30:")
for s in shapes_larger_than(shapes, 30):
    print(f"  {s.describe()}")

# Test that Shape() can't be instantiated
try:
    Shape()
    print("ERROR: should not be able to instantiate Shape")
except TypeError as e:
    print(f"✅ ABC works: {e}")

# Test is_square
rect = Rectangle(5, 5)
print(f"\nRectangle(5,5) is_square: {rect.is_square()}")   # True
rect2 = Rectangle(4, 6)
print(f"Rectangle(4,6) is_square: {rect2.is_square()}")    # False
```

---

### D4. Vehicle Rental System (Independent Practice 1 — Full Solution)

```python
class Vehicle:
    def __init__(self, vehicle_id: str, model: str, base_rate: float):
        self.vehicle_id = vehicle_id
        self.model = model
        self.base_rate = base_rate

    def calculate_rental_cost(self, days: int) -> float:
        return self.base_rate * days

    def get_info(self) -> str:
        return f"{self.__class__.__name__} | {self.model} | ${self.base_rate}/day"


class Car(Vehicle):
    def __init__(self, vehicle_id, model, base_rate, num_passengers):
        super().__init__(vehicle_id, model, base_rate)
        self.num_passengers = num_passengers

    def calculate_rental_cost(self, days: int) -> float:
        base = super().calculate_rental_cost(days)
        if days > 7:
            base *= 0.90    # 10% discount for week+
        return base


class Truck(Vehicle):
    def __init__(self, vehicle_id, model, base_rate, payload_tons):
        super().__init__(vehicle_id, model, base_rate)
        self.payload_tons = payload_tons

    def calculate_rental_cost(self, days: int) -> float:
        base = super().calculate_rental_cost(days)
        surcharge = self.payload_tons * 50 * days
        return base + surcharge


class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, model, base_rate, engine_cc):
        super().__init__(vehicle_id, model, base_rate)
        self.engine_cc = engine_cc

    def calculate_rental_cost(self, days: int) -> float:
        base = super().calculate_rental_cost(days)
        if self.engine_cc > 600:
            base *= 1.20    # 20% premium for high-cc bikes
        return base


def generate_rental_quote(vehicles: list, days: int) -> None:
    print(f"\n{'='*50}")
    print(f"Rental Quote — {days} day(s)")
    print(f"{'='*50}")
    total = 0
    for v in vehicles:
        cost = v.calculate_rental_cost(days)
        total += cost
        print(f"  {v.get_info()}")
        print(f"    Cost for {days} days: ${cost:,.2f}")
    print(f"{'─'*50}")
    print(f"  Total: ${total:,.2f}")
    print(f"{'='*50}")


# Test
vehicles = [
    Car("C001", "Toyota Camry", 50, num_passengers=5),
    Truck("T001", "Ford F-150", 80, payload_tons=2),
    Motorcycle("M001", "Honda CBR600RR", 40, engine_cc=600),
    Motorcycle("M002", "Harley Davidson", 60, engine_cc=1200),
]

generate_rental_quote(vehicles, 3)
generate_rental_quote(vehicles, 10)   # Car gets 10% discount
```

---

## Section E — MRO Experiments

### E1. Trace the MRO Manually

```python
# For each class, predict __mro__ BEFORE running
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
class E(D, C): pass

# Predict (fill blanks):
# A.__mro__: A → object
# B.__mro__: B → ___ → object
# D.__mro__: D → ___ → ___ → ___ → object
# E.__mro__: E → ___ → ___ → ___ → ___ → object

# Now run and verify:
for cls in [A, B, C, D, E]:
    print(f"{cls.__name__}.__mro__: {[c.__name__ for c in cls.__mro__]}")
```

---

### E2. `super()` Chain Demo

```python
# This demonstrates how super() chains through the MRO

class Layer1:
    def process(self):
        print("Layer1: pre-processing")
        result = "data"
        print("Layer1: post-processing")
        return result

class Layer2(Layer1):
    def process(self):
        print("Layer2: starts")
        result = super().process()
        print(f"Layer2: got '{result}' from below")
        return result + "_L2"

class Layer3(Layer2):
    def process(self):
        print("Layer3: starts")
        result = super().process()
        print(f"Layer3: got '{result}' from below")
        return result + "_L3"

# Trace the call chain manually, then run
obj = Layer3()
final = obj.process()
print(f"\nFinal result: {final}")
```

**Trace the execution order manually:**
```
Expected output order:
1: ______________________
2: ______________________
3: ______________________
4: ______________________
5: ______________________
6: ______________________
Final: ______________________
```

---

## Section F — Mini Project: Complete Banking System

```python
"""
Complete Banking System — Day 6 Mini Project

Build the full hierarchy and demonstrate polymorphism:

1. Account (base class — from Section D1)
2. SavingsAccount(Account)
3. CurrentAccount(Account)
4. FixedDepositAccount(Account)
5. PremiumSavingsAccount(SavingsAccount):
   - Higher rate: 0.06
   - No monthly withdrawal limit
   - Minimum balance: $10,000
   - Bonus interest on balance > $100,000

6. Polymorphic functions:
   a. process_monthly_interest(accounts) → dict
   b. total_bank_funds(accounts) → float
   c. accounts_in_overdraft(accounts) → list
   d. generate_monthly_report(accounts) → str (formatted table)

7. Demonstrate:
   - Creating each account type
   - Different withdrawal rules
   - Same calculate_interest() call → different results
   - Monthly report showing all account types
"""

# PremiumSavingsAccount
class PremiumSavingsAccount(SavingsAccount):
    DEFAULT_RATE = 0.06
    MIN_BALANCE = 10000.0
    BONUS_RATE = 0.01       # extra 1% on balances > $100k

    def __init__(self, owner: str, balance: float = 0.0):
        # override SavingsAccount's minimum and rate
        super().__init__(owner, balance, interest_rate=self.DEFAULT_RATE)
        self.MINIMUM_BALANCE = self.MIN_BALANCE

    def withdraw(self, amount: float) -> float:
        # No monthly limit for premium — skip SavingsAccount's limit check
        # But still enforce minimum balance
        if self.balance - amount < self.MINIMUM_BALANCE:
            raise ValueError(
                f"Premium account minimum balance: ${self.MINIMUM_BALANCE:,.2f}"
            )
        # Skip SavingsAccount.withdraw, go straight to Account.withdraw
        return Account.withdraw(self, amount)   # careful use of explicit class

    def calculate_interest(self) -> float:
        # Base interest from SavingsAccount
        interest = super().calculate_interest()
        # Bonus interest for high balances
        if self.balance > 100000:
            bonus = self.balance * self.BONUS_RATE
            self.balance += bonus
            self._log("bonus_interest", bonus)
            interest += bonus
        return interest


# Monthly report function
def generate_monthly_report(accounts: list) -> str:
    """
    Generate a formatted monthly report.
    Must work polymorphically for all account types.
    """
    lines = [
        f"{'='*65}",
        f"  {Account.bank_name} — Monthly Report",
        f"{'─'*65}",
        f"  {'Type':<25} {'Owner':<15} {'Balance':>12} {'Interest':>10}",
        f"{'─'*65}",
    ]

    total_funds = 0
    total_interest = 0

    for acc in accounts:
        interest = acc.calculate_interest()
        total_funds += acc.get_balance()
        total_interest += interest
        lines.append(
            f"  {acc.__class__.__name__:<25} {acc.owner:<15} "
            f"${acc.get_balance():>10,.2f} ${interest:>8,.2f}"
        )

    lines += [
        f"{'─'*65}",
        f"  {'TOTALS':<40} ${total_funds:>10,.2f} ${total_interest:>8,.2f}",
        f"{'='*65}",
    ]
    return "\n".join(lines)


# Run the full demo
def run_banking_demo():
    accounts = [
        SavingsAccount("Alice", 50000),
        CurrentAccount("Bob", 20000, overdraft_limit=10000),
        FixedDepositAccount("Carol", 100000, lock_in_months=6),
        PremiumSavingsAccount("Diana", 200000),
        CurrentAccount("Eve", 5000, overdraft_limit=2000),
    ]

    print("=== Initial State ===")
    for acc in accounts:
        print(acc)

    print("\n=== Running Transactions ===")
    accounts[0].deposit(10000)      # Alice deposits
    accounts[1].withdraw(25000)     # Bob uses overdraft
    accounts[3].deposit(50000)      # Diana deposits more

    print("\n=== Monthly Report ===")
    print(generate_monthly_report(accounts))

    # Show polymorphism explicitly
    print("\n=== Overdraft Accounts ===")
    overdrawn = [a for a in accounts if a.get_balance() < 0]
    for acc in overdrawn:
        print(f"  {acc}")


if __name__ == "__main__":
    run_banking_demo()
```

---

## ✅ Answer Key

<details>
<summary>Click to reveal — attempt everything first!</summary>

### A1 Answers
```
Line 1: Toyota with 4 wheels
Line 2: Honda with 2 wheels   (Motorcycle.wheels = 2 overrides class var)
Line 3: Volvo with 4 wheels   (Truck uses Vehicle.wheels = 4)
Line 4: 2  (Motorcycle's class variable)
Line 5: 4  (Vehicle's class variable unchanged)
Line 6: True  (moto is an instance of Vehicle via inheritance)
Line 7: False (Truck is not a subclass of Motorcycle)
```

### A2 Answers
```
1st: C.__init__
2nd: B.__init__
3rd: A.__init__
4th: from_A from_B from_C
```

### A3 Answers
```
Line 1: Shape with area 0.00
Line 2: Shape with area 16.00  ← Square's area() is called! self.area() dispatches to Square
Line 3: Shape with area 78.50
Line 4: 16

Key question: Square's area() is called — because self IS a Square.
Even though describe() is defined in Shape, self.area() uses the actual object's type.
This IS polymorphism!
```

### A4 Answers
```
Line 1: E->B->C->A
Line 2: E → D → B → C → A → object
```

### A5 Answers
```
animal_show:
Dog: Woof!
Cat: Meow!
Robot: Beep!

movement_show:
Dog: runs
Cat: slinks
Robot: ERROR - 'Robot' object has no attribute 'move'
```

### B1 Fix
```python
super().__init__(name, salary)
self.language = language

# pay_details fix:
def pay_details(self):
    base = super().pay_details()   # not super().__init__!
    return f"{base} | Language: {self.language}"

# SeniorDeveloper:
super().__init__(name, salary, language)
base_details = super().pay_details()
```

### C1 Fix
```python
class Car(Vehicle):
    def __init__(self, make, model, year, doors):
        super().__init__(make, model, year)  # ← add this
        self.doors = doors
```

### C2 Fix
```python
class Shape:
    def area(self): raise NotImplementedError

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2

class Rectangle(Shape):
    def __init__(self, w, h): self.w = w; self.h = h
    def area(self): return self.w * self.h

class Triangle(Shape):
    def __init__(self, b, h): self.b = b; self.h = h
    def area(self): return 0.5 * self.b * self.h

def calculate_area(shape: Shape) -> float:
    return shape.area()   # one line — no isinstance needed
```

### C3 Fix
```python
class Car:
    def __init__(self, brand, horsepower):
        self.brand = brand
        self.engine = Engine(horsepower)   # HAS-AN engine

    def start_car(self):
        return self.engine.start()

    def drive(self):
        return f"{self.brand} driving at {self.engine.horsepower}hp"
```

### C4 Fix
```
Error: A is a parent of B. class D(A, B) requires A to come AFTER B in MRO
(a class must come after all its subclasses). Since B is a subclass of A,
B must appear before A. Writing D(A, B) tries to put A before B, violating MRO.

Fix: class D(B, A) or just class D(B) — A is already in B's MRO
```

### C5 Fix
```python
class Dog(Animal):
    def make_sound(self):
        super().make_sound()         # increments _sound_count
        return f"{self.name} says: Woof!"
```

</details>

---

## 📊 Self-Assessment Checklist

| Concept | ✅ Got it | 🔄 Need review | ❓ Confused |
|---------|-----------|---------------|------------|
| IS-A vs HAS-A distinction | | | |
| `class Child(Parent):` syntax | | | |
| `super().__init__()` — why and when | | | |
| What gets inherited (methods + class vars) | | | |
| Method overriding — extending vs replacing | | | |
| Using `super()` inside an overridden method | | | |
| `isinstance()` — inheritance-aware checking | | | |
| Duck typing — behavior not type | | | |
| Polymorphic function with any compatible object | | | |
| Single, multilevel, hierarchical inheritance | | | |
| Multiple inheritance syntax | | | |
| MRO — reading `__mro__` output | | | |
| How `super()` follows MRO (not just parent) | | | |
| Diamond inheritance — C3 resolution | | | |
| Abstract methods — enforcing contracts | | | |
| Composition as an alternative to inheritance | | | |

**Score:**
- 16/16 ✅ — Excellent! Ready for Day 7 (Dunder methods — `__len__`, `__iter__`, `__eq__`)
- 10–15 ✅ — Good. Review `super()` chaining and MRO — they're critical for Django CBVs
- < 10 ✅ — Re-do Guided Exercises 1 & 2, re-read the Account hierarchy section

---

*Day 6 Exercises Complete — Day 7: Magic Methods / Dunders — making your classes behave like Python built-ins*
