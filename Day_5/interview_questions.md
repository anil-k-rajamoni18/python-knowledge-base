# 🎯 Python Full Stack — Day 5 Interview Preparation
# Topic: OOP Fundamentals — Classes, Objects, Methods & the Four Pillars

> **How to use this file:** Attempt each answer before reading. For senior roles, study the "Depth" sections. Be ready to write code on a whiteboard or shared editor — OOP questions almost always involve live coding.

---

## 🟢 Beginner Level Questions

---

### Q1. What are the four pillars of Object-Oriented Programming? Give a one-sentence example of each.

**Answer:**

| Pillar | Definition | Example |
|--------|-----------|---------|
| **Encapsulation** | Bundling data and methods together; restricting direct access to internal state | `BankAccount` stores `_balance` privately — only `deposit()` and `withdraw()` can change it |
| **Abstraction** | Hiding implementation complexity; exposing only what the user needs | You call `account.deposit(100)` without knowing how transactions are recorded internally |
| **Inheritance** | A child class reuses and extends a parent class | `SavingsAccount(BankAccount)` inherits all bank methods and adds interest logic |
| **Polymorphism** | Different objects responding differently to the same method call | `account.calculate_interest()` works on Savings and Checking accounts but computes differently |

```python
# Quick code illustration
class Animal:                       # Base class (abstraction)
    def __init__(self, name):
        self.name = name            # encapsulation — bundled with speak()
    def speak(self): pass           # interface

class Dog(Animal):                  # inheritance
    def speak(self): return "Woof!"

class Cat(Animal):                  # inheritance
    def speak(self): return "Meow!"

animals = [Dog("Rex"), Cat("Luna")]
for a in animals:
    print(a.speak())                # polymorphism — same call, different result
# Woof!
# Meow!
```

---

### Q2. What is the difference between a class and an object (instance)?

**Answer:**
- **Class** — a blueprint/template that defines structure (attributes) and behavior (methods). It exists in memory as a type object. Created once.
- **Object (Instance)** — a concrete realization of a class. Each instance occupies its own memory and holds its own data. You can create many instances from one class.

```python
class Car:                          # class — blueprint
    def __init__(self, make, model):
        self.make = make            # instance variable
        self.model = model

car1 = Car("Toyota", "Camry")      # object 1 — instance
car2 = Car("Honda", "Civic")       # object 2 — different instance

print(car1 is car2)                 # False — different objects
print(type(car1))                   # <class '__main__.Car'>
print(isinstance(car1, Car))        # True
```

**Analogy:** `Car` is the blueprint. `car1` and `car2` are actual cars built from it. Each car has its own mileage, color, fuel — but they share the same structure.

---

### Q3. What is `__init__`? When is it called?

**Answer:**
`__init__` is Python's **instance initializer** (constructor). It's called automatically immediately after a new object is created, to set up the object's initial state.

```python
class Student:
    def __init__(self, name: str, age: int):
        # Called automatically when: s = Student("Alice", 20)
        self.name = name    # initialize instance variables
        self.age = age
        self.grades = []    # start with empty grades

s = Student("Alice", 20)
# Python internally does:
# 1. s = Student.__new__(Student)    — allocate memory
# 2. Student.__init__(s, "Alice", 20) — initialize

print(s.name)   # Alice
print(s.grades) # []
```

**Key points:**
- `__init__` does NOT create the object — `__new__` does. `__init__` sets up data.
- `__init__` does NOT return a value (`return None` implicitly)
- You can define parameters with defaults: `def __init__(self, name, age=0):`

---

### Q4. What is `self` and why does Python require it explicitly?

**Answer:**
`self` is the reference to the **current instance** being operated on. Python requires it to be declared explicitly as the first parameter of every instance method.

When you call `obj.method(arg)`, Python translates it to `ClassName.method(obj, arg)` — `self` IS `obj`.

```python
class Counter:
    def __init__(self):
        self.count = 0      # self.count = THIS counter's count

    def increment(self):
        self.count += 1     # modifies THIS specific counter

c1 = Counter()
c2 = Counter()

c1.increment()
c1.increment()

print(c1.count)     # 2 — c1's own count
print(c2.count)     # 0 — c2 unaffected

# Python internally calls: Counter.increment(c1) — self = c1
```

**Why explicit:** Python's design philosophy — "Explicit is better than implicit" (PEP 20). Other languages like Java have implicit `this`. Python makes the receiver of every method call visible in the method signature.

