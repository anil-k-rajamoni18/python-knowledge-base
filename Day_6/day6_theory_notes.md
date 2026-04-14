# 🐍 Python Full Stack — Day 6 of 35
# Topic: Inheritance & Polymorphism
## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, learners will be able to:
- Create class hierarchies using inheritance and explain what a child class inherits from a parent
- Use `super()` correctly in constructors and overridden methods
- Override parent methods to change or extend behavior in child classes
- Write polymorphic code — one function that works with multiple types
- Read and understand Method Resolution Order (MRO) for any class hierarchy

### 📋 Prerequisites (Days 1–5 Review)
- Python data types, functions, loops (Days 1–3)
- Modules and packages (Day 4)
- OOP fundamentals — classes, objects, `__init__`, instance/class variables, all three method types (Day 5)

### 🔗 Connection to the Full Stack Journey
- **Django Models (Day 20+):** `class Product(models.Model)` — your model IS inheriting from Django's `Model` class. Every Django model you write uses inheritance
- **Django Class-Based Views (Day 21+):** `class ProductListView(ListView)` — CBVs are built entirely on multi-level inheritance chains
- **Django Forms (Day 22+):** `class ContactForm(forms.Form)` — form classes inherit validation, rendering, and cleaning logic
- **REST Framework (Day 24+):** `class ProductSerializer(serializers.ModelSerializer)` — serializer classes use deep inheritance
- **Decorators & Mixins (Day 8):** Mixins are small classes designed specifically for multiple inheritance — you'll write them daily in Django

---

## 2. Concept Explanation

### 2.1 Inheritance — Why It Exists

**The "Why":** Imagine you're building a banking app. You have `SavingsAccount`, `CurrentAccount`, and `FixedDepositAccount`. All three have an `owner`, `balance`, `deposit()`, and `withdraw()`. Without inheritance, you'd write that shared code three times — three places to update when a bug is found, three places to keep in sync.

Inheritance solves this: write the shared code **once** in a parent class, and all child classes get it for free.

> **Core idea:** Inheritance is about **"is-a" relationships.**
> - A `SavingsAccount` **is a** type of `Account`
> - A `Dog` **is a** type of `Animal`
> - A `Circle` **is a** type of `Shape`
>
> If you can say "B is a type of A," inheritance is appropriate.

**Terminology — all these mean the same thing:**
| Term 1 | Term 2 | Term 3 |
|--------|--------|--------|
| Parent class | Base class | Superclass |
| Child class | Derived class | Subclass |

**Analogy:** Think of a job offer letter template. The company has a standard template (parent class) with common sections — company name, date, salary format. Each department then creates their own version (child class) — Engineering adds a tech stack section, Sales adds commission structure. The standard template is written once; departments only write what's new or different.

---

### 2.2 The `super()` Function

**The "Why":** When a child class overrides `__init__`, it takes over completely — the parent's `__init__` no longer runs automatically. If the parent sets up important attributes (like `owner` and `balance`), the child needs to call the parent's `__init__` too. `super()` is how you do this without hardcoding the parent's name.

```python
# Without super() — fragile, duplicated code
class SavingsAccount(Account):
    def __init__(self, owner, balance):
        self.owner = owner      # duplicated from Account!
        self.balance = balance  # duplicated from Account!
        self.interest_rate = 0.04

# With super() — DRY, maintainable
class SavingsAccount(Account):
    def __init__(self, owner, balance):
        super().__init__(owner, balance)   # call parent's __init__
        self.interest_rate = 0.04          # add only what's new
```

**Why `super()` over `Account.__init__(self, owner, balance)`?**
- `super()` respects the MRO (important in multiple inheritance)
- If you rename the parent class, `super()` still works — hardcoded name breaks
- Django and professional code always uses `super()`

---

### 2.3 Method Overriding

**The "Why":** Child classes inherit all parent methods, but sometimes they need to behave differently. Overriding lets a child class **redefine** an inherited method with its own implementation.

**Two flavors:**
1. **Replacing** — the child completely replaces the parent's logic
2. **Extending** — the child calls the parent's logic first, then adds more (`super().method()`)

**Real example:**
- `Account.withdraw(amount)` — basic withdrawal, just subtracts
- `SavingsAccount.withdraw(amount)` — extends: checks minimum balance limit first, THEN does the withdrawal
- `CurrentAccount.withdraw(amount)` — replaces: allows overdraft (can go negative), completely different logic

---

### 2.4 Polymorphism — One Interface, Many Forms

**The "Why":** "Polymorphism" means "many forms." In Python, it means you can write code that works with any object that has a certain method — without knowing or caring about the exact class.

**Analogy:** Think of a universal TV remote. The "Volume Up" button works whether you're watching Netflix, a DVD, or cable TV. The button is the same interface; each device responds differently underneath. The remote doesn't know or care how the device implements "volume up."

**Two types of polymorphism in Python:**

1. **Method overriding polymorphism:** Different child classes override the same method differently. You can call `account.calculate_interest()` on ANY account object and it does the right thing for that account type.

2. **Duck typing:** Python doesn't check the class — it checks whether the object has the method. "If it quacks like a duck, it's a duck." A function that calls `.area()` works for `Circle`, `Rectangle`, or any object with an `.area()` method — no inheritance required.

---

### 2.5 Types of Inheritance

| Type | Description | Example |
|------|-------------|---------|
| **Single** | One parent, one child | `SavingsAccount(Account)` |
| **Multilevel** | Chain: A → B → C | `FixedDepositAccount(SavingsAccount(Account))` |
| **Hierarchical** | One parent, multiple children | `Account` → `Savings`, `Current`, `Fixed` |
| **Multiple** | One child, multiple parents | `class C(A, B)` |
| **Hybrid** | Combination of the above | Django CBVs use this |

---

### 2.6 Method Resolution Order (MRO)

