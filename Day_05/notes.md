# 🐍 Python Full Stack — Day 5
---

## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, learners will be able to:
- Explain the four pillars of OOP (Encapsulation, Abstraction, Inheritance, Polymorphism) and identify them in real code
- Define classes with `__init__`, instance variables, class variables, and all three method types
- Distinguish between instance methods, class methods (`@classmethod`), and static methods (`@staticmethod`) — and choose the right one for each use case
- Predict how instance vs class variable modifications behave across multiple objects
- Build a complete, well-structured class from scratch following Python conventions

### 📋 Prerequisites (Days 1–4 Review)
- Python data types, mutability, reference model (Day 1)
- Functions, scope, LEGB, `*args`/`**kwargs`, type hints (Day 2)
- Data structures — lists, dicts, sets (Day 3)
- Modules, packages, `__init__.py` (Day 4)

### 🔗 Connection to the Full Stack Journey
- **Django Models (Day 20+):** Every Django model IS a Python class — `class Product(models.Model)` — with instance variables mapping to database columns
- **Django Views (Day 21+):** Class-Based Views (CBVs) use inheritance and method overriding directly
- **Django Forms (Day 22+):** `forms.ModelForm` uses class variables to define fields
- **Flask (Day 18+):** Flask's `Blueprint` and extension objects are class instances
- **REST APIs (Day 24+):** Serializers and ViewSets are class hierarchies built on OOP
- **Decorators (Day 8):** `@classmethod`, `@staticmethod`, `@property` are all decorator patterns you'll see daily

---

## 2. Concept Explanation

### 2.1 The OOP Paradigm — Why It Exists

**The "Why":** As programs grow, procedural code (functions operating on data separately) becomes hard to maintain. You end up passing the same data to dozens of functions, losing track of what belongs to what. OOP solves this by **bundling data and the functions that operate on it into a single unit — the object**.

**Real-world analogy:** Think of a `BankAccount`. In procedural code, you'd have a `balance` variable and separate `deposit()`, `withdraw()` functions that must always receive that balance as an argument — and any function could touch it. In OOP, the `BankAccount` **object** owns its `balance` and exposes only the methods it approves — `deposit()` and `withdraw()`. Nothing else can reach in.

**The Four Pillars:**

| Pillar | What It Means | Real Example |
|--------|---------------|--------------|
| **Encapsulation** | Bundle data + methods; hide internal state | `balance` is private; only `deposit()`/`withdraw()` can change it |
| **Abstraction** | Expose only what's necessary; hide complexity | You call `account.deposit(100)` — you don't care how it updates the DB |
| **Inheritance** | New class reuses and extends an existing class | `SavingsAccount` extends `BankAccount` with interest logic |
| **Polymorphism** | Different objects respond to the same interface | `account.calculate_interest()` works for both Savings and Checking accounts differently |

---

### 2.2 Class vs Object — Blueprint vs Instance

**The "Why":** A class is a **template** (blueprint). An object is a **concrete thing** built from that template. You define a class once and create as many objects (instances) as you need.

**Analogy:**
- Class = architectural blueprint for a house
- Object = an actual house built from that blueprint
- You can build 1000 houses from one blueprint — each has the same structure but different contents (different owners, colors, furniture)

```
Class BankAccount (blueprint)
    - Has: account_number, balance, owner
    - Can: deposit, withdraw, get_balance

alice_account  (instance 1) → account_number=1001, balance=5000, owner="Alice"
bob_account    (instance 2) → account_number=1002, balance=2500, owner="Bob"
```

Every object is independent — changing Alice's balance doesn't affect Bob's.

---

### 2.3 `__init__` — The Constructor

**The "Why":** When you create an object, Python needs to set it up — give it its initial state (its starting data). `__init__` is called automatically right after the object is created. It's Python's constructor.

**`__new__` vs `__init__`:**
- `__new__` — allocates memory and creates the object (called first, rarely overridden)
- `__init__` — initializes the object's state (called second, what you always use)

Think of `__new__` as building the empty house; `__init__` as furnishing it.

---

### 2.4 Instance Variables vs Class Variables

**The "Why":** This is the most critical distinction in OOP for avoiding bugs:

- **Instance variable** — belongs to ONE specific object (`self.balance`). Each object has its own copy. Changing one doesn't affect others.
- **Class variable** — belongs to the CLASS itself, shared by ALL instances (`BankAccount.bank_name`). If you change it at the class level, every instance sees the change.

**Analogy:**
- **Instance variable** = the amount of money in YOUR specific bank account. Alice's balance and Bob's balance are independent.
- **Class variable** = the name on the bank's sign. If the bank renames itself from "First Bank" to "National Bank", every account holder's bank name changes.

**The shadowing trap:** If you assign to `self.class_variable_name`, Python creates a **new instance variable** that shadows (hides) the class variable for that specific object — the class variable itself is not changed.

---

### 2.5 The Three Method Types

**The "Why":** Not all methods need access to the same data. Python gives you three method types, each with the right level of access:

| Method Type | Decorator | First Parameter | Has Access To |
|-------------|-----------|-----------------|----------------|
| Instance method | (none) | `self` | Instance data + class data |
| Class method | `@classmethod` | `cls` | Class data only (no instance) |
| Static method | `@staticmethod` | (none) | Neither — pure utility function |

