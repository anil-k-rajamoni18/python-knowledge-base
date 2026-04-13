# 🎯 Python Full Stack — Day 1 Interview Preparation
# Topic: Python Basics — Data Types, Variables & Memory Model

> **How to use this file:** Read the question, attempt an answer mentally or on paper, then reveal the answer. For senior roles, go beyond the answer — add depth from the "Depth Add-on" notes.

---

## 🟢 Beginner Level Questions

---

### Q1. What are the basic data types in Python?

**Answer:**
Python's built-in data types include:
- **Numeric:** `int`, `float`, `complex`
- **Text:** `str`
- **Sequence:** `list`, `tuple`, `range`
- **Mapping:** `dict`
- **Set types:** `set`, `frozenset`
- **Boolean:** `bool`
- **Binary:** `bytes`, `bytearray`, `memoryview`
- **None:** `NoneType`

```python
x = 42           # int
y = 3.14         # float
name = "Alice"   # str
active = True    # bool
data = None      # NoneType
```

---

### Q2. What is the difference between `int` and `float` in Python?

**Answer:**
- `int` represents whole numbers with arbitrary precision (no size limit in Python 3)
- `float` represents decimal numbers stored as 64-bit IEEE 754 double-precision values

```python
x = 10          # int
y = 10.0        # float
z = 10 / 3      # float: 3.3333... (true division always returns float)
w = 10 // 3     # int: 3 (floor division)

print(type(x))  # <class 'int'>
print(type(y))  # <class 'float'>
```

> ⚠️ Float precision: `0.1 + 0.2 != 0.3` due to binary floating-point representation. Use `decimal.Decimal` for financial calculations.

---

### Q3. How do you check the type of a variable in Python?

**Answer:**
Two ways:
- `type(x)` — returns the exact type
- `isinstance(x, SomeType)` — preferred in production; handles inheritance

```python
x = 42
print(type(x))              # <class 'int'>
print(isinstance(x, int))   # True
print(isinstance(x, (int, float)))  # True — checks multiple types
```

**Interview tip:** Interviewers prefer `isinstance()` in code reviews because it respects subclassing.

---

### Q4. What is `None` in Python?

**Answer:**
`None` is a singleton object of type `NoneType`. It represents the absence of a value — similar to `null` in other languages.

```python
result = None
print(type(result))         # <class 'NoneType'>
print(result is None)       # True  ← correct check
print(result == None)       # True  ← works but not idiomatic
```

**Key rule:** Always compare to `None` with `is`, not `==`.

---

### Q5. What is the difference between `=` and `==` in Python?

**Answer:**
- `=` is the **assignment operator** — binds a name to an object
- `==` is the **equality operator** — compares the *values* of two objects

```python
x = 10          # assigns value 10 to name x
print(x == 10)  # True  — compares value
print(x == 20)  # False
```

---

### Q6. Can you have multiple assignments on one line in Python?

**Answer:**
Yes — two common patterns:

```python
# Tuple unpacking (multiple different values)
x, y, z = 1, 2, 3

# Chained assignment (same value to multiple names)
a = b = c = 0

# Swap without temp variable
x, y = y, x
```

---

## 🟡 Intermediate Level Questions

---

### Q7. What is the difference between mutable and immutable objects in Python?

**Answer:**
- **Immutable:** Value cannot change after creation. Any "modification" creates a new object. Examples: `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`
- **Mutable:** Value can be changed in-place. The same object is modified. Examples: `list`, `dict`, `set`, `bytearray`

```python
# Immutable — new object created
s = "hello"
old_id = id(s)
s += " world"
print(id(s) == old_id)      # False — new object

# Mutable — same object modified
lst = [1, 2, 3]
old_id = id(lst)
lst.append(4)
print(id(lst) == old_id)    # True — same object
```

**Why it matters:** Determines whether changes inside a function affect the caller's data.

---

### Q8. How does Python pass arguments to functions — by value or by reference?

**Answer:**
Neither exactly. Python uses **pass-by-object-reference** (also called pass-by-assignment).

