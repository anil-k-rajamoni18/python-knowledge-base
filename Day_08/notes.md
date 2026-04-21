# 🐍 Python Full Stack — Day 8 of 35
# Topic: Magic Methods & Dataclasses
**Audience:** Beginner | **Duration:** 3 Hours | **Track:** Python → Django/Flask → Frontend → Deployment

---

## 1. Session Overview

### 🎯 Learning Objectives
By the end of this session, learners will be able to:
- Implement `__str__` and `__repr__` correctly and explain when each is called
- Add comparison, arithmetic, and container magic methods to make custom classes behave like Python built-ins
- Build context managers using `__enter__` and `__exit__` for resource management
- Create `@dataclass` classes that auto-generate boilerplate (`__init__`, `__repr__`, `__eq__`)
- Choose between plain classes, dataclasses, and namedtuples for the right scenario

### 📋 Prerequisites (Days 1–7 Review)
- OOP fundamentals — classes, `__init__`, instance variables (Day 5)
- Inheritance, `super()`, polymorphism (Day 6)
- Encapsulation, `@property`, ABC (Day 7)


### 2.1 What Are Magic Methods (Dunders)?

**The "Why":** Python's built-in operations — `print(obj)`, `len(obj)`, `obj + other`, `obj[0]`, `with obj:` — all call special methods under the hood. These methods have double underscores on both sides: `__method__`. That's why they're called "dunders" (double underscores) or "magic methods."

**The key insight:** When you write `len([1, 2, 3])`, Python calls `list.__len__([1, 2, 3])`. When you write `"a" + "b"`, Python calls `str.__add__("a", "b")`. Every built-in operation has a corresponding dunder method you can implement in your own classes.

**Analogy:** Magic methods are like **electrical outlet standards**. A USB device works in any socket that implements the USB standard — it doesn't matter what's inside the wall. Similarly, once your class implements `__len__`, Python can pass your objects to `len()`, just like it does for lists and strings.

**Complete magic method categories:**

| Category | Methods |
|----------|---------|
| String repr | `__str__`, `__repr__`, `__format__` |
| Comparison | `__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__` |
| Arithmetic | `__add__`, `__sub__`, `__mul__`, `__truediv__`, etc. |
| Container | `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__contains__`, `__iter__` |
| Context manager | `__enter__`, `__exit__` |
| Callable | `__call__` |
| Attribute access | `__getattr__`, `__setattr__`, `__delattr__` |
| Lifecycle | `__new__`, `__init__`, `__del__` |

---

### 2.2 String Representation — `__str__` vs `__repr__`

**The "Why":** Every object needs a way to present itself as a string. But there are two audiences:
- End users (non-technical) → `__str__` — readable, friendly
- Developers (debugging, logging) → `__repr__` — precise, unambiguous

**Rule of thumb:**
- `__repr__` should ideally produce a string that, when passed to `eval()`, recreates the object: `eval(repr(obj)) == obj`
- If only one is defined, `__repr__` is used everywhere (it's the fallback)
- `print(obj)` calls `__str__`, falling back to `__repr__`
- Lists and dicts display items using `__repr__`

---

### 2.3 Comparison Methods

**The "Why":** Python doesn't automatically know how to compare your custom objects with `==`, `<`, `>`. You tell it how.

Without `__eq__`, `obj1 == obj2` compares **identity** (same memory address), not value — almost never what you want.

`@functools.total_ordering` is a powerful decorator: define `__eq__` + one of (`__lt__`, `__le__`, `__gt__`, `__ge__`), and it generates all the rest automatically.

---

### 2.4 Arithmetic Methods

**The "Why":** Makes custom objects work naturally with `+`, `-`, `*`, `/` operators. Essential for mathematical objects (Vector, Matrix, Money, Polynomial) and domain objects that logically support arithmetic (combining Orders, merging inventories).

**Three variants for each operator:**
- `__add__(self, other)` — handles `self + other`
- `__radd__(self, other)` — handles `other + self` (when `other` doesn't know how to add `self`)
- `__iadd__(self, other)` — handles `self += other` (in-place modification)

---

### 2.5 Container Methods

**The "Why":** Makes your class work with Python's container protocol — `len()`, indexing `[]`, `in` operator, `for` loops. Once you implement these, your objects feel native.

- `__len__` → `len(obj)`, also used for truth value (`if obj:`)
- `__getitem__` → `obj[key]`, `obj[0:3]` (slicing)
- `__setitem__` → `obj[key] = value`
- `__delitem__` → `del obj[key]`
- `__contains__` → `x in obj` (falls back to iteration if not defined)
- `__iter__` → `for x in obj:`

---

### 2.6 Context Managers — `__enter__` and `__exit__`

**The "Why":** Resources (files, database connections, network sockets, locks) must be properly released even when errors occur. Without context managers, you need `try/finally` everywhere. Context managers guarantee cleanup.

```python
# Without context manager — fragile
conn = get_db_connection()
try:
    result = conn.execute("SELECT ...")
    return result
finally:
    conn.close()    # MUST remember this every time

# With context manager — elegant
with get_db_connection() as conn:
    return conn.execute("SELECT ...")
# conn.close() happens automatically, even on exception
```

**How it works:**
1. `__enter__` runs when the `with` block starts → returns the resource
2. `__exit__` runs when the `with` block ends (normally or by exception)
3. `__exit__` receives exception info — return `True` to suppress, `False` to propagate

---

### 2.7 Callable Objects — `__call__`

**The "Why":** Sometimes you want an object to behave like a function — callable, but carrying state between calls. Perfect for configurable callbacks, validators, and function factories.

---

### 2.8 Dataclasses — Remove the Boilerplate

**The "Why":** Writing `__init__`, `__repr__`, and `__eq__` for every data class is repetitive. 95% of the time they're identical boilerplate. `@dataclass` generates all of it from your field declarations.

**Before dataclasses:**
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```

**After dataclasses (equivalent):**
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

---

## 3. Syntax & Code Examples

### 3.1 `__str__` and `__repr__`

```python
class Product:
    def __init__(self, name: str, price: float, sku: str):
        self.name = name
        self.price = price
        self.sku = sku

    def __str__(self) -> str:
        """User-facing: called by print(), str(), f-strings."""
        return f"{self.name} — ${self.price:.2f}"

    def __repr__(self) -> str:
        """Developer-facing: called in REPL, lists, logging, repr()."""
        return f"Product(name={self.name!r}, price={self.price}, sku={self.sku!r})"


p = Product("Widget", 9.99, "WDG-001")

# When each is called:
print(p)                    # Widget — $9.99             ← __str__
print(str(p))               # Widget — $9.99             ← __str__
print(repr(p))              # Product(name='Widget', price=9.99, sku='WDG-001') ← __repr__
print(f"Item: {p}")         # Item: Widget — $9.99       ← __str__
print(f"Debug: {p!r}")      # Debug: Product(...)         ← __repr__ (force with !r)

# Lists use __repr__ for items
products = [p, Product("Gadget", 24.99, "GDG-002")]
print(products)
# [Product(name='Widget', ...), Product(name='Gadget', ...)] ← __repr__

# If only __repr__ is defined, print() falls back to it
class SimpleObj:
    def __repr__(self): return "SimpleObj()"

s = SimpleObj()
print(s)        # SimpleObj() ← falls back to __repr__
```

---

### 3.2 Comparison Methods with `@total_ordering`

```python
from functools import total_ordering


@total_ordering
class Money:
    """Demonstrates __eq__ + one comparison → total_ordering generates the rest."""

    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = round(float(amount), 2)
        self.currency = currency.upper()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented       # let Python try other.__eq__(self)
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} with {other.currency}")
        return self.amount < other.amount

    # @total_ordering generates: __le__, __gt__, __ge__ automatically!

    def __repr__(self) -> str:
        return f"Money({self.amount}, {self.currency!r})"

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:,.2f}"