**When to use each:**
- **Instance method:** When you need `self` — the object's own data (deposit, withdraw, get_balance)
- **Class method:** Alternative constructors, factory methods, operations on the class itself (create_savings_account)
- **Static method:** Utility/helper functions logically related to the class but not needing instance or class data (validate_account_number, format_currency)

---

### 2.6 The `self` Parameter

**The "Why":** Python does NOT automatically pass the calling object to methods — you must declare it explicitly as the first parameter. This is by design: **explicit is better than implicit** (PEP 20 — The Zen of Python).

When you call `alice_account.deposit(100)`, Python internally calls `BankAccount.deposit(alice_account, 100)` — `self` IS the object.

`self` is a convention, not a keyword — you could name it anything, but **never do**. `self` is universally understood.

---

## 3. Syntax & Code Examples

### 3.1 Basic Class Definition

```python
# Simplest possible class
class Dog:
    pass    # empty class — valid Python

# Create instances
dog1 = Dog()
dog2 = Dog()
print(type(dog1))               # <class '__main__.Dog'>
print(isinstance(dog1, Dog))    # True
print(dog1 is dog2)             # False — different objects
```

---

### 3.2 `__init__`, Instance Variables, and `self`

```python
class Dog:
    """Represents a dog with a name and breed."""

    def __init__(self, name: str, breed: str, age: int = 0):
        """
        Constructor — runs automatically when Dog() is called.
        self refers to the newly created Dog instance.
        """
        # Instance variables — each Dog gets its own copies
        self.name = name        # self.name belongs to THIS dog
        self.breed = breed
        self.age = age
        self._tricks: list[str] = []    # private by convention (underscore)

    def bark(self) -> str:
        """Instance method — has access to self (this specific dog)."""
        return f"{self.name} says: Woof!"

    def learn_trick(self, trick: str) -> None:
        """Add a trick to this dog's list."""
        self._tricks.append(trick)
        print(f"{self.name} learned: {trick}!")

    def show_tricks(self) -> None:
        if not self._tricks:
            print(f"{self.name} knows no tricks yet.")
        else:
            print(f"{self.name}'s tricks: {', '.join(self._tricks)}")

    def __repr__(self) -> str:
        """Official string representation — shown in REPL and debugging."""
        return f"Dog(name={self.name!r}, breed={self.breed!r}, age={self.age})"

    def __str__(self) -> str:
        """User-friendly string representation — shown by print()."""
        return f"{self.name} ({self.breed}, {self.age} years old)"


# Creating instances
rex = Dog("Rex", "German Shepherd", 3)
buddy = Dog("Buddy", "Golden Retriever")   # age defaults to 0

print(rex)          # Rex (German Shepherd, 3 years old)   ← __str__
print(repr(rex))    # Dog(name='Rex', breed='German Shepherd', age=3)  ← __repr__
print(rex.bark())   # Rex says: Woof!

rex.learn_trick("sit")
rex.learn_trick("shake")
buddy.learn_trick("roll over")

rex.show_tricks()   # Rex's tricks: sit, shake
buddy.show_tricks() # Buddy's tricks: roll over

# Each dog has independent state
print(rex.name)     # Rex
print(buddy.name)   # Buddy
```

---

### 3.3 Class Variables vs Instance Variables

```python
class BankAccount:
    """Demonstrates class vs instance variables clearly."""

    # ── Class Variables — shared by ALL instances ─────────────────────────
    bank_name: str = "Python National Bank"
    interest_rate: float = 0.035        # 3.5% — same for all accounts
    _account_counter: int = 0           # private class var — tracks total accounts

    def __init__(self, owner: str, initial_balance: float = 0.0):
        # ── Instance Variables — unique to each account ───────────────────
        BankAccount._account_counter += 1
        self.account_number: int = BankAccount._account_counter
        self.owner: str = owner
        self.balance: float = initial_balance
        self._transaction_history: list[dict] = []

    def get_bank_info(self) -> str:
        # Accessing class variable via self — works, but cls is more correct
        return f"Bank: {self.bank_name}, Rate: {self.interest_rate:.1%}"


# Create two accounts
alice = BankAccount("Alice", 5000.0)
bob = BankAccount("Bob", 2500.0)

# ── Instance variables are independent ────────────────────────────────────
print(alice.balance)        # 5000.0
print(bob.balance)          # 2500.0

# ── Class variables are shared ────────────────────────────────────────────
print(alice.bank_name)      # Python National Bank
print(bob.bank_name)        # Python National Bank
print(BankAccount.bank_name)# Python National Bank — access from class directly

# ── Changing class variable via class — affects ALL instances ─────────────
BankAccount.interest_rate = 0.04    # Bank raises rates
print(alice.interest_rate)  # 0.04  ← sees the change
print(bob.interest_rate)    # 0.04  ← sees the change too

# ── The shadowing trap — assigning via instance creates instance variable ─
alice.bank_name = "Alice's Private Bank"  # creates INSTANCE variable, doesn't change class var
print(alice.bank_name)      # "Alice's Private Bank" — alice's own var shadows class var
print(bob.bank_name)        # "Python National Bank" — class var unchanged
print(BankAccount.bank_name)# "Python National Bank" — class var unchanged

# ── Confirm with __dict__ ─────────────────────────────────────────────────
print(alice.__dict__)       # {'account_number': 1, 'owner': 'Alice', 'balance': 5000.0,
                            #  '_transaction_history': [], 'bank_name': "Alice's Private Bank"}
                            # Notice: bank_name IS in alice's dict now (instance var)
print(bob.__dict__)         # {'account_number': 2, 'owner': 'Bob', 'balance': 2500.0,
                            #  '_transaction_history': []}
                            # Notice: bank_name is NOT in bob's dict (uses class var)

# Track total accounts created
print(BankAccount._account_counter)     # 2
```