**The "Why":** In multiple inheritance, when Python looks for a method, it needs a rule for which class to check first. The MRO defines this lookup order.

Python uses the **C3 Linearization algorithm** — it guarantees:
1. A class always appears before its parents
2. The order of parents (left to right) is respected
3. No class appears twice

For `class D(B, C)` where both `B` and `C` inherit from `A`:
```
MRO: D → B → C → A → object
```

**Simple rule to remember:** Python searches left to right, depth first, but respects the C3 algorithm to handle diamonds.

---

## 3. Syntax & Code Examples

### 3.1 Basic Inheritance

```python
# ── Parent class ────────────────────────────────────────────────────────────
class Animal:
    """Base class for all animals."""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def eat(self) -> str:
        return f"{self.name} is eating."

    def sleep(self) -> str:
        return f"{self.name} is sleeping."

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, age={self.age})"


# ── Child class — inherits everything from Animal ─────────────────────────
class Dog(Animal):
    """Dog IS-A Animal. Inherits eat() and sleep()."""

    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)     # call parent's __init__ FIRST
        self.breed = breed              # add what's new for Dog

    def bark(self) -> str:              # new method — only Dogs have this
        return f"{self.name} says: Woof!"

    def fetch(self, item: str) -> str:
        return f"{self.name} fetched the {item}!"


class Cat(Animal):
    """Cat IS-A Animal."""

    def __init__(self, name: str, age: int, indoor: bool = True):
        super().__init__(name, age)
        self.indoor = indoor

    def meow(self) -> str:
        return f"{self.name} says: Meow!"


# ── Using the classes ────────────────────────────────────────────────────────
rex = Dog("Rex", 3, "German Shepherd")
luna = Cat("Luna", 2)

# Inherited methods work on child instances
print(rex.eat())        # Rex is eating.      ← inherited from Animal
print(rex.sleep())      # Rex is sleeping.    ← inherited from Animal
print(rex.bark())       # Rex says: Woof!     ← Dog-specific

print(luna.eat())       # Luna is eating.     ← inherited from Animal
print(luna.meow())      # Luna says: Meow!    ← Cat-specific

# isinstance() understands inheritance
print(isinstance(rex, Dog))     # True  — rex is a Dog
print(isinstance(rex, Animal))  # True  — rex is ALSO an Animal!
print(isinstance(rex, Cat))     # False — rex is not a Cat

# issubclass() checks class hierarchy
print(issubclass(Dog, Animal))  # True
print(issubclass(Cat, Animal))  # True
print(issubclass(Dog, Cat))     # False

print(rex)      # Dog(name='Rex', age=3)  ← inherited __str__ uses self.__class__.__name__
```

---

### 3.2 `super()` — All Use Cases

```python
class Vehicle:
    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year
        self._speed = 0

    def start(self) -> str:
        return f"{self.make} {self.model} engine started."

    def accelerate(self, amount: int) -> str:
        self._speed += amount
        return f"Speed: {self._speed} km/h"

    def describe(self) -> str:
        return f"{self.year} {self.make} {self.model}"


class ElectricVehicle(Vehicle):
    def __init__(self, make: str, model: str, year: int, battery_kwh: float):
        # super().__init__ sets make, model, year — we don't repeat them
        super().__init__(make, model, year)
        self.battery_kwh = battery_kwh      # EV-specific attribute
        self._charge_level = 100            # starts fully charged

    # ── Extending parent method (calling super() + adding more) ───────────
    def start(self) -> str:
        parent_result = super().start()     # get parent's behavior
        return f"{parent_result} (silently, it's electric)"

    # ── Replacing parent method entirely ─────────────────────────────────
    def accelerate(self, amount: int) -> str:
        # EVs drain battery when accelerating — completely different behavior
        drain = amount * 0.01
        self._charge_level -= drain
        self._speed += amount
        return f"Speed: {self._speed} km/h | Battery: {self._charge_level:.1f}%"

    # ── New method unique to EV ──────────────────────────────────────────
    def charge(self, kwh: float) -> str:
        self._charge_level = min(100, self._charge_level + (kwh / self.battery_kwh * 100))
        return f"Charged to {self._charge_level:.1f}%"

    # ── Extending describe() ─────────────────────────────────────────────
    def describe(self) -> str:
        base = super().describe()           # reuse parent's description
        return f"{base} | Electric | {self.battery_kwh}kWh battery"


# Test
tesla = ElectricVehicle("Tesla", "Model 3", 2023, 75.0)

print(tesla.start())
# Tesla Model 3 engine started. (silently, it's electric)

print(tesla.accelerate(60))
# Speed: 60 km/h | Battery: 99.4%

print(tesla.describe())
# 2023 Tesla Model 3 | Electric | 75.0kWh battery
```

---

### 3.3 Complete Account Hierarchy

