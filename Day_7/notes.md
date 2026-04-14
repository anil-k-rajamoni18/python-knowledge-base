# 🐍 Python Full Stack — Day 7 of 35
# Topic: Encapsulation & Abstraction
**Audience:** Beginner | **Duration:** 3 Hours | **Track:** Python → Django/Flask → Frontend → Deployment

---

## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, learners will be able to:
- Implement the three levels of access control in Python (`public`, `_protected`, `__private`) and explain name mangling
- Use `@property`, `@setter`, and `@deleter` decorators to build clean, validated attribute access
- Create abstract base classes with `ABC` and `@abstractmethod` to define enforced contracts
- Explain the difference between abstract classes and informal protocols (duck typing)
- Design classes that hide internal complexity and expose only what users need

### 📋 Prerequisites (Days 1–6 Review)
- Python data types, functions (Days 1–3)
- Modules, packages (Day 4)
- OOP — classes, `__init__`, instance variables, three method types (Day 5)
- Inheritance, `super()`, polymorphism, MRO (Day 6)

### 🔗 Connection to the Full Stack Journey
- **Django Models (Day 20+):** Django uses `@property` everywhere — `user.full_name`, `product.is_in_stock` are computed properties on model classes
- **Django REST Framework (Day 24+):** `SerializerMethodField` uses the property pattern; access control determines what fields APIs expose
- **Django Forms (Day 22+):** Form validation in `clean_<fieldname>()` methods mirrors setter validation patterns
- **Flask (Day 18+):** Flask's `current_user.is_authenticated` is a property on the User model
- **Abstract classes (Day 9+):** Django's `Model`, `View`, `Form` are all abstract-like base classes — understanding this today makes Day 20+ instantly familiar

---

## 2. Concept Explanation

### 2.1 Encapsulation — Bundling and Protecting

**The "Why":** Encapsulation means two things:
1. **Bundling** — keeping data (attributes) and the methods that operate on it together inside a class (we covered this in Day 5)
2. **Access control** — deciding WHO can read or change the data

Without access control, any code anywhere can reach into your object and corrupt its state:
```python
account = BankAccount("Alice", 1000)
account.balance = -99999    # anyone can do this — breaks the contract!
```

With encapsulation:
```python
account._balance = 1000     # protected — "please don't touch directly"
account.__balance = 1000    # private — Python actively helps enforce this
```

**Real-world analogy:** Think of a car's dashboard. You see the speedometer, fuel gauge, and radio (the public interface). You don't see the engine internals — fuel injectors, pistons, transmission gears (the private implementation). The car maker encapsulates the engine complexity. You drive through a clean interface. If you could directly touch the fuel injectors while driving, you'd break the engine.

---

### 2.2 Python's Three Access Levels

Python doesn't have `private`/`public` keywords like Java. It uses a **naming convention system**:

| Prefix | Convention | Enforcement | Example |
|--------|-----------|-------------|---------|
| No prefix | **Public** — anyone can access | None | `self.name` |
| `_` (single) | **Protected** — for internal use, subclasses OK | Convention only | `self._balance` |
| `__` (double) | **Private** — name mangling applied | Python renames it | `self.__pin` |

**The single underscore `_variable`:**
- A "gentleman's agreement" — "I marked this as internal, please don't use it from outside"
- Python does NOT enforce this — it's purely a signal to other developers
- Subclasses CAN access it (intentionally)
- Used for internal implementation details, helper attributes

**The double underscore `__variable` — Name Mangling:**
- Python renames `self.__pin` to `self._ClassName__pin` automatically
- Accessing `obj.__pin` from outside the class raises `AttributeError`
- Designed to prevent accidental overriding in subclasses, not for strong security
- You CAN still access it via `obj._ClassName__pin` — Python is honest about this

**Important: Python philosophy says "we're all consenting adults"** — there's no truly unbreakable private. The conventions are about communication and accidental access prevention, not security walls.

---

### 2.3 Property Decorators — The Professional Way to Add Access Control

**The "Why":** Initially you might write:
```python
class Circle:
    def __init__(self, radius):
        self.radius = radius    # direct attribute — no validation
```