---

### 3.4 All Three Method Types — Complete BankAccount

```python
from datetime import datetime
from typing import Optional


class BankAccount:
    """
    A bank account demonstrating all three method types.
    """

    # Class variables
    bank_name: str = "Python National Bank"
    interest_rate: float = 0.035
    _account_counter: int = 0
    MINIMUM_BALANCE: float = 0.0        # constant — uppercase convention

    def __init__(
        self,
        owner: str,
        initial_balance: float = 0.0,
        account_type: str = "checking"
    ):
        """Initialize account with owner, balance, and type."""
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Owner name must be a non-empty string")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

        BankAccount._account_counter += 1
        self.account_number: int = BankAccount._account_counter
        self.owner: str = owner.strip()
        self.balance: float = initial_balance
        self.account_type: str = account_type
        self._transaction_history: list[dict] = []
        self._is_active: bool = True

    # ── Instance Methods — need self (access instance data) ───────────────

    def deposit(self, amount: float) -> float:
        """Deposit money. Returns new balance."""
        self._validate_active()
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive, got {amount}")
        self.balance += amount
        self._record_transaction("deposit", amount)
        return self.balance

    def withdraw(self, amount: float) -> float:
        """Withdraw money. Returns new balance."""
        self._validate_active()
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be positive, got {amount}")
        if amount > self.balance:
            raise ValueError(f"Insufficient funds: balance={self.balance:.2f}, requested={amount:.2f}")
        self.balance -= amount
        self._record_transaction("withdrawal", amount)
        return self.balance

    def get_balance(self) -> float:
        """Return current balance."""
        return self.balance

    def apply_interest(self) -> float:
        """Apply annual interest to balance. Returns interest earned."""
        self._validate_active()
        interest = self.balance * BankAccount.interest_rate
        self.balance += interest
        self._record_transaction("interest", interest)
        return interest

    def get_statement(self) -> str:
        """Return formatted account statement."""
        lines = [
            f"{'=' * 45}",
            f"  {BankAccount.bank_name}",
            f"  Account #{self.account_number} — {self.account_type.title()}",
            f"  Owner: {self.owner}",
            f"  Balance: ${self.balance:,.2f}",
            f"{'─' * 45}",
            f"  Transaction History:",
        ]
        for tx in self._transaction_history[-5:]:    # last 5
            sign = "+" if tx["type"] in ("deposit", "interest") else "-"
            lines.append(f"  {tx['date']}  {sign}${tx['amount']:,.2f}  ({tx['type']})")
        lines.append(f"{'=' * 45}")
        return "\n".join(lines)

    # Private helper — underscore convention signals "not for external use"
    def _validate_active(self) -> None:
        if not self._is_active:
            raise RuntimeError("Account is closed")

    def _record_transaction(self, tx_type: str, amount: float) -> None:
        self._transaction_history.append({
            "type": tx_type,
            "amount": round(amount, 2),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "balance_after": round(self.balance, 2)
        })

    # ── Class Methods — @classmethod, receive cls (the class itself) ───────

    @classmethod
    def create_savings_account(cls, owner: str, initial_balance: float = 0.0) -> "BankAccount":
        """
        Alternative constructor (factory method).
        Creates a savings account with higher interest rate.
        Uses cls so subclasses can call this and get the right type back.
        """
        account = cls(owner, initial_balance, account_type="savings")
        # Savings accounts get a bonus interest rate bump
        account.interest_rate = cls.interest_rate + 0.01   # instance var shadows class var
        return account

    @classmethod
    def create_joint_account(cls, owner1: str, owner2: str, initial_balance: float = 0.0) -> "BankAccount":
        """Create a joint account with combined owner name."""
        joint_name = f"{owner1} & {owner2}"
        return cls(joint_name, initial_balance, account_type="joint")

    @classmethod
    def get_total_accounts(cls) -> int:
        """Return total number of accounts ever created."""
        return cls._account_counter

    @classmethod
    def update_interest_rate(cls, new_rate: float) -> None:
        """Update the bank-wide interest rate."""
        if not 0 <= new_rate <= 1:
            raise ValueError("Interest rate must be between 0 and 1")
        cls.interest_rate = new_rate
        print(f"Interest rate updated to {new_rate:.1%} for all accounts")

    # ── Static Methods — @staticmethod, no self or cls ────────────────────

    @staticmethod
    def validate_account_number(account_num: int) -> bool:
        """
        Validate format of account number.
        Static because it doesn't need account or class data —
        pure utility function logically grouped with the class.
        """
        return isinstance(account_num, int) and 1000 <= account_num <= 9999

    @staticmethod
    def format_currency(amount: float, currency: str = "USD") -> str:
        """Format a number as currency string."""
        symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹"}
        symbol = symbols.get(currency, currency)
        return f"{symbol}{amount:,.2f}"

    @staticmethod
    def calculate_compound_interest(
        principal: float,
        rate: float,
        years: int,
        compounds_per_year: int = 12
    ) -> float:
        """
        Calculate compound interest.
        Pure math — no instance or class state needed.
        A = P(1 + r/n)^(nt)
        """
        return principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)

    def __repr__(self) -> str:
        return (f"BankAccount(owner={self.owner!r}, "
                f"balance={self.balance:.2f}, "
                f"type={self.account_type!r})")

    def __str__(self) -> str:
        return (f"Account #{self.account_number} | {self.owner} | "
                f"${self.balance:,.2f} | {self.account_type.title()}")
```