```python
from datetime import datetime, date
from typing import Optional


class Account:
    """
    Base class for all bank account types.
    Contains shared logic: owner, balance, deposit, basic withdraw.
    """
    bank_name: str = "Python National Bank"

    def __init__(self, owner: str, balance: float = 0.0):
        if not owner.strip():
            raise ValueError("Owner name cannot be empty")
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.owner = owner.strip()
        self.balance = balance
        self.account_number = id(self) % 100000     # simple unique ID
        self._transactions: list[dict] = []
        self.created_date = date.today()

    # ── Shared methods — all accounts have these ─────────────────────────

    def deposit(self, amount: float) -> float:
        """Deposit money. Returns new balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self._log("deposit", amount)
        return self.balance

    def withdraw(self, amount: float) -> float:
        """Base withdrawal — no overdraft, no minimum balance check."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError(f"Insufficient funds: balance={self.balance:.2f}")
        self.balance -= amount
        self._log("withdrawal", amount)
        return self.balance

    def get_balance(self) -> float:
        return self.balance

    def get_statement(self) -> str:
        lines = [
            f"{'='*50}",
            f"  {self.bank_name}",
            f"  {self.__class__.__name__} — #{self.account_number}",
            f"  Owner: {self.owner}",
            f"  Balance: ${self.balance:,.2f}",
            f"{'─'*50}",
        ]
        for tx in self._transactions[-5:]:
            sign = "+" if tx["type"] == "deposit" else "-"
            lines.append(f"  {tx['date']}  {sign}${tx['amount']:,.2f}  ({tx['type']})")
        lines.append(f"{'='*50}")
        return "\n".join(lines)

    # ── Abstract-like method — child classes should override this ─────────
    def calculate_interest(self) -> float:
        """Base accounts earn no interest. Override in subclasses."""
        return 0.0

    def _log(self, tx_type: str, amount: float) -> None:
        self._transactions.append({
            "type": tx_type,
            "amount": round(amount, 2),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "balance_after": round(self.balance, 2)
        })

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"owner={self.owner!r}, balance={self.balance:.2f})")

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}] {self.owner}: ${self.balance:,.2f}"


# ── SavingsAccount ──────────────────────────────────────────────────────────
class SavingsAccount(Account):
    """
    Savings account with interest and withdrawal limits.
    IS-A Account with additional rules.
    """
    DEFAULT_INTEREST_RATE = 0.04    # 4% annually
    MINIMUM_BALANCE = 1000.0
    MAX_WITHDRAWALS_PER_MONTH = 3

    def __init__(self, owner: str, balance: float = 0.0,
                 interest_rate: float = DEFAULT_INTEREST_RATE):
        super().__init__(owner, balance)    # parent sets owner, balance
        self.interest_rate = interest_rate  # SavingsAccount-specific
        self._monthly_withdrawals = 0

    def withdraw(self, amount: float) -> float:
        """
        OVERRIDES parent withdraw.
        Extends with: minimum balance check, monthly withdrawal limit.
        """
        # Check monthly limit
        if self._monthly_withdrawals >= self.MAX_WITHDRAWALS_PER_MONTH:
            raise ValueError(
                f"Monthly withdrawal limit ({self.MAX_WITHDRAWALS_PER_MONTH}) reached"
            )
        # Check minimum balance requirement
        if self.balance - amount < self.MINIMUM_BALANCE:
            raise ValueError(
                f"Cannot withdraw: balance would fall below "
                f"minimum of ${self.MINIMUM_BALANCE:,.2f}"
            )
        # Call parent's withdraw logic (the actual subtraction + logging)
        result = super().withdraw(amount)
        self._monthly_withdrawals += 1
        return result

    def calculate_interest(self) -> float:
        """OVERRIDES base. Savings accounts earn interest."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        self._log("interest", interest)
        return interest

    def reset_monthly_withdrawals(self) -> None:
        """Call at start of each month."""
        self._monthly_withdrawals = 0


# ── CurrentAccount ──────────────────────────────────────────────────────────
class CurrentAccount(Account):
    """
    Current/Checking account with overdraft facility.
    No interest. Suitable for frequent transactions.
    """
    def __init__(self, owner: str, balance: float = 0.0,
                 overdraft_limit: float = 5000.0):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit  # can go this much negative

    def withdraw(self, amount: float) -> float:
        """
        OVERRIDES parent withdraw.
        REPLACES behavior: allows overdraft up to the limit.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        # Instead of checking balance, check balance + overdraft limit
        if amount > self.balance + self.overdraft_limit:
            raise ValueError(
                f"Exceeds overdraft limit: available=${self.balance + self.overdraft_limit:,.2f}"
            )
        self.balance -= amount
        self._log("withdrawal", amount)
        if self.balance < 0:
            print(f"⚠️  Warning: Account is in overdraft (${self.balance:,.2f})")
        return self.balance

    def calculate_interest(self) -> float:
        """OVERRIDES base. Current accounts earn NO interest."""
        return 0.0  # explicitly returns 0 — no-interest account

    @property
    def available_balance(self) -> float:
        """Total available including overdraft."""
        return self.balance + self.overdraft_limit


# ── FixedDepositAccount ─────────────────────────────────────────────────────
class FixedDepositAccount(Account):
    """
    Fixed deposit account with lock-in period and higher interest.
    Cannot withdraw during lock-in period.
    """
    DEFAULT_INTEREST_RATE = 0.075   # 7.5% — higher than savings

    def __init__(self, owner: str, principal: float,
                 lock_in_months: int = 12,
                 interest_rate: float = DEFAULT_INTEREST_RATE):
        if principal <= 0:
            raise ValueError("Fixed deposit requires a positive principal")
        super().__init__(owner, principal)
        self.lock_in_months = lock_in_months
        self.interest_rate = interest_rate
        self.maturity_date = self._calculate_maturity()
        self._is_mature = False

    def _calculate_maturity(self) -> date:
        from dateutil.relativedelta import relativedelta
        try:
            from dateutil.relativedelta import relativedelta
            return date.today() + relativedelta(months=self.lock_in_months)
        except ImportError:
            # fallback without dateutil
            month = date.today().month + self.lock_in_months
            year = date.today().year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            return date(year, month, date.today().day)

    def withdraw(self, amount: float) -> float:
        """
        OVERRIDES parent withdraw.
        RESTRICTS behavior: cannot withdraw before maturity.
        """
        if date.today() < self.maturity_date:
            days_remaining = (self.maturity_date - date.today()).days
            raise ValueError(
                f"Fixed deposit locked until {self.maturity_date} "
                f"({days_remaining} days remaining)"
            )
        return super().withdraw(amount)     # after maturity, normal withdraw

    def calculate_interest(self) -> float:
        """OVERRIDES base. Fixed deposits earn higher interest."""
        # Simple interest for the lock-in period
        interest = (self.balance * self.interest_rate * self.lock_in_months) / 12
        self.balance += interest
        self._log("maturity interest", interest)
        self._is_mature = True
        return interest

    def get_maturity_value(self) -> float:
        """Preview how much you'll get at maturity."""
        interest = (self.balance * self.interest_rate * self.lock_in_months) / 12
        return self.balance + interest


# ── Polymorphism in action ──────────────────────────────────────────────────
def process_monthly_interest(accounts: list) -> None:
    """
    Polymorphic function — calls calculate_interest() on ANY account type.
    Doesn't know or care which account type each object is.
    """
    print("\n📊 Monthly Interest Processing")
    print("─" * 40)
    for account in accounts:
        interest = account.calculate_interest()     # ← POLYMORPHIC CALL
        if interest > 0:
            print(f"{account.owner} ({account.__class__.__name__}): "
                  f"+${interest:.2f} interest earned")
        else:
            print(f"{account.owner} ({account.__class__.__name__}): "
                  f"No interest (type doesn't earn interest)")


# ── Demo ─────────────────────────────────────────────────────────────────────
savings = SavingsAccount("Alice", 50000, interest_rate=0.04)
current = CurrentAccount("Bob", 10000, overdraft_limit=5000)
fixed = FixedDepositAccount("Carol", 100000, lock_in_months=12)

# All support deposit — inherited from Account
savings.deposit(5000)
current.deposit(2000)

# All support withdraw — each with their own rules
savings.withdraw(2000)  # limited by minimum balance + monthly limit
current.withdraw(12000) # uses overdraft: 10000 + 2000 deposited = 12000 available
                        # ⚠️ Warning: Account is in overdraft

try:
    fixed.withdraw(10000)   # will raise ValueError (locked)
except ValueError as e:
    print(f"FD Withdrawal blocked: {e}")

# Polymorphism: same function works for all account types
all_accounts = [savings, current, fixed]
process_monthly_interest(all_accounts)

# Print statements use inherited __str__
for acc in all_accounts:
    print(acc)

# Output:
# [SavingsAccount] Alice: $52,200.00   (with interest applied)
# [CurrentAccount] Bob: $0.00
# [FixedDepositAccount] Carol: $100,000.00
```