`self` is a **convention**, not a keyword. You could use `this`, but NEVER should.

---

### Q5. What is the difference between a class variable and an instance variable?

**Answer:**
- **Class variable** — defined inside the class but outside any method; shared by all instances; accessed via `ClassName.var` or `self.var`
- **Instance variable** — defined inside `__init__` using `self.var`; unique to each instance

```python
class Employee:
    company = "TechCorp"    # class variable — shared by ALL employees

    def __init__(self, name, salary):
        self.name = name        # instance variable — unique to this employee
        self.salary = salary    # instance variable

e1 = Employee("Alice", 80000)
e2 = Employee("Bob", 60000)

# Class variable — same for both
print(e1.company)   # TechCorp
print(e2.company)   # TechCorp

# Instance variables — different
print(e1.salary)    # 80000
print(e2.salary)    # 60000

# Changing class variable — affects ALL
Employee.company = "NewTechCorp"
print(e1.company)   # NewTechCorp
print(e2.company)   # NewTechCorp

# Assigning via instance — creates instance var (shadowing, not modifying class var)
e1.company = "StartupX"
print(e1.company)   # StartupX — e1's own instance variable
print(e2.company)   # NewTechCorp — still uses class variable
```

---

### Q6. What is the difference between `__str__` and `__repr__`?

**Answer:**
Both define string representations of an object, but for different audiences:

| | `__str__` | `__repr__` |
|-|-----------|------------|
| Audience | End users | Developers |
| Called by | `print()`, `str()` | `repr()`, REPL, `logging`, inside lists |
| Goal | Human-readable | Unambiguous, ideally recreatable |
| Fallback | Falls back to `__repr__` if not defined | Falls back to `<ClassName object at 0x...>` |

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: ${self.price:.2f}"

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price})"

p = Product("Widget", 9.99)
print(p)            # Widget: $9.99       ← __str__
print(repr(p))      # Product(name='Widget', price=9.99)  ← __repr__
print([p])          # [Product(name='Widget', price=9.99)] ← lists use __repr__
```

**Rule of thumb:** If you can only define one, define `__repr__` — `str()` falls back to it. Define `__str__` only when user-facing display needs to look different from the developer view.

---

## 🟡 Intermediate Level Questions

---

### Q7. Explain the three types of methods in Python classes: instance, class, and static.

**Answer:**

```python
class BankAccount:
    interest_rate = 0.035   # class variable

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    # ── Instance method ─────────────────────────────────────────────────
    # Receives 'self' — has access to instance AND class data
    def deposit(self, amount: float) -> float:
        self.balance += amount      # accesses instance variable
        return self.balance

    # ── Class method ────────────────────────────────────────────────────
    # Receives 'cls' — has access to class data only, not instance data
    # Used for: alternative constructors, factory methods
    @classmethod
    def create_savings(cls, owner: str) -> "BankAccount":
        account = cls(owner, 0)     # cls works with subclasses too
        account.interest_rate = cls.interest_rate + 0.01
        return account

    @classmethod
    def update_rate(cls, new_rate: float) -> None:
        cls.interest_rate = new_rate    # modifies the class variable

    # ── Static method ───────────────────────────────────────────────────
    # No 'self' or 'cls' — pure utility, logically belongs to class
    @staticmethod
    def validate_amount(amount: float) -> bool:
        return isinstance(amount, (int, float)) and amount > 0

    @staticmethod
    def format_currency(amount: float) -> str:
        return f"${amount:,.2f}"
```

**Decision flowchart:**
```
Need instance data (self.xxx)?  → Instance method
Need class data only (cls.xxx)? → @classmethod
Need neither?                   → @staticmethod
```

---

### Q8. Why is it dangerous to use a mutable object as a class variable? How do you fix it?

**Answer:**
A mutable class variable (like a list or dict) is **shared across all instances**. When one instance mutates it (`.append()`, `.update()`), ALL instances see the change — because they all reference the same object.

```python
# ❌ Dangerous
class Student:
    grades = []     # ONE list shared by ALL Student instances

    def add_grade(self, g):
        self.grades.append(g)   # modifies the shared list!

a = Student()
b = Student()
a.add_grade(90)
print(b.grades)     # [90] ← b sees a's grade! Bug!

# ✅ Fixed — each instance gets its own list
class Student:
    def __init__(self):
        self.grades = []        # new list created for each instance

    def add_grade(self, g):
        self.grades.append(g)