---

### 3.5 Using the BankAccount Class

```python
# ── Instance method usage ─────────────────────────────────────────────────
alice = BankAccount("Alice", 5000.0)
bob = BankAccount("Bob", 1000.0)

alice.deposit(500)
alice.withdraw(200)
alice.apply_interest()
print(alice.get_balance())          # 5300.0 + interest
print(alice)                        # Account #1 | Alice | $5,472.50 | Checking

# ── Class method usage — alternative constructors ─────────────────────────
carol_savings = BankAccount.create_savings_account("Carol", 10000.0)
joint = BankAccount.create_joint_account("Diana", "Eve", 2000.0)

print(carol_savings.account_type)   # savings
print(carol_savings.interest_rate)  # 0.045 (3.5% + 1% bonus)
print(joint.owner)                  # Diana & Eve

# ── Class method on class (not instance) ──────────────────────────────────
print(BankAccount.get_total_accounts())     # 4
BankAccount.update_interest_rate(0.04)     # Updates for ALL accounts

# ── Static method usage — called on class or instance ─────────────────────
print(BankAccount.validate_account_number(1234))    # True
print(BankAccount.validate_account_number(99))      # False
print(BankAccount.format_currency(5472.50))         # $5,472.50
print(BankAccount.format_currency(5472.50, "EUR"))  # €5,472.50

# Static methods can also be called on instances (less common)
print(alice.format_currency(100))                   # $100.00

future = BankAccount.calculate_compound_interest(10000, 0.05, 10)
print(f"Future value: ${future:,.2f}")              # Future value: $16,470.09

# ── Statement ─────────────────────────────────────────────────────────────
alice.deposit(1000)
alice.withdraw(300)
print(alice.get_statement())
```

**Output:**
```
=============================================
  Python National Bank
  Account #1 — Checking
  Owner: Alice
  Balance: $6,172.50
─────────────────────────────────────────────
  Transaction History:
  2024-01-15 10:30  +$500.00  (deposit)
  2024-01-15 10:30  -$200.00  (withdrawal)
  2024-01-15 10:30  +$172.50  (interest)
  2024-01-15 10:30  +$1,000.00  (deposit)
  2024-01-15 10:30  -$300.00  (withdrawal)
=============================================
```

---

### 3.6 `__new__` — When and Why

```python
# __new__ is called BEFORE __init__ — allocates the object
# You almost never override it, but knowing it exists prevents confusion

class Singleton:
    """A class that allows only ONE instance to exist."""
    _instance = None    # class variable tracks the single instance

    def __new__(cls):
        if cls._instance is None:
            # Only create a new instance if none exists
            cls._instance = super().__new__(cls)
            print("Creating the Singleton instance...")
        else:
            print("Returning existing instance...")
        return cls._instance

    def __init__(self):
        # This runs EVERY time Singleton() is called
        # even if __new__ returned the existing instance
        pass

s1 = Singleton()    # Creating the Singleton instance...
s2 = Singleton()    # Returning existing instance...
print(s1 is s2)     # True — same object!
```

---

## 4. Common Mistakes & Gotchas

### ❌ Mistake 1: Forgetting `self` in Method Definition

```python
# ❌ Wrong — Python will pass the instance as first arg, causing TypeError
class Dog:
    def bark():          # Missing 'self'!
        return "Woof"

d = Dog()
d.bark()    # TypeError: bark() takes 0 positional arguments but 1 was given
            # Python tried: Dog.bark(d) — but bark takes no args!

# ✅ Correct
class Dog:
    def bark(self) -> str:
        return "Woof"
```

**Why it happens:** Python automatically passes the calling instance as the first argument. If you don't declare `self`, there's no parameter to receive it.

---

### ❌ Mistake 2: Mutable Class Variable Shared Across All Instances

```python
# ❌ Wrong — ALL instances share the SAME list!
class Student:
    grades = []         # class variable — one list for ALL students

    def add_grade(self, grade):
        self.grades.append(grade)   # modifies the SHARED class list!

alice = Student()
bob = Student()

alice.add_grade(90)
print(bob.grades)   # [90] ← Bob sees Alice's grade! Bug!

# ✅ Correct — create a new list for EACH instance in __init__
class Student:
    def __init__(self):
        self.grades = []    # instance variable — each student gets their own list

    def add_grade(self, grade):
        self.grades.append(grade)

alice = Student()
bob = Student()
alice.add_grade(90)
print(bob.grades)   # [] ← Bob's list is empty, as expected
```

**Why it happens:** Mutable class variables are shared — mutations (`.append()`, `.update()`) modify the shared object in place without triggering shadowing.

---

### ❌ Mistake 3: Using `@classmethod` When You Need `@staticmethod` (and Vice Versa)