---

### 3.4 Duck Typing

```python
# Duck typing — no inheritance needed!
# "If it has the method we need, it works"

class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def describe(self) -> str:
        return f"Circle with radius {self.radius}"


class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def describe(self) -> str:
        return f"Rectangle {self.width}×{self.height}"


class Triangle:
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height

    def describe(self) -> str:
        return f"Triangle base={self.base}, height={self.height}"


# This function works for ANY object with .area() and .describe()
# No need for a common parent class!
def print_area_report(shapes: list) -> None:
    print("\n📐 Shape Area Report")
    print("─" * 35)
    total = 0
    for shape in shapes:
        area = shape.area()             # duck typing — works if .area() exists
        total += area
        print(f"  {shape.describe():<30} Area: {area:.2f}")
    print(f"{'─'*35}")
    print(f"  {'Total area':<30} {total:.2f}")


shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8), Circle(2)]
print_area_report(shapes)


### 3.5 Multiple Inheritance and MRO

```python
# ── Multiple inheritance ──────────────────────────────────────────────────
class Flyable:
    """Mixin — adds flying capability."""
    def fly(self) -> str:
        return f"{self.__class__.__name__} is flying!"

    def describe_movement(self) -> str:
        return "flies through the air"


class Swimmable:
    """Mixin — adds swimming capability."""
    def swim(self) -> str:
        return f"{self.__class__.__name__} is swimming!"

    def describe_movement(self) -> str:
        return "swims through water"


class Duck(Flyable, Swimmable):
    """Duck can both fly AND swim. Inherits from both mixins."""

    def __init__(self, name: str):
        self.name = name

    def quack(self) -> str:
        return f"{self.name} says: Quack!"

    # Duck can also override describe_movement from either parent
    def describe_movement(self) -> str:
        fly = super().describe_movement()   # uses MRO: gets Flyable's version
        return f"can fly AND swim"


duck = Duck("Donald")
print(duck.fly())               # Donald is flying!
print(duck.swim())              # Donald is swimming!
print(duck.quack())             # Donald says: Quack!
print(duck.describe_movement()) # can fly AND swim

# ── MRO — understand the lookup order ────────────────────────────────────
print(Duck.__mro__)
# (<class 'Duck'>, <class 'Flyable'>, <class 'Swimmable'>, <class 'object'>)

print(Duck.mro())
# [<class 'Duck'>, <class 'Flyable'>, <class 'Swimmable'>, <class 'object'>]

# When Duck calls super().describe_movement(), MRO tells Python:
# 1. Check Duck — has it? Yes (our override). Done for that call.
# 2. If Duck calls super(), check Flyable next.
# 3. Then Swimmable.
# 4. Then object.


# ── Diamond inheritance — MRO shines ─────────────────────────────────────
class A:
    def greet(self): return "Hello from A"

class B(A):
    def greet(self): return f"B extends: {super().greet()}"

class C(A):
    def greet(self): return f"C extends: {super().greet()}"

class D(B, C):
    pass    # no override — uses MRO to find greet()

d = D()
print(d.greet())
# B extends: C extends: Hello from A

print(D.__mro__)


### 3.6 Multilevel Inheritance