Later you need to add validation (radius can't be negative). If you change `radius` to a method, all existing code breaks:
```python
circle.radius = 5       # was attribute
circle.set_radius(5)    # now method — breaks all callers!
```

`@property` solves this elegantly — you add validation without changing the public interface:
```python
@property
def radius(self): return self._radius      # still accessed as circle.radius

@radius.setter
def radius(self, value):                   # still assigned as circle.radius = 5
    if value < 0: raise ValueError(...)
```

**The three decorators:**
- `@property` — creates a **getter** (called when you READ `obj.attr`)
- `@attr.setter` — creates a **setter** (called when you WRITE `obj.attr = value`)
- `@attr.deleter` — creates a **deleter** (called when you `del obj.attr`)

---

### 2.4 Abstraction with Abstract Base Classes

**The "Why":** Abstraction means showing only what's necessary, hiding what's complex.

At the class design level, abstraction means defining **what a class must do** (interface/contract) without defining **how it does it**.

**Analogy:** Think of a USB port standard. Every USB device must implement: power delivery, data transfer, device identification. The USB standard doesn't say *how* a mouse implements these — it just says every USB device *must* implement them. `ABC` + `@abstractmethod` is Python's way of defining such standards for classes.

```python
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):   # the "USB standard"
    @abstractmethod
    def process_payment(self, amount): ...   # every processor MUST implement this

class StripeProcessor(PaymentProcessor):    # a specific "USB device"
    def process_payment(self, amount):       # implements the required method
        ...
```

**Key rules:**
1. Abstract classes **cannot be instantiated** directly
2. Subclasses **must** implement ALL abstract methods — or they also become abstract
3. Abstract classes CAN have concrete (non-abstract) methods — shared behavior
4. An abstract class can define abstract properties too

---

### 2.5 Interfaces vs Abstract Classes

**In Python, there's no separate `interface` keyword** (unlike Java/C#). We have two approaches:

| Approach | Tool | Enforcement | Best For |
|----------|------|-------------|----------|
| Formal contract | `ABC` + `@abstractmethod` | Enforced at instantiation | Class hierarchies where IS-A matters |
| Informal protocol | Duck typing | No enforcement | Flexible code, any object that "quacks" |
| Structural protocol | `typing.Protocol` (PEP 544) | Checked by type checkers | Modern type-checked codebases |

**Duck typing (Days 6 recap):** Works without any formal declaration. If an object has the method, use it.

**`Protocol` (modern Python 3.8+):** Defines a structural interface. A class "implements" it by having the right methods — no inheritance needed. Type checkers like `mypy` verify it statically.

---

## 3. Syntax & Code Examples

### 3.1 Access Level Demonstration

```python
class BankAccount:
    bank_name = "Python Bank"       # public class variable

    def __init__(self, owner: str, balance: float, pin: int):
        self.owner = owner          # public — intended for anyone to read
        self._balance = balance     # protected — internal, subclasses OK
        self.__pin = pin            # private — name-mangled to _BankAccount__pin

    def get_balance(self):
        """Public method — safe to call from anywhere."""
        return self._balance

    def _calculate_interest(self):
        """Protected — internal helper, subclasses may override."""
        return self._balance * 0.04

    def __validate_pin(self, entered_pin: int) -> bool:
        """Private — only called internally, never from outside."""
        return self.__pin == entered_pin

    def withdraw(self, amount: float, pin: int) -> float:
        """Public method that uses private validation internally."""
        if not self.__validate_pin(pin):
            raise ValueError("Invalid PIN")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        return self._balance


# ── Usage ──────────────────────────────────────────────────────────────────
acc = BankAccount("Alice", 5000, 1234)

# Public access — works fine
print(acc.owner)            # Alice
print(acc.get_balance())    # 5000

# Protected access — works (but you're breaking the convention)
print(acc._balance)         # 5000 — works, but signaled as "don't do this"

# Private access — direct access FAILS
try:
    print(acc.__pin)        # AttributeError: no attribute '__pin'
except AttributeError as e:
    print(f"Direct access: {e}")

# Private access — name mangling reveals the real name
print(acc._BankAccount__pin)   # 1234 — works, but you're really not supposed to!

# Normal usage through the public interface
acc.withdraw(1000, 1234)    # works
try:
    acc.withdraw(500, 9999) # Invalid PIN — raises ValueError
except ValueError as e:
    print(f"Blocked: {e}")

print(acc.get_balance())    # 4000
```

**Output:**
```
Alice
5000
5000
Direct access: 'BankAccount' object has no attribute '__pin'
1234
Blocked: Invalid PIN
4000
```

---

### 3.2 Name Mangling in Inheritance

```python
class Parent:
    def __init__(self):
        self.__secret = "parent_secret"   # mangled to _Parent__secret

    def reveal(self):
        return self.__secret              # uses _Parent__secret internally

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__secret = "child_secret"    # mangled to _Child__secret — DIFFERENT!

    def child_reveal(self):
        return self.__secret              # uses _Child__secret

child = Child()
print(child.reveal())           # parent_secret  — Parent's method uses _Parent__secret
print(child.child_reveal())     # child_secret   — Child's method uses _Child__secret

# Both attributes coexist independently because mangling uses class name
print(child._Parent__secret)    # parent_secret
print(child._Child__secret)     # child_secret
print(child.__dict__)
# {'_Parent__secret': 'parent_secret', '_Child__secret': 'child_secret'}
```

> **This is exactly why name mangling exists** — it prevents child classes from accidentally overriding parent's private attributes. Both can have `__secret` independently.

---

### 3.3 `@property` — All Three Decorators

```python
class Temperature:
    """Demonstrates all three property decorators."""

    def __init__(self, celsius: float = 0.0):
        self._celsius = celsius     # private storage

    # ── @property — GETTER ────────────────────────────────────────────────
    @property
    def celsius(self) -> float:
        """Read temperature in Celsius."""
        return self._celsius

    # ── @celsius.setter — SETTER with validation ─────────────────────────
    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set temperature — validates it's above absolute zero."""
        if value < -273.15:
            raise ValueError(f"Temperature cannot be below absolute zero: {value}")
        self._celsius = value

    # ── @celsius.deleter — DELETER ────────────────────────────────────────
    @celsius.deleter
    def celsius(self) -> None:
        """Reset temperature to 0."""
        print("Resetting temperature to 0°C")
        self._celsius = 0.0

    # ── Computed property (no setter — read-only) ─────────────────────────
    @property
    def fahrenheit(self) -> float:
        """Computed from celsius — no separate storage needed."""
        return self._celsius * 9 / 5 + 32

    @property
    def kelvin(self) -> float:
        """Another computed property."""
        return self._celsius + 273.15

    # ── fahrenheit setter — set via fahrenheit, stores as celsius ─────────
    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5 / 9    # uses celsius setter (with validation!)

    def __str__(self) -> str:
        return f"{self.celsius:.1f}°C / {self.fahrenheit:.1f}°F / {self.kelvin:.2f}K"


# ── Usage ──────────────────────────────────────────────────────────────────
t = Temperature(25)

# Accessing properties looks like attribute access
print(t.celsius)        # 25.0      ← calls @property getter
print(t.fahrenheit)     # 77.0      ← computed getter
print(t.kelvin)         # 298.15    ← computed getter
print(t)                # 25.0°C / 77.0°F / 298.15K

# Setting through setter — looks like assignment
t.celsius = 100         # calls @celsius.setter
print(t)                # 100.0°C / 212.0°F / 373.15K

# Set via fahrenheit — goes through setter which stores as celsius
t.fahrenheit = 32       # calls @fahrenheit.setter → stores as 0°C
print(t)                # 0.0°C / 32.0°F / 273.15K

# Validation in setter
try:
    t.celsius = -300    # below absolute zero — raises ValueError
except ValueError as e:
    print(f"Validation: {e}")

# Deleter
del t.celsius           # calls @celsius.deleter
print(t)                # 0.0°C / 32.0°F / 273.15K

# Read-only: no setter for kelvin
try:
    t.kelvin = 300      # AttributeError — no setter defined
except AttributeError as e:
    print(f"Read-only: {e}")
```

---

### 3.4 Secure BankAccount with Properties

```python
from datetime import datetime


class SecureBankAccount:
    """
    Demonstrates encapsulation with private attributes and property decorators.
    """
    _interest_rate: float = 0.04    # protected class variable

    def __init__(self, owner: str, balance: float, pin: int):
        # Validate at construction time
        self.__owner = self.__validate_owner(owner)
        self.__balance = self.__validate_amount(balance, "Initial balance")
        self.__pin = pin
        self.__transaction_history: list[dict] = []
        self.__failed_attempts: int = 0
        self.__locked: bool = False

    # ── Private validation helpers ─────────────────────────────────────────
    @staticmethod
    def __validate_owner(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Owner must be a non-empty string")
        return name.strip()

    @staticmethod
    def __validate_amount(amount: float, label: str = "Amount") -> float:
        if not isinstance(amount, (int, float)):
            raise TypeError(f"{label} must be numeric")
        if amount < 0:
            raise ValueError(f"{label} cannot be negative")
        return float(amount)

    def __verify_pin(self, entered: int) -> bool:
        """Checks PIN and manages lockout after 3 failed attempts."""
        if self.__locked:
            raise RuntimeError("Account locked — too many failed attempts. Contact support.")
        if self.__pin == entered:
            self.__failed_attempts = 0
            return True
        self.__failed_attempts += 1
        if self.__failed_attempts >= 3:
            self.__locked = True
            raise RuntimeError("Account locked after 3 failed PIN attempts!")
        remaining = 3 - self.__failed_attempts
        raise ValueError(f"Invalid PIN. {remaining} attempt(s) remaining.")

    # ── Public read-only property for owner ───────────────────────────────
    @property
    def owner(self) -> str:
        return self.__owner

    # ── Balance: read-only from outside, writable via deposit/withdraw ─────
    @property
    def balance(self) -> float:
        """Balance is read-only — use deposit()/withdraw() to change it."""
        return self.__balance

    # ── PIN change: secured, validated ────────────────────────────────────
    def change_pin(self, current_pin: int, new_pin: int) -> None:
        """Allows PIN change after verifying the current PIN."""
        self.__verify_pin(current_pin)
        if not isinstance(new_pin, int) or new_pin < 1000 or new_pin > 9999:
            raise ValueError("PIN must be a 4-digit integer (1000–9999)")
        self.__pin = new_pin
        print("✅ PIN changed successfully.")

    # ── Public transactional methods ──────────────────────────────────────
    def deposit(self, amount: float) -> float:
        """Deposit — no PIN needed (anyone can deposit into your account)."""
        amount = self.__validate_amount(amount, "Deposit amount")
        if amount == 0:
            raise ValueError("Deposit amount must be greater than 0")
        self.__balance += amount
        self.__log("deposit", amount)
        return self.__balance

    def withdraw(self, amount: float, pin: int) -> float:
        """Withdraw — requires PIN verification."""
        self.__verify_pin(pin)                  # raises if invalid
        amount = self.__validate_amount(amount, "Withdrawal amount")
        if amount > self.__balance:
            raise ValueError(f"Insufficient funds (balance: ${self.__balance:,.2f})")
        self.__balance -= amount
        self.__log("withdrawal", amount)
        return self.__balance

    def get_statement(self, pin: int) -> str:
        """Full statement — requires PIN (sensitive information)."""
        self.__verify_pin(pin)
        lines = [
            f"  Account Owner: {self.__owner}",
            f"  Balance: ${self.__balance:,.2f}",
            f"  Transactions:"
        ]
        for tx in self.__transaction_history[-5:]:
            lines.append(f"    {tx['date']}  {tx['type']}: ${tx['amount']:,.2f}")
        return "\n".join(lines)

    # ── Computed properties ────────────────────────────────────────────────
    @property
    def is_locked(self) -> bool:
        return self.__locked

    @property
    def annual_interest(self) -> float:
        """Computed — what you'd earn in a year at current rate."""
        return self.__balance * self._interest_rate

    # ── Private logging ───────────────────────────────────────────────────
    def __log(self, tx_type: str, amount: float) -> None:
        self.__transaction_history.append({
            "type": tx_type,
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    def __repr__(self) -> str:
        return f"SecureBankAccount(owner={self.__owner!r}, balance={self.__balance:.2f})"

    def __str__(self) -> str:
        return f"[Account] {self.__owner} | ${self.__balance:,.2f}"


# ── Demo ──────────────────────────────────────────────────────────────────
acc = SecureBankAccount("Alice", 5000, 1234)

# Public properties — read-only
print(acc.owner)        # Alice
print(acc.balance)      # 5000.0
print(acc.annual_interest)  # 200.0

# Cannot set balance directly
try:
    acc.balance = 99999     # AttributeError — no setter defined
except AttributeError as e:
    print(f"Protected: {e}")

# Normal operations
acc.deposit(2000)
print(acc.balance)      # 7000.0

acc.withdraw(500, 1234)
print(acc.balance)      # 6500.0

# PIN required for statement
print(acc.get_statement(1234))

# Wrong PIN
try:
    acc.withdraw(100, 9999)
except ValueError as e:
    print(e)    # Invalid PIN. 2 attempt(s) remaining.
```

---

### 3.5 Abstract Base Classes (ABC)

```python
from abc import ABC, abstractmethod
from datetime import datetime


class PaymentProcessor(ABC):
    """
    Abstract base class defining the contract for ALL payment processors.
    Cannot be instantiated directly.
    """

    def __init__(self, processor_name: str):
        self.processor_name = processor_name
        self._transaction_log: list[dict] = []

    # ── Abstract methods — MUST be implemented by subclasses ──────────────
    @abstractmethod
    def process_payment(self, amount: float, recipient: str) -> bool:
        """Process a payment. Returns True if successful."""
        ...

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Issue a refund. Returns True if successful."""
        ...

    # ── Abstract property — subclasses must implement as a property ────────
    @property
    @abstractmethod
    def payment_type(self) -> str:
        """Return the type identifier string (e.g., 'credit_card', 'upi')."""
        ...

    @property
    @abstractmethod
    def transaction_fee(self) -> float:
        """Return the per-transaction fee as a decimal (e.g., 0.02 = 2%)."""
        ...

    # ── Concrete methods — shared implementation, ALL subclasses inherit ──
    def log_transaction(self, tx_id: str, amount: float,
                        recipient: str, status: str) -> None:
        """Concrete — shared logging logic. No need to override."""
        self._transaction_log.append({
            "id": tx_id,
            "amount": amount,
            "recipient": recipient,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "processor": self.processor_name,
        })
        print(f"[LOG] {self.payment_type} | {tx_id} | ${amount:.2f} → {recipient} | {status}")

    def get_fee(self, amount: float) -> float:
        """Calculate fee for a given amount."""
        return amount * self.transaction_fee

    def get_history(self) -> list[dict]:
        return list(self._transaction_log)  # return a copy

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.payment_type!r})"


# ── Concrete implementations ───────────────────────────────────────────────
class CreditCardProcessor(PaymentProcessor):
    def __init__(self):
        super().__init__("CreditCard Gateway")

    @property
    def payment_type(self) -> str:
        return "credit_card"

    @property
    def transaction_fee(self) -> float:
        return 0.025    # 2.5%

    def process_payment(self, amount: float, recipient: str) -> bool:
        fee = self.get_fee(amount)
        tx_id = f"CC-{id(self) % 10000:04d}"
        # Simulate payment processing
        print(f"Processing credit card payment: ${amount:.2f} + ${fee:.2f} fee")
        self.log_transaction(tx_id, amount, recipient, "success")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"Issuing credit card refund for: {transaction_id}")
        return True


class UPIProcessor(PaymentProcessor):
    def __init__(self, upi_id: str):
        super().__init__("UPI Gateway")
        self.upi_id = upi_id

    @property
    def payment_type(self) -> str:
        return "upi"

    @property
    def transaction_fee(self) -> float:
        return 0.0      # UPI is free!

    def process_payment(self, amount: float, recipient: str) -> bool:
        if amount > 100000:
            raise ValueError("UPI limit: ₹1,00,000 per transaction")
        tx_id = f"UPI-{id(self) % 10000:04d}"
        print(f"Processing UPI payment: ₹{amount:.2f} (no fee)")
        self.log_transaction(tx_id, amount, recipient, "success")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"Initiating UPI refund: {transaction_id} (2-3 business days)")
        return True


class CryptoProcessor(PaymentProcessor):
    def __init__(self, wallet_address: str):
        super().__init__("Crypto Gateway")
        self.wallet = wallet_address

    @property
    def payment_type(self) -> str:
        return "cryptocurrency"

    @property
    def transaction_fee(self) -> float:
        return 0.01     # 1% (gas fee)

    def process_payment(self, amount: float, recipient: str) -> bool:
        fee = self.get_fee(amount)
        tx_id = f"CRYPTO-{id(self) % 10000:04d}"
        print(f"Broadcasting crypto tx: ${amount:.2f} + ${fee:.4f} gas fee")
        self.log_transaction(tx_id, amount, recipient, "pending")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"Crypto payments are irreversible. Issuing new payment instead.")
        return False


# ── Cannot instantiate abstract class ─────────────────────────────────────
try:
    p = PaymentProcessor("test")
except TypeError as e:
    print(f"Abstract class blocked: {e}")
# Can't instantiate abstract class PaymentProcessor with abstract methods...

# ── Polymorphism with abstract classes ─────────────────────────────────────
def checkout(processor: PaymentProcessor, amount: float, merchant: str) -> None:
    """Works for ANY PaymentProcessor — that's the contract."""
    print(f"\n--- Checkout via {processor.payment_type} ---")
    fee = processor.get_fee(amount)
    print(f"Amount: ${amount:.2f} | Fee: ${fee:.2f} | Total: ${amount + fee:.2f}")
    success = processor.process_payment(amount, merchant)
    print(f"Status: {'✅ Paid' if success else '❌ Failed'}")


processors = [
    CreditCardProcessor(),
    UPIProcessor("alice@upi"),
    CryptoProcessor("0xABCD1234"),
]

for proc in processors:
    checkout(proc, 1000, "TechStore")
```

---

### 3.6 Protocol (Structural Subtyping — PEP 544)

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    """
    Protocol — defines what a 'Drawable' object must implement.
    No inheritance needed. Just have the right methods.
    """
    def draw(self) -> str: ...
    def get_color(self) -> str: ...


# These classes don't inherit from Drawable or anything
class Circle:
    def draw(self) -> str: return "Drawing a circle ○"
    def get_color(self) -> str: return "red"

class Square:
    def draw(self) -> str: return "Drawing a square □"
    def get_color(self) -> str: return "blue"

class NotDrawable:
    def display(self) -> str: return "I don't have draw()"


def render(item: Drawable) -> None:
    """Type-checked to accept Drawable objects."""
    print(f"{item.get_color()}: {item.draw()}")


# Works without any inheritance declaration!
render(Circle())    # red: Drawing a circle ○
render(Square())    # blue: Drawing a square □

# runtime_checkable allows isinstance with Protocol
print(isinstance(Circle(), Drawable))       # True  — has draw() and get_color()
print(isinstance(NotDrawable(), Drawable))  # False — missing required methods
```

---

## 4. Common Mistakes & Gotchas

### ❌ Mistake 1: Trying to Directly Access `__private` from Outside

```python
class Person:
    def __init__(self, name, ssn):
        self.name = name
        self.__ssn = ssn    # private

p = Person("Alice", "123-45-6789")

# ❌ Wrong
print(p.__ssn)    # AttributeError — '__ssn' doesn't exist as 'p.__ssn'

# ✅ Correct — use the public interface
print(p.name)     # Alice — public attribute

# ✅ (for debugging only) — access via mangled name
print(p._Person__ssn)   # 123-45-6789 — but you're breaking encapsulation!
```

**Why it happens:** Beginners forget name mangling. Python renames `__ssn` to `_Person__ssn` to avoid conflicts in inheritance. Accessing it as `p.__ssn` looks for an attribute literally named `__ssn`, which doesn't exist.

---

### ❌ Mistake 2: Defining `@property` and `@setter` Out of Order or Wrong Name

```python
# ❌ Wrong — setter defined before getter, or wrong name
class Circle:
    @radius.setter           # NameError: name 'radius' is not defined
    def radius(self, value):
        self._radius = value

    @property
    def radius(self):
        return self._radius

# ❌ Wrong — setter name doesn't match property name
class Circle:
    @property
    def radius(self):
        return self._radius

    @rad.setter              # NameError: 'rad' undefined
    def radius(self, value):
        self._radius = value

# ✅ Correct — property FIRST, then @property_name.setter
class Circle:
    @property
    def radius(self):           # 1. Define property first
        return self._radius

    @radius.setter              # 2. Use @radius.setter (same name)
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius can't be negative")
        self._radius = value
```

**Why it happens:** The `@radius.setter` decorator requires `radius` to already exist as a property in the local class namespace. Define the `@property` getter first, always.

---

### ❌ Mistake 3: Forgetting `@abstractmethod` Makes the Class Uninstantiable

```python
# ❌ Confusing — thinking you can instantiate an abstract class
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...

# ❌ Wrong — TypeError at runtime
s = Shape()     # TypeError: Can't instantiate abstract class Shape

# Also wrong — subclass that doesn't implement ALL abstract methods
class IncompleteShape(Shape):
    pass

is_shape = IncompleteShape()    # Still TypeError! Must implement area()

# ✅ Correct — implement ALL abstract methods in the concrete subclass
class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2

c = Circle(5)    # Works!
```

---

### ❌ Mistake 4: Infinite Recursion in Property

```python
# ❌ Wrong — property name == attribute name → infinite recursion!
class Person:
    @property
    def name(self):
        return self.name    # calls the property again → RecursionError!

    @name.setter
    def name(self, value):
        self.name = value   # calls the setter again → RecursionError!

# ✅ Correct — property stores data in a DIFFERENT name (usually prefixed with _)
class Person:
    @property
    def name(self):
        return self._name   # reads from _name (private storage)

    @name.setter
    def name(self, value):
        self._name = value  # writes to _name (private storage)

p = Person()
p.name = "Alice"    # calls setter → stores in _name
print(p.name)       # calls getter → reads from _name
```

**Why it happens:** The property `name` replaces the normal attribute `name`. Writing `self.name = value` inside the setter calls the setter again (not the underlying storage), creating infinite recursion.

---

### ❌ Mistake 5: Making Everything Private (Over-Encapsulation)

```python
# ❌ Wrong — hiding things that should be accessible
class Circle:
    def __init__(self, radius):
        self.__radius = radius      # private

    def __calculate_area(self):     # private — but why?
        return 3.14 * self.__radius ** 2

    def __get_description(self):    # private — but users need this!
        return f"Circle with r={self.__radius}"

c = Circle(5)
c.__calculate_area()    # AttributeError! Can't use from outside

# ✅ Correct — be intentional about what you hide
class Circle:
    def __init__(self, radius):
        self._radius = radius       # protected — subclasses can use

    def area(self) -> float:        # public — users need this
        return 3.14 * self._radius ** 2

    def describe(self) -> str:      # public
        return f"Circle with r={self._radius}"

    def _internal_helper(self):     # protected — for subclasses
        pass

## 5. Hands-on Exercises

### 🧑‍🏫 Guided Exercise 1: Secure BankAccount Step-by-Step

**Goal:** Build a secure bank account from scratch, testing at each stage.

```python
# Step 1: Basic class with private attributes
class BankAccount:
    def __init__(self, owner: str, balance: float, pin: int):
        self.__owner = owner
        self.__balance = balance
        self.__pin = pin

# Test name mangling
acc = BankAccount("Alice", 1000, 1234)
print(acc.__dict__)
# {'_BankAccount__owner': 'Alice', '_BankAccount__balance': 1000, '_BankAccount__pin': 1234}
# Notice: Python renamed everything!


# Step 2: Add @property for balance (read-only from outside)
class BankAccount:
    def __init__(self, owner: str, balance: float, pin: int):
        self.__owner = owner
        self.__balance = float(balance)
        self.__pin = pin

    @property
    def balance(self) -> float:
        return self.__balance

    @property
    def owner(self) -> str:
        return self.__owner

acc = BankAccount("Alice", 1000, 1234)
print(acc.balance)      # 1000.0 — reads via property
try:
    acc.balance = 9999  # AttributeError — no setter!
except AttributeError as e:
    print(f"Protected: {e}")


# Step 3: Add deposit and withdraw with PIN
class BankAccount:
    def __init__(self, owner: str, balance: float, pin: int):
        self.__owner = owner
        self.__balance = float(balance)
        self.__pin = pin

    @property
    def balance(self): return self.__balance

    @property
    def owner(self): return self.__owner

    def __verify_pin(self, pin: int) -> None:
        """Private helper — raises if PIN is wrong."""
        if self.__pin != pin:
            raise ValueError("Invalid PIN")

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount: float, pin: int) -> float:
        self.__verify_pin(pin)              # private call
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        return self.__balance


# Test
acc = BankAccount("Alice", 1000, 1234)
acc.deposit(500)
print(acc.balance)      # 1500.0
acc.withdraw(200, 1234)
print(acc.balance)      # 1300.0

try:
    acc.withdraw(100, 9999)
except ValueError as e:
    print(e)    # Invalid PIN

# Demonstrate __verify_pin name mangling
try:
    acc.__verify_pin(1234)
except AttributeError:
    print("Cannot call __verify_pin from outside — name mangled!")
```

**Discussion questions:**
- Why is `balance` a read-only property rather than a writable attribute?
- What's the difference between `_verify_pin` and `__verify_pin`?
- Could a subclass accidentally overwrite `__balance`? Demonstrate with `__dict__`.

---

### 🧑‍🏫 Guided Exercise 2: Abstract Payment System

**Goal:** Build the abstract payment hierarchy live.

```python
from abc import ABC, abstractmethod

# Step 1: Define the abstract class
class Payment(ABC):
    """Abstract class — contract for all payment types."""

    def __init__(self, currency: str = "INR"):
        self.currency = currency
        self._processed = False

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Must be implemented. Returns True if payment succeeds."""
        ...

    @property
    @abstractmethod
    def payment_type(self) -> str:
        """Must return a string like 'cash', 'card', 'upi'."""
        ...

    # Concrete method — shared by ALL payment types
    def log_transaction(self, amount: float, status: str) -> None:
        print(f"[LOG] {self.payment_type}: {self.currency} {amount:.2f} — {status}")


# Step 2: Test that abstract class can't be instantiated
try:
    p = Payment()
    print("ERROR: Should have raised TypeError!")
except TypeError as e:
    print(f"✅ Correctly blocked: {e}")


# Step 3: Implement concrete subclasses
class CashPayment(Payment):
    @property
    def payment_type(self) -> str:
        return "cash"

    def process_payment(self, amount: float) -> bool:
        print(f"Accepting {self.currency} {amount:.2f} in cash...")
        self.log_transaction(amount, "received")
        self._processed = True
        return True


class UPIPayment(Payment):
    def __init__(self, upi_id: str):
        super().__init__()
        self.upi_id = upi_id

    @property
    def payment_type(self) -> str:
        return "upi"

    def process_payment(self, amount: float) -> bool:
        if amount > 100000:
            self.log_transaction(amount, "failed — limit exceeded")
            return False
        print(f"Sending {self.currency} {amount:.2f} via UPI ({self.upi_id})...")
        self.log_transaction(amount, "success")
        self._processed = True
        return True


# Step 4: Demonstrate polymorphism
def process_order(payment: Payment, amount: float) -> None:
    """Works for ANY Payment subclass."""
    print(f"\nProcessing order via {payment.payment_type}:")
    success = payment.process_payment(amount)
    print(f"Result: {'✅ OK' if success else '❌ Failed'}")


payments = [CashPayment(), UPIPayment("bob@upi")]
for p in payments:
    process_order(p, 999.99)
```

---

### 💻 Independent Practice 1: Student Report Card

**Task:** Build a `Student` class with encapsulation and validation.

```python
"""
Student class with:

Private attributes:
- __name: str
- __grades: list[float] (empty initially)
- __student_id: str

Properties:
- name: str — read-only (set once in __init__)
- student_id: str — read-only
- grades: list — read-only (returns a COPY, not the original list)
- average: float — computed property, returns 0.0 if no grades

Methods:
- add_grade(grade: float) → None
    Validation: grade must be between 0 and 100
- remove_last_grade() → float
    Returns and removes last grade; raises IndexError if empty
- get_report() → str
    Formatted report showing name, ID, all grades, average, letter grade

Static method:
- generate_id() → str: generates a random 6-digit student ID

Rules:
- Name cannot be changed after creation (read-only property)
- Grades list cannot be assigned from outside (read-only, but add_grade works)
- Average is auto-computed, never stored separately
"""

# Hint: use id(self) or uuid for generate_id()
# Hint: return list(self.__grades) in grades property — not self.__grades directly!

# Test:
s = Student("Alice")
print(s.name)           # Alice
print(s.student_id)     # e.g., "STU-482391"
print(s.average)        # 0.0

s.add_grade(85)
s.add_grade(92)
s.add_grade(78)
print(s.grades)         # [85, 92, 78] — a copy
print(s.average)        # 85.0

try:
    s.add_grade(105)    # ValidationError — above 100
except ValueError as e:
    print(e)

# Can't assign grades directly
try:
    s.grades = [100, 100]   # AttributeError — no setter
except AttributeError:
    print("Grades list is protected")

print(s.get_report())
```

> **Hints:** `@property` with no setter = read-only. Return `list(self.__grades)` not `self.__grades` to prevent mutation of the internal list. Use `random.randint(100000, 999999)` for ID generation.

---

### 💻 Independent Practice 2: Abstract Shape Factory

**Task:** Create a shape system using ABC that enforces the full contract.

```python
"""
Shape (ABC)
- @abstractmethod area() → float
- @abstractmethod perimeter() → float
- @abstractproperty name → str
- @abstractproperty color → str
- @color.setter — must allow setting color
- Concrete: describe() → str  (uses name, color, area, perimeter)
- Concrete: scale(factor: float) → Shape  (returns new shape scaled by factor)

Circle(Shape)
- __init__(radius: float, color: str = "white")
- Private __radius with @property and @setter (validate > 0)

Rectangle(Shape)
- __init__(width: float, height: float, color: str = "white")
- Private __width and __height with validation (> 0)

Triangle(Shape)
- __init__(a: float, b: float, c: float, color: str = "white")
- Validate triangle inequality: sum of any two sides > third
- Area using Heron's formula

Required functions:
- total_area(shapes: list) → float (polymorphic)
- largest_shape(shapes: list) → Shape
"""

# Test:
shapes = [Circle(5, "red"), Rectangle(4, 6, "blue"), Triangle(3, 4, 5)]

for s in shapes:
    print(s.describe())

# Polymorphism
print(f"Total area: {total_area(shapes):.2f}")
print(f"Largest: {largest_shape(shapes).describe()}")

# scale() returns a new shape
big_circle = shapes[0].scale(2)
print(big_circle.describe())   # Circle, radius=10, area=314.16
```

> **Hints:** Heron's formula: `s = (a+b+c)/2; area = sqrt(s*(s-a)*(s-b)*(s-c))`. Abstract property + setter requires both `@property @abstractmethod` and `@color.setter`.

---

### 🏆 Challenge Problem: Plugin-Based Payment Gateway

```python
"""
Build a complete payment gateway system:

1. Abstract BaseProcessor(ABC):
   - @abstractmethod process(amount, recipient) → dict  (returns status dict)
   - @abstractmethod validate(amount) → bool
   - @abstractproperty name → str
   - @abstractproperty supports_refund → bool
   - Concrete: execute(amount, recipient) → dict
       - Calls validate() first; if fails, returns error dict
       - Calls process() if valid
       - Logs the transaction
       - Returns the result dict
   - Concrete: log(tx_dict) → None

2. Three implementations:
   - CardProcessor: 2.5% fee, max $10,000/transaction, supports refund
   - WalletProcessor: 0% fee, max $5,000, supports refund
   - CryptoProcessor: 1% fee, min $10, NO refund (immutable blockchain)

3. GatewayRouter class:
   - __init__(processors: list[BaseProcessor])
   - __processors: private (list)
   - add_processor(proc) → None: validated addition
   - remove_processor(name) → bool
   - route(amount, recipient) → dict:
       tries processors in order until one succeeds
   - best_for(amount) → BaseProcessor:
       returns processor with lowest fee for that amount

4. Transaction dataclass:
   - id, amount, recipient, processor_name, status, timestamp, fee

Demonstrate:
- Cannot instantiate BaseProcessor
- All three processor types work with execute()
- GatewayRouter tries next processor if one fails
- best_for() picks cheapest processor
"""
```

---

## 6. Best Practices & Industry Standards

### Use `_protected` by Default, `__private` Sparingly

```python
# ✅ Professional standard: single underscore for most "internal" things
class DataProcessor:
    def __init__(self, data):
        self._data = data               # protected — subclasses may access
        self._cache = {}                # protected — internal state

    def _validate(self, item):          # protected helper
        return item is not None

    def process(self):                  # public API
        return [x for x in self._data if self._validate(x)]


class Base:
    def __init__(self):
        self.__id = id(self)    # each class in hierarchy gets its own __id

class Child(Base):
    def __init__(self):
        super().__init__()
        self.__id = id(self)    # different attribute: _Child__id, doesn't conflict
```

---

### Always Use `@property` for Validated Attributes (Start Simple)

```python
# ✅ Start with a plain attribute:
class Product:
    def __init__(self, price):
        self.price = price      # simple attribute

# ✅ When you need validation, refactor to property:
class Product:
    def __init__(self, price):
        self.price = price      # this now calls the setter!

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)

# Callers don't need to change: p.price = 9.99 still works!

### ABCs for Framework Design, Duck Typing for Flexibility


from abc import ABC, abstractmethod
class Storage(ABC):
    @abstractmethod
    def save(self, key: str, value) -> None: ...
    @abstractmethod
    def load(self, key: str): ...

def process_all(items):
    for item in items:
        if hasattr(item, 'process'):
            item.process()      # duck typing — works for anything with process()
```

---

### PEP 8 Conventions for Encapsulation

```python
# ✅ Naming conventions
self.name           # public attribute
self._name          # protected — "please don't use from outside"
self.__name         # private — name mangling applied

# ✅ Property naming — same as the logical attribute, no 'get_' prefix
@property
def full_name(self): ...    # NOT get_full_name
@full_name.setter
def full_name(self, v): ... # NOT set_full_name

# ✅ Abstract method body — use ... (Ellipsis) or pass
@abstractmethod
def method(self): ...       # preferred — clearly signals "no implementation"

# ✅ Document your properties
@property
def balance(self) -> float:
    """Account balance in the base currency. Read-only."""
    return self._balance
```

---

## 7. Real-World Application

### Django Uses `@property` Extensively

```python
# Django User model — property pattern (Day 20+ preview)
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def full_name(self) -> str:
        """Computed property — not stored in database."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_admin(self) -> bool:
        """Check if user has admin role."""
        return self.groups.filter(name="admin").exists()


from rest_framework.views import APIView  # itself extends an ABC chain

class ProductAPI(APIView):
    def get(self, request):     # must implement request handlers
        ...
    def post(self, request):
        ...
```

### Flask's User Model (Flask-Login)

```python
# Flask-Login pattern — properties for user status
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    _password_hash = db.Column("password_hash", db.String(256))

    @property
    def password(self):
        """Password is write-only — cannot read the hash."""
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, plain_text: str) -> None:
        """Hash the password before storing."""
        from werkzeug.security import generate_password_hash
        self._password_hash = generate_password_hash(plain_text)

    def check_password(self, plain_text: str) -> bool:
        from werkzeug.security import check_password_hash
        return check_password_hash(self._password_hash, plain_text)

    @property
    def is_authenticated(self) -> bool:  # Flask-Login checks this
        return True


### Abstract Pattern in Django's CBVs

```python
# Django CBVs use mixins + abstract-like base classes extensively
from django.views.generic.base import View  # abstract-like: you MUST define get/post

class ProductView(View):
    def get(self, request, pk):     # "implement" the abstract interface
        product = get_object_or_404(Product, pk=pk)
        return JsonResponse({"name": product.name, "price": str(product.price)})

# Django's LoginRequiredMixin — encapsulates auth logic
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, View):
    login_url = "/login/"
    # __init__ (in LoginRequiredMixin) encapsulates the check
    # Callers never need to know HOW the check works — just that it works