a = Money(10.00)
b = Money(20.00)
c = Money(10.00)

print(a == c)       # True
print(a == b)       # False
print(a < b)        # True   ← __lt__
print(a <= b)       # True   ← generated by @total_ordering
print(b > a)        # True   ← generated
print(b >= c)       # True   ← generated

# Sorting works because comparison is defined
prices = [Money(30), Money(10), Money(20), Money(5)]
prices.sort()
print(prices)       # [Money(5, 'USD'), Money(10, 'USD'), Money(20, 'USD'), Money(30, 'USD')]

# Returns NotImplemented for wrong types (Pythonic)
print(a == 10)      # False (not NotImplemented — Python handles gracefully)
```

---

### 3.3 Arithmetic Methods — Vector Class

```python
from __future__ import annotations
import math


class Vector:
    """2D vector with full arithmetic support."""

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    # ── String ─────────────────────────────────────────────────────────────
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    # ── Equality ──────────────────────────────────────────────────────────
    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    # ── Arithmetic ────────────────────────────────────────────────────────
    def __add__(self, other: Vector) -> Vector:
        """v1 + v2"""
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other) -> Vector:
        """other + v (when other doesn't know how to add Vector)"""
        if other == 0:      # needed for sum([v1, v2, v3]) — starts with 0
            return self
        return self.__add__(other)

    def __sub__(self, other: Vector) -> Vector:
        """v1 - v2"""
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector:
        """v * scalar (scale the vector)"""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vector:
        """scalar * v (commutativity)"""
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> Vector:
        """v / scalar"""
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide vector by zero")
        return Vector(self.x / scalar, self.y / scalar)

    def __neg__(self) -> Vector:
        """-v (negate)"""
        return Vector(-self.x, -self.y)

    def __abs__(self) -> float:
        """abs(v) → magnitude"""
        return math.sqrt(self.x**2 + self.y**2)

    def __iadd__(self, other: Vector) -> Vector:
        """v += other (in-place add)"""
        if not isinstance(other, Vector):
            return NotImplemented
        self.x += other.x
        self.y += other.y
        return self

    # ── Additional math ───────────────────────────────────────────────────
    def dot(self, other: Vector) -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y

    @property
    def magnitude(self) -> float:
        return abs(self)

    def normalize(self) -> Vector:
        mag = self.magnitude
        if mag == 0:
            raise ValueError("Cannot normalize zero vector")
        return self / mag


# ── Demo ──────────────────────────────────────────────────────────────────
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)          # (4.0, 6.0)
print(v1 - v2)          # (2.0, 2.0)
print(v1 * 2)           # (6.0, 8.0)
print(3 * v2)           # (3.0, 6.0)    ← __rmul__
print(v1 / 2)           # (1.5, 2.0)
print(-v1)              # (-3.0, -4.0)
print(abs(v1))          # 5.0           ← __abs__

v1 += v2
print(v1)               # (4.0, 6.0)   ← __iadd__

# sum() works because of __radd__ with 0
vectors = [Vector(1, 0), Vector(2, 0), Vector(3, 0)]
print(sum(vectors))     # (6.0, 0.0)
```

---

### 3.4 Container Methods — Custom Cart

```python
from typing import Iterator


