# 🎯 Python Full Stack — Day 6 Interview Preparation
# Topic: Inheritance & Polymorphism

> **How to use:** Attempt each answer before revealing. OOP interviews almost always involve writing code live — practise writing these examples from memory.

---

## 🟢 Beginner Level Questions

---

### Q1. What is inheritance in Python? Why do we use it?

**Answer:**
Inheritance allows a class (child) to acquire attributes and methods from another class (parent). The child can use the parent's code directly and can add new features or change existing behavior.

**Why we use it:**
- **Code reuse** — write shared logic once in the parent
- **IS-A modeling** — `SavingsAccount` IS-A `Account`; `Dog` IS-A `Animal`
- **Extensibility** — add new behavior without modifying existing code
- **Polymorphism** — treat different types uniformly through a shared interface

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        return f"{self.name} is eating."

class Dog(Animal):              # Dog inherits from Animal
    def bark(self):
        return f"{self.name} barks!"

d = Dog("Rex")
print(d.eat())      # Rex is eating.  ← inherited from Animal
print(d.bark())     # Rex barks!      ← Dog's own method
```

---

### Q2. What is `super()` and why should you use it?

**Answer:**
`super()` returns a proxy object that delegates method calls to the parent class, following the MRO. It's used most commonly in `__init__` to call the parent's constructor.

```python
class Account:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

class SavingsAccount(Account):
    def __init__(self, owner, balance, interest_rate):
        super().__init__(owner, balance)    # ← calls Account.__init__
        self.interest_rate = interest_rate   # only what's new

acc = SavingsAccount("Alice", 1000, 0.04)
print(acc.owner)    # Alice — set by Account.__init__ via super()
```

**Why `super()` over `Account.__init__(self, ...)`:**
1. Respects MRO in multiple inheritance — doesn't skip intermediate classes
2. If you rename the parent, code still works
3. Industry standard — Django, Python stdlib all use `super()`

---

### Q3. What is method overriding? Give an example.

**Answer:**
Method overriding is when a child class defines a method with the same name as one in the parent, replacing or extending the parent's implementation.

```python
class Account:
    def withdraw(self, amount):
        self.balance -= amount
        return self.balance

class SavingsAccount(Account):
    MIN_BALANCE = 1000

    def withdraw(self, amount):     # OVERRIDES Account.withdraw
        if self.balance - amount < self.MIN_BALANCE:
            raise ValueError("Would fall below minimum balance")
        return super().withdraw(amount)  # calls parent after check
```

**Two types:**
- **Extending** — call `super().method()` then add extra logic
- **Replacing** — completely new implementation, no `super()` call

---

### Q4. What is the difference between `isinstance()` and `type()`?

**Answer:**

```python
class Animal: pass
class Dog(Animal): pass

d = Dog()

print(type(d) == Dog)       # True  — exact type check
print(type(d) == Animal)    # False — NOT Animal (even though Dog inherits)

print(isinstance(d, Dog))   # True  — d is a Dog
print(isinstance(d, Animal))# True  — d IS ALSO an Animal (inheritance-aware)
```

**Key difference:** `isinstance()` understands inheritance. `type() ==` checks the **exact** class only.

**Rule:** Always use `isinstance()` in professional code. `type() ==` breaks polymorphism.

---

### Q5. What does it mean for Python to use "duck typing"?

**Answer:**
Duck typing means Python doesn't check an object's type before calling a method — it just checks if the object **has** the method. "If it walks like a duck and quacks like a duck, it's a duck."

```python
class Dog:
    def speak(self): return "Woof!"

class Cat:
    def speak(self): return "Meow!"

class Robot:
    def speak(self): return "Beep boop."

# No common parent needed — duck typing!
def make_noise(thing):
    print(thing.speak())    # works for anything with .speak()

