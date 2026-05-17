# Hands-On Real-Time Exercises (Data Structures)

## 1. Clean and Normalize API Response Data

You receive an API response:

```python
api_data = [
  {"id": 1, "name": "John  ", "active": "YES"},
  {"id": 2, "name": "  Priya", "active": "NO"},
  {"id": 3, "name": "Arun", "active": "YES"},
]
```

**Tasks:**
- Strip spaces in names
- Convert "YES"/"NO" to boolean values (True/False)
- Store cleaned data in a new list of dicts
- Count how many users are active

---

## 2. Identify Duplicate Transactions Using Sets

Transaction IDs:

```python
tx_ids = ["TX1001", "TX1002", "TX1001", "TX1005", "TX1002", "TX1007"]
```

**Tasks:**
- Find all duplicate transaction IDs
- Find all unique IDs
- Create a list containing IDs that occurred only once

---

## 3. Flatten a Complex Nested JSON (without libraries)

Data from a logging system:

```python
logs = {
  "level": "INFO",
  "entries": [
    {"id": 1, "messages": ["start", "processing", "done"]},
    {"id": 2, "messages": ["start", "error", "retry", "done"]},
  ]
}
```

**Tasks:**
- Create a single list of all messages
- Count how many times the word "error" appears
- Extract only entries where "error" is present

---

## 4. Convert CSV Rows (as dicts) to Query Params

Given:

```python
record = {"name": "John Doe", "role": "developer", "active": True}
```

**Task:**  
Convert into:

```
name=John%20Doe&role=developer&active=True
```

(Replace spaces with %20)

---

## 5. Build a Simple In-Memory User Directory

Users:

```python
users = [
  ("john", "admin"),
  ("akash", "dev"),
  ("sara", "admin"),
  ("mike", "guest"),
]
```

**Tasks:**
- Convert to a dictionary: `{role: [usernames...]}`
- Display all admins
- Add a new role "super_admin" with an empty list
- Ensure usernames remain unique for each role

---

## 6. Count Word Frequency in Log Files

Given:

```python
log_data = [
  "ERROR Disk failure",
  "WARNING Low memory",
  "ERROR Network timeout",
  "INFO System rebooted",
  "ERROR Disk failure",
]
```

**Tasks:**
- Count frequency of each log level (ERROR, WARNING, INFO)
- Count the most repeated message (full text)
- Find all unique messages

---

## 7. Remove Stopwords From a Sentence (Set-Based Filtering)

Given:

```python
sentence = "Python is widely used and Python is easy to learn"
stopwords = {"is", "and", "to"}
```

**Tasks:**
- Remove stopwords
- Count unique meaningful words
- Create a list sorted by word length

---

## 8. Create a Product Price Lookup (Dict Comprehension)

Products data:

```python
products = [
  {"id": 101, "name": "Laptop", "price": 75000},
  {"id": 102, "name": "Mouse", "price": 500},
  {"id": 103, "name": "Keyboard", "price": 1200},
]
```

**Tasks:**
- Build a dict `{id: price}` using comprehension
- Find the most expensive product
- Increase all prices by 10%

---

## 9. Merge Two Employee Lists Using Sets

Lists:

```python
office_employees = ["john", "sara", "mike"]
remote_employees = ["mike", "tina", "akash"]
```

**Tasks:**
- Find employees working both modes
- Find who works only remotely
- Find total unique employees

---

## 10. Create a Reverse Lookup Dictionary (Value → Key)

Given:

```python
countries = {
  "IN": "India",
  "US": "United States",
  "CA": "Canada"
}
```

**Tasks:**
- Create reverse mapping: `"India" → "IN"`
- Ensure values are unique before reversing
- Sort reversed dictionary by key (country name)

---

## 11. Extract Nested Keys from Config File

Config:

```python
config = {
  "server": {
    "host": "localhost",
    "ports": {
      "http": 80,
      "https": 443
    }
  }
}
```

**Tasks:**
- Get HTTP & HTTPS port values
- Add a new port `"ssh": 22`
- List all keys present inside "server"

---

## 12. Transform Survey Responses Using List Comprehension

Given:

```python
responses = ["Yes ", " No", "YES", "no", " yes", " NO "]
```

**Tasks:**
- Normalize to lowercase
- Strip spaces
- Convert into booleans (yes → True, no → False)
- Count how many "yes" responses

---

## 13. Build a Role-Based Permission System Using Sets

Roles:

```python
permissions = {
  "admin": {"read", "write", "delete"},
  "dev": {"read", "write"},
  "guest": {"read"}
}
```