class ShoppingCart:
    """Demonstrates all container magic methods."""

    def __init__(self, customer: str):
        self.customer = customer
        self._items: list[dict] = []

    # ── Container protocol ────────────────────────────────────────────────
    def __len__(self) -> int:
        """len(cart) → number of items"""
        return len(self._items)

    def __bool__(self) -> bool:
        """if cart: → True if has items (falls back to __len__ if not defined)"""
        return len(self._items) > 0

    def __getitem__(self, index):
        """cart[0], cart[1:3] — supports indexing and slicing"""
        return self._items[index]

    def __setitem__(self, index: int, item: dict) -> None:
        """cart[0] = new_item"""
        self._items[index] = item

    def __delitem__(self, index: int) -> None:
        """del cart[0]"""
        del self._items[index]

    def __contains__(self, item_name: str) -> bool:
        """'ProductName' in cart → O(n) search by name"""
        return any(item["name"] == item_name for item in self._items)

    def __iter__(self) -> Iterator[dict]:
        """for item in cart: → makes cart iterable"""
        return iter(self._items)

    # ── Arithmetic ────────────────────────────────────────────────────────
    def __add__(self, other: "ShoppingCart") -> "ShoppingCart":
        """cart1 + cart2 → merge into new cart"""
        merged = ShoppingCart(f"{self.customer}+{other.customer}")
        merged._items = self._items + other._items
        return merged

    # ── Business methods ──────────────────────────────────────────────────
    def add_item(self, name: str, price: float, qty: int = 1) -> None:
        self._items.append({"name": name, "price": price, "qty": qty})

    @property
    def total(self) -> float:
        return sum(item["price"] * item["qty"] for item in self._items)

    def __str__(self) -> str:
        if not self._items:
            return f"Cart({self.customer!r}) — empty"
        lines = [f"Cart for {self.customer}:"]
        for item in self._items:
            lines.append(f"  {item['name']} × {item['qty']} = ${item['price'] * item['qty']:.2f}")
        lines.append(f"  Total: ${self.total:.2f}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"ShoppingCart(customer={self.customer!r}, items={len(self)})"


# ── Demo ──────────────────────────────────────────────────────────────────
cart = ShoppingCart("Alice")
cart.add_item("Widget", 9.99, 2)
cart.add_item("Gadget", 24.99)
cart.add_item("Thingamajig", 4.99, 3)

print(len(cart))                # 3      ← __len__
print(bool(cart))               # True   ← __bool__
print(cart[0])                  # {'name': 'Widget', ...} ← __getitem__
print(cart[0:2])                # first 2 items ← slicing via __getitem__
print("Widget" in cart)         # True   ← __contains__
print("Invisible" in cart)      # False

# Iteration
for item in cart:               # ← __iter__
    print(f"  {item['name']}: ${item['price']:.2f}")

# Delete
del cart[2]                     # ← __delitem__
print(len(cart))                # 2

# Merge two carts
cart2 = ShoppingCart("Bob")
cart2.add_item("Donut", 1.99, 6)

combined = cart + cart2         # ← __add__
print(len(combined))            # 3

print(cart)                     # ← __str__
```

---

### 3.5 Context Manager — `__enter__` and `__exit__`

```python
import time
from typing import Optional


class DatabaseConnection:
    """
    Simulates a database connection context manager.
    Demonstrates: __enter__, __exit__, exception handling.
    """

    def __init__(self, db_name: str, timeout: int = 5):
        self.db_name = db_name
        self.timeout = timeout
        self._connected = False
        self._queries: list[str] = []

    def __enter__(self) -> "DatabaseConnection":
        """Called when entering 'with' block. Returns the resource."""
        print(f"🔌 Connecting to '{self.db_name}'...")
        time.sleep(0.1)     # simulate connection time
        self._connected = True
        print(f"✅ Connected to '{self.db_name}'")
        return self         # the value bound to 'as conn'

    def __exit__(self,
                 exc_type: Optional[type],
                 exc_val: Optional[Exception],
                 exc_tb) -> bool:
        """
        Called when exiting 'with' block (normally or due to exception).
        exc_type, exc_val, exc_tb: exception info (all None if no exception)
        Return True to SUPPRESS the exception, False to PROPAGATE it.
        """
        print(f"\n🔌 Disconnecting from '{self.db_name}'...")
        self._connected = False

        if exc_type is not None:
            print(f"⚠️  Exception during transaction: {exc_type.__name__}: {exc_val}")
            print("↩️  Rolling back transaction...")
            # Return False → exception propagates to caller
            return False

        print(f"✅ Transaction committed. Queries run: {len(self._queries)}")
        return True

    def execute(self, query: str) -> list:
        """Execute a query."""
        if not self._connected:
            raise RuntimeError("Not connected! Use 'with' statement.")
        print(f"  SQL: {query}")
        self._queries.append(query)
        return [{"result": "mock data"}]


# ── Normal usage ───────────────────────────────────────────────────────────
print("=== Normal transaction ===")
with DatabaseConnection("users_db") as conn:
    users = conn.execute("SELECT * FROM users")
    orders = conn.execute("SELECT * FROM orders WHERE user_id=1")

# ── Exception during transaction ──────────────────────────────────────────
print("\n=== Failed transaction ===")
try:
    with DatabaseConnection("payments_db") as conn:
        conn.execute("INSERT INTO payments VALUES (...)")
        raise ValueError("Payment validation failed!")
        conn.execute("UPDATE balance ...")   # never reached
except ValueError as e:
    print(f"Caught in caller: {e}")
# __exit__ runs even when exception occurs — guaranteed cleanup!

# ── Without context manager — bad pattern ─────────────────────────────────
db = DatabaseConnection("test_db")
try:
    db.__enter__()   # manual entry — ugly
    db.execute("SELECT 1")
finally:
    db.__exit__(None, None, None)  # manual exit — fragile
```

**Output:**
```
=== Normal transaction ===
🔌 Connecting to 'users_db'...
✅ Connected to 'users_db'
  SQL: SELECT * FROM users
  SQL: SELECT * FROM orders WHERE user_id=1

🔌 Disconnecting from 'users_db'...
✅ Transaction committed. Queries run: 2

=== Failed transaction ===
🔌 Connecting to 'payments_db'...
✅ Connected to 'payments_db'
  SQL: INSERT INTO payments VALUES (...)

🔌 Disconnecting from 'payments_db'...
⚠️  Exception during transaction: ValueError: Payment validation failed!
↩️  Rolling back transaction...
Caught in caller: Payment validation failed!
```

---

### 3.6 Callable Objects — `__call__`

```python
class Multiplier:
    """Makes instances callable like functions, but with state."""

    def __init__(self, factor: float):
        self.factor = factor
        self.call_count = 0

    def __call__(self, value: float) -> float:
        """Called when instance is used as a function: obj(x)"""
        self.call_count += 1
        return value * self.factor

    def __repr__(self) -> str:
        return f"Multiplier(factor={self.factor}, calls={self.call_count})"


double = Multiplier(2)
triple = Multiplier(3)

print(double(5))        # 10.0   ← instance called like a function
print(double(7))        # 14.0
print(triple(4))        # 12.0
print(double)           # Multiplier(factor=2, calls=2)

# Works with map, filter, etc. (any callable)
numbers = [1, 2, 3, 4, 5]
doubled = list(map(double, numbers))   # double is callable!
print(doubled)          # [2.0, 4.0, 6.0, 8.0, 10.0]
print(callable(double)) # True — has __call__


# Real-world: validator as callable class (stateful)
class RangeValidator:
    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val

    def __call__(self, value: float) -> bool:
        return self.min_val <= value <= self.max_val

    def __repr__(self):
        return f"RangeValidator({self.min_val}, {self.max_val})"


is_valid_age = RangeValidator(0, 150)
is_valid_score = RangeValidator(0, 100)

print(is_valid_age(25))     # True
print(is_valid_age(200))    # False
print(is_valid_score(105))  # False
```

---

### 3.7 Dataclasses — Complete Guide

```python
from dataclasses import dataclass, field, asdict, astuple
from typing import ClassVar


# ── Basic dataclass ───────────────────────────────────────────────────────
@dataclass
class Point:
    x: float
    y: float

# Automatically generated:
# __init__(self, x: float, y: float)
# __repr__(self)  → Point(x=1.0, y=2.0)
# __eq__(self, other)  → compares field values

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)
p3 = Point(3.0, 4.0)

