

## 🧪 DAY 4 — Hands-On & Real-Time Practice Questions (Industry Style)

-----

## 🔵 SECTION 1 — Functions, Arguments & Return (Real-World Tasks)

### 1️⃣ Build a Unit Conversion Service (Backend Simulation)

Write functions to convert: **km → miles**, **Celsius → Fahrenheit**, **kg → pounds**.

  * **Requirements:**
      * Each conversion function must accept **default arguments**.
      * Write a **wrapper function**: `convert(value, type="km_to_miles")`.
      * Return results rounded to **2 decimals**.

### 2️⃣ Generate a Report Summary Function (Data Engineering)

  * **Given:** `sales = [1200, 900, 4500, 1200, 800]`
  * **Write a function:** `def sales_summary(data):`
      * *Return* **total, average, highest, lowest**.
  * *Used in ETL/Data pipelines.*

### 3️⃣ Build a Simple Logger Function (DevOps-style)

  * **Function:**
    ```python
    def log(message, level="INFO"):
        # print log in: [LEVEL] - message
    ```
  * **Example Output:** `[ERROR] - Server down`
  * *Add default values, keyword arguments, and multiple return behavior if needed.*

### 4️⃣ Function That Accepts Unlimited User Inputs

  * **Write:**
    ```python
    def combine_strings(*strings):
        return " ".join(strings)
    ```
  * *Simulates real-time chatbot string processing.*

### 5️⃣ Create a Metadata Collector (APIs & Microservices)

  * **Function:**
    ```python
    def request_info(**kwargs):
        # returns dict of all request metadata
    ```
  * **Example Input:** `request_info(ip="10.0.0.1", route="/users", method="POST")`

-----

## 🟣 SECTION 2 — Lambda, map, filter, reduce (Practical Challenges)

### 6️⃣ Clean Product Names (E-commerce System)

  * **Given:** `products = ["   Laptop ", "Mobile ", " Headphone"]`
  * **Tasks:**
      * Use **`map` + `lambda`** to trim spaces.
      * Convert to **lowercase**.

### 7️⃣ Extract Failed API Logs (DevOps)

  * **Given:** `logs = ["200 OK", "500 SERVER ERROR", "404 NOT FOUND", "200 OK"]`
  * **Use:** **`filter()`** and **`lambda`**
      * To extract logs with **`ERROR`** or status code **$\geq 400$**.

### 8️⃣ Compute Total Monthly Expenses (Finance App)

  * **Given:** `expenses = [1200, 450, 600, 520, 700]`
  * **Use:** **`reduce()`** and **`lambda`**.

### 9️⃣ Transform Usernames (Backend User Service)

  * **Given:** `usernames = ["john_doe", "sara_98"]`
  * **Use `map()`** to transform into: `["JOHN DOE", "SARA 98"]` (Uppercase, underscore converted to space).

### 🔟 Filter Students Scoring Above 75 (EdTech App)

  * **Given:** `scores = [45, 78, 92, 66, 81]`
  * **Use `filter()`**
  * **Expected output:** `[78, 92, 81]`

-----

## 🔴 SECTION 3 — Error Handling (try, except, finally)

### 1️⃣1️⃣ Safe File Reader (Backend Config Loader)

  * **Write:**
    ```python
    def read_config(path):
        # try reading file
        # if file missing → print "Config not found"
        # finally → print("Attempt complete")
    ```
  * *Simulates API config loading.*

### 1️⃣2️⃣ Error-Safe Calculator (CLI App)

  * **Ask user:** first number, operator, second number
  * **Handle:**
      * **`ZeroDivisionError`**
      * **`ValueError`** (non-numeric input)
      * **Invalid operator**

### 1️⃣3️⃣ Safe Dictionary Lookup (API Response Handling)

  * **Given:** `data = {"name": "Alice", "age": 30}`
  * **Write:**
    ```python
    def safe_get(d, key):
        # return value if exists
        # else return "Key Missing"
    ```
  * *Equivalent to how API clients safely parse JSON responses.*

### 1️⃣4️⃣ Input Validation Loop

  * Ask user to enter a **valid age (integer)**.
  * Keep looping until **no exception occurs**.
  * *Useful for CLI apps, forms, validation layers.*

### 1️⃣5️⃣ Database Simulation — Handle Missing User

  * **Given:** `users = {"john": 101, "sara": 102}`
  * **Write function:** `get_user_id(username)`
      * If username not found → **catch exception** & print message.

-----

## 🟠 SECTION 4 — Custom Exceptions (Production-Level Behavior)

### 1️⃣6️⃣ Create Custom Exception: `InvalidEmailError`

  * **Rules:**
      * Must have `@`
      * Must end with **`.com`** or **`.in`**
  * **Raise:** `InvalidEmailError("Email format incorrect")`
  * *Used in signup systems and validation engines.*

### 1️⃣7️⃣ Custom Exception for Payment Validation

  * **Define:**
    ```python
    class InsufficientBalanceError(Exception): pass
    ```
  * **Write a function:** `def pay(amount, balance):`
      * **Raise error** if `amount > balance`.
  * *Simulates wallet payments (PayTM, Razorpay style).*

### 1️⃣8️⃣ Custom Password Checker for Registration System

  * **Rules:**
      * min length: **8**
      * must include **digit**
      * must include **uppercase**
  * **Raise:** **`WeakPasswordError`**

### 1️⃣9️⃣ Raise Custom Exception When JSON Field Missing (API Development)

  * **Data:** `{"name": "John"}`
  * **Function:** `validate_user(data)`
  * **Raise:** `MissingFieldError("Email is required")`
  * *Used in FastAPI, Django, Flask.*

### 2️⃣0️⃣ Build a Mini Validator for Product Prices

  * **Rules:** price must be **$> 0$**.
  * If invalid → **raise `InvalidPriceError`**.

-----

## 🔥 BONUS: Scenario-Based Hands-On (Very Real-Time)

These simulate real developer interviews & real work tasks.

### Scenario 1 — Online Form Validator

User fills a form with: **name**, **age**, **email**.

  * **Write:** `validate_form(name, age, email)`
  * **Handle:** Missing values, Wrong formats.
  * **Raise multiple custom exceptions**.

### Scenario 2 — ETL Pipeline Step

  * **Process incoming data:** `["10", "20", "abc", "40"]`
  * **Task:**
      * Convert to **integers**.
      * **Ignore invalid values** (using `try/except` inside a loop).

### Scenario 3 — CLI Password Manager

  * **Inputs:** **website**, **username**, **password**.
  * **Add custom exceptions:** `WeakPasswordError`, `SiteAlreadyExistsError`.
  * **Store in JSON**.

-----

Would you like to start with the solution for **Question 1: Build a Unit Conversion Service**?