**Tasks:**
- Check if dev is allowed to delete
- List permissions missing in guest compared to admin
- Create a set of all unique permissions used in system

---

## 14. Group Employees by First Letter (Dict of Lists)

Data:

```python
employees = ["Alice", "Amit", "Bob", "Charlie", "Catherine"]
```

**Tasks:**

Create:

```python
{ 
  "A": ["Alice", "Amit"], 
  "B": ["Bob"],
  "C": ["Charlie", "Catherine"]
}
```

- Add a new employee "Brian" dynamically
- Sort names inside each list

---

#  HARD LEVEL — REAL-TIME PYTHON DATA STRUCTURE PROBLEMS

## 1. Normalize Deeply Nested JSON (Recursive Parsing) 📦

You receive a complex JSON from a payment gateway:

```python
data = {
  "transaction": {
    "id": "TXN001",
    "amount": 1500,
    "metadata": {
      "customer": {
        "id": 22,
        "name": "John    Doe",
        "phones": ["+91 99999 11111", "  +91 88888 22222 "]
      },
      "location": {
        "country": " India ",
        "state": "Karnataka"
      }
    }
  }
}
```

**Tasks:**

- Write a recursive function to trim all string values regardless of nesting level.
- Convert all phone numbers to: `+91XXXXXXXXXX` format.
- Extract a flat dictionary:

```python
{
 "transaction_id": ...,
 "customer_name": ...,
 "primary_phone": ...,
 "country": ...,
}
```

---

## 2. Build a Lookup Index for Search Engine (Inverted Index) 🗂️

Given sentences:

```python
sentences = [
  "python is great for data",
  "data science uses python",
  "machine learning requires data"
]
```

**Tasks:**

- Create an inverted index:

```python
{
  "python": [0, 1],
  "data": [0, 1, 2],
  "learning": [2],
  ...
}
```

- Remove stopwords (is, for, uses, requires)
- Use sets & dictionaries efficiently
- Handle duplicate words inside a sentence

---

## 3. Implement a Mini "Join" Operation (SQL Join Simulation) 🔗

Given:

```python
employees = [
  {"id": 1, "name": "John", "dept_id": 10},
  {"id": 2, "name": "Sara", "dept_id": 20},
  {"id": 3, "name": "Mike", "dept_id": 10}
]

departments = [
  {"dept_id": 10, "dept_name": "Engineering"},
  {"dept_id": 20, "dept_name": "HR"}
]
```

**Tasks:**

- Implement a manual inner join using dictionaries.
- Optimize it using a dictionary index on `dept_id`.
- Output:

```python
[
  {"name": "John", "dept_name": "Engineering"},
  {"name": "Mike", "dept_name": "Engineering"},
  {"name": "Sara", "dept_name": "HR"}
]
```

---

## 4. Group Sales Data into Dynamic Time Buckets (Aggregation) 📊

Data:

```python
sales = [
 {"amount": 500, "hour": 10},
 {"amount": 1200, "hour": 10},
 {"amount": 800, "hour": 11},
 {"amount": 950, "hour": 12},
 {"amount": 1500, "hour": 12},
]
```

**Tasks:**

- Group by hour: `{10: [...], 11: [...], 12: [...]}`
- Compute total sales per hour
- Sort buckets by total sales descending
- Use:
  - `dict.setdefault()`
  - list comprehensions
  - custom sorting with `sorted(..., key=...)`

---

## 5. Detect Anomalies in Sensor Data (Sliding Window) ⚙️

Sensor readings:

```python
readings = [5, 6, 6, 20, 7, 6, 5, 30, 6, 5]
```

**Tasks:**

- Compute a 3-value sliding window average
- Mark a reading as anomaly if: `value > 2 * window_average`
- Output dictionaries:

```python
{"index": 3, "value": 20, "avg": 6.0}
{"index": 7, "value": 30, "avg": 7.0}
```

**Requires:**
- list slicing
- list comprehensions
- efficient calculations

---

## 6. Create a "Mini Redis" (Key-Value Store with TTL Simulation) ⏱️

Simulated operations:

```python
commands = [
  ("SET", "a", 10),
  ("SET", "b", 20),
  ("EXPIRE", "a", 2),   # expire after 2 operations
  ("GET", "a"),
  ("GET", "b"),
  ("GET", "a")
]
```

**Tasks:**

- Track key-value pairs
- Track TTL (time-to-live) using a dictionary
- Decrease TTL after each command
- Auto-delete when TTL hits 0