make_noise(Dog())    # Woof!
make_noise(Cat())    # Meow!
make_noise(Robot())  # Beep boop.
```

This is why Python is flexible — you don't need interfaces or formal type hierarchies to achieve polymorphism.

---

### Q6. What is polymorphism? How does Python achieve it?

**Answer:**
Polymorphism means "many forms" — the same method name works differently depending on the object it's called on.

Python achieves it through:
1. **Method overriding** — child classes redefine parent methods
2. **Duck typing** — any object with the right method works

```python
class Shape:
    def area(self): return 0

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2

class Rectangle(Shape):
    def __init__(self, w, h): self.w = w; self.h = h
    def area(self): return self.w * self.h

# Polymorphic function
def total_area(shapes):
    return sum(s.area() for s in shapes)  # same call → different result

shapes = [Circle(5), Rectangle(4, 6), Circle(3)]
print(total_area(shapes))   # works for any mix of shapes
```

---

## 🟡 Intermediate Level Questions

---

### Q7. Explain the types of inheritance in Python with examples.

**Answer:**

```python
# 1. Single — one parent, one child
class Account: pass
class SavingsAccount(Account): pass

# 2. Multilevel — chain
class Account: pass
class SavingsAccount(Account): pass
class PremiumSavings(SavingsAccount): pass  # grandchild

# 3. Hierarchical — one parent, multiple children
class Account: pass
class Savings(Account): pass
class Current(Account): pass
class FixedDeposit(Account): pass

# 4. Multiple — one child, multiple parents
class Flyable: pass
class Swimmable: pass
class Duck(Flyable, Swimmable): pass   # inherits from both

# 5. Hybrid — combination
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass   # multiple + hierarchical + diamond
```

---

### Q8. What is MRO (Method Resolution Order)? How does Python calculate it?

**Answer:**
MRO defines the order Python searches classes when looking for a method. Python uses the **C3 Linearization algorithm** which ensures:
- A class always comes before its parents
- Left-to-right order of parents is respected
- No class appears twice

```python
class A:
    def method(self): return "A"

class B(A):
    def method(self): return "B"

class C(A):
    def method(self): return "C"

class D(B, C):
    pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

print(D().method())  # "B" — B is first in MRO after D

# How to check MRO at any time:
print(D.mro())   # returns list of classes in order
```

**Practical rule:** Python searches left to right, skipping classes already covered. Depth first, but adjusted by C3 to handle diamonds properly.

---

### Q9. What is the diamond problem? How does Python solve it?

**Answer:**
The diamond problem occurs in multiple inheritance when a class inherits from two classes that share a common ancestor:

```
    A
   / \
  B   C
   \ /
    D
```

Without a rule, it's ambiguous: if B and C both override A's method, which does D use?

Python solves it with MRO (C3 Linearization):

```python
class A:
    def greet(self): return "Hello from A"

class B(A):
    def greet(self): return f"B: {super().greet()}"

class C(A):
    def greet(self): return f"C: {super().greet()}"

class D(B, C):
    pass

print(D().greet())   # B: C: Hello from A
# MRO: D → B → C → A → object
# super() in B doesn't go to A — it goes to C (next in MRO)
# This is the key insight: super() follows MRO, not the inheritance diagram
```

---

### Q10. What is the Liskov Substitution Principle?

**Answer:**
LSP states: wherever a parent class is expected, a subclass should be substitutable without breaking the program. The subclass must honor the parent's contract.

```python
# ✅ Follows LSP — SavingsAccount can be used anywhere Account is expected
class Account:
    def withdraw(self, amount): ...

class SavingsAccount(Account):
    def withdraw(self, amount):
        # adds a constraint but still performs withdrawal
        if amount > self.balance * 0.5:
            raise ValueError("Can't withdraw more than 50% at once")
        return super().withdraw(amount)

# ❌ Violates LSP — child REMOVES behavior the parent guarantees
class LockedAccount(Account):
    def withdraw(self, amount):
        raise RuntimeError("This account type cannot withdraw!")
        # Code expecting Account.withdraw to work will break with LockedAccount
