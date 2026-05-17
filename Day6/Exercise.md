# REAL-TIME HANDS-ON QUESTIONS — DAY 6

---

## 🔥 SECTION 1: File Handling (TXT, CSV, JSON)

### 1️⃣ Parsing Logs (DevOps-style)

A server generates a `server.log` file:

```
2025-01-01 12:00:01 INFO User John logged in
2025-01-01 12:01:08 ERROR Payment service failed
2025-01-01 12:02:11 WARN Disk space low
2025-01-01 12:02:30 INFO User Anita logged in
```

**Task:** Write a script to:
- Extract only ERROR lines
- Count how many errors occurred
- Save them into `errors.txt`

---

### 2️⃣ Cleanup Automation

A directory contains 200+ log files:

```
log_1.txt
log_2.txt
log_3.txt
...
```

**Task:** Write a script that:
- Reads every file
- Combines all logs into one file `combined.log`
- Adds a header before each file like:
  ```
  ------ LOG FILE: log_1.txt ------
  ```

---

### 3️⃣ JSON Cleaning Script (Used in API pipelines)

You received a messy JSON file:

```json
{
    "user": "Amit",
    "age": "27",
    "premium": "false",
    "score": "240"
}
```

**Task:** Convert string values to correct data types:
- `"27"` → `int`
- `"false"` → `bool`
- `"240"` → `int`

Save new JSON to `clean_user.json`.

---

### 4️⃣ CSV Salary Adjustment (HR Automation)

You have a CSV:

```csv
name,salary
John,45000
Sara,52000
Mike,48000
```

**Task:** Increase every salary by 10% and write to `updated_salaries.csv`.

---

### 5️⃣ Build a File Backup Utility

**Task:** Write a script:
- Takes an input folder
- Copies all files into `backup/`
- Renames files with timestamp suffix

**Example:**
```
report.pdf → report_2025-11-27_152200.pdf
```

---

## 🔥 SECTION 2: HTTP Requests (API Automation)

### 6️⃣ GitHub User Info Fetcher

Given a list of GitHub usernames:

```python
["torvalds", "octocat", "sundar"]
```

**Task:** Use the GitHub API to fetch:
- Name
- No. of public repos
- Followers

Save results in `users.json`.

---

### 7️⃣ URL Status Checker

Given a list:

```
https://google.com
https://openai.com
https://doesnotexist123.com
```

**Task:** Write a Python script to:
- Send GET request to each URL
- Log status: UP or DOWN
- Save results to `status_report.csv`

---

## 🔥 SECTION 3: Modules & Packages

### 8️⃣ Create a Utility Package for Data Analytics

Create a package:

```
mypkg/
  ├── __init__.py
  ├── math_utils.py
  ├── string_utils.py
  └── file_utils.py
```

**Implement:**
- `math_utils.average(numbers)`
- `string_utils.word_count(text)`
- `file_utils.read_json(path)`

Import them in a main script to analyze a file.

---

### 9️⃣ Circular Dependency Fix Challenge

You have:

**file1.py:**
```python
from file2 import greet

def hello():
    print("Hello from file1")
    greet()
```

**file2.py:**
```python
from file1 import hello

def greet():
    print("Hi from file2")
    hello()
```

Running causes infinite recursion.

**Task:** Refactor to remove circular import using:
- A new helper module, or
- Lazy imports

---

## 🔥 SECTION 4: Virtual Environments & pip

### 🔟 Reproducibility Challenge

You received a project with missing environment information.

**Task:** Reconstruct the environment:
- Create a new venv
- Install dependencies based on Python files (inspect imports)
- Generate a `requirements.txt`
- Package the project into a reusable zip

---

### 1️⃣1️⃣ Dependency Conflicts Simulation

Install:

```bash
pip install numpy==1.21
pip install pandas==2.0
```

If conflict occurs:
- Inspect the error
- Determine which versions are compatible
- Fix by installing correct versions

---

## 🔥 SECTION 5: Python Logging (Real Workflow)

### 1️⃣2️⃣ Login Activity Logger

Create an app that:
- Takes a username input
- Logs successful login
- Logs failed attempts
- Stores logs in:
  ```
  logs/activity_2025-11-27.log
  ```

---

### 1️⃣3️⃣ Error Trace Logger

Write a script that deliberately triggers division by zero.

**Use logging to record:**
- Timestamp
- Error type
- Stack trace

---

## 🔥 SECTION 6: Combined Real-Time Scenarios

### 1️⃣4️⃣ Sales Dashboard Data Prep

Given:
- `sales_2025.json`
- `sales_2024.json`
- `sales_2023.json`

Each file contains:

```json
{"month": "Jan", "revenue": "12000"}
```

**Task:**
- Load all files
- Convert revenue to int
- Merge into `merged_sales.csv`
- Log the processing steps

---

### 1️⃣5️⃣ Build a Config Loader System

You have two config files:

**config_default.json:**
```json
{"debug": true, "host": "localhost"}
```

**config_prod.json:**
```json
{"debug": false, "host": "api.company.com"}
```

**Task:** Build:
- `load_config(env)` function
- Loads default config
- Overwrites values using prod config if `env = "prod"`