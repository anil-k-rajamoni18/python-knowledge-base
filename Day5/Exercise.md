# 🧪 DAY 5 — Hands-On, Real-Time, Industry-Level Exercises (OOP)

-----

## 🟦 SECTION 1 — Classes, Objects, Methods (Foundational but Real-World)

### 1️⃣ User Profile Manager (Web App Style)

Create a class **`User`** with:

  * **Attributes:** `username`, `email`, `role`
  * **Methods:** `update_email()`, `change_role()`, `get_profile()`
  * **Validation:** `email` must include `@`
  * **Simulates:** User management in backend APIs (e.g., Django/FastAPI user model structure).

### 2️⃣ Product Inventory (E-commerce)

Create a class **`Product`** that stores:

  * `id`
  * `name`
  * `stock_quantity`
  * `price`
  * **Methods:**
      * `add_stock(amount)`
      * `reduce_stock(amount)` (cannot go negative)
      * `get_price_with_tax(tax_rate)`

### 3️⃣ Employee Salary Calculator (HR Systems)

Create: **`Employee(name, id, base_salary)`**

  * **Methods:**
      * `calculate_bonus(%)`
      * `yearly_salary()`

### 4️⃣ IoT Sensor Class (Industry Automation)

Class: **`TemperatureSensor`**

  * **Attributes:**
      * `sensor_id`
      * `current_temperature`
  * **Methods:**
      * `read()` $\to$ returns temperature
      * `is_overheated(threshold)`

### 5️⃣ Chatbot Message Object (AI System)

Class: **`Message`**

  * **Attributes:**
      * `sender`
      * `text`
      * `timestamp`
  * **Method:**
      * `preview()` $\to$ prints first **20 characters only**

-----

## 🟩 SECTION 2 — Inheritance (Industry Scenarios)

### 6️⃣ Notification System (Polymorphic Behavior)

  * **Base class:** **`Notification`** $\to$ `.send()`
  * **Derived classes:**
      * `EmailNotification`
      * `SMSNotification`
      * `PushNotification`
  * Each overrides **`.send()`**.
  * **Simulates:** Microservice event handling.

### 7️⃣ Vehicle Simulation System

  * **Base class:** **`Vehicle`**
  * **Derived:**
      * `Car`
      * `Bike`
      * `Truck`
  * Each implements:
      * `max_speed()`
      * `fuel_type()`

### 8️⃣ Employee Hierarchy (HR Management)

  * **Base class:** **`Employee`**
  * **Derived:**
      * `Manager`
      * `Developer`
      * `Intern`
  * **Override:**
      * `calculate_salary()`
      * `get_responsibilities()`

### 9️⃣ Online Payment Methods (FinTech)

  * **Base:** **`PaymentMethod`** $\to$ `pay(amount)`
  * **Derived:**
      * `UPI`
      * `CreditCard`
      * `NetBanking`
  * Each implements its own **`pay`** logic.

### 🔟 Course Content System (EdTech)

  * **Base class:** **`CourseContent`**
  * **Derived:**
      * `Video`
      * `Article`
      * `Quiz`
  * Each overrides:
      * `get_duration()`
      * `display()`

-----

## 🟥 SECTION 3 — Polymorphism (Real-Time Use Cases)

### 1️⃣1️⃣ Train ML Models (AI/ML Pipeline Simulation)

  * **Base:**
    ```python
    class Model:
        def train(self): pass
        def predict(self): pass
    ```
  * **Derived:**
      * `LinearRegression`
      * `RandomForest`
      * `NeuralNetwork`
  * Polymorphic **`train()`** & **`predict()`**.

### 1️⃣2️⃣ File Export System (Excel, PDF, CSV)

  * **Base class:** **`Exporter`** $\to$ `export(data)`
  * **Derived:**
      * `CSVExporter`
      * `PDFExporter`
      * `ExcelExporter`
  * **Simulates:** Enterprise reporting tools.

