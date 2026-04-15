# 💪 Python Full Stack — Day 8 Exercise & Practice File
# Topic: Magic Methods & Dataclasses

> **Instructions:** Work in order. Write predictions before running. Never peek at answers before attempting. The Order class and Vector exercises are the most important — they appear in real interviews.

---

## 📋 Setup Check

```python
from dataclasses import dataclass, field, asdict
from functools import total_ordering
import math

# Quick test
@dataclass
class TestPoint:
    x: float
    y: float

p = TestPoint(1.0, 2.0)
print(p)                    # TestPoint(x=1.0, y=2.0)
print(p == TestPoint(1, 2)) # True
print("✅ Setup complete!")
```

---

## Section A — Predict the Output (No Running Allowed!)

### A1. `__str__` vs `__repr__`

```python
class Coin:
    def __init__(self, value, currency="INR"):
        self.value = value
        self.currency = currency

    def __str__(self):
        return f"₹{self.value}"

    def __repr__(self):
        return f"Coin(value={self.value}, currency={self.currency!r})"

c1 = Coin(10)
c2 = Coin(5, "USD")
coins = [c1, c2]

print(c1)                   # Line 1
print(repr(c1))             # Line 2
print(str(c1))              # Line 3
print(coins)                # Line 4
print(f"Pay {c1}")          # Line 5
print(f"Debug {c1!r}")      # Line 6
```

**Predictions:**
```
Line 1: ______
Line 2: ______
Line 3: ______
Line 4: ______
Line 5: ______
Line 6: ______
```

---

### A2. Comparison and `@total_ordering`

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other):
        if not isinstance(other, Version): return NotImplemented
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other):
        if not isinstance(other, Version): return NotImplemented
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

v1 = Version(1, 0, 0)
v2 = Version(2, 0, 0)
v3 = Version(1, 5, 0)
v4 = Version(1, 0, 0)

print(v1 == v4)         # Line 1
print(v1 < v2)          # Line 2
print(v2 > v3)          # Line 3
print(v1 >= v4)         # Line 4
print(v3 <= v2)         # Line 5

versions = [v2, v1, v3, v4]
versions.sort()
print(versions)         # Line 6
```

**Predictions:**
```
Line 1: ___
Line 2: ___
Line 3: ___
Line 4: ___
Line 5: ___
Line 6: ______________________________
```

---

### A3. Arithmetic Magic Methods

```python
class Counter:
    def __init__(self, count=0):
        self.count = count

    def __add__(self, other):
        if isinstance(other, Counter):
            return Counter(self.count + other.count)
        if isinstance(other, int):
            return Counter(self.count + other)
        return NotImplemented

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)

    def __iadd__(self, other):
        if isinstance(other, Counter):
            self.count += other.count
        elif isinstance(other, int):
            self.count += other
        else:
            return NotImplemented
        return self

    def __repr__(self):
        return f"Counter({self.count})"

c1 = Counter(5)
c2 = Counter(3)

print(c1 + c2)          # Line 1
print(c1 + 10)          # Line 2
print(0 + c1)           # Line 3 — which method?

c1 += c2
print(c1)               # Line 4

print(sum([Counter(1), Counter(2), Counter(3)]))  # Line 5
```

**Predictions:**
```
Line 1: ______
Line 2: ______
Line 3: ______   (which method was called: __add__ or __radd__?)
Line 4: ______
Line 5: ______
```

---

### A4. Container Methods

```python
class NumberRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self._numbers = list(range(start, end + 1))

    def __len__(self): return len(self._numbers)
    def __getitem__(self, idx): return self._numbers[idx]
    def __contains__(self, val): return self.start <= val <= self.end
    def __iter__(self): return iter(self._numbers)
    def __bool__(self): return self.start < self.end

r = NumberRange(3, 7)