```python
# A → B → C (chain)
class LivingThing:
    def breathe(self) -> str:
        return "Breathing..."

class Animal(LivingThing):
    def __init__(self, name: str):
        self.name = name

    def eat(self) -> str:
        return f"{self.name} is eating."

class Mammal(Animal):
    def __init__(self, name: str, warm_blooded: bool = True):
        super().__init__(name)
        self.warm_blooded = warm_blooded

    def nurse_young(self) -> str:
        return f"{self.name} nurses its young."

class Dog(Mammal):
    def __init__(self, name: str, breed: str):
        super().__init__(name)      # calls Mammal.__init__
        self.breed = breed          # which calls Animal.__init__
                                    # which calls LivingThing (implicitly via object)

    def bark(self) -> str:
        return f"{self.name} barks!"

# Dog inherits from ALL levels
rex = Dog("Rex", "Labrador")
print(rex.breathe())        # Breathing...    ← from LivingThing
print(rex.eat())            # Rex is eating.  ← from Animal
print(rex.nurse_young())    # Rex nurses its young. ← from Mammal
print(rex.bark())           # Rex barks!      ← from Dog

print(Dog.__mro__)

## 4. Common Mistakes & Gotchas

### ❌ Mistake 1: Forgetting to Call `super().__init__()` in Child Constructor

```python
# ❌ Wrong — parent's __init__ never runs!
class SavingsAccount(Account):
    def __init__(self, owner: str, balance: float, interest_rate: float):
        # Forgot super().__init__!
        self.interest_rate = interest_rate
        # self.owner and self.balance are NEVER set — AttributeError later

acc = SavingsAccount("Alice", 1000, 0.04)
print(acc.balance)   # AttributeError: 'SavingsAccount' object has no attribute 'balance'

# ✅ Correct
class SavingsAccount(Account):
    def __init__(self, owner: str, balance: float, interest_rate: float):
        super().__init__(owner, balance)    # ← ALWAYS call this first
        self.interest_rate = interest_rate
```

**Why it happens:** Beginners think child class automatically gets parent's `__init__`. It does — but only if the child doesn't define its own `__init__`. Once you define `__init__` in the child, it completely replaces the parent's.

---

### ❌ Mistake 2: Calling Parent Method Without `super()` — Hardcoding the Parent Name

```python
# ❌ Wrong — hardcoded parent name breaks in complex hierarchies
class ElectricCar(Car):
    def start(self):
        Car.start(self)         # hardcoded — brittle!
        return "Running on electricity"

# ✅ Correct — super() respects MRO
class ElectricCar(Car):
    def start(self):
        super().start()         # follows MRO properly
        return "Running on electricity"


### ❌ Mistake 3: Overriding a Method Without Calling `super()` When You Should

```python
# ❌ Wrong — loses parent's validation and logging!
class SavingsAccount(Account):
    def withdraw(self, amount: float) -> float:
        if self.balance - amount < self.MINIMUM_BALANCE:
            raise ValueError("Below minimum balance")
        self.balance -= amount      # duplicated logic from parent!
        # Also: forgot to call parent's _log() — no transaction history!
        return self.balance

# ✅ Correct — extend, don't replace
class SavingsAccount(Account):
    def withdraw(self, amount: float) -> float:
        if self.balance - amount < self.MINIMUM_BALANCE:
            raise ValueError("Below minimum balance")
        return super().withdraw(amount)  # parent handles subtraction + logging
```

**Rule of thumb:** If you're writing the same code as the parent plus extra logic → use `super()`. If your logic is completely different from the parent's → replace entirely but be intentional about it.

---

### ❌ Mistake 4: Confusing Multiple Inheritance Order

```python
# ❌ Wrong — Method Resolution Order not considered
class A:
    def method(self): return "A"

class B(A):
    def method(self): return "B"

class C(A):
    def method(self): return "C"

class D(C, B):   # ← C comes before B
    pass

print(D().method())    # "C" — students often expect "B" or "A"
print(D.__mro__)

### ❌ Mistake 5: Using Inheritance for "Has-A" Relationships

```python
# ❌ Wrong — Car doesn't "IS-A" Engine; it HAS an Engine
class Engine:
    def start(self): return "Vroom!"

class Car(Engine):    # Wrong! Car is NOT a type of Engine
    pass

# ✅ Correct — composition (has-a) instead of inheritance (is-a)
class Car:
    def __init__(self):
        self.engine = Engine()  # Car HAS-AN Engine

    def start(self):
        return self.engine.start()


## 5. Hands-on Exercises

### 🧑‍🏫 Guided Exercise 1: Shape Hierarchy with Polymorphism

**Goal:** Build a shape hierarchy that demonstrates inheritance, method overriding, and polymorphism step by step.

```python
# Step 1: Create the base Shape class
import math

class Shape:
    """Base class for all 2D shapes."""

    def __init__(self, color: str = "white"):
        self.color = color

    def area(self) -> float:
        """Override in subclasses."""
        raise NotImplementedError(f"{self.__class__.__name__} must implement area()")

    def perimeter(self) -> float:
        """Override in subclasses."""
        raise NotImplementedError(f"{self.__class__.__name__} must implement perimeter()")

    def describe(self) -> str:
        return (f"{self.__class__.__name__} | Color: {self.color} | "
                f"Area: {self.area():.2f} | Perimeter: {self.perimeter():.2f}")

    def __str__(self) -> str:
        return self.describe()


# Step 2: Create child classes
class Circle(Shape):
    def __init__(self, radius: float, color: str = "white"):
        super().__init__(color)
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float, color: str = "white"):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, base: float, height: float, side1: float,
                 side2: float, color: str = "white"):
        super().__init__(color)
        self.base = base
        self.height = height
        self.side1 = side1
        self.side2 = side2

    def area(self) -> float:
        return 0.5 * self.base * self.height

    def perimeter(self) -> float:
        return self.base + self.side1 + self.side2


# Step 3: Polymorphic function
def total_area(shapes: list[Shape]) -> float:
    """Works for ANY Shape subclass — that's polymorphism."""
    return sum(shape.area() for shape in shapes)


def largest_shape(shapes: list[Shape]) -> Shape:
    return max(shapes, key=lambda s: s.area())


# Test
shapes = [
    Circle(5, "red"),
    Rectangle(4, 6, "blue"),
    Triangle(3, 4, 5, 5, "green"),
    Circle(3, "yellow"),
]

for shape in shapes:
    print(shape)

print(f"\nTotal area: {total_area(shapes):.2f}")
print(f"Largest: {largest_shape(shapes)}")
```