a = Student()
b = Student()
a.add_grade(90)
print(b.grades)     # [] ← correct: b's own empty list
```

**Why does this happen?**
`a.grades.append(g)` doesn't assign to `a.grades` — it calls a method on the existing list object. No assignment → no shadowing → the class-level list is mutated in place, visible to all.

**The key distinction:**
- `a.grades = [90]` — creates an instance variable (shadowing) → safe
- `a.grades.append(90)` — mutates the class-level list → dangerous

---

### Q9. What is the class variable shadowing trap? Show with code.

**Answer:**
When you write `self.class_var = value` inside an instance method, Python creates a **new instance variable** with the same name on that specific object. The class variable is NOT modified. Other instances still see the class variable.

```python
class Config:
    debug = False       # class variable
    log_level = "INFO"  # class variable

c1 = Config()
c2 = Config()

print(c1.debug)         # False — reads class variable
print(c2.debug)         # False — reads class variable

# Assignment via instance — creates INSTANCE variable (shadowing!)
c1.debug = True         # c1 now has its OWN debug attribute
print(c1.debug)         # True — c1's instance variable
print(c2.debug)         # False — c2 still reads class variable
print(Config.debug)     # False — class variable UNCHANGED

# Prove it with __dict__
print(c1.__dict__)      # {'debug': True} — has its own debug
print(c2.__dict__)      # {} — c2 has no instance attrs, uses class var

# To change the class variable for all instances:
Config.debug = True     # correct way
print(c1.debug)         # True — c1's instance var (shadows class var)
print(c2.debug)         # True — c2 sees the class var change
```

---

### Q10. What is `@classmethod` and when would you use it as an alternative constructor?

**Answer:**
`@classmethod` creates a method that receives the **class** (`cls`) as its first argument instead of an instance (`self`). The primary use case is **alternative constructors** — providing multiple ways to create an instance.

```python
from datetime import datetime

class Employee:
    def __init__(self, name: str, salary: float, department: str):
        self.name = name
        self.salary = salary
        self.department = department
        self.hired_date = datetime.now()

    # Alternative constructor 1: from a dict (e.g., from JSON API response)
    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        return cls(
            name=data["name"],
            salary=data["salary"],
            department=data.get("department", "General")
        )

    # Alternative constructor 2: from a CSV row
    @classmethod
    def from_csv_row(cls, row: str) -> "Employee":
        name, salary, dept = row.strip().split(",")
        return cls(name.strip(), float(salary.strip()), dept.strip())

    # Alternative constructor 3: intern with fixed salary
    @classmethod
    def create_intern(cls, name: str) -> "Employee":
        return cls(name, salary=25000.0, department="Intern")

# Usage — three ways to create an Employee
e1 = Employee("Alice", 80000, "Engineering")

e2 = Employee.from_dict({"name": "Bob", "salary": 70000, "department": "HR"})

e3 = Employee.from_csv_row("Carol, 75000, Marketing")

e4 = Employee.create_intern("Diana")
print(e4.salary)    # 25000.0
```

**Why `cls` matters:** If `SeniorEmployee(Employee)` inherits this class, calling `SeniorEmployee.create_intern("X")` returns a `SeniorEmployee` instance (not just `Employee`) because `cls` = `SeniorEmployee`. A hardcoded `Employee(...)` would break this.

---

### Q11. When would you choose `@staticmethod` over a standalone function?

**Answer:**
Use `@staticmethod` when a function:
1. **Logically belongs with the class** — it operates on the same domain
2. **Doesn't need instance or class data** — no `self`, no `cls`
3. You want it **discoverable via the class** — `BankAccount.validate_amount()`

```python
class BankAccount:
    @staticmethod
    def validate_amount(amount: float) -> bool:
        """Logically belongs to BankAccount — validating account amounts."""
        return isinstance(amount, (int, float)) and amount > 0

    @staticmethod
    def calculate_compound_interest(principal, rate, years):
        """Pure math — related to banking, no instance data needed."""
        return principal * (1 + rate) ** years

# Can be called without an instance
BankAccount.validate_amount(100)    # True
BankAccount.validate_amount(-50)    # False

# Could also be a standalone function — but grouping with class is clearer
def validate_amount(amount):        # works, but less discoverable
    return isinstance(amount, (int, float)) and amount > 0