```python
# ❌ Wrong — static-like utility function declared as classmethod
class MathUtils:
    @classmethod
    def add(cls, a, b):     # cls is never used — wasteful
        return a + b

# ❌ Wrong — factory method (needs cls for subclass support) declared as static
class Shape:
    @staticmethod
    def from_string(s):     # can't use cls — breaks inheritance!
        return Shape()      # hardcoded Shape — subclasses get wrong type

# ✅ Correct — pure utility with no class/instance needs → @staticmethod
class MathUtils:
    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

# ✅ Correct — factory/constructor method → @classmethod (supports inheritance)
class Shape:
    @classmethod
    def from_string(cls, s: str) -> "Shape":
        # cls = Circle if called on Circle, Shape if called on Shape
        return cls()
```

---

### ❌ Mistake 4: Calling Instance Methods Without an Instance

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

# ❌ Wrong — calling on the class, not an instance
Counter.increment()     # TypeError: increment() missing 1 required positional argument: 'self'

# ✅ Correct
c = Counter()           # create an instance first
c.increment()           # call on the instance
print(c.count)          # 1

# Alternatively — unbound call (advanced, rarely used)
Counter.increment(c)    # explicitly pass the instance — works but unusual
```

---

### ❌ Mistake 5: Not Returning `self` for Method Chaining

```python
# ❌ Wrong — can't chain methods because deposit returns None
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        # returns None implicitly

alice = BankAccount(100)
# alice.deposit(50).deposit(50)  # AttributeError: 'NoneType' has no attribute 'deposit'

# ✅ Correct — return self to enable fluent/builder pattern
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount: float) -> "BankAccount":
        self.balance += amount
        return self     # return self for chaining

    def withdraw(self, amount: float) -> "BankAccount":
        self.balance -= amount
        return self

alice = BankAccount(100)
alice.deposit(50).deposit(50).withdraw(30)  # method chaining!
print(alice.balance)    # 170
```

---

## 5. Hands-on Exercises

### 🧑‍🏫 Guided Exercise 1: Build the Complete BankAccount Class

**Goal:** Build the BankAccount class step by step, testing at each stage.

**Step 1 — Skeleton and `__init__`:**
```python
class BankAccount:
    bank_name = "Python National Bank"
    interest_rate = 0.035
    _account_counter = 0

    def __init__(self, owner: str, initial_balance: float = 0.0):
        BankAccount._account_counter += 1
        self.account_number = BankAccount._account_counter
        self.owner = owner
        self.balance = initial_balance

    def __str__(self):
        return f"Account #{self.account_number} | {self.owner} | ${self.balance:,.2f}"

# Test Step 1
a1 = BankAccount("Alice", 1000)
a2 = BankAccount("Bob", 2000)
print(a1)       # Account #1 | Alice | $1,000.00
print(a2)       # Account #2 | Bob | $2,000.00
print(BankAccount._account_counter)     # 2
```

**Step 2 — Instance methods:**
```python
def deposit(self, amount: float) -> float:
    if amount <= 0:
        raise ValueError("Amount must be positive")
    self.balance += amount
    return self.balance

def withdraw(self, amount: float) -> float:
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if amount > self.balance:
        raise ValueError("Insufficient funds")
    self.balance -= amount
    return self.balance

def get_balance(self) -> float:
    return self.balance

# Test Step 2
a1.deposit(500)
a1.withdraw(200)
print(a1.get_balance())     # 1300.0
```

**Step 3 — Class method (factory):**
```python
@classmethod
def create_savings_account(cls, owner: str, initial_balance: float = 0.0):
    account = cls(owner, initial_balance)
    account.account_type = "savings"
    account.interest_rate = cls.interest_rate + 0.01
    return account

# Test Step 3
savings = BankAccount.create_savings_account("Carol", 5000)
print(savings.account_type)     # savings
print(savings.interest_rate)    # 0.045
print(BankAccount.interest_rate)# 0.035 — class var unchanged
```

**Step 4 — Static methods:**
```python
@staticmethod
def validate_account_number(num: int) -> bool:
    return isinstance(num, int) and num > 0

@staticmethod
def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"

# Test Step 4
print(BankAccount.validate_account_number(1001))    # True
print(BankAccount.validate_account_number(-5))      # False
print(BankAccount.format_currency(1234.5))          # $1,234.50
```

**Discussion questions:**
- Why does `savings.interest_rate` not change `BankAccount.interest_rate`?
- What happens if we call `BankAccount.deposit(100)` (no instance)?

---

### 🧑‍🏫 Guided Exercise 2: Observing Class vs Instance State

**Goal:** Run this experiment live and explain every output.

```python
class Counter:
    count = 0           # class variable — shared
    instances = []      # ❌ mutable class variable — DANGER!

    def __init__(self, name: str):
        Counter.count += 1          # correct: modify class var via class name
        self.name = name
        self.personal_count = 0     # instance variable — unique per instance
        Counter.instances.append(self.name)     # modifying shared mutable!

    def increment(self):
        self.personal_count += 1
        Counter.count += 1

    def show(self):
        print(f"{self.name}: personal={self.personal_count}, total={Counter.count}")

c1 = Counter("Alpha")
c2 = Counter("Beta")
c3 = Counter("Gamma")

c1.increment()
c1.increment()
c2.increment()

c1.show()       # Alpha: personal=2, total=5 (3 from inits + 2 from increments)
c2.show()       # Beta:  personal=1, total=5
c3.show()       # Gamma: personal=0, total=5

print(Counter.count)        # 5 — all increments shared
print(Counter.instances)    # ['Alpha', 'Beta', 'Gamma'] — shared list