print(len(r))           # Line 1
print(r[0])             # Line 2
print(r[-1])            # Line 3
print(r[1:3])           # Line 4
print(5 in r)           # Line 5
print(9 in r)           # Line 6
print(list(r))          # Line 7
print(bool(NumberRange(5, 5)))  # Line 8
```

**Predictions:**
```
Line 1: ___
Line 2: ___
Line 3: ___
Line 4: ______
Line 5: ___
Line 6: ___
Line 7: ______
Line 8: ___
```

---

### A5. Context Manager Flow

```python
class Tracker:
    def __init__(self, name):
        self.name = name
        self.operations = []

    def __enter__(self):
        print(f"START: {self.name}")
        self.operations.append("enter")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.operations.append("exit")
        if exc_type:
            print(f"ERROR: {exc_type.__name__}")
            self.operations.append("error")
            return False    # don't suppress
        print(f"END: {self.name}")
        return True

t = Tracker("test")

# Scenario 1: Normal execution
with t as tracker:
    tracker.operations.append("work")

print(t.operations)     # Line 1

# Scenario 2: Exception
t2 = Tracker("risky")
try:
    with t2:
        t2.operations.append("work")
        raise ValueError("oops")
        t2.operations.append("after_error")  # never runs
except ValueError:
    pass

print(t2.operations)    # Line 2
```

**Predictions:**
```
Line 1: ______________________________
Line 2: ______________________________
```

---

### A6. Dataclass Behavior

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    host: str
    port: int = 8080
    debug: bool = False
    allowed_hosts: list = field(default_factory=list)

    def __post_init__(self):
        if self.port < 0 or self.port > 65535:
            raise ValueError(f"Invalid port: {self.port}")

c1 = Config("localhost")
c2 = Config("localhost")
c3 = Config("example.com", port=443)

print(c1)               # Line 1
print(c1 == c2)         # Line 2
print(c1 == c3)         # Line 3
print(c1 is c2)         # Line 4

c1.allowed_hosts.append("local")
print(c2.allowed_hosts) # Line 5 — affected?
```

**Predictions:**
```
Line 1: ______________________________
Line 2: ___
Line 3: ___
Line 4: ___
Line 5: ______   (is c2 affected?)
```

---

## Section B — Fill in the Blanks

### B1. Complete the Magic Methods

```python
from functools import total_ordering

@______
class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius

    def ______(self) -> str:                    # 1. user-friendly: "25°C"
        return f"{self.celsius}°C"

    def ______(self) -> str:                    # 2. developer: "Temperature(25)"
        return f"Temperature({self.celsius})"

    def ______(self, other) -> bool:            # 3. equality: == operator
        if not isinstance(other, Temperature):
            return ______                       # 4. correct return for wrong types
        return self.celsius == other.celsius

    def ______(self, other) -> bool:            # 5. less-than: < operator
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius ______ other.celsius  # 6. comparison

    def ______(self, other) -> "Temperature":   # 7. addition: +
        return Temperature(self.celsius + other.celsius)
```

---

### B2. Complete the Dataclass

```python
from dataclasses import ______, ______        # 1. import dataclass and field
from typing import ClassVar

@______(______)                                # 2. decorator for ordering support
class Employee:
    sort_index: float = ______(init=False, repr=False)  # 3. computed sort field
    name: str
    salary: float
    department: str = "Engineering"
    skills: list = ______(default_factory=______)      # 4. mutable default

    # class variable — NOT a field
    company: ______ = "TechCorp"                        # 5. ClassVar annotation

    def ______(self) -> None:                            # 6. post-init method
        if self.salary < 0:
            raise ValueError("Salary can't be negative")
        self.sort_index = self.salary          # sort by salary
```

---

### B3. Complete the Context Manager

```python
class Timer:
    def __init__(self, label: str = ""):
        self.label = label
        self.elapsed = 0.0

    def ______(self) -> "Timer":           # 1. __enter__ returns self
        import time
        self._______ = time.perf_counter() # 2. store start time (hint: use _start)
        if self.label:
            print(f"⏱ Started: {self.label}")
        return ______                      # 3. return the resource

    def ______(self, exc_type, exc_val, exc_tb) -> bool:  # 4. __exit__ signature
        import time
        self.elapsed = time.perf_counter() - self._start
        status = "⚠️  Failed" if exc_type else "✅ Done"
        print(f"{status}: {self.label} ({self.elapsed:.3f}s)")
        return ______                      # 5. don't suppress exceptions
```