print(p1)           # Point(x=1.0, y=2.0)
print(p1 == p2)     # True  ← value comparison
print(p1 == p3)     # False
print(p1 is p2)     # False ← different objects


# ── Defaults and field() ──────────────────────────────────────────────────
@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0                          # simple default
    tags: list[str] = field(default_factory=list)   # mutable default — MUST use field()
    _id: int = field(default=0, repr=False)    # hidden from repr
    CATEGORY: ClassVar[str] = "General"        # class variable — not a field

    def __post_init__(self) -> None:
        """Runs after __init__ — use for computed fields and validation."""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        self.price = round(self.price, 2)      # normalize

    @property
    def total_value(self) -> float:
        return self.price * self.quantity


p = Product("Widget", 9.99, 10, tags=["sale", "new"])
print(p)            # Product(name='Widget', price=9.99, quantity=10, tags=['sale', 'new'])
print(p.total_value)# 99.9


# ── Ordering (order=True) ─────────────────────────────────────────────────
@dataclass(order=True)
class Student:
    # The ORDER of fields matters for comparison!
    # Comparison uses fields in declaration order
    sort_index: float = field(init=False, repr=False)   # computed sort key
    name: str
    grade: float
    age: int

    def __post_init__(self):
        # Set sort_index to grade for sorting
        self.sort_index = self.grade

students = [
    Student("Alice", 92.5, 20),
    Student("Bob", 85.0, 22),
    Student("Carol", 92.5, 21),
]
students.sort()
for s in students:
    print(s)
# Student(name='Bob', grade=85.0, age=22)
# Student(name='Alice', grade=92.5, age=20)   ← sorted by sort_index (grade)
# Student(name='Carol', grade=92.5, age=21)


# ── Frozen (immutable) dataclass ──────────────────────────────────────────
@dataclass(frozen=True)
class Coordinate:
    lat: float
    lng: float
    # frozen=True → FrozenInstanceError on any assignment
    # Also: __hash__ is auto-generated (hashable, usable as dict key)

home = Coordinate(12.9716, 77.5946)
print(hash(home))    # works because frozen

try:
    home.lat = 0.0   # FrozenInstanceError!
except Exception as e:
    print(f"Immutable: {e}")

# Can be used as dict key (frozen = hashable)
locations = {home: "Bangalore", Coordinate(28.6139, 77.2090): "Delhi"}


# ── asdict() and astuple() ────────────────────────────────────────────────
@dataclass
class Address:
    street: str
    city: str
    country: str = "India"

addr = Address("123 MG Road", "Bangalore")
print(asdict(addr))     # {'street': '123 MG Road', 'city': 'Bangalore', 'country': 'India'}
print(astuple(addr))    # ('123 MG Road', 'Bangalore', 'India')

# asdict() is incredibly useful for JSON serialization!
import json
print(json.dumps(asdict(addr)))
# {"street": "123 MG Road", "city": "Bangalore", "country": "India"}
```

---

### 3.8 `__getattr__` and `__setattr__`

```python
class FlexibleRecord:
    """
    Demonstrates __getattr__ and __setattr__.
    Stores all attributes dynamically in a _data dict.
    """

    def __init__(self, **initial_data):
        # Use object.__setattr__ to avoid recursion during __init__
        object.__setattr__(self, '_data', {})
        object.__setattr__(self, '_access_log', [])
        for key, value in initial_data.items():
            self._data[key] = value

    def __getattr__(self, name: str):
        """Called when attribute NOT found via normal lookup."""
        if name in self._data:
            self._access_log.append(f"GET {name}")
            return self._data[name]
        raise AttributeError(f"No attribute: {name!r}")

    def __setattr__(self, name: str, value) -> None:
        """Called for EVERY attribute assignment — even in __init__!"""
        if name.startswith('_'):
            object.__setattr__(self, name, value)   # handle private attrs normally
        else:
            self._data[name] = value                # store in _data

    def __delattr__(self, name: str) -> None:
        if name in self._data:
            del self._data[name]
        else:
            raise AttributeError(f"Cannot delete: {name!r}")

    def __repr__(self) -> str:
        return f"FlexibleRecord({self._data})"


r = FlexibleRecord(name="Alice", age=25)
print(r.name)       # Alice  ← __getattr__
r.city = "Pune"     # ← __setattr__ → stores in _data
print(r.city)       # Pune
del r.age           # ← __delattr__
print(r)            # FlexibleRecord({'name': 'Alice', 'city': 'Pune'})
```

---

## 4. Common Mistakes & Gotchas

### ❌ Mistake 1: Confusing `__str__` and `__repr__` — Only Defining One

```python
# ❌ Wrong — __str__ and __repr__ are mixed up
class Order:
    def __init__(self, id, total):
        self.id = id
        self.total = total

    def __str__(self):
        return f"Order(id={self.id!r}, total={self.total})"  # developer-style in __str__

    def __repr__(self):
        return f"Order #{self.id}: ${self.total:.2f}"   # user-style in __repr__

o = Order("ORD-001", 59.99)
print(o)            # Order(id='ORD-001', total=59.99) ← looks like repr!
print(repr(o))      # Order #ORD-001: $59.99            ← looks like str!

# ✅ Correct — __str__ is friendly, __repr__ is unambiguous
class Order:
    def __init__(self, id, total):
        self.id = id
        self.total = total

    def __str__(self):
        return f"Order #{self.id}: ${self.total:.2f}"   # friendly

    def __repr__(self):
        return f"Order(id={self.id!r}, total={self.total})"  # recreatable