# Now observe shadowing
c1.count = 99   # creates INSTANCE variable on c1
c1.show()       # still shows Counter.count internally — the show() method uses Counter.count
print(c1.count)         # 99 — c1's own var
print(c2.count)         # 5  — c2 still uses class var
print(Counter.count)    # 5  — class var unchanged
```

**Key observations to discuss:**
1. `Counter.count` tracks ALL increments from ALL instances
2. Mutable `instances = []` is shared and accumulates all instance names
3. `c1.count = 99` shadows the class variable for c1 only
4. Inside methods, `Counter.count` (class name) always finds the class variable

---

### 💻 Independent Practice 1: Library Book System

**Task:** Implement a `Book` class for a library management system.

```python
class Book:
    """
    Represents a library book.

    Class variables:
    - library_name: str = "City Public Library"
    - total_books: int (auto-increments)

    Instance variables:
    - title, author, isbn, is_available (bool), borrow_count

    Instance methods:
    - borrow() → marks unavailable, increments borrow_count
    - return_book() → marks available
    - get_info() → returns formatted string

    Class method:
    - from_isbn(cls, isbn: str, title: str, author: str) → Book
      (alternative constructor — creates book from ISBN lookup)

    Static method:
    - is_valid_isbn(isbn: str) → bool
      (ISBN-13: exactly 13 digits)
    """
    # Your implementation here
    pass


# Test your implementation
book1 = Book("Python Crash Course", "Eric Matthes", "9781593279288")
book2 = Book("Clean Code", "Robert Martin", "9780132350884")

print(book1.get_info())
print(Book.total_books)         # 2

book1.borrow()
print(book1.is_available)       # False
book1.return_book()
print(book1.is_available)       # True
print(book1.borrow_count)       # 1

print(Book.is_valid_isbn("9781593279288"))   # True
print(Book.is_valid_isbn("123"))            # False

book3 = Book.from_isbn("9780201633610", "Design Patterns", "Gang of Four")
print(book3.title)              # Design Patterns
print(Book.total_books)         # 3
```

> **Hints:** Use `str.isdigit()` and `len()` for ISBN validation. `borrow_count` starts at 0. `from_isbn` is just an alias constructor here.

---

### 💻 Independent Practice 2: Temperature Converter

**Task:** Build a `Temperature` class with multiple unit representations.

```python
class Temperature:
    """
    Represents a temperature that can be converted between units.

    Instance variables:
    - _celsius: float (internal storage — always in Celsius)

    Properties (use @property for these):
    - celsius → float
    - fahrenheit → float (C × 9/5 + 32)
    - kelvin → float (C + 273.15)

    Class method:
    - from_fahrenheit(cls, f: float) → Temperature
    - from_kelvin(cls, k: float) → Temperature

    Static method:
    - is_valid_celsius(value: float) → bool (>= -273.15, absolute zero)

    Instance method:
    - __str__ → "25.00°C / 77.00°F / 298.15K"
    - __repr__ → "Temperature(celsius=25.0)"
    - __eq__, __lt__ (for comparisons)
    """
    # Your implementation here
    pass


# Tests
t1 = Temperature(100)               # boiling point in Celsius
print(t1.fahrenheit)                # 212.0
print(t1.kelvin)                    # 373.15
print(str(t1))                      # 100.00°C / 212.00°F / 373.15K

t2 = Temperature.from_fahrenheit(32)
print(t2.celsius)                   # 0.0 (freezing point)

t3 = Temperature.from_kelvin(0)
print(t3.celsius)                   # -273.15 (absolute zero)

print(Temperature.is_valid_celsius(-300))   # False
print(Temperature.is_valid_celsius(0))      # True

# Comparisons
print(Temperature(100) > Temperature(0))   # True
print(Temperature(0) == Temperature.from_fahrenheit(32))  # True
```

> **Hints:** Store everything as Celsius internally. `@property` makes attribute access feel natural. For `from_fahrenheit`: Celsius = (F - 32) × 5/9.

---

### 🏆 Challenge Problem: Inventory Management System

```python
"""
Build an Inventory Management System with two classes:

1. Product class:
   - Class vars: category_tax_rates = {"electronics": 0.18, "food": 0.05, "clothing": 0.12}
   - Instance vars: name, sku, price, quantity, category
   - Instance methods: apply_discount(pct), add_stock(qty), sell(qty)
   - Class method: from_dict(cls, data: dict) → Product (factory from dict)
   - Static method: generate_sku(name, category) → str (e.g., "ELEC-LAPT-001")
   - Property: total_value (price × quantity)
   - Property: price_with_tax

2. Inventory class:
   - Class var: _all_inventories = [] (track all created inventories)
   - Instance vars: name, _products = {}  (sku → Product)
   - Instance methods:
     - add_product(product)
     - remove_product(sku)
     - get_product(sku) → Optional[Product]
     - search(query: str) → list[Product] (search by name)
     - low_stock_report(threshold=5) → list[Product]
     - total_inventory_value() → float
     - category_summary() → dict (category → total value)
   - Class method: get_all_inventories() → list
   - Static method: merge(inv1, inv2) → Inventory

Run with:
    inv = Inventory("Main Warehouse")
    laptop = Product("Laptop Pro", 75000, 10, "electronics")
    inv.add_product(laptop)
    inv.add_product(Product("Rice 5kg", 250, 100, "food"))
    print(inv.total_inventory_value())
    print(inv.category_summary())
    print(inv.low_stock_report(threshold=15))
"""
```

---

## 6. Best Practices & Industry Standards

### Naming Conventions (PEP 8)

```python
class BankAccount:          # ✅ CamelCase for class names
    bank_name = "..."       # ✅ snake_case for class variables
    MAX_WITHDRAWAL = 10000  # ✅ UPPER_SNAKE for constants

    def __init__(self):
        self.account_number = 1     # ✅ snake_case for instance variables
        self._balance = 0           # ✅ single underscore = private by convention
        self.__pin = None           # ⚠️  double underscore = name mangling (use sparingly)

    def get_balance(self):          # ✅ snake_case for methods
        return self._balance

    def _validate(self):            # ✅ private helper — single underscore
        pass
