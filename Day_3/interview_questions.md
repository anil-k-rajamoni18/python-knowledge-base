# Day 3 Interview Preparation
# Topic: Data Structures — Lists, Tuples, Sets, Dictionaries & Complexity

---

## 🟢 Beginner Level Questions

---

### Q1. What are the four main built-in data structures in Python? How do they differ?

**Answer:**

| Structure | Ordered | Mutable | Duplicates | Key Feature |
|-----------|---------|---------|------------|-------------|
| `list` | ✅ Yes | ✅ Yes | ✅ Yes | General-purpose, index access |
| `tuple` | ✅ Yes | ❌ No | ✅ Yes | Immutable, hashable (if elements are) |
| `set` | ❌ No | ✅ Yes | ❌ No | Fast membership, set math |
| `dict` | ✅ Yes (3.7+) | ✅ Yes | Keys: No | Key-value mapping |

```python
lst = [1, 2, 2, 3]            # ordered, duplicates OK
tpl = (1, 2, 2, 3)            # same as list but immutable
st = {1, 2, 3}                # no duplicates, unordered
dct = {"a": 1, "b": 2}       # key-value pairs
```

---

### Q2. How do you safely access a dictionary key that might not exist?

**Answer:**
Three patterns, each with a different use case:

```python
d = {"name": "Alice", "age": 25}

# Option 1: .get() — returns None or a default
email = d.get("email")              # None
email = d.get("email", "unknown")   # "unknown"

# Option 2: setdefault() — gets AND sets if missing
d.setdefault("role", "user")        # sets "role": "user" in d too
print(d["role"])                    # "user"

# Option 3: EAFP style (try/except)
try:
    email = d["email"]
except KeyError:
    email = "unknown"

# Option 4: 'in' check
if "email" in d:
    email = d["email"]
```

**When to use which:**
- `.get()` — most common, one-liners
- `setdefault()` — when you also want to store the default
- `try/except` — when KeyError itself is meaningful

---

### Q3. What is the difference between a list and a tuple?

**Answer:**
- **List** — mutable, dynamic array; use when contents will change over time
- **Tuple** — immutable sequence; use for fixed data, function returns, and dict keys

```python
# List — mutable
lst = [1, 2, 3]
lst.append(4)           # works
lst[0] = 99             # works

# Tuple — immutable
tpl = (1, 2, 3)
# tpl.append(4)         # AttributeError
# tpl[0] = 99           # TypeError

# Tuple as dict key (list cannot be)
grid = {(0, 0): "start", (1, 1): "middle"}

# Tuple returned from function
def get_range(data): return min(data), max(data)
low, high = get_range([3, 1, 4, 1, 5])   # unpacking
```

**Performance:** Tuples are faster to create and iterate. `tuple.__sizeof__()` < `list.__sizeof__()`.

---

### Q4. How do you create an empty set? Why can't you use `{}`?

**Answer:**
`{}` creates an empty **dict**, not a set. This is for historical reasons — dict literals existed before set literals.

```python
# ❌ Wrong
empty = {}
print(type(empty))      # <class 'dict'>

# ✅ Correct
empty_set = set()
print(type(empty_set))  # <class 'set'>

# Non-empty sets CAN use {} syntax
fruits = {"apple", "banana"}    # This IS a set (no colons = set)
config = {"key": "value"}       # This IS a dict (colons = dict)
```

---

### Q5. What is list slicing? Give examples of common slicing patterns.

**Answer:**
Slicing extracts a portion of a list using `[start:stop:step]` syntax. `stop` is exclusive. Returns a **new list** (shallow copy).

```python
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

nums[2:5]       # [2, 3, 4]          — elements 2, 3, 4
nums[:4]        # [0, 1, 2, 3]       — first 4
nums[6:]        # [6, 7, 8, 9]       — from index 6 to end
nums[::2]       # [0, 2, 4, 6, 8]   — every 2nd element
nums[::-1]      # [9, 8, 7, ..., 0] — reversed
nums[:]         # full shallow copy
```

---

### Q6. What is the difference between `remove()` and `discard()` on a set?

