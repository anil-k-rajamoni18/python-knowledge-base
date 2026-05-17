## Class Diagrams & Relationships

A **class diagram** is a UML (Unified Modeling Language) diagram that shows the structure of a system by modeling classes, their attributes, methods, and relationships between them.

---

## 📦 Anatomy of a Class Box

```
┌─────────────────────┐
│      ClassName      │  ← Class Name (bold, centered)
├─────────────────────┤
│ - attribute1: type  │  ← Attributes
│ # attribute2: type  │
│ + attribute3: type  │
├─────────────────────┤
│ + method1(): type   │  ← Methods
│ - method2(): void   │
└─────────────────────┘
```

### Visibility Symbols

| Symbol | Meaning |
|--------|---------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package/Internal |

---

## 🔗 Types of Relationships

### 1. 🔷 Inheritance (Is-A) `——▷`
Child class **inherits** from parent class. Solid line with **hollow arrowhead**.

> A `Dog` **is-a** `Animal`

### 2. 🔷 Realization / Implementation `- - -▷`
A class **implements** an interface. Dashed line with **hollow arrowhead**.

> `EmailNotifier` **implements** `Notifier`

### 3. 🔷 Association `———`
A class **uses** or **knows about** another. Basic relationship. Solid line.

> A `Doctor` **is associated with** a `Patient`

### 4. 🔷 Aggregation (Has-A, weak) `———◇`
One class **has** another, but the child **can exist independently**. Solid line with **hollow diamond**.

> A `Department` **has** `Employees` — but employees exist even if department is deleted.

### 5. 🔷 Composition (Has-A, strong) `———◆`
One class **owns** another, child **cannot exist without** parent. Solid line with **filled diamond**.

> A `House` **has** `Rooms` — rooms cannot exist without the house.

### 6. 🔷 Dependency (Uses-A) `- - ->`
A class **temporarily uses** another (e.g., as a method parameter). Dashed arrow.

> `OrderService` **depends on** `PaymentGateway`

---

## 🛒 Full Example — Online Order System

Let's model a simple e-commerce order flow.