```

### 🔭 Connection to Upcoming Days
- **Day 8:** Decorators — `@property` is a decorator; you'll build your own
- **Day 9:** Dataclasses — `@dataclass` generates `__init__`, `__repr__`, `__eq__` automatically; `field()` controls access
- **Day 10:** Context managers — `__enter__`/`__exit__` are another form of encapsulation
- **Day 20:** Django Models — every field, every `clean()` method, every `@property` on a model uses today's concepts directly

---

## 8. Quick Revision Summary

### Key Terms

| Term | One-line Definition |
|------|---------------------|
| Encapsulation | Bundling data + methods; controlling what's accessible from outside |
| Access control | Deciding who can read/modify an object's attributes |
| Public attribute | No prefix — accessible from anywhere (`self.name`) |
| Protected attribute | Single underscore — convention says "internal use" (`self._name`) |
| Private attribute | Double underscore — name mangling applied (`self.__name`) |
| Name mangling | Python renames `__attr` to `_ClassName__attr` to prevent subclass conflicts |
| `@property` | Decorator that turns a method into a readable attribute |
| `@attr.setter` | Decorator that turns a method into an attribute assignment handler |
| `@attr.deleter` | Decorator that turns a method into a `del attr` handler |
| Computed property | A `@property` that calculates its value on each access (no storage) |
| Read-only property | A `@property` with no `@setter` — cannot be assigned |
| Abstraction | Hiding complexity; exposing only what users need to know |
| ABC | Abstract Base Class — cannot be instantiated; defines a contract |
| `@abstractmethod` | Marks a method that subclasses MUST implement |
| Abstract property | `@property @abstractmethod` — subclasses must implement as a property |
| Concrete method (in ABC) | A regular implemented method in an abstract class — shared by all subclasses |
| Protocol | Structural interface from `typing.Protocol` — satisfied by having the right methods |
| Duck typing | If an object has the method, use it — no inheritance required |

---

### Core Syntax Cheat Sheet

```python
# ── Access levels ─────────────────────────────────────────────────────────
self.name           # public
self._name          # protected (convention)
self.__name         # private (name mangled to self._ClassName__name)

