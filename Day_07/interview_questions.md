# 🎯 Python Full Stack — Day 7 Interview Preparation
# Topic: Encapsulation & Abstraction

> **How to use:** Attempt each answer before reading. OOP interviews on encapsulation almost always involve writing a class with `@property` and asking about name mangling. Practise writing these from memory.

---

## 🟢 Beginner Level Questions

---

### Q1. What are the three levels of access control in Python? How are they different from Java/C++?

**Answer:**

| Level | Syntax | Enforcement |
|-------|--------|-------------|
| Public | `self.name` | None — accessible from everywhere |
| Protected | `self._name` | Convention only — "please don't use from outside" |
| Private | `self.__name` | Name mangling — `_ClassName__name` |

```python
class Person:
    def __init__(self, name, salary, ssn):
        self.name = name        # public — for everyone
        self._salary = salary   # protected — internal/subclass use
        self.__ssn = ssn        # private — name mangled

p = Person("Alice", 80000, "123-45-6789")
print(p.name)           # Alice — works
print(p._salary)        # 80000 — works (but breaks convention)
# print(p.__ssn)        # AttributeError — mangled to _Person__ssn
print(p._Person__ssn)   # 123-45-6789 — accessible via mangled name
```

**Unlike Java/C++:** Python has NO true enforcement. `private` in Java is compiler-enforced. Python's `__private` is just name mangling — it can still be accessed as `_ClassName__attr`. Python's philosophy: "We're all consenting adults."

---

### Q2. What is name mangling? Why does Python do it?

**Answer:**
Name mangling is Python automatically renaming `__attr` to `_ClassName__attr` when the attribute is accessed inside a class.

```python
class Account:
    def __init__(self):
        self.__id = 42    # stored as _Account__id

class SavingsAccount(Account):
    def __init__(self):
        super().__init__()
        self.__id = 99    # stored as _SavingsAccount__id — DIFFERENT attribute!

acc = SavingsAccount()
print(acc.__dict__)
# {'_Account__id': 42, '_SavingsAccount__id': 99}
# Both coexist independently!
```

**Why:** Name mangling prevents child classes from **accidentally** overriding a parent's private attribute. Without it, `self.__id` in both classes would be the same attribute — the child would overwrite the parent's value.

---

### Q3. What is `@property` and why is it better than a getter method?

**Answer:**
`@property` turns a method into an attribute-like accessor. Callers read `obj.name` instead of `obj.get_name()` — cleaner, more Pythonic.

```python
# Without @property — Java-style (not Pythonic)
class Circle:
    def __init__(self, r): self._r = r
    def get_radius(self): return self._r
    def set_radius(self, v): self._r = max(0, v)

c = Circle(5)
c.set_radius(10)        # verbose
print(c.get_radius())   # verbose

# With @property — Pythonic
class Circle:
    def __init__(self, r): self.radius = r   # calls setter!

    @property
    def radius(self): return self._r

    @radius.setter
    def radius(self, v):
        if v < 0: raise ValueError("Radius can't be negative")
        self._r = v

c = Circle(5)
c.radius = 10           # clean — calls setter with validation
print(c.radius)         # clean — calls getter
```

**The key advantage:** You can add validation **without breaking existing code**. If callers already use `c.radius`, adding a `@property` doesn't change their code at all.

---

### Q4. What is an Abstract Base Class? What happens if you try to instantiate one?

**Answer:**
An Abstract Base Class (ABC) defines a contract — a set of methods that all concrete subclasses MUST implement. It cannot be instantiated directly.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str: ...    # must be implemented

    @abstractmethod
    def move(self) -> str: ...     # must be implemented

    def breathe(self) -> str:      # concrete method — shared
        return f"{self.__class__.__name__} is breathing"

# Cannot instantiate
try:
    a = Animal()
except TypeError as e:
    print(e)
# Can't instantiate abstract class Animal with abstract methods speak, move

class Dog(Animal):
    def speak(self): return "Woof!"
    def move(self): return "runs"

d = Dog()           # works — all abstract methods implemented
print(d.breathe())  # Animal is breathing — inherited concrete method
```

---

### Q5. What is the difference between a read-only property and a regular attribute?

**Answer:**
A regular attribute can be read and written by anyone. A read-only property (defined with `@property` but no `@setter`) raises `AttributeError` on assignment.

```python
class Circle:
    def __init__(self, r):
        self._r = r

    # Read-only property — no setter
    @property
    def radius(self): return self._r

    # Computed read-only property
    @property
    def area(self): return 3.14 * self._r ** 2