### The Scenario
- A `Customer` places an `Order`
- An `Order` contains multiple `OrderItem`s
- Each `OrderItem` refers to a `Product`
- `Order` uses a `PaymentService` to process payment
- `PaymentService` is an interface, implemented by `CreditCardPayment` and `UPIPayment`
- An `Order` has an `Address` (can't exist without the order)

---

### Class Diagram

```
        «interface»
       ┌─────────────────────┐
       │   PaymentService    │
       ├─────────────────────┤
       │ + pay(amount): bool │
       └─────────────────────┘
               △
          (implements)
         ╱             ╲
┌──────────────────┐  ┌──────────────────┐
│ CreditCardPayment│  │   UPIPayment     │
├──────────────────┤  ├──────────────────┤
│ - cardNumber: str│  │ - upiId: str     │
├──────────────────┤  ├──────────────────┤
│ + pay(): bool    │  │ + pay(): bool    │
└──────────────────┘  └──────────────────┘


┌─────────────────────┐         ┌──────────────────────────┐
│      Customer       │1      * │         Order            │
├─────────────────────┤─────────├──────────────────────────┤
│ - id: int           │ places  │ - id: int                │
│ - name: str         │         │ - status: str            │
│ - email: str        │         │ - total: float           │
├─────────────────────┤         ├──────────────────────────┤
│ + place_order()     │         │ + add_item()             │
│ + get_orders()      │         │ + calculate_total()      │
└─────────────────────┘         │ + process_payment()      │
                                └──────────────────────────┘
                                          │ ◆ (composition)
                                          │ 1
                                          ▼ *
                                ┌──────────────────────────┐
                                │         Address          │
                                ├──────────────────────────┤
                                │ - street: str            │
                                │ - city: str              │
                                │ - pincode: str           │
                                └──────────────────────────┘

                                          │
                                          │ 1..*  (aggregation)
                                          ▼
                                ┌──────────────────────────┐
                                │       OrderItem          │
                                ├──────────────────────────┤
                                │ - quantity: int          │
                                │ - unit_price: float      │
                                ├──────────────────────────┤
                                │ + get_subtotal(): float  │
                                └──────────────────────────┘
                                          │ (association)
                                          │ *         1
                                          ▼
                                ┌──────────────────────────┐
                                │        Product           │
                                ├──────────────────────────┤
                                │ - id: int                │
                                │ - name: str              │
                                │ - price: float           │
                                │ - stock: int             │
                                ├──────────────────────────┤
                                │ + is_available(): bool   │
                                └──────────────────────────┘
```

---

## Relationships Explained (in this example)

| Relationship | Between | Type | Why |
|---|---|---|---|
| `Customer` → `Order` | places | **Association (1 to many)** | A customer places many orders |
| `Order` → `Address` | has | **Composition** | Address cannot exist without the Order |
| `Order` → `OrderItem` | contains | **Aggregation** | Items are part of an order but Product exists independently |
| `OrderItem` → `Product` | refers to | **Association** | An item points to a product |
| `Order` → `PaymentService` | uses | **Dependency** | Order calls `pay()` but doesn't own the service |
| `CreditCardPayment` → `PaymentService` | implements | **Realization** | Concrete class fulfills the interface contract |

---

## Python Code Mapping

```python
from abc import ABC, abstractmethod

# Interface → Realization
class PaymentService(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentService):       # Realization
    def __init__(self, card_number: str):
        self.__card_number = card_number        # private attr

    def pay(self, amount: float) -> bool:
        print(f"Charging ₹{amount} to card {self.__card_number[-4:]}")
        return True

class UPIPayment(PaymentService):              # Realization
    def __init__(self, upi_id: str):
        self.__upi_id = upi_id

    def pay(self, amount: float) -> bool:
        print(f"Paying ₹{amount} via UPI {self.__upi_id}")
        return True

# Composition — Address lives inside Order
class Address:
    def __init__(self, street: str, city: str, pincode: str):
        self.street = street
        self.city = city
        self.pincode = pincode

class Product:
    def __init__(self, id: int, name: str, price: float, stock: int):
        self.id = id
        self.name = name
        self.price = price
        self.__stock = stock                   # private

    def is_available(self) -> bool:
        return self.__stock > 0

# Aggregation — OrderItem has a Product reference
class OrderItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.unit_price = product.price

    def get_subtotal(self) -> float:
        return self.unit_price * self.quantity

# Association + Composition + Dependency
class Order:
    def __init__(self, order_id: int, address: Address):
        self.__id = order_id
        self.__status = "PENDING"
        self.__items: list[OrderItem] = []
        self.__address = address               # composition

    def add_item(self, item: OrderItem):
        self.__items.append(item)

    def calculate_total(self) -> float:
        return sum(item.get_subtotal() for item in self.__items)

    def process_payment(self, payment_service: PaymentService) -> bool:  # dependency
        total = self.calculate_total()
        success = payment_service.pay(total)
        if success:
            self.__status = "CONFIRMED"
        return success

class Customer:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.__email = email
        self.__orders: list[Order] = []        # 1-to-many association

    def place_order(self, order: Order):
        self.__orders.append(order)
        return order

    def get_orders(self) -> list[Order]:
        return self.__orders


# ── Quick Simulation ──────────────────────────────────────────
if __name__ == "__main__":
    customer = Customer(1, "Ravi", "ravi@example.com")
    address  = Address("12 MG Road", "Hyderabad", "500001")

    laptop  = Product(101, "Laptop", 75000.0, 10)
    mouse   = Product(102, "Mouse", 1500.0, 50)

    order = Order(order_id=1001, address=address)
    order.add_item(OrderItem(laptop, 1))
    order.add_item(OrderItem(mouse, 2))

    print(f"Total: ₹{order.calculate_total()}")   # ₹78000.0

    payment = UPIPayment("ravi@upi")
    order.process_payment(payment)                 # Paying ₹78000 via UPI

    customer.place_order(order)
    print(f"Orders placed by {customer.name}: {len(customer.get_orders())}")
```

---

## 🧠 Quick Reference Card

```
Inheritance    A ——————▷ B       "A is a B"              (extends)
Realization    A - - - -▷ B      "A implements B"         (interface)
Association    A ———————  B       "A knows B"             (uses ref)
Aggregation    A ———————◇ B       "A has B (weak)"        (B survives)
Composition    A ———————◆ B       "A owns B (strong)"     (B dies with A)
Dependency     A - - - -> B       "A temporarily uses B"  (method param)
```

---
## 📚 Library Management System — Full Class Diagram & OOP Design

---

## Step 1: Requirements Clarification

Before drawing anything, identify what the system must do:

- Members can **search** books by title, author, or genre
- Members can **borrow** and **return** books
- A book can have **multiple copies**
- **Fines** are charged for late returns
- **Librarian** can add/remove books and manage members
- System sends **notifications** when a book is due or available

---

## Step 2: Identify Entities (Classes)

Reading the requirements, the main nouns become classes:

```
Person          → base class
Member          → extends Person (borrows books)
Librarian       → extends Person (manages system)
Book            → the catalog entry
BookCopy        → physical copy of a book
BorrowRecord    → tracks who borrowed what and when
Fine            → penalty for late return
Notification    → alert system (interface)
EmailNotifier   → implements Notification
Catalog         → searchable book registry
Library         → central system orchestrator
```

---

## Step 3: Class Diagram

```
                    ┌──────────────────────────┐
                    │          Person          │  ← Abstract Base
                    ├──────────────────────────┤
                    │ # id: int                │
                    │ # name: str              │
                    │ # email: str             │
                    │ # phone: str             │
                    ├──────────────────────────┤
                    │ + get_info(): str        │
                    └──────────────────────────┘
                               △
                    (Inheritance / Is-A)
                   ╱                          ╲
   ┌───────────────────────┐    ┌───────────────────────────┐
   │        Member         │    │         Librarian         │
   ├───────────────────────┤    ├───────────────────────────┤
   │ - member_id: str      │    │ - employee_id: str        │
   │ - membership: str     │    │ - department: str         │
   │ - is_active: bool     │    ├───────────────────────────┤
   ├───────────────────────┤    │ + add_book()              │
   │ + borrow_book()       │    │ + remove_book()           │
   │ + return_book()       │    │ + register_member()       │
   │ + get_borrowed()      │    │ + revoke_member()         │
   │ + pay_fine()          │    │ + view_all_borrows()      │
   └───────────────────────┘    └───────────────────────────┘
              │ 1
              │ (Association — member has borrow records)
              │ *
   ┌──────────────────────────────┐
   │         BorrowRecord         │
   ├──────────────────────────────┤
   │ - record_id: str             │
   │ - borrow_date: date          │
   │ - due_date: date             │
   │ - return_date: date          │
   │ - status: str                │  ← BORROWED | RETURNED | OVERDUE
   ├──────────────────────────────┤
   │ + is_overdue(): bool         │
   │ + days_overdue(): int        │
   │ + calculate_fine(): Fine     │
   └──────────────────────────────┘
              │ 1
              │ (Composition — Fine can't exist without BorrowRecord)
              ▼ 0..1
   ┌──────────────────────────────┐
   │            Fine              │
   ├──────────────────────────────┤
   │ - amount: float              │
   │ - is_paid: bool              │
   │ - generated_on: date         │
   ├──────────────────────────────┤
   │ + pay()                      │
   │ + get_amount(): float        │
   └──────────────────────────────┘

              │ (BorrowRecord ↔ BookCopy — Association)
              ▼ *                            1
   ┌──────────────────────────────┐
   │          BookCopy            │
   ├──────────────────────────────┤
   │ - copy_id: str               │
   │ - condition: str             │  ← GOOD | DAMAGED | LOST
   │ - is_available: bool         │
   ├──────────────────────────────┤
   │ + mark_borrowed()            │
   │ + mark_returned()            │
   └──────────────────────────────┘
              │ * (Aggregation — copies belong to Book, but can be tracked independently)
              │
              ▼ 1
   ┌──────────────────────────────┐          ┌──────────────────────────┐
   │            Book              │          │         Catalog          │
   ├──────────────────────────────┤          ├──────────────────────────┤
   │ - isbn: str                  │ *──────1 │ - books: list[Book]      │
   │ - title: str                 │  (Aggr.) ├──────────────────────────┤
   │ - author: str                │          │ + search_by_title()      │
   │ - genre: str                 │          │ + search_by_author()     │
   │ - published_year: int        │          │ + search_by_genre()      │
   ├──────────────────────────────┤          │ + add_book()             │
   │ + get_available_copies()     │          │ + remove_book()          │
   │ + total_copies(): int        │          └──────────────────────────┘
   └──────────────────────────────┘

        «interface»
   ┌──────────────────────────────┐
   │       Notifier               │
   ├──────────────────────────────┤
   │ + send(member, msg): void    │
   └──────────────────────────────┘
               △
          (Realization)
         ╱             ╲
┌─────────────────┐  ┌─────────────────┐
│  EmailNotifier  │  │   SMSNotifier   │
├─────────────────┤  ├─────────────────┤
│ + send()        │  │ + send()        │
└─────────────────┘  └─────────────────┘

   ┌──────────────────────────────────────────────┐
   │                  Library                     │  ← Orchestrator
   ├──────────────────────────────────────────────┤
   │ - name: str                                  │
   │ - catalog: Catalog            (composition)  │
   │ - members: list[Member]       (aggregation)  │
   │ - notifier: Notifier          (dependency)   │
   ├──────────────────────────────────────────────┤
   │ + borrow_book(member, isbn)                  │
   │ + return_book(member, copy_id)               │
   │ + search(query)                              │
   └──────────────────────────────────────────────┘
```

---

## Step 4: Relationship Summary

| From | To | Relationship | Reason |
|------|-----|------|--------|
| `Member` / `Librarian` | `Person` | **Inheritance** | Both are persons |
| `Member` | `BorrowRecord` | **Association (1..*)** | Member has many borrow records |
| `BorrowRecord` | `Fine` | **Composition** | Fine cannot exist without a borrow record |
| `BorrowRecord` | `BookCopy` | **Association** | Record tracks which copy was borrowed |
| `Book` | `BookCopy` | **Aggregation** | Copies belong to a book; copies tracked independently |
| `Catalog` | `Book` | **Aggregation** | Catalog holds books; books exist independently |
| `Library` | `Catalog` | **Composition** | Catalog is part of Library; destroyed with it |
| `Library` | `Member` | **Aggregation** | Library manages members; members exist independently |
| `Library` | `Notifier` | **Dependency** | Library uses notifier temporarily |
| `EmailNotifier` / `SMSNotifier` | `Notifier` | **Realization** | Implement the interface |

---

## Step 5: Full Python Implementation

```python
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import Optional
import uuid


# ─────────────────────────────────────────────
# NOTIFIER INTERFACE + IMPLEMENTATIONS
# ─────────────────────────────────────────────
class Notifier(ABC):
    @abstractmethod
    def send(self, email: str, message: str) -> None:
        pass

class EmailNotifier(Notifier):
    def send(self, email: str, message: str) -> None:
        print(f"[EMAIL → {email}]: {message}")

class SMSNotifier(Notifier):
    def send(self, email: str, message: str) -> None:
        print(f"[SMS → {email}]: {message}")


# ─────────────────────────────────────────────
# FINE — Composition with BorrowRecord
# ─────────────────────────────────────────────
class Fine:
    FINE_PER_DAY = 5.0  # ₹5 per day

    def __init__(self, days_overdue: int):
        self.amount = days_overdue * self.FINE_PER_DAY
        self.is_paid = False
        self.generated_on = date.today()

    def pay(self) -> None:
        self.is_paid = True
        print(f"  ✅ Fine of ₹{self.amount} paid.")

    def __repr__(self):
        status = "Paid" if self.is_paid else "Unpaid"
        return f"Fine(₹{self.amount}, {status})"


# ─────────────────────────────────────────────
# BOOK COPY — Aggregation with Book
# ─────────────────────────────────────────────
class BookCopy:
    def __init__(self, isbn: str):
        self.copy_id = str(uuid.uuid4())[:8].upper()
        self.isbn = isbn
        self.condition = "GOOD"
        self.is_available = True

    def mark_borrowed(self) -> None:
        self.is_available = False

    def mark_returned(self) -> None:
        self.is_available = True

    def __repr__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"Copy({self.copy_id} | {status})"


# ─────────────────────────────────────────────
# BOOK
# ─────────────────────────────────────────────
class Book:
    def __init__(self, isbn: str, title: str, author: str,
                 genre: str, year: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.published_year = year
        self.__copies: list[BookCopy] = []

    def add_copy(self) -> BookCopy:
        copy = BookCopy(self.isbn)
        self.__copies.append(copy)
        return copy

    def get_available_copies(self) -> list[BookCopy]:
        return [c for c in self.__copies if c.is_available]

    def total_copies(self) -> int:
        return len(self.__copies)

    def __repr__(self):
        available = len(self.get_available_copies())
        return (f'"{self.title}" by {self.author} '
                f'[{available}/{self.total_copies()} available]')


# ─────────────────────────────────────────────
# BORROW RECORD — Association with Member & BookCopy
# Fine is Composition inside here
# ─────────────────────────────────────────────
class BorrowRecord:
    LOAN_DAYS = 14

    def __init__(self, member_id: str, copy: BookCopy, book_title: str):
        self.record_id = str(uuid.uuid4())[:8].upper()
        self.member_id = member_id
        self.copy = copy
        self.book_title = book_title
        self.borrow_date = date.today()
        self.due_date = date.today() + timedelta(days=self.LOAN_DAYS)
        self.return_date: Optional[date] = None
        self.status = "BORROWED"
        self.fine: Optional[Fine] = None

    def is_overdue(self) -> bool:
        check_date = self.return_date or date.today()
        return check_date > self.due_date

    def days_overdue(self) -> int:
        if not self.is_overdue():
            return 0
        check_date = self.return_date or date.today()
        return (check_date - self.due_date).days

    def calculate_fine(self) -> Optional[Fine]:
        if self.is_overdue():
            self.fine = Fine(self.days_overdue())  # Composition
        return self.fine

    def close(self, return_date: Optional[date] = None) -> Optional[Fine]:
        self.return_date = return_date or date.today()
        self.copy.mark_returned()
        fine = self.calculate_fine()
        self.status = "OVERDUE" if fine else "RETURNED"
        return fine

    def __repr__(self):
        return (f"Record({self.record_id} | {self.book_title} | "
                f"Due: {self.due_date} | {self.status})")


# ─────────────────────────────────────────────
# PERSON — Abstract Base
# ─────────────────────────────────────────────
class Person(ABC):
    def __init__(self, name: str, email: str, phone: str):
        self._id = str(uuid.uuid4())[:8].upper()
        self._name = name
        self._email = email
        self._phone = phone

    @abstractmethod
    def get_info(self) -> str:
        pass

    @property
    def name(self): return self._name

    @property
    def email(self): return self._email


# ─────────────────────────────────────────────
# MEMBER — Inherits Person
# ─────────────────────────────────────────────
class Member(Person):
    MAX_BORROW_LIMIT = 3

    def __init__(self, name: str, email: str, phone: str):
        super().__init__(name, email, phone)
        self.member_id = f"MEM-{self._id}"
        self.membership = "STANDARD"
        self.is_active = True
        self.__borrow_records: list[BorrowRecord] = []

    def borrow_book(self, copy: BookCopy, book_title: str) -> BorrowRecord:
        if not self.is_active:
            raise PermissionError("Membership is inactive.")
        active = self.get_active_borrows()
        if len(active) >= self.MAX_BORROW_LIMIT:
            raise Exception(f"Borrow limit ({self.MAX_BORROW_LIMIT}) reached.")
        
        record = BorrowRecord(self.member_id, copy, book_title)
        copy.mark_borrowed()
        self.__borrow_records.append(record)
        return record

    def return_book(self, record_id: str) -> Optional[Fine]:
        record = self._find_record(record_id)
        if not record:
            raise Exception("Record not found.")
        fine = record.close()
        return fine

    def pay_fine(self, record_id: str) -> None:
        record = self._find_record(record_id)
        if record and record.fine:
            record.fine.pay()

    def get_active_borrows(self) -> list[BorrowRecord]:
        return [r for r in self.__borrow_records if r.status == "BORROWED"]

    def get_all_records(self) -> list[BorrowRecord]:
        return self.__borrow_records

    def _find_record(self, record_id: str) -> Optional[BorrowRecord]:
        return next((r for r in self.__borrow_records
                     if r.record_id == record_id), None)

    def get_info(self) -> str:
        return (f"Member: {self._name} | ID: {self.member_id} "
                f"| Active Borrows: {len(self.get_active_borrows())}")


# ─────────────────────────────────────────────
# LIBRARIAN — Inherits Person
# ─────────────────────────────────────────────
class Librarian(Person):
    def __init__(self, name: str, email: str, phone: str, dept: str):
        super().__init__(name, email, phone)
        self.employee_id = f"LIB-{self._id}"
        self.department = dept

    def get_info(self) -> str:
        return f"Librarian: {self._name} | Dept: {self.department}"


# ─────────────────────────────────────────────
# CATALOG — Aggregation with Book
# ─────────────────────────────────────────────
class Catalog:
    def __init__(self):
        self.__books: dict[str, Book] = {}  # isbn → Book

    def add_book(self, book: Book) -> None:
        self.__books[book.isbn] = book
        print(f"  📗 Added to catalog: {book.title}")

    def remove_book(self, isbn: str) -> None:
        self.__books.pop(isbn, None)

    def search_by_title(self, query: str) -> list[Book]:
        q = query.lower()
        return [b for b in self.__books.values()
                if q in b.title.lower()]

    def search_by_author(self, query: str) -> list[Book]:
        q = query.lower()
        return [b for b in self.__books.values()
                if q in b.author.lower()]

    def search_by_genre(self, genre: str) -> list[Book]:
        return [b for b in self.__books.values()
                if b.genre.lower() == genre.lower()]

    def get_book(self, isbn: str) -> Optional[Book]:
        return self.__books.get(isbn)


# ─────────────────────────────────────────────
# LIBRARY — Orchestrator (Central System)
# ─────────────────────────────────────────────
class Library:
    def __init__(self, name: str, notifier: Notifier):
        self.name = name
        self.__catalog = Catalog()           # Composition
        self.__members: dict[str, Member] = {}  # Aggregation
        self.__notifier = notifier           # Dependency

    def register_member(self, member: Member) -> None:
        self.__members[member.member_id] = member
        print(f"  👤 Registered: {member.name} ({member.member_id})")
        self.__notifier.send(
            member.email,
            f"Welcome to {self.name}, {member.name}! Happy reading! 📚"
        )

    def add_book(self, book: Book, copies: int = 1) -> None:
        self.__catalog.add_book(book)
        for _ in range(copies):
            book.add_copy()
        print(f"  📦 {copies} copy/copies added for '{book.title}'")

    def borrow_book(self, member_id: str, isbn: str) -> BorrowRecord:
        member = self.__members.get(member_id)
        if not member:
            raise Exception("Member not found.")
        book = self.__catalog.get_book(isbn)
        if not book:
            raise Exception("Book not found in catalog.")
        available = book.get_available_copies()
        if not available:
            raise Exception(f"No copies available for '{book.title}'.")

        record = member.borrow_book(available[0], book.title)
        self.__notifier.send(
            member.email,
            f"You borrowed '{book.title}'. Due: {record.due_date} 📅"
        )
        print(f"  ✅ {member.name} borrowed '{book.title}' "
              f"(Record: {record.record_id})")
        return record

    def return_book(self, member_id: str, record_id: str) -> None:
        member = self.__members.get(member_id)
        if not member:
            raise Exception("Member not found.")
        fine = member.return_book(record_id)
        if fine:
            self.__notifier.send(
                member.email,
                f"Late return! Fine of ₹{fine.amount} is due. Please pay at the counter."
            )
            print(f"  ⚠️  Fine generated: ₹{fine.amount}")
        else:
            print(f"  ✅ Book returned on time. No fine.")

    def search(self, query: str, by: str = "title") -> list[Book]:
        if by == "title":
            return self.__catalog.search_by_title(query)
        elif by == "author":
            return self.__catalog.search_by_author(query)
        elif by == "genre":
            return self.__catalog.search_by_genre(query)
        return []


# ─────────────────────────────────────────────
# SIMULATION
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("       📚 LIBRARY MANAGEMENT SYSTEM")
    print("=" * 55)

    # Setup
    notifier = EmailNotifier()
    library = Library("City Central Library", notifier)

    print("\n── Setting Up Books ──")
    b1 = Book("ISBN001", "Clean Code", "Robert Martin", "Tech", 2008)
    b2 = Book("ISBN002", "The Alchemist", "Paulo Coelho", "Fiction", 1988)
    b3 = Book("ISBN003", "Atomic Habits", "James Clear", "Self-Help", 2018)
    library.add_book(b1, copies=2)
    library.add_book(b2, copies=1)
    library.add_book(b3, copies=3)

    print("\n── Registering Members ──")
    alice = Member("Alice", "alice@email.com", "9999999991")
    bob   = Member("Bob",   "bob@email.com",   "9999999992")
    library.register_member(alice)
    library.register_member(bob)

    print("\n── Searching Books ──")
    results = library.search("clean", by="title")
    for r in results:
        print(f"  Found: {r}")

    results = library.search("Fiction", by="genre")
    for r in results:
        print(f"  Found: {r}")

    print("\n── Borrowing Books ──")
    rec1 = library.borrow_book(alice.member_id, "ISBN001")
    rec2 = library.borrow_book(alice.member_id, "ISBN003")
    rec3 = library.borrow_book(bob.member_id, "ISBN002")

    print("\n── Alice's Active Borrows ──")
    for r in alice.get_active_borrows():
        print(f"  {r}")

    print("\n── Returning a Book (on time) ──")
    library.return_book(alice.member_id, rec1.record_id)

    print("\n── Simulating Late Return ──")
    # Manually set borrow date to 20 days ago to simulate overdue
    rec2.borrow_date = date.today() - timedelta(days=20)
    rec2.due_date    = date.today() - timedelta(days=6)
    library.return_book(alice.member_id, rec2.record_id)

    print("\n── Paying Fine ──")
    alice.pay_fine(rec2.record_id)

    print("\n── Final Member Info ──")
    print(f"  {alice.get_info()}")
    print(f"  {bob.get_info()}")
    print("\n" + "=" * 55)
```

---

## Step 6: Sample Output

```
=======================================================
       📚 LIBRARY MANAGEMENT SYSTEM
=======================================================

── Setting Up Books ──
  📗 Added to catalog: Clean Code
  📦 2 copy/copies added for 'Clean Code'
  📗 Added to catalog: The Alchemist
  📦 1 copy/copies added for 'The Alchemist'
  📗 Added to catalog: Atomic Habits
  📦 3 copy/copies added for 'Atomic Habits'

── Registering Members ──
  👤 Registered: Alice (MEM-XXXX)
  [EMAIL → alice@email.com]: Welcome to City Central Library, Alice!
  👤 Registered: Bob (MEM-YYYY)
  [EMAIL → bob@email.com]: Welcome to City Central Library, Bob!

── Searching Books ──
  Found: "Clean Code" by Robert Martin [2/2 available]
  Found: "The Alchemist" by Paulo Coelho [1/1 available]

── Borrowing Books ──
  ✅ Alice borrowed 'Clean Code' (Record: REC-001)
  ✅ Alice borrowed 'Atomic Habits' (Record: REC-002)
  ✅ Bob borrowed 'The Alchemist' (Record: REC-003)

── Returning a Book (on time) ──
  ✅ Book returned on time. No fine.

── Simulating Late Return ──
  ⚠️  Fine generated: ₹30.0
  [EMAIL → alice@email.com]: Late return! Fine of ₹30.0 is due.

── Paying Fine ──
  ✅ Fine of ₹30.0 paid.

── Final Member Info ──
  Member: Alice | ID: MEM-XXXX | Active Borrows: 0
  Member: Bob   | ID: MEM-YYYY | Active Borrows: 1
=======================================================
```

---

## 🧠 Key OOP Concepts Used

| Concept | Where Applied |
|---|---|
| **Abstraction** | `Person`, `Notifier` as abstract base |
| **Inheritance** | `Member`, `Librarian` extend `Person` |
| **Encapsulation** | Private `__copies`, `__borrow_records`, `__catalog` |
| **Polymorphism** | `EmailNotifier` & `SMSNotifier` both implement `send()` |
| **Composition** | `Fine` inside `BorrowRecord`; `Catalog` inside `Library` |
| **Aggregation** | `BookCopy` inside `Book`; `Member` inside `Library` |
| **Dependency** | `Library` uses `Notifier` without owning it |
| **Interface** | `Notifier` is a pluggable contract |