```

**When NOT to use `@staticmethod`:**
- If you need `self` → use instance method
- If you need `cls` for subclass compatibility → use `@classmethod`
- If the function truly has no relationship to the class → just make it a standalone function

---

### Q12. What is `@property` and how does it differ from a regular attribute?

**Answer:**
`@property` turns a method into an attribute-like accessor — callers read it like a variable but get a method's computed result. It enables validation, lazy computation, and read-only attributes.

```python
class Circle:
    def __init__(self, radius: float):
        self._radius = radius       # private storage

    @property
    def radius(self) -> float:
        """Getter — called when you read circle.radius"""
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        """Setter — called when you assign circle.radius = x"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self) -> float:
        """Computed property — no setter (read-only)"""
        import math
        return math.pi * self._radius ** 2

    @property
    def diameter(self) -> float:
        return self._radius * 2

c = Circle(5)
print(c.radius)     # 5 — getter called, looks like attribute
print(c.area)       # 78.54 — computed dynamically
print(c.diameter)   # 10

c.radius = 10       # setter called with validation
# c.radius = -1     # ValueError — validation triggered
# c.area = 50       # AttributeError — no setter defined (read-only)
```

**Key benefit:** You can start with a plain attribute and later add validation via `@property` **without changing the caller's code**.

---

## 🔴 Advanced / Senior Level Questions

---

### Q13. How does Python look up attributes on an object? (Instance vs class vs MRO)

**Answer:**
Python follows a specific lookup chain for `obj.attr`:

1. **Instance `__dict__`** — check `obj.__dict__` first
2. **Class `__dict__`** — check `type(obj).__dict__` (the class)
3. **Base classes** — check parent classes in MRO order
4. **`__getattr__`** — if defined, called as a last resort

```python
class Base:
    x = "class_base"

class Child(Base):
    pass

obj = Child()
obj.x = "instance"      # set on instance

# Lookup order:
print(obj.x)            # "instance" — found in obj.__dict__ first
del obj.x               # remove instance attribute
print(obj.x)            # "class_base" — now found in Child → Base MRO

# Demonstrate with __dict__
obj.y = "instance_y"
print(obj.__dict__)     # {'y': 'instance_y'}
print(Child.__dict__)   # {'__module__': ..., '__dict__': ..., '__weakref__': ...}
print(Base.__dict__)    # {'x': 'class_base', ...}
```

**MRO (Method Resolution Order) — relevant for inheritance (Day 6):**
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

---

### Q14. What is the Singleton pattern in Python? How would you implement it?

**Answer:**
A Singleton ensures only ONE instance of a class can ever exist. Used for database connections, logging, configuration managers.

```python
# Method 1: Override __new__
class DatabaseConnection:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host="localhost", port=5432):
        if not self.__class__._initialized:
            self.host = host
            self.port = port
            self._initialized = True
            print(f"Connecting to {host}:{port}")

db1 = DatabaseConnection("prod-server", 5432)  # "Connecting to prod-server:5432"
db2 = DatabaseConnection("other-server", 3306) # No output — returns existing instance
print(db1 is db2)       # True
print(db2.host)         # prod-server (not overwritten)

# Method 2: Using a decorator (cleaner)
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class AppConfig:
    def __init__(self):
        self.debug = False
        self.database_url = "sqlite:///db.sqlite3"

config1 = AppConfig()
config2 = AppConfig()
print(config1 is config2)   # True
```

---

### Q15. Explain the difference between name mangling (`__attr`) and the `_attr` convention.

**Answer:**

| Convention | Meaning | Enforcement |
|-----------|---------|-------------|
| `_attr` | Private by convention — "don't use this outside the class" | Not enforced — just a signal |
| `__attr` | Name-mangled — Python renames it to `_ClassName__attr` | Enforced at the interpreter level |
| `__attr__` | Dunder (magic) method — part of Python's protocol | Used by Python itself |

```python
class BankAccount:
    def __init__(self, pin):
        self._balance = 1000        # private by convention
        self.__pin = pin            # name-mangled
        self.__transaction_log__ = []   # DON'T do this — looks like dunder

    def verify_pin(self, entered: int) -> bool:
        return self.__pin == entered    # accesses mangled name within class

account = BankAccount(1234)

# Single underscore — accessible (just a convention)
print(account._balance)         # 1000 — works (but you shouldn't)

# Double underscore — name mangled to _BankAccount__pin
# print(account.__pin)          # AttributeError — name doesn't exist as __pin
print(account._BankAccount__pin)# 1234 — accessible via mangled name

# Subclass limitation — name mangling prevents accidental override
class SavingsAccount(BankAccount):
    def check_pin(self, entered):
        # self.__pin would look for _SavingsAccount__pin — different name!
        return self._BankAccount__pin == entered    # must use mangled name
```

**When to use `__` (name mangling):** When you specifically want to prevent subclasses from accidentally overriding an attribute. In most cases, a single `_` convention is sufficient and less confusing.

---

### Q16. How would you implement an interface/abstract base class in Python?

**Answer:**
Python doesn't have interfaces, but the `abc` module provides `ABC` and `@abstractmethod` to enforce a contract — subclasses MUST implement abstract methods.

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Abstract base class — defines the interface all processors must implement."""

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """All subclasses must implement this."""
        ...

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        ...

    # Concrete method — shared implementation all subclasses inherit
    def validate_amount(self, amount: float) -> bool:
        return isinstance(amount, (int, float)) and amount > 0

