# 🎯 Python Full Stack — Day 8 Interview Preparation
# Topic: Magic Methods & Dataclasses

> **How to use:** Attempt each answer before reading. Magic methods questions almost always ask you to write a class from scratch — practise doing that. Know the difference between `__str__`/`__repr__`, when `__hash__` matters, and the three `__add__`/`__radd__`/`__iadd__` variants.

---

## 🟢 Beginner Level Questions

---

### Q1. What are magic methods (dunders)? Give three examples.

**Answer:**
Magic methods are special methods with double underscores on both sides (`__method__`). Python calls them automatically in response to built-in operations — you never call them directly.

```python
class Box:
    def __init__(self, volume):      # called by Box(5) — constructor
        self.volume = volume

    def __str__(self):               # called by print(box) and str(box)
        return f"Box({self.volume}L)"

    def __add__(self, other):        # called by box1 + box2
        return Box(self.volume + other.volume)

    def __len__(self):               # called by len(box)
        return self.volume

b1 = Box(10)
b2 = Box(5)
print(b1)           # Box(10L)       ← __str__
print(b1 + b2)      # Box(15L)       ← __add__
print(len(b1))      # 10             ← __len__
```

**Other examples:** `__repr__`, `__eq__`, `__lt__`, `__getitem__`, `__enter__`, `__exit__`, `__call__`, `__iter__`, `__contains__`.

---

### Q2. What is the difference between `__str__` and `__repr__`?

**Answer:**

| | `__str__` | `__repr__` |
|-|-----------|------------|
| Audience | End users | Developers |
| Called by | `print()`, `str()`, f-strings | `repr()`, REPL, inside lists/dicts |
| Goal | Readable, friendly | Unambiguous, ideally recreatable |
| Fallback | Falls back to `__repr__` if not defined | Falls back to `<ClassName at 0x...>` |

```python
class Temperature:
    def __init__(self, c): self.c = c

    def __str__(self): return f"{self.c}°C"          # friendly

    def __repr__(self): return f"Temperature({self.c})"  # precise

t = Temperature(25)
print(t)             # 25°C          ← __str__
print(repr(t))       # Temperature(25) ← __repr__
print([t])           # [Temperature(25)] ← list uses __repr__
print(f"{t!r}")      # Temperature(25)  ← force __repr__ in f-string
```

**Rule:** If you define only one, define `__repr__` — it's used as fallback everywhere.

---

### Q3. What does `__eq__` do? What happens if you don't define it?

**Answer:**
`__eq__` defines the behavior of `==`. Without it, Python compares **identity** (whether two variables point to the same object in memory) — almost never what you want for custom objects.

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Without __eq__
p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)     # False! — different objects in memory

# With __eq__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)     # True — compares values!
```

---

### Q4. What does `__len__` enable?

**Answer:**
`__len__` enables the `len()` function and also controls truth testing (`if obj:`). When `__len__` returns 0, the object is falsy.

```python
class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __len__(self):
        return len(self.songs)

p = Playlist(["Song A", "Song B", "Song C"])
print(len(p))   # 3

empty = Playlist([])
print(bool(empty))  # False  — len() returns 0 → falsy
if p:
    print("Has songs!")   # prints — len() returns 3 → truthy
```

---

### Q5. What is `@dataclass` and what does it generate automatically?

**Answer:**
`@dataclass` is a decorator that automatically generates boilerplate methods based on field annotations.

Auto-generated with default settings: `__init__`, `__repr__`, `__eq__`

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

# This is equivalent to writing ALL of this:
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point(x={self.x!r}, y={self.y!r})"
    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented

p = Point(1.0, 2.0)
print(p)                # Point(x=1.0, y=2.0)
print(p == Point(1,2))  # True
```

---

### Q6. What does `__contains__` enable? What happens if it's not defined but `__iter__` is?

**Answer:**
`__contains__` defines the `in` operator: `x in obj`.

```python
class NumberSet:
    def __init__(self, *nums): self.nums = set(nums)

    def __contains__(self, item) -> bool:
        return item in self.nums

ns = NumberSet(1, 2, 3, 4, 5)
print(3 in ns)   # True   ← __contains__
print(9 in ns)   # False
```

**If `__contains__` is not defined but `__iter__` is:** Python falls back to iterating through all elements and checking equality — works but is O(n) instead of potentially O(1). Always define `__contains__` explicitly for containers where membership testing should be fast.

---