```

---

### Property vs Direct Attribute Access

```python
# ✅ Use @property for computed attributes and validation
class Circle:
    def __init__(self, radius: float):
        self._radius = radius   # store privately

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self) -> float:
        """Computed property — no setter needed."""
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(c.radius)     # 5  — looks like attribute access
print(c.area)       # 78.54... — computed on demand
c.radius = 10       # triggers the setter with validation
# c.radius = -1     # ValueError!
```

---

### `__repr__` vs `__str__`

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        """
        Unambiguous — for developers/debugging.
        Ideally: repr(obj) == eval(repr(obj)) recreates the object.
        """
        return f"Product(name={self.name!r}, price={self.price})"

    def __str__(self) -> str:
        """
        Readable — for end users.
        Falls back to __repr__ if not defined.
        """
        return f"{self.name} — ${self.price:.2f}"

p = Product("Widget", 29.99)
print(p)            # Widget — $29.99        ← __str__
print(repr(p))      # Product(name='Widget', price=29.99) ← __repr__
print([p])          # [Product(name='Widget', price=29.99)] ← lists use __repr__
```

---

### What Professionals Do

```python
# ✅ Use dataclasses for simple data containers (Day 6 preview)
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    age: int
    grades: list[float] = field(default_factory=list)
    # Auto-generates __init__, __repr__, __eq__ for free!

# ✅ Use __slots__ for memory efficiency in high-volume classes
class Point:
    __slots__ = ['x', 'y']     # restrict to only these attributes
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ✅ Guard mutable defaults with field(default_factory=...)
# ✅ Type hint everything
# ✅ Document with docstrings (class + all public methods)
# ✅ Keep __init__ simple — just assign; complex logic goes in class methods
# ✅ Single Responsibility Principle — one class, one job
```

---

## 7. Real-World Application

### Django Models ARE Python Classes

```python
# Django's ORM uses OOP principles directly
# Every Django model is a Python class (Day 20+ preview)

from django.db import models

class Product(models.Model):
    """Django model = Python class with ORM superpowers."""

    # Class variables → database columns
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]         # inner class — Django metadata
        verbose_name_plural = "products"

    # Instance methods — work exactly like our BankAccount methods
    def is_in_stock(self) -> bool:
        return self.stock > 0

    def apply_discount(self, percent: float) -> None:
        self.price *= (1 - percent / 100)
        self.save()     # Django's save() persists to DB

    # Class method = Django Manager method (queryset operations)
    @classmethod
    def get_by_category(cls, category: str):
        return cls.objects.filter(category=category)

    def __str__(self) -> str:
        return f"{self.name} (${self.price})"
```

### Class-Based Views in Django

```python
# Django Class-Based Views use OOP inheritance directly
from django.views import View
from django.http import JsonResponse

class ProductView(View):
    """Each HTTP method maps to a method on the class."""

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return JsonResponse({"name": product.name, "price": str(product.price)})

    def post(self, request):
        # create new product
        pass

    def delete(self, request, product_id):
        # delete product
        pass
```

### 🔭 Connection to Upcoming Days
- **Day 6:** OOP Advanced — Inheritance, `super()`, multiple inheritance, MRO, `@property`, `@abstractmethod`, dataclasses
- **Day 7:** Dunder methods — `__len__`, `__iter__`, `__getitem__`, `__eq__`, `__hash__` for custom containers
- **Day 8:** Decorators — `@classmethod`, `@staticmethod`, `@property` are just decorators; you'll build your own
- **Day 20:** Django Models — class variables map to DB columns; `save()`, `delete()`, `objects.filter()` are instance/class methods

---

## 8. Quick Revision Summary

### Key Terms

| Term | One-line Definition |
|------|---------------------|
| Class | Blueprint/template that defines the structure and behavior of objects |
| Object / Instance | A concrete entity created from a class; occupies memory |
| `__init__` | Constructor — initializes an object's state after creation |
| `__new__` | Allocates memory for an object before `__init__` runs (rarely overridden) |
| Instance variable | Attribute unique to each object, defined via `self.name` |
| Class variable | Attribute shared by all instances of a class |
| Instance method | Function on a class that receives `self` as first argument |
| `@classmethod` | Method that receives the class (`cls`) as first argument; used for factory methods |
| `@staticmethod` | Method that receives neither `self` nor `cls`; pure utility function |
| Encapsulation | Bundling data and methods; hiding internal state |
| Abstraction | Exposing only necessary interface; hiding implementation complexity |
| Inheritance | A class deriving behavior from another class (`class Child(Parent)`) |
| Polymorphism | Different classes responding to the same interface in different ways |
| `self` | Reference to the current instance; passed automatically by Python |
| Shadowing | Creating an instance variable with the same name as a class variable |
| `@property` | Decorator that makes a method callable like an attribute |
| `__repr__` | Unambiguous string for developers/debugging |
| `__str__` | User-friendly string for display |

