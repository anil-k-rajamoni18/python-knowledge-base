
# 🚀 DAY 3 — Data Structures

Python's data structures are the backbone of everything — APIs, ML pipelines, ETL workflows, databases, and automation systems. Industry systems rely heavily on efficient manipulation of lists, dictionaries, sets, and tuples.

---

## 🟦 1. Lists

### ✔ What is a List?

A mutable, ordered, indexed collection of items.

```python
fruits = ["apple", "banana", "mango"]
```

### ⭐ Key Characteristics

- **Mutable** — items can be changed
- **Ordered** — index-based access
- Allows duplicates
- Supports slicing

```python
fruits[1]       # "banana"
fruits[-1]      # "mango"
fruits[0:2]     # ["apple", "banana"]
```

### ✔ Real-Time / Industry Examples

#### 1. API Response Handling

APIs often return lists of dictionaries:

```python
users = [
  {"id": 1, "name": "John"},
  {"id": 2, "name": "Aisha"},
]
```

#### 2. ML Data Preprocessing

Datasets in Python (before converting to NumPy) often start as lists:

```python
raw_data = [23, 45, 11, 67, 89]
```

#### 3. Automation / DevOps

Parsing command output:

```python
output_lines = logs.split("\n")
```

### ⭐ Common List Methods

| Method | Purpose |
|--------|---------|
| `append(x)` | add item |
| `extend([x,y])` | merge lists |
| `insert(i,x)` | insert at index |
| `remove(x)` | remove first match |
| `pop(i)` | remove & return |
| `sort()` | sort in place |
| `sorted(list)` | return new sorted list |

---

## 🟪 2. Tuples

### ✔ What is a Tuple?

An immutable, ordered collection.

```python
location = ("Bangalore", 560001)
```

### ⭐ Key Characteristics

- **Immutable** → safe for constants
- Faster than lists
- Used for fixed-size data

### ✔ Real-Time / Industry Examples

#### 1. Database Rows

DB queries often return tuples:

```python
(101, "John", 25)
```

#### 2. Geolocation Coordinates

Latitude & longitude:

```python
coords = (12.9716, 77.5946)
```

#### 3. Function Multiple Returns

Python returns tuples internally:

```python
def get_stats():
    return (avg, min_value, max_value)
```

### ⚠ When to Use Tuples?

Use when:
- Data should not change
- You need faster iteration
- Items have fixed structure

Example: `(name, age, role)`

---

## 🟨 3. Sets

### ✔ What is a Set?

An unordered, unique, mutable collection.

```python
skills = {"python", "sql", "docker"}
```

### ⭐ Key Characteristics

- No duplicates
- Faster membership testing (`x in set`)
- Supports mathematical operations

### ✔ Real-Time / Industry Examples

#### 1. Removing Duplicates from Data

```python
emails = list(set(email_list))
```

#### 2. Access Control (Permissions)

```python
admin_permissions = {"read", "write", "delete"}
user_permissions  = {"read", "write"}
```

#### 3. Keyword Filtering

Useful in NLP tasks:

```python
stopwords = {"the", "and", "is", "of"}
```

### ⭐ Set Operations

| Operation | Example |
|-----------|---------|
| Union | `a \| b` |
| Intersection | `a & b` |
| Difference | `a - b` |
| Symmetric diff | `a ^ b` |

---

## 🟧 4. Dictionaries

### ✔ What is a Dictionary?

A key-value store (hash map).

```python
user = {
  "name": "Alice",
  "age": 30,
  "skills": ["Python", "AWS"]
}
```

### ⭐ Key Characteristics

- Fast lookups (O(1))
- Mutable
- Keys must be unique
- Keys must be immutable

### ✔ Real-Time / Industry Examples

#### 1. JSON Data / API Data

Most API payloads are dictionaries:

```python
response["data"]["users"]
```

#### 2. Configurations in Apps

