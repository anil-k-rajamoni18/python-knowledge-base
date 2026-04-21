
# Topic: Python Basics — Data Types, Variables & Memory Model

> **Instructions:** Work through sections in order. Each section builds on the last.
> Run all code in your Python environment (terminal, VS Code, or Jupyter Notebook).

---

## 📋 Setup Check

Before you begin, confirm your environment is ready:

```python
# Run this cell first
import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
# Expected: Python 3.10 or higher
```

---

## Section A — Predict the Output (No Running Allowed!)

> ✏️ Write your predictions on paper or in a comment. Then run the code and compare.

---

### A1. Type Identification

```python
values = [42, 3.14, "hello", True, None, [1, 2], (1, 2), {1: "a"}]
for v in values:
    print(type(v).__name__)
```

**Your predictions (fill in the blanks):**
```
42      → ______
3.14    → ______
"hello" → ______
True    → ______
None    → ______
[1, 2]  → ______
(1, 2)  → ______
{1:"a"} → ______
```

---

### A2. Identity vs Equality

```python
a = 50
b = 50
print(a is b, a == b)     # Line 1

a = 500
b = 500
print(a is b, a == b)     # Line 2

a = "python"
b = "python"
print(a is b, a == b)     # Line 3

a = [1, 2]
b = [1, 2]
print(a is b, a == b)     # Line 4

a = [1, 2]
b = a
print(a is b, a == b)     # Line 5
```

**Your predictions:**
```
Line 1: ______ ______
Line 2: ______ ______
Line 3: ______ ______
Line 4: ______ ______
Line 5: ______ ______
```

---

### A3. Mutation Tracking

```python
x = [10, 20, 30]
y = x
y.append(40)
print(x)       # Line 1

y = [1, 2, 3]
print(x)       # Line 2

x.clear()
print(y)       # Line 3
```

**Your predictions:**
```
Line 1: ______
Line 2: ______
Line 3: ______
```

---

### A4. String "Mutation"

```python
s = "hello"
print(id(s))      # Line 1

s = s.upper()
print(id(s))      # Line 2 — same or different than Line 1?

t = s
s += "!"
print(t)          # Line 3
print(s)          # Line 4
```

**Your predictions:**
```
Line 2 id — same or different? ______
Line 3: ______
Line 4: ______
```

---

## Section B — Fill in the Blanks

### B1. Complete the code so each `print` outputs the shown result.

```python
# Make x and y point to the same list
x = [1, 2, 3]
y = ______
print(x is y)       # True

# Make a and b have equal values but different identities
a = [1, 2, 3]
b = ______
print(a == b)       # True
print(a is b)       # False

# Swap p and q without a temporary variable
p, q = 10, 20
______, ______ = ______, ______
print(p, q)         # 20 10
```

---

### B2. Fix the type errors — fill in the correct conversion.

```python
age = "25"
next_year = age + 1         # TypeError!
# Fix: next_year = ______(age) + 1
print(next_year)            # 26

price = 9.99
label = "Price: " + price   # TypeError!
# Fix: label = "Price: " + ______(price)
print(label)                # Price: 9.99

score = True
total = score + 4           # This actually works — why?
print(total)                # ______ (fill in the result)
```

---

### B3. Identify whether each type is mutable or immutable.

```python
data = {
    42:           "______",
    3.14:         "______",
    "hello":      "______",
    True:         "______",
    (1, 2, 3):    "______",
    [1, 2, 3]:    "______",
    {1: "a"}:     "______",
    {1, 2, 3}:    "______",
    frozenset():  "______",
}
# Fill each blank with "mutable" or "immutable"
```

---

## Section C — Debugging Exercises

> Each snippet below has a bug. Identify the bug, explain why it's a bug, and write the corrected version.

---

### C1. The Aliasing Bug

```python
# Bug: This function is supposed to return a modified COPY of the list
def double_values(data):
    result = data
    for i in range(len(result)):
        result[i] *= 2
    return result

original = [1, 2, 3, 4]
doubled = double_values(original)
print("Original:", original)    # Expected: [1, 2, 3, 4]
print("Doubled:", doubled)      # Expected: [2, 4, 6, 8]
```