```

**In Django context:** Every Django `ModelForm` is a `Form`, so any code using `Form` works with `ModelForm` — LSP in action.

---

### Q11. How does `super()` work in multiple inheritance?

**Answer:**
`super()` doesn't just call the "immediate parent" — it calls the **next class in the MRO**. This enables "cooperative multiple inheritance" where each class in the chain can participate.

```python
class LogMixin:
    def save(self):
        print("LogMixin: logging before save")
        super().save()                  # calls next in MRO (not LogMixin's parent)

class ValidateMixin:
    def save(self):
        print("ValidateMixin: validating before save")
        super().save()                  # calls next in MRO

class BaseModel:
    def save(self):
        print("BaseModel: actually saving to database")

class Product(LogMixin, ValidateMixin, BaseModel):
    pass

p = Product()
p.save()
# LogMixin: logging before save
# ValidateMixin: validating before save
# BaseModel: actually saving to database

print(Product.__mro__)
# Product → LogMixin → ValidateMixin → BaseModel → object
```

**Django uses this exact pattern** for Class-Based Views with mixins.

---

### Q12. When should you use composition instead of inheritance?

**Answer:**
Use **inheritance** for IS-A relationships. Use **composition** for HAS-A relationships.

```python
# IS-A → Inheritance ✅
class Animal: pass
class Dog(Animal): pass   # Dog IS-A Animal

# HAS-A → Composition ✅
class Engine:
    def start(self): return "Vroom!"

class Car:
    def __init__(self):
        self.engine = Engine()   # Car HAS-AN Engine

    def start(self):
        return self.engine.start()

# ❌ Wrong — Car is NOT an Engine
class Car(Engine): pass
```

**Signs you're using inheritance incorrectly:**
- The child class never uses some inherited methods
- You're using inheritance just for code reuse, not IS-A
- You have to override methods to raise `NotImplementedError` to "block" them

**Rule of thumb:** "Favour composition over inheritance" — GoF Design Patterns

---

## 🔴 Advanced / Senior Level Questions

---

### Q13. How would you implement an abstract class in Python? Why use it?

**Answer:**
Python's `abc` module provides `ABC` and `@abstractmethod` to create abstract classes — classes that define an interface but can't be instantiated directly.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class — enforces a contract."""

    @abstractmethod
    def area(self) -> float:
        """Every subclass MUST implement this."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    # Concrete method — shared by all shapes
    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}"

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2
    def perimeter(self): return 2 * 3.14 * self.r

# Shape()   → TypeError: Can't instantiate abstract class
# Circle()  → Works
# If Circle doesn't implement area() → TypeError at instantiation
```

**Why use ABC over just `raise NotImplementedError`:**
- ABC prevents instantiation of the base class itself
- Missing implementation is caught at **class creation time**, not at runtime
- Clearer documentation of the interface contract
- Compatible with `isinstance()` checking

---

### Q14. Explain cooperative multiple inheritance with a practical example.

**Answer:**
Cooperative multiple inheritance uses `super()` consistently in all classes, allowing each class in the MRO chain to participate in the method call. It's called "cooperative" because every class cooperates by calling `super()`.

```python
class TimestampMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # pass args up the chain
        from datetime import datetime
        self.created_at = datetime.now()

class ValidationMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # pass args up the chain
        self._is_valid = False

    def validate(self):
        self._is_valid = True
        return self

class BaseModel:
    def __init__(self, name):
        self.name = name

    def save(self):
        return f"Saving {self.name}..."

class User(TimestampMixin, ValidationMixin, BaseModel):
    def __init__(self, name, email):
        super().__init__(name)              # cooperative: passes name up
        self.email = email

u = User("Alice", "alice@example.com")
print(u.name)           # Alice       ← from BaseModel
print(u.created_at)     # datetime    ← from TimestampMixin
print(u._is_valid)      # False       ← from ValidationMixin
print(u.validate().save())  # Saving Alice...
```