**Expected behavior:**

```
SET a = 10
SET b = 20
GET a → 10
GET b → 20
GET a → None (expired)
```

---

## 7. Merge and Deduplicate Large Datasets Efficiently (Millions Simulation) 📁

Simulate two dataset chunks:

```python
chunk1 = ["u1", "u2", "u3", "u4"]
chunk2 = ["u3", "u4", "u5", "u6"]
```

**Tasks:**

- Merge using sets
- Maintain sorted order
- Identify users present in both chunks
- Identify users unique to each chunk
- Must be solved using only list/set operations (no pandas)

---

## 8. Create a Histogram from Raw Log Events (Frequency Buckets) 📈

Logs:

```python
events = [
  {"type": "CLICK", "user": "u1"},
  {"type": "VIEW", "user": "u2"},
  {"type": "CLICK", "user": "u3"},
  {"type": "CLICK", "user": "u1"},
  {"type": "VIEW", "user": "u1"},
]
```

**Tasks:**

- Count events by type
- Count unique users per type
- Output:

```python
{
 "CLICK": {"count": 3, "users": ["u1", "u3"]},
 "VIEW": {"count": 2, "users": ["u1", "u2"]}
}
```

---

## 9. Implement a Custom Sorting Algorithm Using Keys (Complex Sort) 🔀

Given:

```python
employees = [
  {"name": "John", "age": 30, "salary": 50000},
  {"name": "Sara", "age": 28, "salary": 65000},
  {"name": "Mike", "age": 35, "salary": 45000},
]
```

**Tasks:**

Sort by:
- Salary descending
- If salary same → sort by age ascending
- Use `sorted(..., key=lambda ...)`

---

## 10. Text Compression Using Frequency Dictionary (Huffman-Like Preprocessing) 🗃️

Given text:

```python
"aaabbccccddeeeeaaa"
```

**Tasks:**

- Create frequency dict: `{char: count}`
- Convert to list of tuples sorted by frequency
- Create mapping:

```
a → 0
b → 10
c → 110
...
```

(This simulates Huffman encoding preparation step)

---

## 11. Build a Mini Access Control System Using Sets 🔐

Roles and permissions:

```python
roles = {
  "admin": {"read", "write", "delete", "deploy"},
  "dev": {"read", "write"},
  "qa": {"read", "test"},
  "guest": {"read"}
}
```

**Tasks:**

- Find permission differences: admin vs dev
- Find common permissions across all roles
- Find roles that have unique permissions not shared by others (requires frequency counting using dict)

---

## 12. Rebuild Directory Tree from File Paths (Nested Dictionary) 📁

Input:

```python
files = [
  "src/app/main.py",
  "src/app/utils/helpers.py",
  "src/config/settings.py",
  "tests/test_main.py"
]
```

**Tasks:**

Build:

```python
{
 "src": {
   "app": {
     "main.py": None,
     "utils": {
       "helpers.py": None
     }
   },
   "config": {
     "settings.py": None
   }
 },
 "tests": {
   "test_main.py": None
 }
}
```

**Requires:**
- split path
- nested dictionary construction
- dynamic creation using loops

---

## 13. Compute Similarity Score Between Documents (Set & Dict) 📄

Given two articles:

```python
doc1 = "python is great for ai and machine learning"
doc2 = "machine learning uses python for deep learning"
```

**Tasks:**

- Convert to sets
- Compute Jaccard Similarity:

```
|intersection| / |union|
```

- Compute word frequency vectors (dicts)
- Compute cosine similarity manually

---

## 14. Chunk Large List Into Fixed-Size Batches (Generator Logic) 📦

Input:

```python
data = list(range(1, 51))  # 1 to 50
```

**Tasks:**

- Split into chunks of size 7
- Last chunk can be smaller
- Store batches in a dictionary with keys: `"batch_1"`, `"batch_2"`, ...

---

## 15. Multi-Level Sorting and Grouping (Nested Structures) 🧂

Data:

```python
food_items = [
  {"category": "fruit", "name": "apple", "price": 120},
  {"category": "vegetable", "name": "carrot", "price": 40},
  {"category": "fruit", "name": "mango", "price": 150},
  {"category": "vegetable", "name": "broccoli", "price": 80}
]
```

**Tasks:**

- Group by category
- Sort each group by price descending
- Create summary:

```python
{
 "fruit": {"count":2, "avg_price":135},
 "vegetable": {"count":2, "avg_price":60}
}
```