---

## Section C — Debugging Exercises

### C1. The Recursion in `__repr__`

```python
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

    def __repr__(self):
        return f"Node({self.value!r}, next={repr(self.next_node)})"

# This can cause infinite recursion!
n1 = Node(1)
n2 = Node(2, n1)
n3 = Node(3, n2)
n1.next_node = n3   # circular reference!
print(repr(n1))     # RecursionError!
```

**Explain the problem and write a fix:**
```python
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

    def __repr__(self):
        # Fix: don't recursively repr the next node
        next_val = ______ if self.next_node else None
        return f"Node({self.value!r}, next={next_val})"
```

---

### C2. The Missing `__hash__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

p1 = Point(1, 2)
p2 = Point(1, 2)

print(p1 == p2)         # True — works
visited = {p1, p2}      # TypeError: unhashable type!
cache = {p1: "home"}    # TypeError: unhashable type!
```

**Fix it:**
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def ______(self):              # add __hash__
        return hash(______)        # hash a tuple of the same fields as __eq__
```

---

### C3. Wrong Return Type from `__add__`

```python
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return self.amount + other.amount   # BUG: returns a number, not Money!

m1 = Money(10, "USD")
m2 = Money(5, "USD")
result = m1 + m2
print(result)               # 15 — not a Money object!
print(type(result))         # <class 'int'> — wrong!

# result + Money(1)         # TypeError: unsupported operand types!
```

**Fix:**
```python
def __add__(self, other):
    if self.currency != other.currency:
        raise ValueError("Cannot add different currencies")
    return ______  # return correct type
```

---

### C4. Context Manager Not Closing on Exception

```python
class ResourceManager:
    def __init__(self, name):
        self.name = name
        self.open = False

    def __enter__(self):
        self.open = True
        print(f"Opened: {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:        # BUG: only closes on success!
            self.open = False
            print(f"Closed: {self.name}")

rm = ResourceManager("DB")
try:
    with rm:
        raise RuntimeError("crash!")
except RuntimeError:
    pass

print(rm.open)   # True! — resource was NOT closed!
```

**Fix `__exit__`:**
```python
def __exit__(self, exc_type, exc_val, exc_tb):
    ______          # always close
    ______
    if exc_type:
        print(f"Exception: {exc_val}")
    return ______   # don't suppress
```

---

### C5. Dataclass Mutable Default

```python
from dataclasses import dataclass

@dataclass
class Team:
    name: str
    members: list = []      # Bug! ValueError at class definition

t1 = Team("Alpha")
t2 = Team("Beta")
t1.members.append("Alice")
print(t2.members)   # Would show ['Alice'] — shared list bug!
```

**Fix:**
```python
from dataclasses import dataclass, field

@dataclass
class Team:
    name: str
    members: list = ______(default_factory=______)  # Fix here
```

---

## Section D — Write the Code

### D1. Order Class — Full Magic Methods