c = Circle(5)
print(c.radius)     # 5 — read works
print(c.area)       # 78.5 — computed read works

try:
    c.radius = 10   # AttributeError: can't set attribute
except AttributeError as e:
    print(e)

try:
    c.area = 100    # AttributeError: can't set attribute
except AttributeError as e:
    print(e)
```

---

### Q6. Why does this cause a RecursionError? How do you fix it?

```python
class Person:
    @property
    def name(self): return self.name

    @name.setter
    def name(self, value): self.name = value
```

**Answer:**
Inside the getter, `self.name` calls the property getter again — infinite recursion.  
Inside the setter, `self.name = value` calls the setter again — infinite recursion.

**Fix:** Store data in a DIFFERENT private attribute (typically `_name`):

```python
class Person:
    @property
    def name(self): return self._name      # reads _name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()          # writes _name

p = Person()
p.name = "Alice"    # setter called → stores in _name
print(p.name)       # getter called → reads from _name
```

---

## 🟡 Intermediate Level Questions

---

### Q7. Explain all three property decorators with a complete example.

**Answer:**

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    # GETTER — @property
    @property
    def celsius(self) -> float:
        """Called when you READ: t.celsius"""
        return self._celsius

    # SETTER — @attr.setter (validation goes here)
    @celsius.setter
    def celsius(self, value: float) -> None:
        """Called when you WRITE: t.celsius = 25"""
        if value < -273.15:
            raise ValueError(f"Below absolute zero: {value}")
        self._celsius = value

    # DELETER — @attr.deleter
    @celsius.deleter
    def celsius(self) -> None:
        """Called when you DEL: del t.celsius"""
        print("Resetting to 0°C")
        self._celsius = 0.0

    # COMPUTED property (no separate storage, no setter)
    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

t = Temperature(25)
print(t.celsius)    # 25.0   — getter
t.celsius = 100     # setter (with validation)
print(t.fahrenheit) # 212.0  — computed getter
del t.celsius       # deleter — "Resetting to 0°C"
print(t.celsius)    # 0.0
```

---

### Q8. What is the difference between `@abstractmethod` and just raising `NotImplementedError`?

**Answer:**

| | `@abstractmethod` | `raise NotImplementedError` |
|-|-------------------|-----------------------------|
| When caught | At **class instantiation** time | At **runtime** (when method is called) |
| Enforcement | Cannot even create the class | Can create; fails only when method called |
| Missing method | TypeError at `SubClass()` | Only fails when you call the uncovered method |
| Intent | Design contract — subclasses MUST implement | Reminder — "please override this" |

```python
from abc import ABC, abstractmethod

# With @abstractmethod
class AbstractShape(ABC):
    @abstractmethod
    def area(self): ...

class IncompleteShape(AbstractShape):
    pass

IncompleteShape()   # TypeError immediately — caught at creation!

# With raise NotImplementedError
class BaseShape:
    def area(self):
        raise NotImplementedError("Subclass must implement area()")

class IncompleteShape2(BaseShape):
    pass

s = IncompleteShape2()  # No error — created fine
s.area()                # NotImplementedError — only when called!
```

**Professional practice:** Use `@abstractmethod` for formal framework contracts. Use `raise NotImplementedError` for simpler cases or when you can't use ABC.

---

### Q9. How do you define an abstract property in Python?