**Answer:**
Both remove an element, but they differ in error behavior:

```python
s = {1, 2, 3}

s.remove(2)         # Works — removes 2
# s.remove(99)      # KeyError — element not found!

s.discard(3)        # Works — removes 3
s.discard(99)       # No error — silently ignored

# Rule: use discard() when absence is acceptable
#       use remove() when absence indicates a bug
```

---

## 🟡 Intermediate Level Questions

---

### Q7. How does Python's hash table work for dicts and sets?

**Answer:**
Both `dict` and `set` use a **hash table** — a sparse array where element positions are determined by a hash function.

**Process for `key in my_dict`:**
1. Compute `h = hash(key)`
2. Map to an index: `slot = h % table_size`
3. Check if that slot has the matching key
4. If collision (two keys hash to same slot) — probe next slot (open addressing)
5. If key found → O(1). If not → O(1) average.

```python
# You can see hash values
print(hash("hello"))    # some large integer (consistent per process)
print(hash(42))         # 42 (integers hash to themselves)
print(hash((1, 2)))     # some integer (tuples are hashable)

# Lists are NOT hashable — no consistent hash possible
# hash([1, 2])          # TypeError: unhashable type: 'list'
```

**Why it matters:** O(1) average for dict/set lookups vs O(n) for lists.

**Hash collisions:** In worst case (all keys collide), lookups degrade to O(n). Python's hash table design makes this extremely unlikely in practice.

---

### Q8. What is a `namedtuple`? When would you use it over a regular tuple or a dict?

**Answer:**
`namedtuple` creates a tuple subclass with named fields — readable like a dict, efficient like a tuple.

```python
from collections import namedtuple

# Define the "type"
Point = namedtuple("Point", ["x", "y"])
Employee = namedtuple("Employee", ["name", "department", "salary"])

p = Point(3, 4)
e = Employee("Alice", "Engineering", 85000)

# Access by name (readable) or index (compatible with tuple)
print(p.x, p.y)             # 3 4
print(p[0], p[1])           # 3 4

# Immutable — can't change fields
# e.salary = 90000          # AttributeError

# _replace() creates a new instance with changed fields
e2 = e._replace(salary=90000)
print(e2.salary)            # 90000

# _asdict() — convert to OrderedDict
print(e._asdict())          # {'name': 'Alice', 'department': 'Engineering', 'salary': 85000}
```

**When to choose:**

| Scenario | Use |
|----------|-----|
| Fixed structure, read-only, many instances | `namedtuple` |
| Flexible, needs methods | `dataclass` (Day 4) |
| One-off return value | regular `tuple` |
| Needs mutation | `dict` or `dataclass` |

**Memory:** `namedtuple` instances are ~3× smaller than equivalent dicts.

---

### Q9. Explain the difference between `defaultdict`, `Counter`, and a regular `dict`.

**Answer:**

**Regular dict:**
```python
# ❌ KeyError on missing access
d = {}
d["a"] += 1     # KeyError: 'a'
```

**`defaultdict`:**
```python
from collections import defaultdict

# Auto-creates default value on missing key access
word_count = defaultdict(int)       # default: 0
word_count["python"] += 1          # no error — creates 0, then +1
word_count["python"] += 1
print(word_count["python"])         # 2
print(word_count["unknown"])        # 0 (auto-created)

# Common factories:
defaultdict(int)    # missing → 0
defaultdict(list)   # missing → []
defaultdict(set)    # missing → set()
defaultdict(dict)   # missing → {}
```

**`Counter`:**
```python
from collections import Counter

# Specialized for counting — built-in frequency analysis
c = Counter("mississippi")
print(c)                        # Counter({'s': 4, 'i': 4, 'p': 2, 'm': 1})
print(c.most_common(2))         # [('s', 4), ('i', 4)]
print(c["z"])                   # 0 (missing keys return 0, no KeyError)

# Counter arithmetic
c1 = Counter({"a": 3, "b": 2})
c2 = Counter({"a": 1, "b": 4, "c": 1})
print(c1 + c2)                  # Counter({'b': 6, 'a': 4, 'c': 1})
print(c1 - c2)                  # Counter({'a': 2}) — only positive results
```