## 🟡 Intermediate Level Questions

---

### Q7. What is `@functools.total_ordering`? When and why do you use it?

**Answer:**
`@total_ordering` is a class decorator. If you define `__eq__` and ONE comparison method (`__lt__`, `__le__`, `__gt__`, or `__ge__`), it **generates all the remaining five comparison methods** automatically.

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa

    def __eq__(self, other):
        if not isinstance(other, Student): return NotImplemented
        return self.gpa == other.gpa

    def __lt__(self, other):
        if not isinstance(other, Student): return NotImplemented
        return self.gpa < other.gpa

    # total_ordering generates: __le__, __gt__, __ge__ automatically!

students = [Student("Carol", 3.9), Student("Bob", 3.5), Student("Alice", 3.7)]
students.sort()             # uses __lt__
for s in students:
    print(f"{s.name}: {s.gpa}")

s1 = Student("Alice", 3.7)
s2 = Student("Bob", 3.5)
print(s1 > s2)              # True — generated by total_ordering
print(s1 >= s2)             # True — generated
print(s1 <= s2)             # False — generated
```

**Without `@total_ordering`:** You'd have to write all 6 comparison methods manually.

---

### Q8. What is `__radd__` and why is it needed for `sum()` to work with custom objects?

**Answer:**
`__radd__` handles the case where the LEFT operand doesn't know how to add the RIGHT operand.

When Python evaluates `a + b`:
1. Tries `a.__add__(b)` — if returns `NotImplemented`, try next
2. Tries `b.__radd__(a)` — the right object's reflected add

`sum([v1, v2, v3])` starts with an implicit `0` (the identity element). So it does:
`0 + v1` → `int.__add__(0, v1)` → `NotImplemented` → `v1.__radd__(0)` → handles it!

```python
class Vector:
    def __init__(self, x, y): self.x = x; self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector): return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        if other == 0:          # sum() starts with integer 0
            return self
        return self.__add__(other)

    def __repr__(self): return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = Vector(5, 6)