```

---

### ❌ Mistake 2: `__eq__` Without `__hash__` — Breaking Hashability

```python
# ❌ Wrong — defining __eq__ automatically sets __hash__ = None!
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

p = Point(1, 2)
{p: "home"}     # TypeError: unhashable type: 'Point'!
# Python sets __hash__ = None when you define __eq__

# ✅ Correct — also define __hash__ if you need it in sets/dicts
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))   # use a tuple for hash

p = Point(1, 2)
locations = {p: "home"}     # works!
{Point(1, 2), Point(1, 2)}  # set deduplication works!
```

---

### ❌ Mistake 3: Returning Wrong Type from Arithmetic Methods

```python
# ❌ Wrong — __add__ returns a tuple instead of the same type
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return (self.x + other.x, self.y + other.y)   # returns tuple!

v1 = Vector(1, 2)
v2 = Vector(3, 4)
result = v1 + v2
print(type(result))  # <class 'tuple'> — not Vector!
result + v2          # AttributeError: tuple has no __add__ for Vector

# ✅ Correct — arithmetic should return the SAME type
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)  # returns Vector!

result = v1 + v2
print(type(result))  # <class 'Vector'>
```

---

### ❌ Mistake 4: Forgetting `__exit__` Always Runs — Even on Exceptions

```python
# ❌ Wrong assumption — thinking __exit__ only runs on success
class FileProcessor:
    def __enter__(self):
        self.file = open("data.txt", "w")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:            # BUG: only closes on success!
            self.file.close()
        # If exception occurs, file is NEVER closed — resource leak!

# ✅ Correct — always close, check for exception separately
class FileProcessor:
    def __enter__(self):
        self.file = open("data.txt", "w")
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()               # ALWAYS close
        if exc_type is not None:
            print(f"Exception: {exc_val}. File closed.")
        return False                    # don't suppress exception
```

---

### ❌ Mistake 5: Mutable Default in Dataclass Without `field()`

```python
# ❌ Wrong — list default without field() → TypeError
from dataclasses import dataclass

@dataclass
class Order:
    items: list = []    # ValueError: mutable default is not allowed

# ✅ Correct — use field(default_factory=list)
@dataclass
class Order:
    items: list = field(default_factory=list)   # creates new list for each instance

# Why? Same reason as normal classes: a bare [] would be SHARED across all instances!
# field(default_factory=list) creates a new [] for each Order instance.
```

---

## 5. Hands-on Exercises

### 🧑‍🏫 Guided Exercise 1: Order Class with Full Magic Methods

**Goal:** Build a complete `Order` class step by step.

```python
from functools import total_ordering
from typing import Iterator


@total_ordering
class Order:
    """E-commerce order with complete magic method support."""

    def __init__(self, order_id: str, customer: str):
        self.order_id = order_id
        self.customer = customer
        self._items: list[dict] = []

    # Step 1: String representation
    def __repr__(self) -> str:
        return f"Order(id={self.order_id!r}, customer={self.customer!r}, items={len(self)})"

    def __str__(self) -> str:
        if not self._items:
            return f"Order {self.order_id} (empty) for {self.customer}"
        lines = [f"Order {self.order_id} for {self.customer}:"]
        for item in self._items:
            lines.append(f"  {item['name']} × {item['qty']} @ ${item['price']:.2f}")
        lines.append(f"  Total: ${self.total:.2f}")
        return "\n".join(lines)

    # Step 2: Comparison
    def __eq__(self, other) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __lt__(self, other) -> bool:
        """Sort orders by total amount."""
        if not isinstance(other, Order):
            return NotImplemented
        return self.total < other.total

    # Step 3: Container
    def __len__(self) -> int:
        """len(order) → number of line items."""
        return len(self._items)

    def __bool__(self) -> bool:
        return len(self._items) > 0

    def __getitem__(self, index):
        """order[0], order[0:2]"""
        return self._items[index]

    def __iter__(self) -> Iterator[dict]:
        """for item in order:"""
        return iter(self._items)

    def __contains__(self, item_name: str) -> bool:
        """'ProductName' in order"""
        return any(item["name"] == item_name for item in self._items)

    # Step 4: Arithmetic
    def __add__(self, other: "Order") -> "Order":
        """order1 + order2 → merged order."""
        merged = Order(f"{self.order_id}+{other.order_id}", self.customer)
        merged._items = self._items + other._items
        return merged

    # Business methods
    def add_item(self, name: str, price: float, qty: int = 1) -> None:
        self._items.append({"name": name, "price": price, "qty": qty})

    @property
    def total(self) -> float:
        return sum(item["price"] * item["qty"] for item in self._items)

    @property
    def item_count(self) -> int:
        return sum(item["qty"] for item in self._items)


# ── Test all magic methods ─────────────────────────────────────────────────
o1 = Order("ORD-001", "Alice")
o1.add_item("Widget", 9.99, 2)
o1.add_item("Gadget", 24.99, 1)

o2 = Order("ORD-002", "Alice")
o2.add_item("Thingamajig", 4.99, 5)

# String
print(o1)                   # __str__
print(repr(o1))             # __repr__

# Container
print(len(o1))              # 2  ← __len__
print(o1[0])                # {'name': 'Widget', ...} ← __getitem__
print("Widget" in o1)       # True ← __contains__
for item in o1:             # ← __iter__
    print(f"  {item['name']}")

# Comparison
print(o1 > o2)              # True (44.97 > 24.95) ← __gt__ from total_ordering
orders = [o1, o2, Order("ORD-003", "Bob")]
o3 = orders[2]
o3.add_item("Mega Item", 100.0)
orders.sort()               # uses __lt__
for o in orders:
    print(f"  {o.order_id}: ${o.total:.2f}")