### 🧑‍🏫 Guided Exercise 2: Employee Hierarchy with `super()`

**Goal:** Build an employee payroll system that uses `super()` at every level.

```python
class Employee:
    company = "TechCorp"

    def __init__(self, name: str, base_salary: float, employee_id: str):
        self.name = name
        self.base_salary = base_salary
        self.employee_id = employee_id

    def calculate_pay(self) -> float:
        """Base pay — just the salary."""
        return self.base_salary

    def get_details(self) -> str:
        return (f"ID: {self.employee_id} | {self.name} | "
                f"Base: ${self.base_salary:,.2f} | "
                f"Total Pay: ${self.calculate_pay():,.2f}")


class Manager(Employee):
    def __init__(self, name: str, base_salary: float,
                 employee_id: str, team_size: int):
        super().__init__(name, base_salary, employee_id)
        self.team_size = team_size
        self.team_bonus_rate = 0.10     # 10% bonus per person managed

    def calculate_pay(self) -> float:
        """Extends: base pay + team management bonus."""
        base = super().calculate_pay()
        bonus = self.team_size * self.base_salary * self.team_bonus_rate
        return base + bonus


class SeniorManager(Manager):
    def __init__(self, name: str, base_salary: float,
                 employee_id: str, team_size: int, departments: int):
        super().__init__(name, base_salary, employee_id, team_size)
        self.departments = departments

    def calculate_pay(self) -> float:
        """Extends: manager pay + department bonus."""
        manager_pay = super().calculate_pay()   # gets Manager's full pay
        dept_bonus = self.departments * 5000
        return manager_pay + dept_bonus


# Test
emp = Employee("Alice", 60000, "E001")
mgr = Manager("Bob", 80000, "M001", team_size=5)
sr_mgr = SeniorManager("Carol", 100000, "SM001", team_size=10, departments=3)

for person in [emp, mgr, sr_mgr]:
    print(person.get_details())

# Output:
# ID: E001 | Alice | Base: $60,000.00 | Total Pay: $60,000.00
# ID: M001 | Bob | Base: $80,000.00 | Total Pay: $120,000.00
# ID: SM001 | Carol | Base: $100,000.00 | Total Pay: $215,000.00
```

---

### 💻 Independent Practice 1: Vehicle Rental System

**Task:** Create a vehicle rental hierarchy with different rate calculations.

```python
"""
Build this hierarchy:
    Vehicle (base)
    ├── Car(Vehicle)
    ├── Truck(Vehicle)
    └── Motorcycle(Vehicle)

Vehicle:
- __init__(vehicle_id, model, base_rate_per_day)
- calculate_rental_cost(days) → float: just base_rate × days
- get_info() → str

Car(Vehicle):
- __init__(..., num_passengers)
- calculate_rental_cost(days) → extends: if days > 7, apply 10% discount

Truck(Vehicle):
- __init__(..., payload_tons)
- calculate_rental_cost(days) → extends: add $50/day surcharge per ton payload

Motorcycle(Vehicle):
- __init__(..., engine_cc)
- calculate_rental_cost(days) → extends: if engine_cc > 600, premium rate (+20%)

Polymorphic function:
- def generate_rental_quote(vehicles: list, days: int) → None
  → prints rental cost for each vehicle type
"""

# Hints:
# - super().__init__() in every child
# - super().calculate_rental_cost(days) for the base calculation
# - All __init__ methods pass appropriate args to parent

# Expected output for 10 days:
# Car (Toyota Camry): $450.00  (500*10 = 5000, with 10% discount = 4500... wait)
# Truck (Ford F-150, 2 tons): $1800.00
# Motorcycle (Honda CBR600): $720.00
```

> **Hints:** Call `super().calculate_rental_cost(days)` inside each child's method. Use `isinstance(self, ...)` is NOT needed — let polymorphism do the work.

---

### 💻 Independent Practice 2: Notification System

**Task:** Build a polymorphic notification system.

```python
"""
Notifier (base class)
- __init__(sender_name)
- send(recipient, message) → bool: base implementation just prints
- format_message(message) → str: returns "[sender_name]: message"

EmailNotifier(Notifier):
- __init__(sender_name, smtp_server)
- send(recipient, message) → extends: validates email format first
  - raise ValueError if recipient doesn't contain '@'
  - calls super().send() if valid

SMSNotifier(Notifier):
- __init__(sender_name, service_provider)
- send(recipient, message) → extends: truncates message to 160 chars

PushNotifier(Notifier):
- __init__(sender_name, app_name)
- format_message(message) → overrides: adds app badge "🔔 [app_name]: message"
- send(recipient, message) → extends: prepends "PUSH: " to all messages

Polymorphic function:
- def broadcast(notifiers: list, recipients: list, message: str):
    → sends message to all recipients via all notifiers
"""

# Hint: super().format_message() in PushNotifier
# Hint: super().send() in all children after their custom logic
```

---

### 🏆 Challenge Problem: Complete Banking System

```python
"""
Build the full Account hierarchy from the class notes,
then add these additional requirements:

1. PremiumSavingsAccount(SavingsAccount):
   - Higher interest rate (6%)
   - No monthly withdrawal limit
   - Minimum balance $10,000
   - Earns bonus interest on balance > $100,000

2. StudentAccount(SavingsAccount):
   - Lower minimum balance ($100)
   - No monthly fee
   - Lower interest rate (2%)
   - Extra method: apply_scholarship(amount) that deposits with a special log entry

3. BusinessCurrentAccount(CurrentAccount):
   - Higher overdraft limit ($50,000)
   - Monthly transaction fee deducted automatically
   - Bulk transfer method: transfer_to_multiple(accounts: list, amounts: list)

4. Polymorphic monthly_report(accounts: list) function that:
   - Calls calculate_interest() on each account
   - Prints a formatted table with account type, owner, balance, interest earned
   - Calculates and prints the bank's total managed funds

5. Demonstrate the full MRO for PremiumSavingsAccount using __mro__
"""
```