---

### Core Syntax Cheat Sheet

```python
# ── Class definition ────────────────────────────────────────────────────────
class MyClass:
    class_var = "shared"                # class variable

    def __init__(self, value):          # constructor
        self.instance_var = value       # instance variable
        self._private = None            # private by convention

    # ── Instance method ───────────────────────────────────────────────────
    def method(self):
        return self.instance_var

    # ── Class method ──────────────────────────────────────────────────────
    @classmethod
    def from_string(cls, s: str) -> "MyClass":
        return cls(s)                   # cls = MyClass (or subclass)

    # ── Static method ─────────────────────────────────────────────────────
    @staticmethod
    def utility(x: int) -> int:
        return x * 2                    # no self, no cls

    # ── Property ──────────────────────────────────────────────────────────
    @property
    def computed(self) -> str:
        return self.instance_var.upper()

    # ── Dunder methods ────────────────────────────────────────────────────
    def __repr__(self): return f"MyClass({self.instance_var!r})"
    def __str__(self): return str(self.instance_var)
    def __eq__(self, other): return self.instance_var == other.instance_var

# ── Usage ───────────────────────────────────────────────────────────────────
obj = MyClass("hello")              # creates instance, calls __init__
obj.method()                        # instance method
MyClass.from_string("world")        # class method — alternative constructor
MyClass.utility(5)                  # static method — no instance needed
print(obj.computed)                 # property — looks like attribute
print(obj)                          # calls __str__
print(repr(obj))                    # calls __repr__
```

---

### 5 MCQ Recap Questions

**Q1.** What is the difference between a class variable and an instance variable?
- A) Class variables are faster to access
- **B) Class variables are shared across all instances; instance variables are unique to each object** ✅
- C) Instance variables must be defined before `__init__`
- D) There is no difference — they're the same thing

**Q2.** What is the first argument of a `@classmethod`?
- A) `self` — the instance
- **B) `cls` — the class itself** ✅
- C) Nothing — class methods take no automatic argument
- D) `super` — the parent class

**Q3.** When should you use `@staticmethod`?
- A) When you need access to instance variables
- B) When you want to modify the class
- C) When you need to create alternative constructors
- **D) When the method is a utility function logically related to the class but needs neither instance nor class data** ✅

**Q4.** What happens when you assign `self.class_variable = new_value` inside an instance method?
- A) It modifies the class variable for all instances
- B) It raises an AttributeError
- **C) It creates a new instance variable that shadows the class variable for that specific object** ✅
- D) It raises a TypeError

**Q5.** What is the purpose of `__repr__`?
- A) It runs when the object is deleted
- B) It's called by `print()` to display the object
- **C) It provides an unambiguous developer-friendly string representation, ideally one that could recreate the object** ✅
- D) It's called instead of `__init__` for object creation

---

## 9. Instructor Notes

### 📌 Anticipated Student Questions

| Question | Suggested Answer |
|----------|-----------------|
| "Why does Python need `self` explicitly? Other languages don't." | By design — "explicit is better than implicit" (Zen of Python). It makes the code clear that `self.balance` is an instance attribute, not a local variable. Java/C++ hide `this` implicitly, which can cause confusion. |
| "What's the difference between `__str__` and `__repr__`?" | `__str__` is for end users (`print(obj)`). `__repr__` is for developers/debugging (REPL, logging). If only `__repr__` is defined, `print()` falls back to it. |
| "When exactly do I use `@classmethod` vs `@staticmethod`?" | `@classmethod` when you need `cls` — alternative constructors, factory methods. `@staticmethod` when the function belongs conceptually to the class but needs zero access to instance or class state. |
| "Can I change a class variable from an instance?" | Yes, but `self.class_var = value` creates an instance variable that shadows it — it does NOT change the class variable. Use `ClassName.class_var = value` or `cls.class_var = value` to change the class variable. |
| "Is `self` a keyword?" | No — it's a convention. You could name it `this` or `me`. But NEVER do it — `self` is universal, expected by every Python developer and tool. |
| "What's `__new__`? Do I need it?" | It allocates memory before `__init__` runs. You almost never need to override it — only in advanced patterns like Singleton, metaclasses, or immutable types. |
| "What's the difference between a method and a function?" | A function stands alone. A method is a function defined inside a class and associated with instances of that class. |

---

### 📚 Resources & Further Reading

- [Python Docs — Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python Docs — `dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [Real Python — OOP in Python](https://realpython.com/python3-object-oriented-programming/)
- [Real Python — `@classmethod` vs `@staticmethod`](https://realpython.com/instance-class-and-static-methods-an-overview/)
- [Real Python — Python `__repr__` vs `__str__`](https://realpython.com/python-repr-vs-str/)
- [PEP 8 — Class naming conventions](https://peps.python.org/pep-0008/#class-names)
- [Raymond Hettinger — Python's Class Development Toolkit (PyCon)](https://www.youtube.com/watch?v=HTLu2DFOdTg) ← must-watch
- [Python Tutor](https://pythontutor.com/) ← visualize object creation and instance/class variable separation