# Arithmetic
combined = o1 + o2          # ← __add__
print(f"Combined items: {len(combined)}")
```

---

### 🧑‍🏫 Guided Exercise 2: Dataclass BankTransaction

**Goal:** Refactor a plain class to a dataclass with full features.

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar


# Before: plain class (verbose)
class BankTransaction_Old:
    def __init__(self, tx_id, amount, tx_type, timestamp=None):
        self.tx_id = tx_id
        self.amount = amount
        self.tx_type = tx_type
        self.timestamp = timestamp or datetime.now()

    def __repr__(self):
        return f"BankTransaction_Old(tx_id={self.tx_id!r}, amount={self.amount}, type={self.tx_type!r})"

    def __eq__(self, other):
        return self.tx_id == other.tx_id


# After: dataclass (concise + more features)
@dataclass(order=True)
class BankTransaction:
    sort_index: float = field(init=False, repr=False)   # sort by amount
    tx_id: str
    amount: float
    tx_type: str                                        # "deposit" | "withdrawal"
    timestamp: datetime = field(default_factory=datetime.now)
    notes: str = field(default="", repr=False)          # hidden from repr

    # Class-level tracking
    _all_transactions: ClassVar[list] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validation and computed fields after __init__."""
        if self.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        if self.tx_type not in ("deposit", "withdrawal"):
            raise ValueError(f"Unknown transaction type: {self.tx_type!r}")
        # Set sort key
        self.sort_index = self.amount

    @property
    def is_credit(self) -> bool:
        return self.tx_type == "deposit"

    @property
    def signed_amount(self) -> float:
        return self.amount if self.is_credit else -self.amount


# Test
t1 = BankTransaction("TX-001", 1000.0, "deposit")
t2 = BankTransaction("TX-002", 500.0, "withdrawal")
t3 = BankTransaction("TX-003", 250.0, "deposit", notes="Birthday gift")

print(t1)                   # BankTransaction(sort_index=..., tx_id='TX-001', ...)
print(t1 == t1)             # True
print(t1 > t2)              # True (1000 > 500) ← order=True

transactions = [t2, t3, t1]
transactions.sort()
for tx in transactions:
    print(f"  {tx.tx_id}: ${tx.amount:.2f} ({tx.tx_type})")

# asdict for serialization
from dataclasses import asdict
print(asdict(t1))
```

---

### 💻 Independent Practice 1: Matrix Class with Arithmetic

```python
"""
Build a Matrix class with:
- __init__(rows: list[list[float]])
- __repr__ and __str__ (display as a grid)
- __add__: matrix addition (same dimensions required)
- __mul__: scalar multiplication AND matrix multiplication
  - if other is a number: scalar multiply each element
  - if other is a Matrix: matrix multiply (dot product rules)
- __eq__: element-wise comparison
- __len__: returns number of rows
- __getitem__: row access (matrix[0] → first row)
- Property: shape → tuple (rows, cols)
- Property: is_square → bool
- Method: transpose() → Matrix (new matrix, rows become columns)

Tests:
m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[5, 6], [7, 8]])

print(m1.shape)         # (2, 2)
print(m1 + m2)          # [[6, 8], [10, 12]]
print(m1 * 2)           # [[2, 4], [6, 8]]
print(2 * m1)           # [[2, 4], [6, 8]]   ← __rmul__
print(m1 * m2)          # [[19, 22], [43, 50]] ← matrix multiplication
print(m1.transpose())   # [[1, 3], [2, 4]]
print(len(m1))          # 2
print(m1[0])            # [1, 2]
"""

# Hints:
# - For matrix multiply: result[i][j] = sum(row_i[k] * col_j[k] for k in range(cols))
# - isinstance(other, (int, float)) to distinguish scalar vs matrix multiply
# - __rmul__ delegates to __mul__: return self.__mul__(other)
```

---

### 💻 Independent Practice 2: Timer Context Manager

```python
"""
Build a Timer context manager that:
- __enter__: records start time, prints "⏱ Timer started"
- __exit__: records end time, prints elapsed time
  - if exception: print warning but still show time
  - never suppress exceptions

Additionally:
- The timer should have a .elapsed property (works even outside with block)
- Support named timers: Timer("database_query")

Build a second version using @contextmanager from contextlib (bonus).

Usage:
with Timer("page_load") as t:
    time.sleep(0.5)
    result = "expensive operation"
# ⏱ Timer 'page_load' started
# ✅ Timer 'page_load' finished: 0.500s

print(t.elapsed)    # 0.500 (accessible after the with block)

# With exception:
with Timer("risky_op"):
    raise ValueError("oops")
# ⏱ Timer 'risky_op' started
# ⚠️  Timer 'risky_op' stopped by ValueError: 0.001s
# (ValueError propagates to caller)
"""

# Hints:
# - import time; start = time.perf_counter()
# - elapsed = time.perf_counter() - start
# - __exit__ receives exc_type (None if no exception)
# - Store elapsed on self so it's accessible after the block
```

---

### 🏆 Challenge Problem: Full Inventory System with Dataclasses

```python
"""
Build a complete inventory system using dataclasses and magic methods:

1. @dataclass Product:
   - sku: str, name: str, price: float, stock: int
   - tags: list[str] = field(default_factory=list)
   - Validation in __post_init__
   - Properties: total_value, is_available, tax_inclusive_price
   - order=True with sort by price

2. @dataclass(frozen=True) ProductSnapshot:
   - Immutable record for logging
   - sku, name, price (at time of snapshot), timestamp

3. Inventory class with magic methods:
   - __len__: number of unique products
   - __contains__: sku in inventory
   - __getitem__: inventory["SKU"] → Product
   - __iter__: iterate over products
   - __add__: merge two inventories
   - __str__: formatted table
   - add(product), remove(sku), restock(sku, qty)

4. SaleEvent @dataclass:
   - products: list[Product], discount_pct: float
   - __post_init__: validates 0 < discount_pct <= 100
   - apply_discount() → list[ProductSnapshot]
   - total_savings() → float

Demonstrate:
- Create inventory, add products
- 'SKU' in inventory
- for product in inventory
- sorted(inventory) (via order=True)
- sale = SaleEvent([...], 20)  → 20% off
- inv1 + inv2 → merged inventory
"""
```

---

## 6. Best Practices & Industry Standards

### Define `__repr__` First, `__str__` Second

```python
# ✅ Best practice: ALWAYS define __repr__
# Define __str__ ONLY when user-facing display differs significantly

class DatabaseRecord:
    def __init__(self, table, pk, data):
        self.table = table
        self.pk = pk
        self.data = data

    # __repr__ — always define this (minimum)
    def __repr__(self):
        return f"DatabaseRecord(table={self.table!r}, pk={self.pk})"

    # __str__ — only if print() output should look different
    def __str__(self):
        return f"[{self.table}:{self.pk}] {self.data}"
```