---

### Q10. What is the time complexity of common list operations, and why?

**Answer:**

| Operation | Complexity | Reason |
|-----------|-----------|--------|
| `lst[i]` (index) | O(1) | Direct pointer lookup in array |
| `lst.append(x)` | O(1) amortized | Add to end; rarely triggers realloc |
| `lst.insert(0, x)` | O(n) | Shifts all n elements right |
| `x in lst` | O(n) | Must scan each element |
| `lst.pop()` | O(1) | Remove last — no shifting |
| `lst.pop(0)` | O(n) | Shifts all remaining elements left |
| `lst.sort()` | O(n log n) | Timsort algorithm |
| `len(lst)` | O(1) | Length cached on the list object |

```python
# Demonstrating why insert(0) is slow at scale
import timeit

data = list(range(100_000))

# O(n) — insert at beginning (shifts 100k elements)
t1 = timeit.timeit(lambda: data.insert(0, -1), number=100)

# O(1) — append at end
t2 = timeit.timeit(lambda: data.append(-1), number=100)

print(f"insert(0): {t1:.4f}s")
print(f"append():  {t2:.6f}s")
# insert(0) will be ~100-1000x slower
```

**Interview takeaway:** If you need fast inserts at both ends, use `collections.deque` (double-ended queue) — it's O(1) at both ends.

---

### Q11. What are dictionary views? How are they different from `.keys()` returning a list?

**Answer:**
Dictionary views (`keys()`, `values()`, `items()`) return **live, dynamic objects** that reflect changes to the underlying dict. They are NOT lists — they are view objects.

```python
d = {"a": 1, "b": 2, "c": 3}

keys = d.keys()
print(keys)         # dict_keys(['a', 'b', 'c'])

d["d"] = 4          # modify the dict AFTER creating the view
print(keys)         # dict_keys(['a', 'b', 'c', 'd']) ← updated automatically!

# View supports set operations
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
common_keys = d1.keys() & d2.keys()    # set intersection on views
print(common_keys)      # {'b'}

# Convert to list when you need a snapshot
snapshot = list(d.keys())   # static copy — won't update
```

**Why views exist:** Memory efficiency — no need to copy all keys/values just to iterate.

---

### Q12. How do sets implement mathematical set operations, and what are the Python operators?

**Answer:**

```python
A = {1, 2, 3, 4, 5}
B = {3, 4, 5, 6, 7}

# Union — all elements from A or B (or both)
print(A | B)            # {1, 2, 3, 4, 5, 6, 7}
print(A.union(B))       # same

# Intersection — only elements in BOTH A and B
print(A & B)            # {3, 4, 5}
print(A.intersection(B))

# Difference — in A but NOT in B
print(A - B)            # {1, 2}
print(A.difference(B))

# Symmetric difference — in either A or B but NOT both
print(A ^ B)            # {1, 2, 6, 7}
print(A.symmetric_difference(B))

# Subset and superset
print({1, 2} <= A)      # True  — {1,2} is subset of A
print({1, 2} < A)       # True  — proper subset (not equal)
print(A >= {1, 2})      # True  — A is superset of {1,2}
print(A.isdisjoint({8, 9}))  # True — no common elements
```

**Performance:** All set operations are O(min(len(A), len(B))) on average — much faster than equivalent list operations.

---

## 🔴 Advanced / Senior Level Questions

---

### Q13. Explain amortized O(1) complexity for list `append()`. What triggers a reallocation?

**Answer:**
`append()` is "amortized O(1)" — occasionally expensive, cheap on average.

**Mechanism:** Python's list over-allocates storage when the internal array is full. Instead of allocating exactly n+1 slots, it allocates roughly 1.125× the current size (the growth pattern is approximately: 0, 4, 8, 16, 25, 35, 46, ...).

```python
import sys

lst = []
prev_size = sys.getsizeof(lst)
print(f"Empty list: {prev_size} bytes")

for i in range(20):
    lst.append(i)
    new_size = sys.getsizeof(lst)
    if new_size != prev_size:
        print(f"Reallocation at len={len(lst)}: {prev_size} → {new_size} bytes")
        prev_size = new_size

# Output shows reallocation at specific lengths (implementation-defined)
```