# ── Name mangling reveal ──────────────────────────────────────────────────
obj._ClassName__attr     # the real name after mangling

# ── @property — getter ────────────────────────────────────────────────────
@property
def attr(self) -> type:
    return self._attr

# ── @setter ───────────────────────────────────────────────────────────────
@attr.setter
def attr(self, value: type) -> None:
    self._attr = value   # stores in _attr, not attr (avoid recursion!)

# ── @deleter ──────────────────────────────────────────────────────────────
@attr.deleter
def attr(self) -> None:
    del self._attr

# ── Read-only: property with no setter ───────────────────────────────────
@property
def computed(self) -> float:
    return self._a * self._b   # no @computed.setter → read-only

# ── ABC ───────────────────────────────────────────────────────────────────
from abc import ABC, abstractmethod

class MyABC(ABC):
    @abstractmethod
    def must_implement(self) -> type: ...

    @property
    @abstractmethod
    def must_implement_property(self) -> type: ...

    def concrete_shared(self):   # concrete — all subclasses inherit
        ...

# ── Protocol ──────────────────────────────────────────────────────────────
from typing import Protocol, runtime_checkable

@runtime_checkable
class MyProtocol(Protocol):
    def required_method(self) -> str: ...
```

---

### 5 MCQ Recap Questions

**Q1.** What does Python do to `self.__balance` when you define it in a class called `Account`?
- A) Makes it completely inaccessible
- B) Stores it as `self.__balance` (unchanged)
- **C) Renames it to `self._Account__balance` (name mangling)** ✅
- D) Raises an error if accessed from outside

**Q2.** What is wrong with this property?
```python
@property
def name(self):
    return self.name   # returning self.name