**Key:** Every class uses `*args, **kwargs` in `__init__` to pass unrecognized arguments up the chain. This is the Django mixin pattern.

---

### Q15. How does Python's `__init_subclass__` work?

**Answer:**
`__init_subclass__` is called on the base class every time a new subclass is created. It's useful for registering subclasses, enforcing constraints, or auto-configuring child classes.

```python
class PluginBase:
    _registry: dict = {}

    def __init_subclass__(cls, plugin_name: str = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            PluginBase._registry[plugin_name] = cls
            print(f"Registered plugin: {plugin_name}")

class CSVExporter(PluginBase, plugin_name="csv"):
    def export(self, data): return "CSV output"

class JSONExporter(PluginBase, plugin_name="json"):
    def export(self, data): return "JSON output"

# Plugin system!
print(PluginBase._registry)
# {'csv': <class 'CSVExporter'>, 'json': <class 'JSONExporter'>}

exporter = PluginBase._registry["json"]()
print(exporter.export([1, 2, 3]))   # JSON output
```

Django uses `__init_subclass__` internally for model registration and app discovery.

---

## 📝 Quick-Fire Answers

| Question | Answer |
|----------|--------|
| What keyword defines inheritance? | `class Child(Parent):` |
| What does `super()` return? | A proxy object for the next class in the MRO |
| What is `__mro__`? | Attribute listing the class lookup order |
| Can a Python class inherit from multiple parents? | Yes — `class D(B, C):` |
| What method does ABC add to enforce implementation? | `@abstractmethod` |
| What does `isinstance(obj, Parent)` return for a child object? | `True` |
| What is duck typing? | Calling a method based on its presence, not the object's type |
| What algorithm does Python use for MRO? | C3 Linearization |
| What is a mixin? | A small class designed to add one feature via multiple inheritance |
| What is LSP? | Subclasses must be substitutable wherever the parent is used |
| Is calling `super()` in `__init__` required? | Yes, if the parent sets attributes the child needs |
| What happens if you don't call `super().__init__()` in the child? | Parent's attributes are never set — AttributeError at runtime |

---

## 🧠 Behavioral / Scenario Questions

### "Design a class hierarchy for a ride-sharing app (Uber-like)."

**Model answer structure:**
```python
class Vehicle:          # base — make, model, license_plate
class Car(Vehicle):     # 4 seats, standard rate
class SUV(Vehicle):     # 7 seats, higher rate
class Moto(Vehicle):    # 1 seat, budget rate

class Driver:           # driver info, rating
class Ride:             # vehicle, driver, distance, calculate_fare() → polymorphic
```
- `Car.calculate_fare()` → base rate × distance
- `SUV.calculate_fare()` → premium rate × distance + surcharge
- `Moto.calculate_fare()` → discount rate × distance

### "You're reviewing a PR and see `class JSONLogger(dict)`. What would you say?"

**Model answer:** "I'd flag this as an inheritance misuse. `JSONLogger` is NOT a dictionary — it HAS data it wants to store as JSON. Using `dict` as a parent gives JSONLogger all dict methods (`__getitem__`, `pop`, `keys`, etc.) that are irrelevant and potentially confusing. I'd refactor to composition: `self._store = {}` inside `JSONLogger`. This is a classic HAS-A vs IS-A mistake."

### "How would you add a new account type without changing existing code?"

**Model answer:** "That's the Open/Closed Principle combined with polymorphism. I'd create a new subclass of `Account`, override `calculate_interest()` and `withdraw()` with the new rules, and the existing `process_monthly_interest(accounts)` function would handle it automatically — no changes needed. This is the real power of polymorphic design: the function is closed for modification but open for extension."

---

*End of Day 6 Interview Prep — Day 7: Dunder/Magic Methods — `__len__`, `__iter__`, `__eq__`, `__add__`, making custom classes behave like Python built-ins*