**What's the bug?**
```
_______________________________________________________
```

**Fixed version:**
```python
def double_values(data):
    # Your fix here
    pass
```

---

### C2. The Mutable Default Bug

```python
# Bug: Each call should return a fresh list with only the new item
def add_score(score, scoreboard=[]):
    scoreboard.append(score)
    return scoreboard

print(add_score(100))    # Expected: [100]
print(add_score(200))    # Expected: [200]  — but you'll get [100, 200]
print(add_score(300))    # Expected: [300]  — but you'll get [100, 200, 300]
```

**What's the bug?**
```
_______________________________________________________
```

**Fixed version:**
```python
def add_score(score, scoreboard=None):
    # Your fix here
    pass
```

---

### C3. The Wrong Comparison

```python
# Bug: This function should check if a value "doesn't exist yet"
def process(value):
    if value == None:
        return "no value"
    return f"processing {value}"

# This works but is not Pythonic.
# Rewrite using the correct idiom.
```

**Fixed version:**
```python
def process(value):
    # Your fix here
    pass
```

---

### C4. The Identity Trap

```python
# Bug: A developer wrote this to check if a value is exactly 1000
x = 1000
if x is 1000:
    print("found it!")
else:
    print("not found!")    # This may print even though x = 1000
```

**What's the bug?**
```
_______________________________________________________
```

**Fixed version:**
```python
x = 1000
# Your fix here
```

---

## Section D — Write the Code

### D1. Reference Counter Inspector