### 1️⃣3️⃣ Pluggable Authentication System

  * **Base:** **`AuthProvider`** $\to$ `authenticate(user, password)`
  * **Supports:**
      * `LDAPAuth`
      * `SSOAuth`
      * `TokenAuth`

### 1️⃣4️⃣ Media Player (Polymorphic Play)

  * **Classes:**
      * `MP3`
      * `WAV`
      * `MP4`
  * All implement: **`play()`**

### 1️⃣5️⃣ Pricing Strategy (E-commerce Discounts)

  * **Base:** **`DiscountStrategy`** $\to$ `apply(price)`
  * **Derived:**
      * `FestivalDiscount`
      * `CouponDiscount`
      * `ClearanceSaleDiscount`

-----

## 🟨 SECTION 4 — Encapsulation & Abstraction (Realistic Use)

### 1️⃣6️⃣ Bank Account with Private Balance

Class **`BankAccount`**:

  * **Private** `__balance`
  * `deposit()`
  * `withdraw()`
  * `get_balance()`
  * Must validate **negative deposits** & **over-withdrawals**.

### 1️⃣7️⃣ Credentials Vault (Security System)

Class **`Credential`**

  * **Private** `password`
  * Method `verify(password)`
  * Method `update_password()` with validations

### 1️⃣8️⃣ Payment Gateway (Abstract Base Class)

Using **`abc`**:

```python
class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
```

  * **Implement:**
      * `PayPalGateway`
      * `RazorpayGateway`

### 1️⃣9️⃣ Encryption Service (Abstraction Layer)

  * **Base:** **`Encryptor`** $\to$ `encrypt(data)`, `decrypt(data)`
  * **Derived:**
      * `AESEncryptor`
      * `DESEncryptor`

### 2️⃣0️⃣ Database Connector (Abstracted I/O)

  * **Classes:**
      * `BaseConnector`
      * `MySQLConnector`
      * `MongoConnector`
  * Must implement:
      * `connect()`
      * `execute_query()`

-----

## 🟧 SECTION 5 — Class vs Instance Variables

### 2️⃣1️⃣ Track Total Number of Users

Class **`User`** with:

  * **Instance vars:** `name`, `email`
  * **Class var:** `total_users`
  * Increment count on each object creation.

### 2️⃣2️⃣ Global App Config

  * **Class variable:** `APP_VERSION = "1.0"`
  * **Instance variables:** user-specific settings.

### 2️⃣3️⃣ Tax Calculation System

  * **Class variable:** `GST_RATE = 18`
  * Used across all instances of **`Invoice`**.

### 2️⃣4️⃣ Shared Discount System

  * **Class var:** `global_discount = 10`
  * **Instance var:** product-specific discount

### 2️⃣5️⃣ Track Sessions in a Chat App

  * **Class var:** number of active sessions
  * **Instance var:** username, login time

-----

## 🟫 SECTION 6 — Magic Methods (Dunder Methods)

### 2️⃣6️⃣ Custom `__str__` for Product Cards

Create: **`Product(name, price)`**

  * **Return:** `"Product: MacBook | Price: ₹120000"`

### 2️⃣7️⃣ Implement `__eq__` for Comparing Users

  * Users with the same `email` should be considered “equal”.

### 2️⃣8️⃣ Implement `__lt__` for Sorting Tasks

  * Class: **`Task(priority)`**
  * Should sort tasks by priority.

### 2️⃣9️⃣ Custom `__add__` for Merging Carts

  * `cart1 + cart2` $\to$ merged cart
  * Used in e-commerce systems.

### 3️⃣0️⃣ Implement Iterator (`__iter__`, `__next__`) for Playlist

  * **`Playlist`** iterates through songs one by one.

-----

## 🟩 BONUS: FULL REAL-TIME SCENARIOS (INTERVIEW LEVEL)

### Scenario 1 — Build a Transport Booking System

  * **Classes:** `Vehicle`, `Bus`, `Taxi`, `Auto`, `Booking`
  * Implement polymorphic fare calculation.