```python
"""
Build Order class with complete magic method support.

Requirements:
- __init__(order_id: str, customer: str)
- __repr__: "Order(id='ORD-001', customer='Alice', items=2)"
- __str__: formatted multi-line order receipt
- __eq__: compare by order_id
- __lt__: compare by total amount (for sorting)
- __len__: number of line items
- __bool__: True if has items
- __getitem__: access item by index, supports slicing
- __setitem__: update item at index
- __delitem__: delete item at index
- __contains__: 'ProductName' in order (by name)
- __iter__: iterate over items
- __add__: merge two orders into a new one
- add_item(name, price, qty=1): adds to _items
- total property: sum of price × qty
- item_count property: sum of all quantities
"""

from functools import total_ordering

@total_ordering
class Order:
    def __init__(self, order_id: str, customer: str):
        self.order_id = order_id
        self.customer = customer
        self._items: list[dict] = []

    # Your implementation here


# Test suite
def test_order():
    o1 = Order("ORD-001", "Alice")
    o1.add_item("Widget", 9.99, 2)
    o1.add_item("Gadget", 24.99, 1)

    o2 = Order("ORD-002", "Bob")
    o2.add_item("Thingamajig", 4.99, 5)

    # String
    print(repr(o1))
    print(o1)

    # Container
    assert len(o1) == 2
    assert bool(o1) == True
    assert bool(Order("x", "y")) == False
    assert o1[0]["name"] == "Widget"
    assert "Widget" in o1
    assert "Invisible" not in o1

    items = list(o1)
    assert len(items) == 2

    # Comparison
    assert o1 > o2      # 44.97 > 24.95
    assert o2 < o1
    orders = [o1, o2]
    orders.sort()
    assert orders[0].order_id == "ORD-002"   # cheaper first

    # Equality
    o3 = Order("ORD-001", "Different Customer")
    assert o1 == o3     # same ID = equal
    assert o1 != o2

    # Arithmetic
    combined = o1 + o2
    assert len(combined) == 3

    # Mutation
    del o1[0]
    assert len(o1) == 1
    assert "Widget" not in o1

    print("✅ All Order tests passed!")

test_order()
```

---

### D2. Vector Class with Full Arithmetic

```python
"""
Build a 2D Vector class with complete arithmetic support.

Requirements:
- __init__(x: float, y: float)
- __repr__: "Vector(3.0, 4.0)"
- __str__: "(3.0, 4.0)"
- __eq__: compare element-wise (use math.isclose for floats)
- __add__: Vector + Vector
- __sub__: Vector - Vector
- __mul__: Vector * scalar (returns Vector) AND scalar * Vector (__rmul__)
- __truediv__: Vector / scalar
- __neg__: -Vector
- __abs__: abs(Vector) → magnitude (Euclidean length)
- __iadd__: Vector += other
- __radd__: supports sum([v1, v2, v3])
- Properties: magnitude (same as abs), normalized
- Methods: dot(other), angle_to(other) in degrees
"""

import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    # Your implementation here


# Test suite
def test_vector():
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    # String
    print(v1)                               # (3.0, 4.0)
    print(repr(v1))                         # Vector(3.0, 4.0)

    # Arithmetic
    assert (v1 + v2) == Vector(4, 6)
    assert (v1 - v2) == Vector(2, 2)
    assert (v1 * 2) == Vector(6, 8)
    assert (2 * v1) == Vector(6, 8)         # __rmul__
    assert (v1 / 2) == Vector(1.5, 2.0)
    assert (-v1) == Vector(-3, -4)
    assert abs(v1) == 5.0                   # 3-4-5 triangle

    # in-place
    v3 = Vector(1, 0)
    v3 += Vector(2, 0)
    assert v3 == Vector(3, 0)

    # sum() works
    total = sum([Vector(1,0), Vector(2,0), Vector(3,0)])
    assert total == Vector(6, 0)

    # Properties
    assert math.isclose(v1.magnitude, 5.0)
    normalized = v1.normalized
    assert math.isclose(normalized.magnitude, 1.0)

    # Methods
    dot = v1.dot(v2)
    assert dot == 11.0  # 3×1 + 4×2

    print("✅ All Vector tests passed!")

test_vector()
```

---

### D3. Complete Dataclass System