**Answer:**
Use both `@property` and `@abstractmethod` stacked (order matters — `@property` goes first from top to bottom, but innermost decorator applies first):

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Subclass must implement name as a @property."""
        ...

    @property
    @abstractmethod
    def color(self) -> str: ...

    @color.setter
    @abstractmethod
    def color(self, value: str) -> None:
        """Subclass must implement color setter too."""
        ...

class Circle(Shape):
    def __init__(self, r, color):
        self._r = r
        self._color = color

    @property
    def name(self) -> str:
        return "Circle"

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = value

c = Circle(5, "red")
print(c.name)   # Circle
c.color = "blue"
print(c.color)  # blue
```

---

### Q10. When would you choose an ABC over duck typing?

**Answer:**

Use **ABC** when:
- You're building a framework or library others will extend
- You need `isinstance()` checks to work reliably
- You want errors at class definition time, not runtime
- The contract must be enforced (missing method = error before deployment)

Use **Duck typing** when:
- Writing application code (not framework code)
- You don't control all the classes involved
- You want maximum flexibility
- The objects come from multiple unrelated class hierarchies

```python
# ABC — good for Django-style framework design
from abc import ABC, abstractmethod
class Storage(ABC):
    @abstractmethod
    def save(self, key, value): ...

# Django uses this pattern: Model, Form, View are all "abstract-like"

# Duck typing — good for application logic
def render_all(items):
    for item in items:
        item.render()   # works for any object with render() — no ABC needed
```

---

### Q11. How does Python's `typing.Protocol` differ from ABC?

**Answer:**

| | `ABC` | `Protocol` |
|-|-------|------------|
| Inheritance required | Yes (`class Foo(MyABC)`) | No — just have the right methods |
| Check type | `isinstance(obj, MyABC)` | `isinstance(obj, MyProtocol)` (if `@runtime_checkable`) |
| When checked | Runtime | Also at static analysis (mypy) |
| Use case | Class hierarchies, runtime checks | Flexible structural typing, type hints |

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:           # No inheritance from Drawable!
    def draw(self): return "○"

class Square:           # No inheritance from Drawable!
    def draw(self): return "□"

class NotDrawable:
    def display(self): return "not drawable"

# Works without any inheritance — structural check
print(isinstance(Circle(), Drawable))       # True
print(isinstance(NotDrawable(), Drawable))  # False

def render(item: Drawable) -> None:
    print(item.draw())

render(Circle())    # ○
render(Square())    # □
# render(NotDrawable())  # mypy would warn; runtime would fail
```

---

### Q12. Design a `Config` class that allows reading settings freely but protects writes.

**Answer:**

```python
class Config:
    """Immutable after creation — settings are read-only."""

    def __init__(self, **settings):
        self.__settings = dict(settings)   # private storage

    def __getattr__(self, name: str):
        """Allow reading any setting as an attribute."""
        if name.startswith("_"):
            raise AttributeError(name)
        try:
            return self.__settings[name]
        except KeyError:
            raise AttributeError(f"Config has no setting: {name!r}")

    def __setattr__(self, name: str, value):
        """Block assignment after __init__."""
        if name.startswith("_Config__"):    # allow setting private attrs
            super().__setattr__(name, value)
        else:
            raise AttributeError("Config is immutable — cannot modify settings")

    def get(self, key: str, default=None):
        return self.__settings.get(key, default)

    def __repr__(self):
        return f"Config({self.__settings})"


config = Config(debug=True, db_url="sqlite:///db.sqlite3", port=8000)
print(config.debug)     # True
print(config.port)      # 8000

try:
    config.debug = False    # AttributeError — immutable
except AttributeError as e:
    print(e)
```

---

## 🔴 Advanced / Senior Level Questions

---

### Q13. Explain the property descriptor protocol. How does `@property` work internally?

**Answer:**
`property` is a **descriptor** — an object that implements `__get__`, `__set__`, and/or `__delete__`. When Python accesses `obj.attr`, it checks if the attribute is a descriptor and calls the appropriate dunder method.

```python
# @property is syntactic sugar for property()
class Circle:
    # These are equivalent:

    # Using @property decorator:
    @property
    def radius(self): return self._r

    # Manually using property():
    def _get_radius(self): return self._r
    def _set_radius(self, v): self._r = v
    radius = property(_get_radius, _set_radius)
```

**How Python resolves `obj.radius`:**
1. Python finds `radius` in `Circle.__dict__`
2. It's a `property` object (a descriptor)
3. Python calls `property.__get__(obj, type(obj))` → calls your getter
4. For `obj.radius = 5`: calls `property.__set__(obj, 5)` → calls your setter

```python
# You can even build a descriptor from scratch:
class ValidatedFloat:
    """Custom descriptor — works like @property but reusable."""
    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        return getattr(obj, self.private_name, 0.0)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Must be non-negative number, got {value!r}")
        setattr(obj, self.private_name, float(value))

class Product:
    price = ValidatedFloat()    # reusable validator!
    weight = ValidatedFloat()

p = Product()
p.price = 9.99   # calls ValidatedFloat.__set__
p.weight = 2.5
# p.price = -1   # ValueError
```

---

### Q14. How does Django use `@property` in its ORM?

**Answer:**
Django uses `@property` extensively for computed attributes that aren't stored in the database:

```python
# Django model pattern
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    @property
    def full_name(self) -> str:
        """Computed — not a DB column."""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def age(self) -> int | None:
        """Computed from birth_date — not stored."""
        if not self.birth_date: return None
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    @property
    def is_senior(self) -> bool:
        """Derived from age."""
        return self.age is not None and self.age >= 60

# Template usage: {{ user.full_name }} — looks like attribute
# Python usage: user.full_name — looks like attribute
# But actually calls the @property method
```

---

### Q15. What is the difference between `__getattr__` and `@property`?

**Answer:**

| | `@property` | `__getattr__` |
|-|-------------|---------------|
| Called when | Always on access (defined attributes) | Only when attribute NOT found normally |
| Defined on | Specific named attributes | Catches all missing attribute lookups |
| Use case | Known, specific attributes with custom logic | Dynamic attribute generation |

```python
class DynamicConfig:
    def __init__(self, settings: dict):
        self._settings = settings

    # __getattr__ only called when normal attribute lookup fails
    def __getattr__(self, name: str):
        try:
            return self._settings[name]
        except KeyError:
            raise AttributeError(f"No config key: {name!r}")

config = DynamicConfig({"debug": True, "port": 8000})
print(config.debug)     # True — __getattr__ called
print(config.port)      # 8000 — __getattr__ called
# print(config.host)    # AttributeError — not in settings


class Temperature:
    def __init__(self, c): self._c = c

    @property
    def celsius(self): return self._c

    @property
    def fahrenheit(self): return self._c * 9/5 + 32

t = Temperature(25)
print(t.celsius)        # @property getter called
print(t.fahrenheit)     # @property getter called
# These use @property — defined, specific attributes
```

---

## 📝 Quick-Fire Answers

| Question | Answer |
|----------|--------|
| How does Python store `self.__pin` in `Account` class? | As `self._Account__pin` |
| Can you access `__private` from outside? | Yes, via `obj._ClassName__attr`, but you shouldn't |
| What does `@property` without a setter create? | A read-only attribute |
| What error does attempting to set a read-only property raise? | `AttributeError: can't set attribute` |
| What error does instantiating an ABC raise? | `TypeError: Can't instantiate abstract class X` |
| Can an ABC have non-abstract (concrete) methods? | Yes — subclasses inherit them |
| What module provides `ABC` and `@abstractmethod`? | `abc` |
| What PEP introduced `typing.Protocol`? | PEP 544 |
| What happens if a subclass doesn't implement an `@abstractmethod`? | The subclass also becomes abstract; instantiation raises TypeError |
| What's the recursion trap in properties? | Storing value in same name as property causes infinite recursion |
| What prefix should property's internal storage use? | Single underscore `_attr` (e.g., `_name` for `name` property) |
| When should you use `__private` over `_protected`? | When you specifically need name mangling to prevent subclass attribute conflicts |

---

## 🧠 Behavioral / Scenario Questions

### "Design a `User` model class for a web application that stores a password securely."

**Model answer:**
```python
class User:
    def __init__(self, username, email, password):
        self.username = username
        self._email = email
        self.password = password    # triggers setter — hashes it

    @property
    def email(self): return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email")
        self._email = value.lower()

    @property
    def password(self):
        raise AttributeError("Password is write-only — use check_password()")

    @password.setter
    def password(self, plain: str):
        import hashlib
        self.__password_hash = hashlib.sha256(plain.encode()).hexdigest()

    def check_password(self, plain: str) -> bool:
        import hashlib
        return self.__password_hash == hashlib.sha256(plain.encode()).hexdigest()
```

### "You're reviewing code where a junior developer made all attributes public. What would you say?"

**Model answer:** "I'd walk them through the principle of encapsulation. Public attributes mean external code can set them to invalid values — `account.balance = -99999` — bypassing any validation. I'd suggest making sensible attributes protected (`_balance`) and adding a `@property` with a setter that validates before storing. I'd also explain that in Python, we don't need to make EVERYTHING private — public is fine for simple attributes users genuinely need to read and write. The goal is protecting **state integrity**, not hiding everything."

### "A subclass needs to access a parent's private attribute. How would you handle it?"

**Model answer:** "If a subclass legitimately needs access, the attribute shouldn't be `__private` — it should be `_protected`. Name mangling (`__private`) is specifically designed to prevent subclass access. If I'm inheriting and need the attribute, that's a signal it belongs to the shared interface and should be `_protected`. If it truly must stay private to the parent, I'd expose it through a `@property` getter in the parent class — controlled, read-only access."

---

*End of Day 7 Interview Prep — Day 8: Decorators — function decorators, `@functools.wraps`, class decorators, and building your own*