**Math:** If a list doubles capacity on overflow, each element is moved at most log₂(n) times total across all appends. Total cost = n × O(1) + O(log n) × O(n) reallocations ≈ O(n). Per-operation average = O(n)/n = O(1).

**Interview insight:** This is why `append()` is preferred over `insert(0)` and why building lists in loops is fine, but concatenating (`lst = lst + [x]`) in a loop is O(n²).

---

### Q14. When would you use `ChainMap` over merging dicts with `|`?

**Answer:**
`ChainMap` provides a **logical layered view** — it doesn't copy data, and it maintains the independence of each underlying dict. Changes to the `ChainMap` only affect the **first** (highest-priority) dict.

```python
from collections import ChainMap

defaults = {"color": "blue", "size": "medium", "debug": False}
user_prefs = {"color": "red"}
env_overrides = {"debug": True}

# ChainMap — no copying, live references, layered priority
config = ChainMap(env_overrides, user_prefs, defaults)

print(config["color"])      # "red"  — from user_prefs
print(config["size"])       # "medium" — from defaults
print(config["debug"])      # True  — from env_overrides (highest priority)

# Writes go to the FIRST map only
config["new_key"] = "hello"
print(env_overrides)        # {"debug": True, "new_key": "hello"} — changed!
print(user_prefs)           # {"color": "red"} — unchanged
print(defaults)             # unchanged

# vs dict merge with | — creates a NEW merged dict (copy)
merged = env_overrides | user_prefs | defaults
# Changes to merged do NOT affect originals
```

**Use cases:** CLI argument parsing (argparse does this internally), configuration management with multiple sources, template context variables in Django views.

---

### Q15. What makes an object "hashable"? How would you make a custom class hashable?

**Answer:**
An object is hashable if:
1. It implements `__hash__()` — returns an integer
2. It implements `__eq__()` — for collision resolution
3. The hash value is **consistent** during the object's lifetime (immutable-by-contract)
4. Objects that compare equal must have the same hash

```python
# Built-in hashable types
hash("hello")       # ✅ str
hash(42)            # ✅ int
hash((1, 2, 3))     # ✅ tuple (of hashables)
hash(3.14)          # ✅ float

# Built-in unhashable types (mutable)
hash([1, 2, 3])     # ❌ TypeError — list
hash({"a": 1})      # ❌ TypeError — dict
hash({1, 2, 3})     # ❌ TypeError — set

# Making a custom class hashable
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point): return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        # Must: equal objects → same hash
        return hash((self.x, self.y))   # tuple hash is standard pattern

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)             # True
print(hash(p1) == hash(p2)) # True

# Now usable as dict key or set element
locations = {p1: "home", p2: "office"}  # p1 and p2 are equal → same slot!
```

**Important rule:** If you define `__eq__`, Python automatically sets `__hash__` to `None` (making the class unhashable) — you MUST explicitly define `__hash__` too.

---

### Q16. How would you choose between a list of dicts vs a dict of dicts for storing records?

**Answer:**
The choice depends on your **primary access pattern**:

```python
users_data = [
    {"id": 1, "name": "Alice", "role": "admin"},
    {"id": 2, "name": "Bob", "role": "user"},
    {"id": 3, "name": "Carol", "role": "admin"},
]

# ── List of dicts ─────────────────────────────────────────────────────────
# ✅ Good for: iteration order matters, filtering, no ID-based lookup
# ❌ Bad for: lookup by ID (O(n) scan required)

# Find user by ID: O(n)
alice = next((u for u in users_data if u["id"] == 1), None)

# Filter admins: O(n) — natural for lists
admins = [u for u in users_data if u["role"] == "admin"]

# ── Dict of dicts ─────────────────────────────────────────────────────────
# ✅ Good for: frequent ID-based lookup O(1), deduplication
# ❌ Bad for: ordered iteration (though Python 3.7+ preserves insertion order)

users_by_id = {u["id"]: u for u in users_data}

# Find user by ID: O(1)
alice = users_by_id.get(1)

# Filter admins: still O(n) — iterate values
admins = [u for u in users_by_id.values() if u["role"] == "admin"]
```