```
- A) Missing return type annotation
- **B) Infinite recursion — `self.name` calls the property again** ✅
- C) `@property` doesn't support string return types
- D) Nothing is wrong

**Q3.** Which of the following creates a read-only property?
- A) Defining only `@attr.setter` without `@property`
- **B) Defining `@property` without a corresponding `@attr.setter`** ✅
- C) Using `@readonly` decorator
- D) Naming the attribute with `_` prefix

**Q4.** What happens when you try to instantiate an abstract class directly?
- A) It succeeds but calls the first concrete subclass
- B) It creates an empty object with no methods
- **C) Raises `TypeError: Can't instantiate abstract class`** ✅
- D) Raises `AbstractMethodError`

**Q5.** What is the difference between `_protected` and `__private` in Python?
- A) There is no difference — both are just conventions
- **B) `_protected` is convention-only; `__private` triggers name mangling which changes the attribute name** ✅
- C) `__private` cannot be accessed even via `_ClassName__attr`
- D) `_protected` prevents subclasses from accessing the attribute


> 💡 **Teaching tip:** The property recursion trap (Mistake 4) always gets students. Demonstrate it live — write the buggy version, run it, watch it crash. Then fix it. The "aha moment" sticks.
> 💡 **Live demo power move:** After building the ABC, show `PaymentProcessor()` raising `TypeError`. Then show a concrete subclass that "forgets" one abstract method — it also can't be instantiated. This drives home the contract idea.

---

### 📚 Resources & Further Reading

- [Python Docs — `abc` module](https://docs.python.org/3/library/abc.html)
- [Python Docs — `property` built-in](https://docs.python.org/3/library/functions.html#property)
- [Python Docs — `typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)
- [PEP 544 — Protocols: Structural subtyping](https://peps.python.org/pep-0544/)
- [Real Python — Python Property](https://realpython.com/python-property/)
- [Real Python — Abstract Base Classes](https://realpython.com/python-interface/)
- [Real Python — Python Protocols](https://realpython.com/python-protocol/)
- [Python Tutor](https://pythontutor.com/) ← visualize name mangling and property flow live