- The function receives a reference to the **same object** the caller has
- If the object is **mutable** and you modify it in-place → caller sees the change
- If the object is **immutable**, or if you reassign the parameter inside the function → caller is unaffected

```python
# Mutable — caller sees mutation
def add_item(lst):
    lst.append(99)

nums = [1, 2, 3]
add_item(nums)
print(nums)         # [1, 2, 3, 99]

# Reassignment — caller unaffected
def replace(lst):
    lst = [100, 200]  # local name now points elsewhere

nums = [1, 2, 3]
replace(nums)
print(nums)         # [1, 2, 3]
```

---

### Q9. What is the difference between `is` and `==`?

**Answer:**
- `==` compares **values** (calls `__eq__`)
- `is` compares **identity** — whether two names point to the *same object in memory* (compares `id()`)

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)   # True  — same values
print(a is b)   # False — different objects in memory

c = a
print(a is c)   # True  — same object
```

**Rule:** Use `==` for value comparison. Use `is` only for `None` checks (`if x is None`).

---

### Q10. What is small integer caching in Python?

**Answer:**
CPython pre-creates and caches integer objects for values in the range **-5 to 256**. When you assign these values, Python reuses the existing objects rather than creating new ones.

```python
a = 100
b = 100
print(a is b)   # True  — same cached object

a = 1000
b = 1000
print(a is b)   # False — new objects created each time
```

**Why it exists:** Small integers are used extremely frequently. Caching them saves memory allocation overhead.

**Interview caution:** This is a CPython implementation detail — other Python implementations (PyPy, Jython) may cache differently.

---

### Q11. What is string interning?

**Answer:**
Python automatically interns (reuses) string objects that look like valid Python identifiers — strings containing only letters, digits, and underscores.

```python
a = "hello"
b = "hello"
print(a is b)           # True  — interned

a = "hello world"
b = "hello world"
print(a is b)           # False — space prevents auto-interning
```

You can force interning manually using `sys.intern()`:
```python
import sys
a = sys.intern("hello world")
b = sys.intern("hello world")
print(a is b)           # True
```

**Use case:** Interning improves performance when comparing the same strings repeatedly (e.g., dictionary keys).

---

### Q12. What is reference counting in Python?

**Answer:**
Every Python object maintains an internal counter of how many references (variable names, data structure slots) point to it.

- Counter increments when a new reference is created
- Counter decrements when a reference is deleted or goes out of scope
- When counter reaches **0**, the object is immediately deallocated

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))   # 2 (x + getrefcount's own argument)

y = x
print(sys.getrefcount(x))   # 3

del y
print(sys.getrefcount(x))   # 2 again
```

**Limitation:** Reference counting cannot handle **circular references** (e.g., A → B → A). Python's cyclic garbage collector handles this separately.

---

### Q13. What is the difference between a shallow copy and a deep copy?

**Answer:**
- **Shallow copy:** Copies the outer container, but nested objects are still shared references
- **Deep copy:** Recursively copies all nested objects — fully independent

```python
import copy

original = [[1, 2], [3, 4]]

shallow = original[:]           # or copy.copy(original)
deep = copy.deepcopy(original)

# Modify a nested element
original[0].append(99)

print(shallow[0])   # [1, 2, 99] — affected! (shared reference)
print(deep[0])      # [1, 2]     — unaffected (independent copy)
```

**When to use deep copy:** When working with nested data structures that you need to fully isolate (e.g., copying game state, config objects).

---

## 🔴 Advanced / Senior Level Questions

---

### Q14. Explain CPython's execution pipeline from source code to output.

**Answer:**
1. **Source code** (`.py`) → read as raw text
2. **Lexical analysis (tokenizer)** → splits source into tokens (keywords, identifiers, operators, literals)
3. **Parsing** → builds an **Abstract Syntax Tree (AST)** — a tree representing the grammatical structure
4. **Compilation** → converts AST to **bytecode** (`.pyc` files stored in `__pycache__/`)
5. **Python Virtual Machine (PVM)** → interprets and executes bytecode instructions

```python
# You can inspect the AST yourself
import ast
tree = ast.parse("x = 1 + 2")
print(ast.dump(tree, indent=2))

# You can inspect bytecode
import dis
def add(a, b): return a + b
dis.dis(add)
```