```python
"""
Build a complete product catalog using dataclasses:

1. @dataclass Category:
   - name: str
   - description: str = ""
   - __str__: just the name

2. @dataclass(order=True) Product:
   - sort_index: float (init=False, repr=False) — set in __post_init__
   - sku: str
   - name: str
   - price: float
   - stock: int = 0
   - category: Category = None (field with default)
   - tags: list[str] = field(default_factory=list)
   - __post_init__:
     - price must be > 0
     - stock must be >= 0
     - sort_index = price
   - Properties: total_value, is_available, display_price (with "₹" prefix)
   - Method: apply_discount(percent: float) — creates NEW discounted Product

3. @dataclass(frozen=True) PriceSnapshot:
   - sku: str
   - price: float
   - timestamp: datetime (default_factory=datetime.now)
   - is_discounted: bool = False

4. Functions:
   - cheapest(products: list[Product]) → Product
   - by_category(products, cat_name: str) → list[Product]
   - serialize_catalog(products) → list[dict]  (using asdict)
   - deserialize_product(data: dict) → Product

Demo:
   electronics = Category("Electronics", "Gadgets and devices")
   laptop = Product("LAP001", "Laptop Pro", 75000, 5, electronics)
   phone = Product("PHN001", "Smartphone X", 45000, 10, electronics)
   
   print(sorted([phone, laptop]))   # sorted by price
   snapshot = PriceSnapshot(laptop.sku, laptop.price)
   catalog_json = serialize_catalog([laptop, phone])
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

@dataclass
class Category:
    # Your implementation
    pass

@dataclass(order=True)
class Product:
    # Your implementation
    pass

@dataclass(frozen=True)
class PriceSnapshot:
    # Your implementation
    pass


# Test
def test_catalog():
    electronics = Category("Electronics")
    food = Category("Food", "Consumables")

    laptop = Product("LAP001", "Laptop Pro", 75000, 5, electronics, ["portable", "premium"])
    phone = Product("PHN001", "Smartphone X", 45000, 10, electronics)
    rice = Product("RCE001", "Basmati Rice", 250, 100, food, ["organic"])

    # Ordering
    products = [laptop, rice, phone]
    sorted_products = sorted(products)
    assert sorted_products[0].sku == "RCE001"   # cheapest first

    # Properties
    assert laptop.is_available == True
    assert math.isclose(laptop.total_value, 75000 * 5)

    # Discount
    discounted = laptop.apply_discount(10)
    assert math.isclose(discounted.price, 67500)
    assert laptop.price == 75000    # original unchanged!

    # Frozen PriceSnapshot
    snap = PriceSnapshot(laptop.sku, laptop.price)
    try:
        snap.price = 0  # FrozenInstanceError!
    except Exception:
        pass

    # Serialization
    catalog = [laptop, phone, rice]
    serialized = serialize_catalog(catalog)
    assert isinstance(serialized[0], dict)
    assert "sku" in serialized[0]

    print("✅ All catalog tests passed!")

import math
test_catalog()
```

---

### D4. Context Manager — Database Simulation

```python
"""
Build a DatabaseConnection context manager that simulates real DB behavior:

Requirements:
- __init__(db_name, readonly=False)
- __enter__: "connect", return self
- __exit__: "commit" on success, "rollback" on exception, always "close"
  - Never suppress exceptions
- Methods:
  - execute(sql) → list[dict]: only when connected
  - begin_transaction() → None
  - commit() → None
  - rollback() → None
- Properties:
  - is_connected: bool
  - query_count: int

Also implement using @contextmanager from contextlib (bonus):
- Same behavior as above but using a generator function

Usage:
with DatabaseConnection("users_db") as db:
    results = db.execute("SELECT * FROM users")
    db.execute("UPDATE users SET active=True WHERE id=1")
# → auto-commit on success, auto-close always

try:
    with DatabaseConnection("orders_db") as db:
        db.execute("INSERT INTO orders VALUES (...)")
        raise ValueError("Validation failed!")
except ValueError:
    pass
# → auto-rollback, auto-close, exception propagates
"""

class DatabaseConnection:
    def __init__(self, db_name: str, readonly: bool = False):
        self.db_name = db_name
        self.readonly = readonly
        self._connected = False
        self._in_transaction = False
        self._query_count = 0
        self._query_log: list[str] = []

    def __enter__(self) -> "DatabaseConnection":
        # Your implementation
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        # Your implementation
        pass

    def execute(self, sql: str) -> list[dict]:
        # Your implementation
        pass

    @property
    def is_connected(self) -> bool: return self._connected

    @property
    def query_count(self) -> int: return self._query_count

    def __repr__(self) -> str:
        status = "connected" if self._connected else "closed"
        return f"DatabaseConnection({self.db_name!r}, {status}, queries={self._query_count})"


# Test
def test_db_connection():
    # Normal usage
    with DatabaseConnection("test_db") as db:
        assert db.is_connected == True
        rows = db.execute("SELECT * FROM test")
        assert db.query_count == 1

    assert db.is_connected == False     # closed after with block

    # Exception handling
    conn = DatabaseConnection("prod_db")
    try:
        with conn as db:
            db.execute("INSERT INTO logs VALUES (1)")
            raise ValueError("Simulated error")
    except ValueError:
        pass

    assert conn.is_connected == False   # still closed
    assert conn.query_count == 1        # 1 query before error

    # Cannot execute when not connected
    try:
        conn.execute("SELECT 1")
        assert False, "Should raise RuntimeError"
    except RuntimeError:
        pass

    print("✅ All DatabaseConnection tests passed!")

test_db_connection()
```