print(sum([v1, v2, v3]))    # Vector(9, 12) ← works because of __radd__!
# Without __radd__: TypeError!
```

---

### Q9. Explain context managers: how do `__enter__` and `__exit__` work?

**Answer:**
A context manager implements `__enter__` and `__exit__` to define setup and teardown behavior for the `with` statement.

```python
class ManagedFile:
    def __init__(self, path, mode="r"):
        self.path = path
        self.mode = mode

    def __enter__(self):
        """Setup: open the file, return it."""
        print(f"Opening {self.path}")
        self.file = open(self.path, self.mode)
        return self.file        # bound to 'as f'

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Teardown: always runs, even on exception."""
        print("Closing file")
        self.file.close()
        # Return False → exceptions propagate (correct for most cases)
        # Return True → exceptions are suppressed
        return False

with ManagedFile("test.txt", "w") as f:
    f.write("Hello!")
# File is guaranteed to close — even if f.write() raises!
```

**`__exit__` parameters:**
- `exc_type`: exception class (None if no exception)
- `exc_val`: exception instance
- `exc_tb`: traceback object
- Return `True` → suppresses the exception
- Return `False` (or `None`) → exception propagates

---

### Q10. Why does defining `__eq__` in Python break hashability? How do you fix it?

**Answer:**
Python automatically sets `__hash__ = None` when you define `__eq__`. This is because Python's contract requires: **equal objects must have the same hash**. If you can define custom equality, the default hash (based on `id()`) would violate this contract — two equal objects would have different hashes.

```python
class Color:
    def __init__(self, r, g, b):
        self.r = r; self.g = g; self.b = b

    def __eq__(self, other):
        return (self.r, self.g, self.b) == (other.r, other.g, other.b)
    # Python now sets __hash__ = None!

c = Color(255, 0, 0)
hash(c)             # TypeError: unhashable type: 'Color'
{c: "red"}          # TypeError!

# Fix: explicitly define __hash__
class Color:
    def __init__(self, r, g, b):
        self.r = r; self.g = g; self.b = b

    def __eq__(self, other):
        return (self.r, self.g, self.b) == (other.r, other.g, other.b)

    def __hash__(self):
        return hash((self.r, self.g, self.b))   # tuple hash is stable

c1 = Color(255, 0, 0)
c2 = Color(255, 0, 0)
print(c1 == c2)         # True
print(hash(c1) == hash(c2))  # True ← consistent with equality
color_map = {c1: "red"}       # works!
```

---

### Q11. What is `__post_init__` in dataclasses? When do you use it?

**Answer:**
`__post_init__` is called automatically after the generated `__init__` completes. It's the place for validation, computed fields, and any setup that needs the fields already set.

```python
from dataclasses import dataclass, field
import math

@dataclass
class Circle:
    radius: float
    area: float = field(init=False)        # computed — not in __init__ signature

    def __post_init__(self):
        # 1. Validation
        if self.radius <= 0:
            raise ValueError(f"Radius must be positive, got {self.radius}")
        # 2. Computed field (after radius is set)
        self.area = math.pi * self.radius ** 2

c = Circle(5)
print(c.area)       # 78.54  ← computed by __post_init__
print(c)            # Circle(radius=5, area=78.54...)

try:
    Circle(-1)      # ValueError: Radius must be positive
except ValueError as e:
    print(e)
```

**Common uses:**
- Input validation
- Computing derived fields (`area`, `full_name`, `hash`)
- Post-processing (normalizing, type casting)
- Registering the object somewhere

---

### Q12. What is `frozen=True` in dataclasses and what does it enable?

**Answer:**
`frozen=True` makes all fields immutable — any assignment after `__init__` raises `FrozenInstanceError`. It also **auto-generates `__hash__`**, making the object usable in sets and as dict keys.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float
    # Automatically: immutable + hashable

p = Point(1.0, 2.0)

try:
    p.x = 5.0       # FrozenInstanceError: cannot assign to field 'x'
except Exception as e:
    print(e)

# Now hashable — can be used in sets and dicts
points = {p, Point(3.0, 4.0), Point(1.0, 2.0)}  # {Point(1.0, 2.0), Point(3.0, 4.0)}
print(len(points))  # 2 — duplicates removed!

cache = {Point(0, 0): "origin", Point(1, 0): "unit_x"}
print(cache[Point(0, 0)])   # "origin"
```

**When to use `frozen=True`:**
- Data that should never change (coordinates, configurations, API keys)
- Objects used as dictionary keys or in sets
- Concurrent programming (thread-safe when immutable)

---

## 🔴 Advanced / Senior Level Questions

---

### Q13. Explain the difference between `__getattr__` and `__getattribute__`.

**Answer:**

| | `__getattr__` | `__getattribute__` |
|-|---------------|-------------------|
| When called | Only when attribute is NOT found normally | On EVERY attribute access |
| Risk | Low — safe to override | High — infinite recursion if you access `self.anything` inside it |
| Use case | Dynamic attributes, proxy objects | Complete attribute access control |

```python
class Proxy:
    def __init__(self, target):
        # Must use object.__setattr__ to avoid calling our __setattr__
        object.__setattr__(self, '_target', target)

    def __getattr__(self, name):
        """Only called when attribute is NOT found on Proxy itself."""
        target = object.__getattribute__(self, '_target')
        return getattr(target, name)

# Proxy forwards all attribute access to _target
class Target:
    def hello(self): return "Hello from Target"
    x = 42

proxy = Proxy(Target())
print(proxy.hello())    # Hello from Target ← forwarded via __getattr__
print(proxy.x)          # 42               ← forwarded

# __getattribute__ — called for EVERY access (dangerous!)
class Audited:
    def __getattribute__(self, name):
        print(f"Accessing: {name}")
        return object.__getattribute__(self, name)   # MUST use super version!
        # Don't do: return self.name — infinite recursion!
```

---

### Q14. How would you implement a memoization decorator as a callable class?

**Answer:**
A callable class (with `__call__`) can hold state between calls — perfect for memoization:

```python
class Memoize:
    """Callable class that caches function results."""

    def __init__(self, func):
        self.func = func
        self._cache = {}
        self.__doc__ = func.__doc__         # preserve docstring
        self.__name__ = func.__name__       # preserve name

    def __call__(self, *args, **kwargs):
        # Create a hashable cache key from args
        key = args + tuple(sorted(kwargs.items()))
        if key not in self._cache:
            self._cache[key] = self.func(*args, **kwargs)
        return self._cache[key]

    def cache_info(self) -> dict:
        return {"size": len(self._cache), "keys": list(self._cache.keys())}

    def cache_clear(self) -> None:
        self._cache.clear()

    def __repr__(self):
        return f"Memoize(func={self.__name__!r}, cache_size={len(self._cache)})"


@Memoize
def fibonacci(n: int) -> int:
    """Compute nth Fibonacci number."""
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(35))    # 9227465 — fast!
print(fibonacci.cache_info())
print(callable(fibonacci))  # True — has __call__
```

---

### Q15. When would you choose a dataclass vs namedtuple vs a plain class?

**Answer:**

| | `@dataclass` | `namedtuple` | Plain class |
|-|--------------|--------------|-------------|
| Mutability | Mutable by default (`frozen=True` for immutable) | Always immutable | Flexible |
| Memory | Dict-based (`__dict__`) | Tuple-based (compact) | Dict-based |
| Inheritance | Full support | Limited | Full support |
| Methods | Yes, naturally | Yes, but awkward | Yes |
| Ordering | `order=True` | Built-in tuple ordering | Manual |
| Hashable | Only if `frozen=True` | Yes (always immutable) | Only if `__hash__` defined |
| Ideal for | Data containers with logic | Lightweight records, return values | Full domain objects |

```python
from collections import namedtuple
from dataclasses import dataclass

# namedtuple — ultra-light, immutable, tuple-like
Color = namedtuple("Color", ["r", "g", "b"])
red = Color(255, 0, 0)
print(red.r)            # 255
print(red[0])           # 255  ← tuple indexing works

# @dataclass — mutable, Pythonic, excellent for data containers
@dataclass
class User:
    name: str
    email: str
    is_active: bool = True
    # Mutable — can change fields after creation

# Plain class — when you need full control and complex logic
class Order:
    def __init__(self, customer, items):
        self.customer = customer
        self._items = items
        self._validate()  # complex initialization logic
```

---

## 📝 Quick-Fire Answers

| Question | Answer |
|----------|--------|
| What calls `__str__`? | `print()`, `str()`, f-string `{obj}` |
| What calls `__repr__`? | `repr()`, REPL, inside lists/dicts, `{obj!r}` |
| What does `__bool__` fall back to? | `__len__` (if `__bool__` not defined) |
| What is `NotImplemented`? | Singleton returned to tell Python to try the other object's method |
| What's the difference between `NotImplemented` and `NotImplementedError`? | `NotImplemented` is a return value; `NotImplementedError` is an exception |
| When is `__exit__` called? | Always — whether `with` block succeeds or raises |
| What does returning `True` from `__exit__` do? | Suppresses the exception |
| What does `frozen=True` enable? | Immutability + auto `__hash__` |
| What breaks hashability when `__eq__` is defined? | Python sets `__hash__ = None` |
| Fix for mutable dataclass default? | `field(default_factory=list)` |
| What does `asdict()` do? | Converts dataclass to a dict recursively |
| When does `__radd__` get called? | When `other + self` and `other.__add__(self)` returns `NotImplemented` |
| What is `__call__`? | Makes an instance callable: `obj(args)` |
| What is `__post_init__`? | Called after dataclass `__init__` — use for validation and computed fields |

---

## 🧠 Behavioral / Scenario Questions

### "Your Django model's admin page shows 'Product object (1)'. What do you add?"

**Model answer:** "Add `__str__` to the model. Django admin uses `str(obj)` to display model instances. Without `__str__`, you see the default `object (pk)` representation. The fix is one method:"

```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} — ₹{self.price}"
```

### "You're building a Money class and want `money1 == money2` to work AND to use Money objects as dict keys. What do you implement?"

**Model answer:** "I need both `__eq__` and `__hash__`. Defining `__eq__` alone makes Python set `__hash__ = None`, breaking hashability. The hash should be based on the same fields used in equality:

```python
class Money:
    def __init__(self, amount, currency):
        self.amount = round(float(amount), 2)
        self.currency = currency

    def __eq__(self, other):
        if not isinstance(other, Money): return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __hash__(self):
        return hash((self.amount, self.currency))  # same fields as __eq__
```

### "A junior developer created a dataclass with `tags: list = []`. What would you tell them?"

**Model answer:** "This will raise a `ValueError: mutable default is not allowed` at class definition time — which is actually Python protecting us! The fix is `field(default_factory=list)`. This creates a fresh `[]` for each instance instead of sharing one list. The root cause is the same mutable default argument bug from Day 2 — `@dataclass` enforces the correct pattern by refusing bare mutable defaults."

---

*End of Day 8 Interview Prep — Day 9: Decorators — function wrappers, `@functools.wraps`, class decorators, and building production-ready decorators*