---

### Use `NotImplemented` (not `NotImplementedError`) in Magic Methods

```python
# ✅ Return NotImplemented (the singleton) — NOT raise NotImplementedError
class Money:
    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented   # ✅ lets Python try other.__eq__(self)

        # ❌ Don't do this:
        # if not isinstance(other, Money):
        #     raise NotImplementedError   # breaks equality with other types

# NotImplemented tells Python: "I don't know how to compare with this type,
# try asking the other object." Python will then try other.__eq__(self).
# If both return NotImplemented, Python falls back to identity comparison.
```

---

### `@dataclass` Best Practices

```python
from dataclasses import dataclass, field

# ✅ Use field() for ALL mutable defaults
@dataclass
class Config:
    settings: dict = field(default_factory=dict)
    tags: list = field(default_factory=list)

# ✅ Use __post_init__ for validation and computed fields
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # computed — not in __init__

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be positive")
        self.area = self.width * self.height   # computed field

# ✅ Use frozen=True when you need immutable, hashable objects
@dataclass(frozen=True)
class Point:
    x: float
    y: float
    # Automatically hashable — safe for use as dict key or in sets

# ✅ For complex ordering, use a computed sort_index field
@dataclass(order=True)
class Task:
    sort_index: tuple = field(init=False, repr=False)
    priority: int       # 1=high, 2=medium, 3=low
    name: str

    def __post_init__(self):
        self.sort_index = (self.priority, self.name)   # sort by priority then name
```

---

### Context Manager Idioms

```python
# ✅ Use contextlib.contextmanager for simple cases
from contextlib import contextmanager

@contextmanager
def timer(label: str):
    import time
    start = time.perf_counter()
    try:
        yield                                       # the 'with' block runs here
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.3f}s")          # always runs

with timer("database query"):
    import time; time.sleep(0.1)                   # 0.100s

# ✅ Use __enter__/__exit__ for stateful, reusable context managers
# (like the DatabaseConnection example)

# ✅ contextlib.suppress for swallowing specific exceptions
from contextlib import suppress

with suppress(FileNotFoundError):
    import os; os.remove("temp_file.txt")          # no error if file doesn't exist
```

---

## 7. Real-World Application

### Django Models Need `__str__` — It's Required

```python
# Django admin uses __str__ to display every object
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self) -> str:
        """MANDATORY in Django — used in admin, shell, and ForeignKey displays."""
        return f"{self.name} (${self.price})"

    def __repr__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"

# Without __str__, Django admin shows: "Product object (1)" — useless!
```

### Django QuerySets Use Container Protocols

```python
# Django QuerySet internally uses container methods
products = Product.objects.filter(price__lt=50)

len(products)               # __len__ → COUNT query
products[0]                 # __getitem__ → LIMIT 1
products[0:5]               # slicing → LIMIT 5
product in products         # __contains__ → checking membership
for p in products:          # __iter__ → iteration
    print(p)
```

### Dataclasses for API Response Models

```python
# Modern Django/Flask APIs use dataclasses for clean request/response models
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class ProductResponse:
    """API response shape — asdict() converts directly to JSON."""
    id: int
    name: str
    price: float
    is_available: bool
    category: Optional[str] = None

    @classmethod
    def from_model(cls, product) -> "ProductResponse":
        return cls(
            id=product.pk,
            name=product.name,
            price=float(product.price),
            is_available=product.stock > 0,
            category=product.category.name if product.category else None,
        )


# In a Django view:
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    response = ProductResponse.from_model(product)
    return JsonResponse(asdict(response))   # asdict → dict → JSON
```

### Context Manager for Django Transactions

```python
# Django uses context managers for transactions (you'll write these in Day 25)
from django.db import transaction

def transfer_funds(from_account, to_account, amount):
    with transaction.atomic():      # __enter__: begin transaction
        from_account.balance -= amount
        from_account.save()
        to_account.balance += amount
        to_account.save()
    # __exit__: COMMIT if no exception, ROLLBACK if exception

# This is exactly like your DatabaseConnection example!
```

### 🔭 Connection to Upcoming Days
- **Day 9:** Decorators — `@dataclass` itself is a decorator; `@total_ordering` is a decorator; you'll build your own
- **Day 10:** Iterators & Generators — `__iter__` opens the door to generator-based iterators
- **Day 11:** File I/O — `with open(...)` uses `__enter__`/`__exit__` (you now understand how!)
- **Day 20:** Django Models — `__str__` on every model is your first task; QuerySet protocol is all magic methods

---

## 8. Quick Revision Summary

### Key Terms

| Term | One-line Definition |
|------|---------------------|
| Dunder / Magic method | Method with double underscores on both sides — called by Python operators |
| `__str__` | User-friendly string; called by `print()` and `str()` |
| `__repr__` | Developer-friendly string; called by `repr()`, REPL, lists |
| `__eq__` | Defines `==` operator; without it, compares identity (memory address) |
| `__hash__` | Required in dicts/sets; auto-set to None when `__eq__` is defined |
| `@total_ordering` | Decorator: define `__eq__` + one comparison → generates all 6 |
| `__add__` | Defines `+` operator: `self + other` |
| `__radd__` | Defines `other + self` (right-hand addition) |
| `__iadd__` | Defines `+=` (in-place addition) |
| `__len__` | Defines `len(obj)`; also used for truth value |
| `__getitem__` | Defines `obj[key]` and slicing `obj[0:3]` |
| `__contains__` | Defines `x in obj` operator |
| `__iter__` | Makes object iterable with `for x in obj:` |
| `__enter__` | Called at start of `with` block; returns the resource |
| `__exit__` | Called at end of `with` block; return True to suppress exceptions |
| `__call__` | Makes instance callable: `obj(args)` |
| `@dataclass` | Class decorator that auto-generates `__init__`, `__repr__`, `__eq__` |
| `field()` | Configures individual dataclass fields (defaults, repr, ordering) |
| `__post_init__` | Runs after dataclass `__init__`; use for validation and computed fields |
| `frozen=True` | Makes dataclass immutable (FrozenInstanceError on assignment) |
| `asdict()` | Converts dataclass to dict (great for JSON serialization) |
| `NotImplemented` | Singleton returned by magic methods to tell Python "try the other object" |