---

## Section E — Magic Method Experiments

### E1. Arithmetic Chain with `sum()`

```python
# Experiment: understand __radd__ with sum()
class Money:
    def __init__(self, amount, currency="INR"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if isinstance(other, Money):
            return Money(self.amount + other.amount, self.currency)
        return NotImplemented

    def __radd__(self, other):
        print(f"  __radd__ called with other={other!r}")
        if other == 0:  # sum() starts with 0
            return self
        return self.__add__(other)

    def __repr__(self):
        return f"₹{self.amount}"

prices = [Money(100), Money(200), Money(300)]
print("Calling sum():")
total = sum(prices)
print(f"Total: {total}")
```

**What to observe:**
```
How many times is __radd__ called? ___
What was 'other' on the first call? ___
Why does sum() need __radd__ and not just __add__? 
_____________________________________________
```

---

### E2. Context Manager Exception Suppression

```python
class Suppressor:
    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Return True to suppress the exception!
        if exc_type and issubclass(exc_type, self.exceptions):
            print(f"Suppressed: {exc_type.__name__}: {exc_val}")
            return True
        return False    # don't suppress other exceptions

# Test these scenarios:
print("Scenario 1: suppressed exception")
with Suppressor(ValueError, TypeError):
    raise ValueError("This will be suppressed!")
print("Code continues here!")

print("\nScenario 2: non-suppressed exception")
try:
    with Suppressor(ValueError):
        raise KeyError("This will NOT be suppressed")
except KeyError as e:
    print(f"Got through: {e}")

print("\nScenario 3: no exception")
with Suppressor(ValueError):
    x = 1 + 1
print(f"x = {x}")
```

**Questions:**
```
After Scenario 1, does code continue or stop? ___
Why does `print("Code continues here!")` run? 
_____________________________________________
```

---

### E3. Dataclass Field Inspection

```python
from dataclasses import dataclass, field, fields, asdict, astuple

@dataclass
class Product:
    name: str
    price: float
    stock: int = 0
    tags: list = field(default_factory=list, repr=False)

# Inspect the dataclass fields
p = Product("Widget", 9.99, 5, tags=["sale"])

print("Fields:")
for f in fields(Product):
    print(f"  {f.name}: type={f.type}, default={f.default}, in_repr={f.repr}")

print("\nasdict:", asdict(p))
print("astuple:", astuple(p))

# Modify
p.price = 7.99
p.tags.append("discount")
print("\nAfter modification:")
print(p)
print(asdict(p))
```

**Record what you see:**
```
Which fields appear in __repr__ output? ___
Does 'tags' appear in repr? Why? ___
What does asdict include? ___
Can you modify a non-frozen dataclass? ___
```

---

## Section F — Mini Project: Complete E-commerce Cart System