### Scenario 2 — OOP-Based Logging Framework

  * **Levels:** `INFO`, `WARNING`, `ERROR`
  * Each writes logs differently (file, console, DB).

### Scenario 3 — Chat Application Backend

  * **Classes:** `User`, `Message`, `ChatRoom`
  * **Include:** private attributes, custom dunder methods, class variables

### Scenario 4 — Document Version Control System (Git-Like)

  * **Classes:** `Document`, `Commit`, `VersionManager`
  * **Features:** unique commit IDs, rollback, version history

### Scenario 5 — Rule Engine (Used in Banking Fraud Detection)

  * **Base:** `Rule` $\to$ `evaluate(transaction)`
  * **Implement:** `HighAmountRule`, `CountryMismatchRule`, `VelocityRule`



---

---

## 🏗️ Beginner — OOP Fundamentals in Design

**1. Design a Library Management System**
Model books, members, and borrowing. Practice classes, inheritance, encapsulation. Implement `borrow_book()`, `return_book()`, `search_by_author()`.

**2. Design a Parking Lot**
Classic OOP problem. Model different vehicle types, parking spots, and a ticket system. Think about inheritance (`Car`, `Bike`, `Truck` → `Vehicle`) and single responsibility.

**3. Design a Bank Account System**
Model `SavingsAccount`, `CurrentAccount` inheriting from `BankAccount`. Implement deposit, withdrawal, transfer, and transaction history. Practice polymorphism.

**4. Design a Zoo**
Model animals with different `speak()` and `move()` behaviors. Practice abstract classes and interfaces via Python's `ABC` module.

---

## ⚙️ Intermediate — Real-World System Design

**5. Design a Shopping Cart / E-Commerce System**
Model `User`, `Product`, `Cart`, `Order`, `Payment`. Apply OOP relationships — composition vs inheritance, and design patterns like Strategy (for payment methods).

**6. Design a Hotel Booking System**
Model rooms, bookings, guests, and availability. Focus on encapsulation of booking logic, date conflict detection, and room types.

**7. Design a Ride-Sharing App (Uber-lite)**
Model `Driver`, `Rider`, `Trip`, `Location`. Practice state management (trip states: requested → accepted → ongoing → completed) and Observer pattern.

**8. Design an ATM Machine**
Model card authentication, balance check, cash dispensing, and receipt. Strong focus on state design pattern and encapsulation of machine states.

**9. Design a Movie Ticket Booking System (BookMyShow-lite)**
Model `Movie`, `Theatre`, `Screen`, `Seat`, `Booking`. Handle seat locking, concurrency concept (even at design level), and payment.

---

## 🚀 Advanced — Design Patterns + Architecture

**10. Design a Notification System**
Support Email, SMS, Push notifications. Practice the **Observer** and **Strategy** design patterns. Make it extensible to add new channels without changing existing code.

**11. Design a File System**
Model files and folders recursively. Classic **Composite** design pattern problem. Implement `ls`, `mkdir`, `search`, and `get_size()`.

**12. Design a Cache System (LRU Cache)**
Implement an LRU cache using OOP. Use `OrderedDict` internally. Practice encapsulation and hiding implementation details behind a clean interface.

**13. Design a Task Queue / Job Scheduler**
Model jobs with priorities, workers, and a scheduler. Practice **Producer-Consumer** pattern, state machines, and queue-based design.

**14. Design a Logging Framework (like Python's `logging`)**
Build your own from scratch — `Logger`, `Handler`, `Formatter`, log levels. This is a meta-exercise that reinforces everything you've already learned about logging.

---

## 🧭 How to Approach Each Problem

For every question, follow this structure:

```
1. Clarify requirements     → What are the core features? Constraints?
2. Identify entities        → What are the main nouns? (these become classes)
3. Define relationships     → Inheritance? Composition? Association?
4. Define interfaces        → What methods does each class expose?
5. Code the skeleton        → Classes, attributes, method signatures
6. Implement logic          → Fill in the methods
7. Test with a scenario     → Write a small main() to simulate usage
```

---