---

## 6. Best Practices & Industry Standards

### Favor Composition Over Inheritance (When Appropriate)

```python
# ❌ Bad: using inheritance just to reuse code (no IS-A relationship)
class JSONLogger(dict):     # Logger is NOT a dict!
    def log(self, message):
        self["message"] = message

# ✅ Good: composition — Logger HAS-A dict (or file, or stream)
class JSONLogger:
    def __init__(self):
        self._log_store = {}    # composition

    def log(self, message: str, level: str = "INFO") -> None:
        self._log_store[len(self._log_store)] = {
            "level": level, "message": message
        }
```

---

### Always Use `super()` — Never Hardcode the Parent Name

```python
# ❌ Bad
class SavingsAccount(Account):
    def __init__(self, owner, balance, rate):
        Account.__init__(self, owner, balance)  # brittle

# ✅ Good
class SavingsAccount(Account):
    def __init__(self, owner, balance, rate):
        super().__init__(owner, balance)        # MRO-aware, flexible
```

---

### Use Abstract Base Classes for Enforced Contracts

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Using ABC enforces that subclasses implement required methods."""

    @abstractmethod
    def area(self) -> float:
        """Every shape MUST implement this — can't forget."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}"

# Shape()       → TypeError: Can't instantiate abstract class Shape
# Circle()      → Works, must implement area() and perimeter()
# If Circle doesn't implement area() → TypeError at instantiation
```

---

### Keep Inheritance Hierarchies Shallow

```python
# ❌ Too deep — hard to debug and understand
# A → B → C → D → E → F → G  (7 levels!)

# ✅ Preferred — maximum 2-3 levels
# Account → SavingsAccount
# Account → CurrentAccount

# If you need to share behavior across many classes without deep hierarchy:
# Use MIXINS (small, focused classes designed for multiple inheritance)

class TimestampMixin:
    """Mixin — adds created_at and updated_at to any class."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # cooperative multiple inheritance
        from datetime import datetime
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def touch(self):
        from datetime import datetime
        self.updated_at = datetime.now()

class Account(TimestampMixin):  # Account gets timestamps for free
    def __init__(self, owner, balance):
        super().__init__()              # calls TimestampMixin.__init__
        self.owner = owner
        self.balance = balance
```

---

### Liskov Substitution Principle (LSP)

```python
# ✅ Principle: Wherever a parent is used, a child should work identically
# If SavingsAccount IS-A Account, then any code using Account
# should work with SavingsAccount without modification

def process_deposit(account: Account, amount: float) -> None:
    account.deposit(amount)     # works for Account, SavingsAccount, CurrentAccount, etc.

# ❌ Violates LSP: child REMOVES capabilities parent has
class LockedAccount(Account):
    def withdraw(self, amount: float) -> float:
        raise RuntimeError("This account cannot withdraw!")  # breaks the contract!
        # Any code that uses Account and calls withdraw() will now crash
        # if given a LockedAccount — violation!
```

---

## 7. Real-World Application

### Django Models Use Inheritance Daily

```python
# Every Django model inherits from models.Model
from django.db import models

class BaseModel(models.Model):
    """Abstract base model — shared fields for ALL models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True     # Django won't create a table for this

class Product(BaseModel):       # inherits created_at, updated_at, is_active
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Order(BaseModel):         # also inherits timestamps
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    # created_at, updated_at come from BaseModel for free!
```

### Django Class-Based Views

```python
# Django CBVs ARE inheritance in action (Day 21+ preview)
from django.views.generic import ListView, DetailView, CreateView

class ProductListView(ListView):        # inherits from ListView
    model = Product                     # class variable
    template_name = "products/list.html"
    context_object_name = "products"

    def get_queryset(self):             # overrides parent method!
        return Product.objects.filter(is_active=True).order_by("name")


class ProductDetailView(DetailView):    # different parent, same pattern
    model = Product
    template_name = "products/detail.html"
```

### Django REST Framework Serializers

```python
# Serializers use inheritance for validation and field sharing
from rest_framework import serializers

class BaseUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()