```python
"""
Build a complete cart system using magic methods + dataclasses:

1. @dataclass(frozen=True) ProductID:
   - sku: str (must be uppercase in __post_init__)
   - Use as dict key

2. @dataclass(order=True) CartItem:
   - sort_index: float = field(init=False) → price × quantity
   - product_name: str
   - price: float (validated > 0)
   - quantity: int (validated > 0)
   - __post_init__: set sort_index, validate fields
   - Properties: subtotal, display

3. ShoppingCart class with magic methods:
   - __init__(customer_name: str)
   - __len__: number of cart items
   - __bool__: True if not empty
   - __getitem__: cart[sku] → CartItem
   - __setitem__: cart[sku] = CartItem (or update quantity)
   - __delitem__: cart[sku] removes item
   - __contains__: sku in cart
   - __iter__: iterate over CartItems
   - __add__: cart1 + cart2 → merged cart
   - __str__: formatted receipt
   - __repr__: CartItem(customer, count, total)
   - Properties: total, item_count, is_empty
   - Methods:
     - add(name, price, qty=1) → None
     - remove(sku) → CartItem
     - update_qty(sku, qty) → None
     - apply_coupon(code) → float (discount amount)
       codes: "SAVE10" → 10%, "FLAT50" → ₹50 flat
     - checkout() → dict (summary)

Demo:
cart1 = ShoppingCart("Alice")
cart1.add("Widget", 9.99, 2)
cart1.add("Gadget", 24.99)
print(len(cart1))         # 2
print("Widget" in cart1)  # True
print(cart1.total)        # 44.97

cart2 = ShoppingCart("Alice")
cart2.add("Thingamajig", 4.99)

combined = cart1 + cart2
print(len(combined))      # 3

cart1.apply_coupon("SAVE10")
print(cart1.checkout())
"""

from dataclasses import dataclass, field, asdict
from functools import total_ordering
from typing import Iterator, Optional

@dataclass(frozen=True)
class ProductID:
    sku: str

    def __post_init__(self):
        object.__setattr__(self, 'sku', self.sku.upper())

@dataclass(order=True)
class CartItem:
    # Your implementation
    pass

class ShoppingCart:
    COUPONS = {"SAVE10": ("percent", 10), "FLAT50": ("flat", 50)}

    def __init__(self, customer_name: str):
        self.customer_name = customer_name
        self._items: dict[str, CartItem] = {}   # sku → CartItem

    # Your magic methods and business logic here


# Test
def run_cart_demo():
    cart = ShoppingCart("Alice")

    # Add items
    cart.add("Widget", 9.99, 2)
    cart.add("Gadget", 24.99)
    cart.add("Thingamajig", 4.99, 3)

    # Magic method tests
    print(f"Items: {len(cart)}")               # __len__
    print(f"Has Widget: {'WIDGET' in cart}")   # __contains__
    print(f"Empty: {bool(ShoppingCart('x'))}") # __bool__

    for item in cart:                          # __iter__
        print(f"  {item.product_name}: {item.display}")

    # Modify
    cart.update_qty("WIDGET", 5)
    del cart["GADGET"]                         # __delitem__

    # Merge carts
    cart2 = ShoppingCart("Alice")
    cart2.add("Bonus Item", 1.0)
    combined = cart + cart2                    # __add__

    # Coupon
    discount = cart.apply_coupon("SAVE10")
    print(f"Discount: ₹{discount:.2f}")

    # Checkout
    summary = cart.checkout()
    print(f"Checkout: {summary}")

    print(str(cart))                           # __str__

run_cart_demo()
```

---

## ✅ Answer Key

<details>
<summary>Click to reveal — attempt everything first!</summary>

### A1 Answers
```
Line 1: ₹10
Line 2: Coin(value=10, currency='INR')
Line 3: ₹10
Line 4: [Coin(value=10, currency='INR'), Coin(value=5, currency='USD')]
Line 5: Pay ₹10
Line 6: Debug Coin(value=10, currency='INR')
```

### A2 Answers
```
Line 1: True
Line 2: True
Line 3: True   (2.0.0 > 1.5.0 ← tuple comparison)
Line 4: True   (1.0.0 >= 1.0.0)
Line 5: True   (1.5.0 <= 2.0.0)
Line 6: [1.0.0, 1.0.0, 1.5.0, 2.0.0]  (sorted by tuple comparison)
```

