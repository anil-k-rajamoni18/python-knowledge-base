# Python Built-in Functions 
## 1️⃣ What Are Built-in Functions?

Built-in functions are:
- Always available
- Implemented in C (CPython)
- Faster and memory-efficient
- Accessible without imports

```python
print()
len()
type()
```

**📌 Python exposes built-ins via:**

```python
import builtins
dir(builtins)
```

## 2️⃣ Type Conversion & Constructor Functions

### Core Conversion Functions

| Function | Converts To |
|----------|-------------|
| `int()` | Integer |
| `float()` | Float |
| `str()` | String |
| `bool()` | Boolean |
| `list()` | List |
| `tuple()` | Tuple |
| `set()` | Set |
| `dict()` | Dictionary |

### 🔍 `int()`

```python
int("10")        # 10
int(10.9)        # 10 (truncates)
```

**⚠️ Errors:**

```python
int("10.5")      # ValueError
```

### 🔍 `bool()` — VERY IMPORTANT FOR INTERVIEWS

**Falsy values in Python:**

```python
False
0
0.0
None
''
[]
{}
set()
```

```python
bool("False")    # True
bool("0")        # True
```

**📌 Rule:** Empty → False, Everything else → True

### 🔍 `list()`, `tuple()`, `set()`

```python
list("abc")      # ['a', 'b', 'c']
set([1,1,2])     # {1, 2}
```

**⚠️** `set()` removes duplicates and order

## 3️⃣ Input / Output Built-ins

### 🔹 `print()`

```python
print("A", "B", sep="-", end="!")
```

**Output:**

```
A-B!
```

**Arguments:**
- `sep` → separator
- `end` → line ending
- `file` → output stream

### 🔹 `input()`

```python
x = input("Enter value: ")
```

**⚠️** Always returns `str`

## 4️⃣ Mathematical Built-ins

| Function | Description |
|----------|-------------|
| `abs()` | Absolute value |
| `round()` | Rounds number |
| `pow()` | Exponent |
| `min()` | Minimum |
| `max()` | Maximum |
| `sum()` | Total |

### Examples

```python
abs(-10)             # 10
round(3.14159, 2)    # 3.14
pow(2, 3)            # 8
```

### 🔍 `round()` Edge Case

```python
round(2.5)   # 2
round(3.5)   # 4
```

**📌** Python uses Banker's rounding

## 5️⃣ Iterable & Sequence Built-ins (CRITICAL)

### 🔹 `len()`

```python
len("Python")     # 6
```

**Works with:**
- list
- tuple
- dict
- set
- string

### 🔹 `sorted()` vs `.sort()`

```python
sorted_list = sorted(nums)
nums.sort()
```

| `sorted()` | `.sort()` |
|------------|-----------|
| Returns new list | Modifies existing |
| Works on any iterable | Works only on list |

### 🔹 `range()`

```python
range(start, stop, step)
```

```python
list(range(1, 10, 2))
```

**📌** `range` is lazy & memory-efficient

### 🔹 `enumerate()`

```python
for idx, val in enumerate(["a", "b", "c"]):
    print(idx, val)
```

**Better than:**

```python
for i in range(len(lst)):
```

### 🔹 `zip()`

```python
zip([1,2], ['a','b'])
```

**📌** Stops at shortest iterable

## 6️⃣ Functional Programming Built-ins

### 🔹 `map()`

```python
map(function, iterable)
```

```python
list(map(lambda x: x*x, [1,2,3]))
```

**Equivalent:**

```python
[x*x for x in [1,2,3]]
```

### 🔹 `filter()`

```python
list(filter(lambda x: x%2==0, [1,2,3,4]))
```

### 🔹 `reduce()` (Advanced)

```python
from functools import reduce
reduce(lambda a,b: a+b, [1,2,3])
```

**📌** Often replaced by `sum()`

## 7️⃣ Logical Built-ins

### 🔹 `all()`

```python
all([True, True])     # True
all([])               # True (IMPORTANT)
```

### 🔹 `any()`

```python
any([False, True])    # True
any([])               # False
```

## 8️⃣ Object Introspection & Reflection

### 🔹 `type()`

```python
type(10)
```

### 🔹 `isinstance()`

```python
isinstance(10, int)
```

**✅** Preferred over `type() ==`

### 🔹 `dir()`

```python
dir(list)
```

Lists attributes & methods

### 🔹 `help()`

```python
help(str.upper)
```

## 9️⃣ Memory & Identity Functions

### 🔹 `id()`

```python
id(obj)
```

Memory reference

### 🔹 `hash()`

```python
hash("python")
```

**Used in:**
- dict
- set

### 🔹 `callable()`

```python
callable(print)   # True
```

## 🔟 File Handling Built-in

### 🔹 `open()`

```python
with open("data.txt") as f:
    data = f.read()
```

**Modes:**
- `r`, `w`, `a`, `rb`

## 1️⃣1️⃣ Dynamic Execution (DANGEROUS)

### 🔹 `eval()`

```python
eval("2+3")
```

**❌ Security Risk** ❌ Never use with user input

### 🔹 `exec()`

```python
exec("x = 10")
```

## 1️⃣2️⃣ Namespace Functions

### 🔹 `globals()` / `locals()`

```python
globals()
locals()
```

**Used in:**
- Debugging
- Metaprogramming

## 1️⃣3️⃣ Exception Handling Built-ins

```python
try:
    int("abc")
except ValueError as e:
    print(e)
```

## 🎯 Interview Gold Questions

1. Why `all([])` returns True?
2. Difference between `map()` and list comprehension?
3. Why `bool("False")` is True?
4. `sorted()` vs `.sort()`?
5. When to use `isinstance()`?

## 🧪 Practice Assignments

**Task 1:** Create dictionary using `zip()`

**Task 2:** Filter odd numbers and square them

**Task 3:** Count vowels using `map()` + `filter()`