---

### Core Syntax Cheat Sheet

```python
# ── String representation ─────────────────────────────────────────────────
def __str__(self) -> str: return "user-friendly string"
def __repr__(self) -> str: return f"ClassName(field={self.field!r})"

# ── Comparison ────────────────────────────────────────────────────────────
from functools import total_ordering
@total_ordering
class MyClass:
    def __eq__(self, other):
        if not isinstance(other, MyClass): return NotImplemented
        return self.value == other.value
    def __lt__(self, other):
        if not isinstance(other, MyClass): return NotImplemented
        return self.value < other.value

# ── Arithmetic ────────────────────────────────────────────────────────────
def __add__(self, other): return MyClass(self.val + other.val)
def __radd__(self, other): return self.__add__(other)
def __iadd__(self, other): self.val += other.val; return self
def __neg__(self): return MyClass(-self.val)
def __abs__(self): return abs(self.val)

# ── Container ─────────────────────────────────────────────────────────────
def __len__(self) -> int: return len(self._data)
def __bool__(self) -> bool: return bool(self._data)
def __getitem__(self, key): return self._data[key]
def __setitem__(self, key, value): self._data[key] = value
def __delitem__(self, key): del self._data[key]
def __contains__(self, item) -> bool: return item in self._data
def __iter__(self): return iter(self._data)

# ── Context manager ───────────────────────────────────────────────────────
def __enter__(self): # setup; return self or resource
def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
    # cleanup; return True to suppress exception

# ── Callable ──────────────────────────────────────────────────────────────
def __call__(self, *args, **kwargs): return result

# ── Dataclass ─────────────────────────────────────────────────────────────
from dataclasses import dataclass, field, asdict, astuple

@dataclass
class MyDC:
    name: str
    value: float = 0.0
    items: list = field(default_factory=list)
    _computed: float = field(init=False, repr=False)

    def __post_init__(self):
        self._computed = self.value * 2

@dataclass(frozen=True)   # immutable + hashable
@dataclass(order=True)    # enables <, >, <=, >= using field order
```

---

### 5 MCQ Recap Questions

**Q1.** When does Python call `__repr__` instead of `__str__`?
- A) When the object is inside a list or another container
- B) When `repr()` is called explicitly
- C) In the REPL when inspecting an object
- **D) All of the above — __repr__ is used in containers, repr(), REPL, and as fallback for print()** ✅

**Q2.** What does returning `NotImplemented` from `__eq__` tell Python?
- A) The objects are not equal
- B) Raise an exception
- **C) Try calling `__eq__` on the other object** ✅
- D) Return `False` for the comparison

**Q3.** In a `@dataclass`, why must mutable defaults use `field(default_factory=list)` instead of `= []`?
- A) Syntax rule — `@dataclass` doesn't accept `[]` literals
- **B) A bare `[]` would be shared across all instances — same bug as mutable class variables** ✅
- C) Lists aren't supported as dataclass fields
- D) `field()` is optional — `= []` works fine

**Q4.** What do `__enter__` and `__exit__` enable?
- A) Making objects printable
- B) Enabling iteration with `for` loops
- **C) Using objects with the `with` statement for guaranteed resource cleanup** ✅
- D) Making objects comparable

**Q5.** What does `frozen=True` in `@dataclass(frozen=True)` do?
- A) Makes the class abstract — cannot be subclassed
- B) Prevents adding new attributes after `__init__`
- **C) Makes all fields immutable (raises FrozenInstanceError on assignment) AND auto-generates `__hash__`** ✅
- D) Removes `__repr__` from auto-generation

---

## 9. Instructor Notes

### 📌 Anticipated Student Questions

| Question | Suggested Answer |
|----------|-----------------|
| "Why use `NotImplemented` and not just `return False` in `__eq__`?" | `NotImplemented` tells Python "I don't know how to compare with this type — ask the other side." `return False` says "they're definitely not equal." For cross-type comparisons, `NotImplemented` gives the other class a chance to handle it. |
| "When does `__radd__` get called?" | When `other + self` is evaluated and `other.__add__(self)` returns `NotImplemented`. Python then tries `self.__radd__(other)`. Classic example: `sum([v1, v2])` — Python starts with `0 + v1`, and since `int.__add__(Vector)` returns `NotImplemented`, Python tries `Vector.__radd__(0)`. |
| "Does `__exit__` run if there's no exception?" | Yes! `__exit__` ALWAYS runs when the `with` block ends, regardless of whether an exception occurred. That's the whole point — guaranteed cleanup. |
| "What's the difference between `__len__` and `__bool__`?" | If `__bool__` is not defined, Python uses `__len__` for truth testing (`if obj:` → `len(obj) != 0`). Define `__bool__` only when truth testing should differ from emptiness — e.g., an object might have length 0 but still be "truthy." |
| "Should I always use `@dataclass` over a plain class?" | Not always. Use `@dataclass` for pure data containers. Use a plain class when you have significant business logic, inheritance hierarchies, or when the auto-generated methods aren't appropriate. Django models don't use `@dataclass` because they need Django's metaclass machinery. |
| "Can a dataclass inherit from another dataclass?" | Yes — child dataclass gets parent fields first (in parent order), then its own. But `frozen` inheritance has rules: frozen can't inherit from non-frozen. |


### 📚 Resources & Further Reading

- [Python Docs — Data Model (all magic methods)](https://docs.python.org/3/reference/datamodel.html)
- [Python Docs — `dataclasses` module](https://docs.python.org/3/library/dataclasses.html)
- [Python Docs — `functools.total_ordering`](https://docs.python.org/3/library/functools.html#functools.total_ordering)
- [Python Docs — `contextlib`](https://docs.python.org/3/library/contextlib.html)
- [Real Python — Magic Methods](https://realpython.com/python-magic-methods/)
- [Real Python — Dataclasses](https://realpython.com/python-data-classes/)
- [Real Python — Context Managers](https://realpython.com/python-with-statement/)
- [Rafe Kettler — A Guide to Python's Magic Methods](https://rszalski.github.io/magicmethods/) ← comprehensive reference
- [PEP 557 — Data Classes](https://peps.python.org/pep-0557/)