### A3 Answers
```
Line 1: Counter(8)   ← __add__ creates new Counter
Line 2: Counter(15)  ← __add__ with int
Line 3: Counter(5)   ← __radd__(0) returns self (0 + Counter)
Line 4: Counter(8)   ← __iadd__ modifies in-place, c1.count was 5, += Counter(3)
Line 5: Counter(6)   ← sum starts with 0, __radd__ handles it
```

### A4 Answers
```
Line 1: 5     (range 3-7 has 5 elements: 3,4,5,6,7)
Line 2: 3     (first element)
Line 3: 7     (last element, negative index)
Line 4: [4, 5] (indices 1:3 → elements at index 1 and 2)
Line 5: True
Line 6: False  (9 is outside 3-7)
Line 7: [3, 4, 5, 6, 7]
Line 8: False  (start == end, __bool__ returns start < end → 5 < 5 → False)
```

### A5 Answers
```
Line 1: ['enter', 'work', 'exit']  (no exception, __exit__ ran normally)
Line 2: ['enter', 'work', 'exit', 'error']  (exception, __exit__ ran with exc)
```

### A6 Answers
```
Line 1: Config(host='localhost', port=8080, debug=False, allowed_hosts=[])
Line 2: True
Line 3: False  (host or port differs)
Line 4: False  (different objects in memory)
Line 5: []   — c2.allowed_hosts is empty! field(default_factory=list) creates SEPARATE lists
```

### B1 Answers
```python
@total_ordering
def __str__(self): return f"{self.celsius}°C"
def __repr__(self): return f"Temperature({self.celsius})"
def __eq__(self, other): ...
    return NotImplemented
def __lt__(self, other): ...
    return self.celsius < other.celsius
def __add__(self, other): return Temperature(self.celsius + other.celsius)
```

### C1 Fix
```python
def __repr__(self):
    next_val = self.next_node.value if self.next_node else None
    return f"Node({self.value!r}, next={next_val})"
```

### C2 Fix
```python
def __hash__(self):
    return hash((self.x, self.y))
```

### C3 Fix
```python
return Money(self.amount + other.amount, self.currency)
```

### C4 Fix
```python
def __exit__(self, exc_type, exc_val, exc_tb):
    self.open = False           # ALWAYS close
    print(f"Closed: {self.name}")
    if exc_type:
        print(f"Exception: {exc_val}")
    return False                # don't suppress
```

### C5 Fix
```python
members: list = field(default_factory=list)
```

</details>

---

## 📊 Self-Assessment Checklist

| Concept | ✅ Got it | 🔄 Need review | ❓ Confused |
|---------|-----------|---------------|------------|
| `__str__` vs `__repr__` — when each is called | | | |
| Writing `__repr__` that looks recreatable | | | |
| `__eq__` and returning `NotImplemented` | | | |
| `__eq__` breaking `__hash__` — and the fix | | | |
| `@total_ordering` and which method to define | | | |
| `__add__`, `__radd__`, `__iadd__` distinction | | | |
| Why `sum()` needs `__radd__` | | | |
| Container methods — `__len__`, `__getitem__`, `__contains__`, `__iter__` | | | |
| `__enter__` and `__exit__` flow | | | |
| `__exit__` always runs (even on exception) | | | |
| Return value of `__exit__` — True vs False | | | |
| `__call__` making objects callable | | | |
| `@dataclass` — what it auto-generates | | | |
| `field(default_factory=list)` — why required | | | |
| `__post_init__` — validation and computed fields | | | |
| `frozen=True` — immutability and hashability | | | |
| `asdict()` — converting dataclass to dict | | | |

**Score:**
- 17/17 ✅ — Excellent! Ready for Day 9 (Decorators — you'll see `@dataclass` from a new angle)
- 11–16 ✅ — Good. Focus on `__radd__`, `__exit__` behavior, and the `__hash__` gotcha
- < 11 ✅ — Re-do the Order class exercise — it covers the most important magic methods in one class

---

*Day 8 Exercises Complete — Day 9: Decorators — function wrappers, `@functools.wraps`, parametrized decorators, class decorators*