class UserCreateSerializer(BaseUserSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_email(self, value):        # override parent validation
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value.lower()

class UserProfileSerializer(BaseUserSerializer):
    bio = serializers.CharField(required=False)
    # Inherits name and email, adds bio
```

### 🔭 Connection to Upcoming Days
- **Day 7:** Dunder/magic methods — `__len__`, `__iter__`, `__eq__`, `__add__` — making custom classes behave like built-in types
- **Day 8:** Decorators — built on first-class functions; `@property`, `@classmethod`, `@staticmethod` revisited with deeper understanding
- **Day 9:** Abstract Base Classes (`abc`), Protocols, and Dataclasses — formalizing class contracts
- **Day 20:** Django Models — you'll recognize the inheritance patterns immediately


### Core Syntax Cheat Sheet

```python
# ── Basic inheritance ─────────────────────────────────────────────────────
class Child(Parent):
    def __init__(self, ...):
        super().__init__(...)       # call parent constructor
        self.new_attr = ...

# ── Override a method ─────────────────────────────────────────────────────
def method(self):
    result = super().method()      # extend: call parent first
    # add extra logic
    return result

def method(self):                  # replace: completely new logic
    # no super() call needed
    return new_result

# ── Multiple inheritance ──────────────────────────────────────────────────
class D(B, C):                     # B is checked before C
    pass

# ── Check MRO ─────────────────────────────────────────────────────────────
ClassName.__mro__
ClassName.mro()

# ── Check relationships ───────────────────────────────────────────────────
isinstance(obj, ClassName)         # is obj an instance of ClassName (or subclass)?
issubclass(ChildClass, ParentClass)# is ChildClass a subclass of ParentClass?

# ── Abstract method (forces subclass to implement) ────────────────────────
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

# ── Polymorphic usage ─────────────────────────────────────────────────────
def process(items: list):
    for item in items:
        item.method()              # duck typing — any object with .method()
```

---

### 5 MCQ Recap Questions

**Q1.** What does `super().__init__(name, age)` do in a child class's `__init__`?
- A) Creates a new parent object
- **B) Calls the parent class's `__init__` method with the given arguments** ✅
- C) Replaces the child's `__init__` with the parent's
- D) Sets the child's class to the parent class

**Q2.** A `SavingsAccount` inherits from `Account`. Which statement about `isinstance()` is TRUE?
- A) `isinstance(savings, SavingsAccount)` is True but `isinstance(savings, Account)` is False
- **B) Both `isinstance(savings, SavingsAccount)` and `isinstance(savings, Account)` are True** ✅
- C) `isinstance(savings, Account)` is True but `isinstance(savings, SavingsAccount)` is False
- D) Both return False unless you explicitly register the types

**Q3.** What is "duck typing" in Python?
- A) Only objects that inherit from `Duck` can be used in duck-typed code
- B) Python checks the type of every object before calling methods
- **C) Python calls a method if the object has it, regardless of the object's class** ✅
- D) Duck typing only works with built-in types

**Q4.** Given `class D(B, C)` where both B and C have a `greet()` method, which `greet()` does `D().greet()` call?
- A) C's `greet()` — it's always the last parent
- B) It raises an `AmbiguousMethodError`
- **C) B's `greet()` — Python uses MRO, left-to-right** ✅
- D) Both are called simultaneously

**Q5.** When should you NOT use inheritance?
- A) When two classes share methods
- B) When one class has more features than another
- **C) When the relationship is "has-a" rather than "is-a" (e.g., Car has an Engine)** ✅
- D) When using Python 3

---

### 🖊️ Whiteboard Diagrams to Draw

1. **IS-A hierarchy diagram:** Box labeled `Account` at top. Three boxes below connected by arrows: `SavingsAccount`, `CurrentAccount`, `FixedDepositAccount`. Label arrows "inherits from." Draw what each child adds in a smaller box beside it.

2. **Method call chain with `super()`:** Draw three boxes: `Account → SavingsAccount → PremiumSavingsAccount`. Show `withdraw()` call going DOWN the chain, then `super()` calling UP. Show what each level adds.

3. **MRO for diamond inheritance:** Draw the diamond: D at top, B and C in middle, A at bottom. Show the MRO arrow as: D → B → C → A → object (left to right, not bottom to top of diamond).

4. **Duck typing vs type checking:** Two columns. Left: "Type-checking (Java-style)" — `if isinstance(obj, Account): obj.withdraw()`. Right: "Duck typing (Python-style)" — just call `obj.withdraw()` — works for anything with `withdraw()`. Show that the right column is shorter and more flexible.

5. **Polymorphism diagram:** Draw one function `process_monthly_interest(accounts)`. Show arrows from it pointing to `SavingsAccount.calculate_interest()`, `CurrentAccount.calculate_interest()`, `FixedDepositAccount.calculate_interest()`. Label: "same call → different behavior."

6. **Inheritance types (quick sketch):** Single, Multilevel, Hierarchical, Multiple — draw each as a simple box diagram with 3-4 boxes.

---

### ⏱️ Timing Guide (3 Hours)

| Time | Activity |
|------|----------|
| 0:00 – 0:10 | Day 5 quick recap (classes, `__init__`, `self`, 3 method types) |
| 0:10 – 0:30 | Inheritance fundamentals — IS-A concept, `class Child(Parent)`, basic example + whiteboard |
| 0:30 – 0:50 | `super()` — why it exists, constructor inheritance, method extending vs replacing |
| 0:50 – 1:10 | Method overriding — full Account hierarchy live coding (Account + SavingsAccount) |
| 1:10 – 1:20 | ☕ Break |
| 1:20 – 1:35 | Polymorphism — duck typing, `process_monthly_interest()` demo, polymorphism vs `isinstance` |
| 1:35 – 1:50 | Types of inheritance + MRO — diagrams, `__mro__`, diamond inheritance demo |
| 1:50 – 2:20 | Guided Exercise 1 (Shape hierarchy) — instructor-led |
| 2:20 – 2:40 | Guided Exercise 2 (Employee hierarchy) — instructor-led |
| 2:40 – 2:50 | Common mistakes walkthrough + Q&A |
| 2:50 – 3:00 | MCQ recap + Day 7 preview (dunder methods) |

> 💡 **Teaching tip:** The `super()` concept takes the most time. Draw the chain on the whiteboard — show that `super()` doesn't go "to the parent" but "to the next class in the MRO." This prevents 90% of MRO confusion.
> 💡 **Live demo tip:** The `process_monthly_interest([savings, current, fixed])` demo is the most impactful moment — show that changing the list order or adding a new account type requires ZERO changes to the function. That's the power of polymorphism.

---

### 📚 Resources & Further Reading

(https://docs.python.org/3/tutorial/classes.html#inheritance)
(https://docs.python.org/3/library/functions.html#super)
(https://docs.python.org/3/library/abc.html)
(https://realpython.com/inheritance-composition-python/)
(https://realpython.com/python-super/)
(https://www.youtube.com/watch?v=EiOglTERPEo)
(https://www.python.org/download/releases/2.3/mro/)