Write a function `show_refcount(obj)` that:
1. Prints the object's value
2. Prints the object's `id`
3. Prints the reference count (subtract 1 for the function's own argument)

```python
import sys

def show_refcount(obj):
    # Your code here
    pass

# Test it
x = [1, 2, 3]
y = x
show_refcount(x)
# Expected output:
# Value:  [1, 2, 3]
# ID:     <some integer>
# Refcount: 2
```

---

### D2. Type Classifier

Write a function `classify(obj)` that returns:
- `"immutable"` if the object is of an immutable type
- `"mutable"` if the object is of a mutable type
- `"unknown"` otherwise

```python
IMMUTABLE_TYPES = (int, float, str, tuple, frozenset, bytes, bool, type(None))
MUTABLE_TYPES = (list, dict, set, bytearray)

def classify(obj):
    # Your code here
    pass

# Test cases
print(classify(42))           # immutable
print(classify(3.14))         # immutable
print(classify("hello"))      # immutable
print(classify((1, 2)))       # immutable
print(classify([1, 2]))       # mutable
print(classify({"a": 1}))     # mutable
print(classify({1, 2}))       # mutable
```

---

### D3. Safe Function Caller

Write a function `safe_call(func, data)` that:
1. If `data` is mutable, passes a **copy** to the function
2. If `data` is immutable, passes it directly
3. Returns both the function's result AND the original (unmodified) data

```python
def safe_call(func, data):
    # Your code here
    pass

# Test: function that modifies its argument
def add_zero(lst):
    lst.append(0)
    return lst

original = [1, 2, 3]
result, unchanged = safe_call(add_zero, original)

print(result)       # [1, 2, 3, 0]
print(unchanged)    # [1, 2, 3]
print(original)     # [1, 2, 3] ← must be unchanged!
```

---

### D4. Variable Swap Variations

Implement `swap` three different ways — using a temp variable, tuple unpacking, and XOR (for integers).

```python
# Method 1: Using a temporary variable
def swap_temp(a, b):
    # Your code
    return a, b

# Method 2: Using tuple unpacking (Pythonic)
def swap_tuple(a, b):
    # Your code
    return a, b

# Method 3: XOR swap (integers only, no temp variable)
def swap_xor(a, b):
    # Hint: a ^= b; b ^= a; a ^= b
    return a, b

# All three should produce the same result
print(swap_temp(10, 20))    # (20, 10)
print(swap_tuple(10, 20))   # (20, 10)
print(swap_xor(10, 20))     # (20, 10)
```

---

## Section E — Tricky Scenarios

### E1. The Shared State Problem

```python
# What will this print? Explain why.
class Config:
    defaults = {"debug": False, "timeout": 30}

c1 = Config()
c2 = Config()

c1.defaults["debug"] = True
print(c2.defaults["debug"])   # True or False? Why?
```

**Your explanation:**
```
_______________________________________________________
_______________________________________________________
```

**How would you fix this so `c1` and `c2` have independent configs?**

```python
class Config:
    def __init__(self):
        # Your fix here
        pass
```

---

### E2. The None Sentinel Pattern

```python
# This function searches a list and returns the found index.
# The problem: what if the item is at index 0? 0 is falsy!

def find_item(lst, target):
    for i, val in enumerate(lst):
        if val == target:
            return i
    return None

result = find_item([5, 10, 15], 5)

# ❌ Buggy check
if result:
    print(f"Found at index {result}")
else:
    print("Not found")       # This prints, even though 5 is at index 0!

# ✅ Correct check — write it here:
if ______:
    print(f"Found at index {result}")
else:
    print("Not found")
```

---

### E3. Integer Caching Edge Case

```python
# Will these print True or False? Think carefully.
import sys

a = -6
b = -6
print(a is b)       # _____ (hint: caching starts at -5)

a = -5
b = -5
print(a is b)       # _____

a = 256
b = 256
print(a is b)       # _____

a = 257
b = 257
print(a is b)       # _____
```

---

## Section F — Mini Project

### F1. Personal Data Card (Putting it all together)

Build a simple "user profile" system that demonstrates all Day 1 concepts.

**Requirements:**
1. Create a user dictionary with: `name` (str), `age` (int), `skills` (list), `is_active` (bool)
2. Write a function `update_skills(user, new_skill)` that adds a skill to the user
3. Write a function `deactivate(user)` that sets `is_active` to `False`
4. Write a function `clone_user(user)` that returns an independent copy (deep copy) of the user dict
5. Verify with `id()` that clone is independent

```python
import copy

# Step 1: Create user
user = {
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "HTML"],
    "is_active": True
}

# Step 2: Write update_skills
def update_skills(user, new_skill):
    # Your code here
    pass

# Step 3: Write deactivate
def deactivate(user):
    # Your code here
    pass

# Step 4: Write clone_user (must be independent!)
def clone_user(user):
    # Your code here
    pass

# Step 5: Test everything
update_skills(user, "CSS")
print(user["skills"])           # ["Python", "HTML", "CSS"]

clone = clone_user(user)
update_skills(clone, "Django")
print(user["skills"])           # ["Python", "HTML", "CSS"] — unchanged!
print(clone["skills"])          # ["Python", "HTML", "CSS", "Django"]

deactivate(clone)
print(user["is_active"])        # True  — unchanged
print(clone["is_active"])       # False
```

---

## ✅ Answer Key

<details>
<summary>Click to reveal answers (attempt first!)</summary>

### A1 Answers
```
42      → int
3.14    → float
"hello" → str
True    → bool
None    → NoneType
[1, 2]  → list
(1, 2)  → tuple
{1:"a"} → dict
```

### A2 Answers
```
Line 1: True  True   (50 is cached, same object)
Line 2: False True   (500 not cached, different objects, equal values)
Line 3: True  True   (short identifier-like string, interned)
Line 4: False True   (different list objects, equal values)
Line 5: True  True   (b = a → same object)
```

### A3 Answers
```
Line 1: [10, 20, 30, 40]  (y and x point to same list)
Line 2: [10, 20, 30, 40]  (y was reassigned, x unchanged from that point)
Line 3: []                (y still points to same list as x; clear() modifies in place)
```

### A4 Answers
```
Line 2: Different (upper() creates a new string object)
Line 3: "HELLO" (t still points to original uppercase string)
Line 4: "HELLO!" (s now points to a new string with "!")
```

### B1 Answers
```python
y = x                   # alias
b = x[:]                # shallow copy
p, q = q, p             # swap
```

### B2 Answers
```python
next_year = int(age) + 1
label = "Price: " + str(price)
total = 5  # True == 1, so True + 4 == 5
```

### B3 Answers
```
42          → immutable
3.14        → immutable
"hello"     → immutable
True        → immutable
(1, 2, 3)   → immutable
[1, 2, 3]   → mutable
{1: "a"}    → mutable
{1, 2, 3}   → mutable
frozenset() → immutable
```

### C1 Fix
```python
def double_values(data):
    result = data[:]            # make a copy first
    for i in range(len(result)):
        result[i] *= 2
    return result
```

### C2 Fix
```python
def add_score(score, scoreboard=None):
    if scoreboard is None:
        scoreboard = []
    scoreboard.append(score)
    return scoreboard
```

### C3 Fix
```python
def process(value):
    if value is None:           # use 'is' not '=='
        return "no value"
    return f"processing {value}"
```

### C4 Fix
```python
x = 1000
if x == 1000:                  # use == not is
    print("found it!")
```

### D1 Answer
```python
def show_refcount(obj):
    print(f"Value:    {obj}")
    print(f"ID:       {id(obj)}")
    print(f"Refcount: {sys.getrefcount(obj) - 1}")
```

### D2 Answer
```python
def classify(obj):
    if isinstance(obj, IMMUTABLE_TYPES):
        return "immutable"
    elif isinstance(obj, MUTABLE_TYPES):
        return "mutable"
    return "unknown"
```

### D3 Answer
```python
def safe_call(func, data):
    if isinstance(data, (list, dict, set, bytearray)):
        import copy
        safe_data = copy.copy(data)
    else:
        safe_data = data
    result = func(safe_data)
    return result, data
```

### D4 Answers
```python
def swap_temp(a, b):
    temp = a
    a = b
    b = temp
    return a, b

def swap_tuple(a, b):
    a, b = b, a
    return a, b

def swap_xor(a, b):
    a ^= b
    b ^= a
    a ^= b
    return a, b
```

### E1 Answer
`c2.defaults["debug"]` will be `True`.

`defaults` is a class-level attribute — a single dict shared by all instances. `c1.defaults` and `c2.defaults` both reference the same dict object.

**Fix:**
```python
class Config:
    def __init__(self):
        self.defaults = {"debug": False, "timeout": 30}
        # Now each instance gets its own dict
```

### E2 Answer
```python
if result is not None:          # correct — distinguishes None from 0
    print(f"Found at index {result}")
else:
    print("Not found")
```

### E3 Answers
```
a = -6: False  (outside cached range -5 to 256)
a = -5: True   (boundary of cached range)
a = 256: True  (boundary of cached range)
a = 257: False (outside cached range)
```

### F1 Answer
```python
import copy

def update_skills(user, new_skill):
    user["skills"].append(new_skill)

def deactivate(user):
    user["is_active"] = False

def clone_user(user):
    return copy.deepcopy(user)
```

</details>

---

## 📊 Self-Assessment Checklist

After completing all sections, rate yourself:

| Concept | ✅ Got it | 🔄 Need review | ❓ Still confused |
|---------|-----------|---------------|-----------------|
| Variables are references, not boxes | | | |
| Mutable vs immutable behavior | | | |
| `is` vs `==` distinction | | | |
| Small integer caching range | | | |
| Pass-by-object-reference | | | |
| Mutable default argument trap | | | |
| Shallow vs deep copy | | | |
| Reference counting basics | | | |

**Score yourself:**
- 8/8 ✅ — Ready for Day 2!
- 5–7 ✅ — Review "Need review" topics, re-read theory notes
- < 5 ✅ — Schedule extra review time; re-do Sections A–C

---

*Day 1 Exercises Complete — Day 2: Collections — Lists, Tuples, Dicts, Sets*