**Real-world pattern (Django):** Use list for queryset iteration; convert to dict for repeated random access during the same request.

---

### Q17. What is the difference between `sorted()` and `.sort()`? When would you use each?

**Answer:**

| | `.sort()` | `sorted()` |
|-|-----------|------------|
| Works on | Lists only | Any iterable |
| Returns | `None` (in-place) | New sorted list |
| Original | Modified | Unchanged |
| Use when | OK to modify original | Need original + sorted |

```python
# .sort() — in-place, returns None
nums = [3, 1, 4, 1, 5, 9]
nums.sort()
print(nums)             # [1, 1, 3, 4, 5, 9] — modified

# sorted() — returns new list, original unchanged
original = [3, 1, 4, 1, 5, 9]
new = sorted(original)
print(original)         # [3, 1, 4, 1, 5, 9] — unchanged
print(new)              # [1, 1, 3, 4, 5, 9]

# Both support key= and reverse=
students = [{"name": "Bob", "grade": 85}, {"name": "Alice", "grade": 92}]
by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)

# Stable sort: equal elements maintain original relative order
data = [(1, "b"), (2, "a"), (1, "a")]
print(sorted(data))     # [(1, 'a'), (1, 'b'), (2, 'a')] — stable!
```

**Python's sort algorithm:** Timsort — a hybrid of merge sort and insertion sort. O(n log n) worst case, O(n) best case (nearly sorted data).

---

## 📝 Quick-Fire Answers

| Question | Answer |
|----------|--------|
| What's the complexity of `x in dict`? | O(1) average |
| What's the complexity of `x in list`? | O(n) |
| What's the complexity of `list.append()`? | O(1) amortized |
| What's the complexity of `list.insert(0, x)`? | O(n) |
| Can a list be a dict key? | No — lists are unhashable |
| Can a tuple be a dict key? | Yes — if all elements are hashable |
| What does `{}` create? | Empty dict |
| What does `set()` create? | Empty set |
| What module provides `Counter`, `defaultdict`? | `collections` |
| What is a `frozenset`? | Immutable, hashable set |
| Does Python 3.7+ guarantee dict insertion order? | Yes |
| What does `Counter.most_common(n)` return? | List of n most common (element, count) tuples |
| What's the difference between `pop()` and `discard()` on a set? | `pop()` removes and returns arbitrary element; `discard()` removes specified element silently |
| How do you deep copy a nested list? | `copy.deepcopy(lst)` |
| What algorithm does Python use to sort? | Timsort |

---

## 🧠 Behavioral / Scenario Questions

### "You need to find all users who completed both a purchase and a review. How would you structure the data?"

**Model answer:** "I'd store purchased users and reviewed users each as a set — then use set intersection (`purchased & reviewed`) to get users who did both. Set membership operations are O(1) and intersection is O(min(|A|, |B|)), which is far more efficient than nested list iteration which would be O(n²)."

### "An API endpoint is slow because it searches a list of 50,000 users by ID on every request. How would you fix it?"

**Model answer:** "Convert the list to a dict indexed by user ID at startup: `users_by_id = {u['id']: u for u in users_list}`. This is an O(n) one-time cost. Subsequent lookups are O(1). This is the same principle behind database indexes — preprocessing for faster reads."

### "How would you implement a word frequency counter for a 10GB log file without loading it all into memory?"

**Model answer:** "Use a generator to read the file line by line, combined with a `Counter`. This way only one line is in memory at a time. `Counter.update()` can be called iteratively, so the counter accumulates frequency data without loading the full file:"

```python
from collections import Counter
import re

def count_words_in_file(filepath: str) -> Counter:
    counter = Counter()
    with open(filepath) as f:
        for line in f:                          # generator — one line at a time
            words = re.findall(r'\w+', line.lower())
            counter.update(words)               # incremental update
    return counter
```

---

*End of Day 3 Interview Prep — Day 4 will add: OOP, classes, dunder methods, inheritance, dataclasses*