# Cannot instantiate abstract class directly:
# p = PaymentProcessor()  # TypeError: Can't instantiate abstract class

class StripeProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} via Stripe")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"Refunding transaction {transaction_id} via Stripe")
        return True

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} via PayPal")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"Refunding via PayPal: {transaction_id}")
        return True

# Polymorphism — same interface, different implementations
processors = [StripeProcessor(), PayPalProcessor()]
for proc in processors:
    proc.process_payment(99.99)
```

---

## 📝 Quick-Fire Answers

| Question | Answer |
|----------|--------|
| What is `self`? | Reference to the current instance; Python passes it automatically |
| Is `self` a keyword? | No — it's a convention; could be any name but never should be |
| What does `__new__` do? | Allocates memory and creates the object; called before `__init__` |
| What does `__init__` return? | `None` — always. Returning anything else is a TypeError |
| Can you have multiple `__init__` methods? | No — but use default args, `*args`/`**kwargs`, or `@classmethod` alternatives |
| What's `@classmethod` first argument? | `cls` — the class itself (not an instance) |
| What's `@staticmethod` first argument? | None — no automatic first argument |
| What is `__dict__` on an instance? | Dict of instance variables for that object |
| What is `__dict__` on a class? | Dict of class-level names (methods, class vars) |
| How do you access a class variable from inside a method? | `ClassName.var` or `self.var` (but `ClassName.var` is clearer for class vars) |
| What's the risk of mutable class variables? | Shared state — mutations affect all instances |
| What does `@property` enable? | Attribute-style access with getter/setter/deleter logic |
| What's name mangling? | `__attr` becomes `_ClassName__attr` — prevents accidental subclass override |

---

## 🧠 Behavioral / Scenario Questions

### "Design a class for a system that tracks the number of objects created."

**Model answer:**
```python
class TrackedObject:
    _count = 0

    def __init__(self, name):
        TrackedObject._count += 1
        self.name = name
        self.id = TrackedObject._count

    @classmethod
    def get_count(cls) -> int:
        return cls._count

    def __del__(self):
        TrackedObject._count -= 1
        print(f"Object '{self.name}' destroyed. Remaining: {TrackedObject._count}")

a = TrackedObject("Alpha")
b = TrackedObject("Beta")
print(TrackedObject.get_count())    # 2
del a
print(TrackedObject.get_count())    # 1
```

### "When would you use `@staticmethod` over a module-level function?"

**Model answer:** "When the function logically belongs to the class's domain and I want it to be discoverable via the class namespace — like `BankAccount.validate_amount()` or `Temperature.is_valid_celsius()`. If other developers see the class, they should be able to find related utilities there. However, if the function is completely general-purpose with no semantic connection to the class, a module-level function in a `utils.py` file is better."

### "You notice a bug where modifying one user's preferences affects all users. What's the likely cause?"

**Model answer:** "Almost certainly a mutable class variable — something like `preferences = {}` defined at the class level, shared by all instances. The fix is to move it into `__init__`: `self.preferences = {}`. I'd check `User.__dict__` vs `user_instance.__dict__` to confirm — if `preferences` appears in the class dict and not the instance dict, that's the bug."

---

*End of Day 5 Interview Prep — Day 6 will add: Inheritance, `super()`, MRO, abstract classes, dataclasses, magic methods*