---

### Q15. What are the consequences of Python's mutable default argument trap, and how do you fix it?

**Answer:**
Default argument values are evaluated **once** when the function is defined, not on each call. If the default is a mutable object (like a list), it persists and accumulates across calls.

```python
# Bug
def append_to(item, lst=[]):
    lst.append(item)
    return lst

print(append_to(1))   # [1]
print(append_to(2))   # [1, 2] ← bug! Same list object reused

# Fix
def append_to(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(append_to(1))   # [1]
print(append_to(2))   # [2] ← correct
```

**Interview insight:** This trips up even experienced developers. Knowing it demonstrates strong Python fluency.

---

### Q16. How does Python's garbage collector handle circular references?

**Answer:**
Reference counting alone cannot free circular references because two objects can keep each other's count above zero indefinitely.

Python's **cyclic garbage collector** (in the `gc` module) periodically scans for groups of objects that reference each other but are unreachable from outside. It then frees them as a group.

```python
import gc

class Node:
    def __init__(self):
        self.ref = None

a = Node()
b = Node()
a.ref = b       # a → b
b.ref = a       # b → a (circular!)

del a
del b
# Reference counts are both 1, not 0 — objects not freed yet
# gc.collect() will detect and free them

gc.collect()    # Force a collection cycle
```

---

### Q17. What are Python's `__slots__` and how do they relate to memory?

**Answer:**
By default, Python stores instance attributes in a `__dict__` (a dictionary) on each object, which has memory overhead.

`__slots__` replaces this dictionary with a fixed set of attributes, reducing memory usage significantly — useful for classes with millions of instances.

```python
# Without slots — has __dict__
class PointNormal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# With slots — no __dict__, less memory
class PointSlotted:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
p1 = PointNormal(1, 2)
p2 = PointSlotted(1, 2)
print(sys.getsizeof(p1))    # ~48 bytes + __dict__ overhead
print(sys.getsizeof(p2))    # ~56 bytes (but no __dict__)
```

---

### Q18. What is the `id()` function and what does it represent in CPython?

**Answer:**
`id(obj)` returns an integer that is **guaranteed to be unique and constant** for the object during its lifetime. In CPython specifically, `id()` returns the **memory address** of the object.

```python
x = [1, 2, 3]
print(id(x))        # e.g., 140234567890

y = x
print(id(y))        # same as id(x) — same object

z = [1, 2, 3]
print(id(z))        # different — new object
```

**Important caveat:** Two objects that exist at different times *can* have the same `id` if one was garbage-collected before the other was created. Never store `id()` values for later comparison.

---

## 📝 Quick-Fire Answers (Common Short Questions)

| Question | Answer |
|----------|--------|
| Is `bool` a subclass of `int` in Python? | Yes — `True == 1`, `False == 0` |
| What happens when you divide two ints with `/`? | Always returns a `float` in Python 3 |
| What is the maximum value of an `int` in Python? | No limit — Python ints have arbitrary precision |
| Is `None` falsy? | Yes — `bool(None)` is `False` |
| Is an empty list `[]` falsy? | Yes |
| Is `0` falsy? | Yes |
| What module lets you inspect bytecode? | `dis` |
| What module gives you AST? | `ast` |
| How do you force string interning? | `sys.intern(string)` |
| What does `sys.getrefcount()` add to the count? | +1 for its own argument reference |

---

## 🧠 Behavioral / Scenario Questions

### "Tell me about a bug you caused or encountered related to mutability."
**Model answer structure:**
1. Describe the scenario (mutable default argument, aliased list, etc.)
2. How you discovered it
3. What the fix was
4. What you learned about Python's memory model

### "How would you explain pass-by-object-reference to a junior developer?"
**Model answer:** Use the sticky-label analogy — "Python doesn't hand the function your box. It hands the function a copy of your sticky label. If the function uses that label to write on the box, you'll see the change. But if the function tears off the label and sticks it on a different box — your label still points to the original."

---

*End of Day 1 Interview Prep — Day 2 will add: list/tuple/dict/set interview questions*