```python
config = {"host": "localhost", "port": 8000}
```

#### 3. Machine Learning Feature Vectors

```python
features = {"age": 45, "income": 75000, "gender": 1}
```

### ⭐ Common Dictionary Methods

| Method | Purpose |
|--------|---------|
| `keys()` | get keys |
| `values()` | get values |
| `items()` | iterate key-value pairs |
| `get(k)` | safe key access |
| `update({...})` | merge dicts |
| `pop(k)` | remove & return |

---

## 🟦 5. Nested Data Structures

Nesting is common when dealing with real-world datasets:

### Example: JSON API Response

```python
student = {
  "name": "Rahul",
  "scores": {
      "math": 90,
      "science": 84
  },
  "hobbies": ["cricket", "gaming"]
}
```

### Industry Use Cases

- API parsing
- Logging structured data
- ML dataset preprocessing
- Complex configuration files

### Traversing Nested Structures

```python
student["scores"]["math"]
student["hobbies"][1]
```

---

## 🟩 6. Comprehensions (List/Set/Dict)

Comprehensions make your code Pythonic and efficient.

### ✔ List Comprehension

```python
squares = [x*x for x in range(10)]
```

Equivalent to:

```python
squares = []
for x in range(10):
    squares.append(x*x)
```

### ✔ Set Comprehension

```python
unique_lengths = {len(word) for word in words}
```

### ✔ Dictionary Comprehension

```python
salaries = {"emp_" + str(i): 50000 + i*1000 for i in range(5)}
```

### ⚡ Real-Time Examples

#### 1. Cleaning ML Data

```python
cleaned = [x.strip().lower() for x in raw_texts]
```

#### 2. Filtering Logs

```python
error_logs = [log for log in logs if "ERROR" in log]
```

#### 3. Mapping Product Prices

```python
price_map = {p["id"]: p["price"] for p in products}
```

---

## 🧪 HANDS-ON EXERCISES (Real-Time Inspired)

### 1. Convert a List of Dicts to CSV (without pandas)

**Input:**

```python
employees = [
  {"name": "John", "age": 30, "dept": "IT"},
  {"name": "Sara", "age": 26, "dept": "HR"},
]
```

**Task:**
- Extract headers
- Write to CSV file manually using `join()`

### 2. Dictionary Frequency Counter

Given text:

```
"The quick brown fox jumps over the lazy dog"
```

**Tasks:**
- Count frequency of each word
- Ignore case
- Remove punctuation
- Show most frequent 3 words

### 3. Find Common Users Between Two Apps

```python
app1_users = ["john", "mike", "emma"]
app2_users = ["mike", "emma", "alex"]
```

**Use set operations:**
- Common users
- Exclusive users
- All unique users

### 4. Flatten a Nested List

**Input:**

```python
[[1,2], [3,4,5], [6]]
```

**Output:**

```python
[1,2,3,4,5,6]
```

### 5. Convert Dictionary → Query Params

```python
{"name":"john", "age":25}
```

**Output:**

```
name=john&age=25
```

### 6. Reverse Dictionary Mapping

```python
{"a": 1, "b": 2}
```

**Output:**

```python
{1: "a", 2: "b"}
```

---

## 🧩 Mini Project — Text Analyzer App (Breakdown)

The project demonstrates:
- ✔ String operations
- ✔ Lists, sets, dictionaries
- ✔ Comprehensions
- ✔ Nested structures

### Features

- Count total words
- Count unique words
- Remove stopwords
- Display top 5 most common words
- Show average word length

### Example Input

```
Python is great and Python is easy to learn
```

### Expected Output

```
Total words: 10
Unique words: 6
Top 5 words: python:2, is:2, great:1, easy:1, learn:1
```

### Key Data Structures Used

- **list** → tokens
- **set** → stopwords removal
- **dict** → frequency count
- **list comprehension** → filtering
- **sorted()** → ranking words
```