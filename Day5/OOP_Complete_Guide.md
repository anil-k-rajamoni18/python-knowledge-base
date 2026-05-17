# Python Object-Oriented Programming (OOP) - Complete Guide

## Table of Contents
1. [Session 1: Fundamentals & Core Concepts](#session-1)
2. [Session 2: Advanced Concepts & Real-world Applications](#session-2)
3. [Mini Projects](#mini-projects)

---

# SESSION 1: Fundamentals & Core Concepts

## 1. Functions vs Object-Oriented Programming

### Why Move from Functions to OOP?

#### Procedural Programming (Functions-Based Approach)

```python
# ❌ Procedural Approach - Without OOP
def create_student(name, age, gpa):
    return {"name": name, "age": age, "gpa": gpa}

def update_gpa(student, new_gpa):
    student["gpa"] = new_gpa
    return student

def display_student(student):
    print(f"Name: {student['name']}, Age: {student['age']}, GPA: {student['gpa']}")

# Usage
student1 = create_student("Alice", 20, 3.8)
student2 = create_student("Bob", 21, 3.5)
update_gpa(student1, 3.9)
display_student(student1)
display_student(student2)

# Problems with this approach:
# - Data and functions are separated
# - No encapsulation
# - Difficult to maintain as code grows
# - No real relationship between data and functions
# - Duplicate code if we have multiple student types
# - Hard to add new behaviors
```

#### Object-Oriented Programming (Class-Based Approach)

```python
# ✅ OOP Approach - With Classes
class Student:
    def __init__(self, name, age, gpa):
        self.name = name
        self.age = age
        self.gpa = gpa
    
    def update_gpa(self, new_gpa):
        """Update student GPA"""
        self.gpa = new_gpa
        print(f"GPA updated to {self.gpa}")
    
    def display_info(self):
        """Display student information"""
        print(f"Name: {self.name}, Age: {self.age}, GPA: {self.gpa}")
    
    def is_honor_student(self):
        """Check if student has honors GPA"""
        return self.gpa >= 3.7

# Usage
student1 = Student("Alice", 20, 3.8)
student2 = Student("Bob", 21, 3.5)

student1.update_gpa(3.9)
student1.display_info()
print(f"Honor Student: {student1.is_honor_student()}")

student2.display_info()
print(f"Honor Student: {student2.is_honor_student()}")
```

### Key Advantages of OOP

| Aspect | Functions | OOP |
|--------|-----------|-----|
| **Code Organization** | Scattered | Grouped with related data |
| **Reusability** | Limited | High through inheritance |
| **Maintainability** | Difficult | Easy and organized |
| **Scalability** | Poor | Excellent |
| **Data Protection** | No | Yes (encapsulation) |
| **Real-world Modeling** | Awkward | Natural and intuitive |

---

## 2. Introduction to OOP

### What is Object-Oriented Programming?

OOP is a programming paradigm that organizes software design around objects rather than functions and logic. An **object** is an instance of a **class**, which serves as a blueprint.

### Core Concepts

**Class**: A blueprint or template for creating objects
```python
class Car:
    """A blueprint for car objects"""
    pass
```

**Object/Instance**: A concrete realization of a class
```python
my_car = Car()  # Creating an object/instance from the Car class
```

**Attributes**: Properties or characteristics of an object
```python
class Car:
    def __init__(self, color, brand):
        self.color = color  # Attribute
        self.brand = brand  # Attribute
```

**Methods**: Functions that belong to an object
```python
class Car:
    def __init__(self, color, brand):
        self.color = color
        self.brand = brand
    
    def drive(self):  # Method
        print(f"The {self.color} {self.brand} is driving")
```

### Real-time Example: Bank Account

```python
class BankAccount:
    """Represents a bank account with balance and transactions"""
    
    def __init__(self, account_holder, initial_balance):
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions = []
    
    def deposit(self, amount):
        """Add money to account"""
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposit: +${amount}")
            print(f"Deposited: ${amount}. New balance: ${self.balance}")
        else:
            print("Deposit amount must be positive")
    
    def withdraw(self, amount):
        """Remove money from account"""
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -${amount}")
            print(f"Withdrew: ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid withdrawal amount")
    
    def show_balance(self):
        """Display current balance"""
        print(f"Account holder: {self.account_holder}")
        print(f"Current balance: ${self.balance}")
    
    def show_transactions(self):
        """Display all transactions"""
        print(f"\nTransaction History for {self.account_holder}:")
        for transaction in self.transactions:
            print(f"  - {transaction}")

# Real-time usage
account = BankAccount("John Doe", 1000)
account.deposit(500)
account.withdraw(200)
account.show_balance()
account.show_transactions()

# Output:
# Deposited: $500. New balance: $1500
# Withdrew: $200. New balance: $1300
# Account holder: John Doe
# Current balance: $1300
# 
# Transaction History for John Doe:
#   - Deposit: +$500
#   - Withdrawal: -$200
```

---

## 3. The Four Pillars of OOP

### Pillar 1: Encapsulation

**Definition**: Bundling data (attributes) and methods (functions) into a single unit (class) and hiding internal details from the outside world.

#### Without Encapsulation
```python
# ❌ Bad - Direct access to attributes
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

temp = Temperature(25)
temp.celsius = 9999  # Can set invalid value!
print(temp.celsius)  # 9999 - Problem!
```

#### With Encapsulation (Using Private Attributes)
```python
# ✅ Good - Protected attributes
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius  # Single underscore = protected (convention)
    
    def set_celsius(self, value):
        """Setter with validation"""
        if -273.15 <= value:
            self._celsius = value
        else:
            print("Invalid temperature! Below absolute zero.")
    
    def get_celsius(self):
        """Getter"""
        return self._celsius
    
    def get_fahrenheit(self):
        """Convert to Fahrenheit"""
        return (self._celsius * 9/5) + 32

temp = Temperature(25)
print(f"Celsius: {temp.get_celsius()}")
print(f"Fahrenheit: {temp.get_fahrenheit()}")

temp.set_celsius(30)  # Valid
print(f"Updated Celsius: {temp.get_celsius()}")

temp.set_celsius(9999)  # Invalid - prevented!
# Invalid temperature! Below absolute zero.
```

#### Using Property Decorators (Python's Elegant Approach)
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """Getter using @property decorator"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        """Setter using @celsius.setter decorator"""
        if -273.15 <= value:
            self._celsius = value
        else:
            print("Invalid temperature!")
    
    @property
    def fahrenheit(self):
        """Computed property"""
        return (self._celsius * 9/5) + 32

temp = Temperature(25)
print(temp.celsius)  # 25 - Uses getter
print(temp.fahrenheit)  # 77.0

temp.celsius = 30  # Uses setter
print(temp.celsius)  # 30

temp.celsius = 9999  # Validation applied
# Invalid temperature!
```

### Pillar 2: Inheritance

**Definition**: A mechanism where a class can inherit properties and methods from another class, promoting code reuse.

#### Basic Inheritance
```python
# Parent Class
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        print(f"{self.name} makes a sound")
    
    def info(self):
        print(f"Name: {self.name}, Species: {self.species}")

# Child Class - Inherits from Animal
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")  # Call parent's __init__
        self.breed = breed
    
    def make_sound(self):  # Override parent method
        print(f"{self.name} barks: Woof! Woof!")
    
    def fetch(self):  # New method specific to Dog
        print(f"{self.name} is fetching the ball")

# Child Class - Inherits from Animal
class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color
    
    def make_sound(self):  # Override parent method
        print(f"{self.name} meows: Meow! Meow!")

# Usage
dog = Dog("Buddy", "Golden Retriever")
dog.info()
dog.make_sound()
dog.fetch()

print()

cat = Cat("Whiskers", "Orange")
cat.info()
cat.make_sound()

# Output:
# Name: Buddy, Species: Dog
# Buddy barks: Woof! Woof!
# Buddy is fetching the ball
# 
# Name: Whiskers, Species: Cat
# Whiskers meows: Meow! Meow!
```

#### Real-time Example: Employee Hierarchy
```python
class Employee:
    """Base class for all employees"""
    
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
    
    def display_info(self):
        print(f"Name: {self.name}, ID: {self.employee_id}, Salary: ${self.salary}")
    
    def give_raise(self, amount):
        self.salary += amount
        print(f"New salary: ${self.salary}")

class Manager(Employee):
    """Manager inherits from Employee"""
    
    def __init__(self, name, employee_id, salary, department):
        super().__init__(name, employee_id, salary)
        self.department = department
        self.team = []
    
    def add_team_member(self, employee):
        self.team.append(employee)
        print(f"{employee.name} added to {self.department} team")
    
    def display_info(self):
        super().display_info()  # Call parent method
        print(f"Department: {self.department}")
        print(f"Team size: {len(self.team)}")

class Developer(Employee):
    """Developer inherits from Employee"""
    
    def __init__(self, name, employee_id, salary, language):
        super().__init__(name, employee_id, salary)
        self.language = language
    
    def display_info(self):
        super().display_info()
        print(f"Primary Language: {self.language}")
    
    def code(self):
        print(f"{self.name} is coding in {self.language}")

# Usage
manager = Manager("Sarah", "M001", 80000, "Engineering")
dev1 = Developer("Alex", "D001", 70000, "Python")
dev2 = Developer("Jordan", "D002", 72000, "JavaScript")

manager.add_team_member(dev1)
manager.add_team_member(dev2)

print("\n--- Manager Info ---")
manager.display_info()

print("\n--- Developer 1 Info ---")
dev1.display_info()
dev1.code()

print("\n--- Developer 2 Info ---")
dev2.display_info()
dev2.code()

# Output:
# Alex added to Engineering team
# Jordan added to Engineering team
# 
# --- Manager Info ---
# Name: Sarah, ID: M001, Salary: $80000
# Department: Engineering
# Team size: 2
# 
# --- Developer 1 Info ---
# Name: Alex, ID: D001, Salary: $70000
# Primary Language: Python
# Alex is coding in Python
# 
# --- Developer 2 Info ---
# Name: Jordan, ID: D002, Salary: $72000
# Primary Language: JavaScript
# Jordan is coding in JavaScript
```

### Pillar 3: Polymorphism

**Definition**: The ability of objects to take on multiple forms. Same method name, different behaviors.

#### Method Overriding (Runtime Polymorphism)
```python
class Shape:
    """Base shape class"""
    
    def area(self):
        pass
    
    def perimeter(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14 * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def area(self):
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5
    
    def perimeter(self):
        return self.a + self.b + self.c

# Polymorphism in action
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 4, 5)
]

print("--- Shape Analysis ---")
for shape in shapes:
    print(f"{shape.__class__.__name__}:")
    print(f"  Area: {shape.area():.2f}")
    print(f"  Perimeter: {shape.perimeter():.2f}\n")

# Output:
# --- Shape Analysis ---
# Circle:
#   Area: 78.50
#   Perimeter: 31.40
# 
# Rectangle:
#   Area: 24.00
#   Perimeter: 20.00
# 
# Triangle:
#   Area: 6.00
#   Perimeter: 12.00
```

#### Duck Typing (Python's Dynamic Polymorphism)
```python
# "If it walks like a duck and quacks like a duck, it's a duck"

class Bird:
    def sound(self):
        print("Tweet tweet!")

class Cat:
    def sound(self):
        print("Meow meow!")

class Machine:
    def sound(self):
        print("Beep boop!")

def make_noise(thing):
    """Works with any object that has sound() method"""
    thing.sound()

# All these objects can be used the same way
bird = Bird()
cat = Cat()
machine = Machine()

for animal in [bird, cat, machine]:
    make_noise(animal)

# Output:
# Tweet tweet!
# Meow meow!
# Beep boop!
```

### Pillar 4: Abstraction

**Definition**: Hiding complex implementation details and showing only necessary features to the user.

#### Using Abstract Base Classes
```python
from abc import ABC, abstractmethod

# ABC = Abstract Base Class
class Vehicle(ABC):
    """Abstract class that cannot be instantiated"""
    
    def __init__(self, brand):
        self.brand = brand
    
    @abstractmethod  # Must be implemented by child classes
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    def info(self):  # Concrete method
        print(f"Brand: {self.brand}")

class Car(Vehicle):
    def start(self):
        print("Car engine started with ignition")
    
    def stop(self):
        print("Car engine stopped with brake")

class Motorcycle(Vehicle):
    def start(self):
        print("Motorcycle engine started by kick-start")
    
    def stop(self):
        print("Motorcycle stopped abruptly")

# Cannot create instance of abstract class
# vehicle = Vehicle("Generic")  # ❌ TypeError

# Can create instances of concrete classes
car = Car("Toyota")
car.info()
car.start()
car.stop()

print()

motorcycle = Motorcycle("Harley")
motorcycle.info()
motorcycle.start()
motorcycle.stop()

# Output:
# Brand: Toyota
# Car engine started with ignition
# Car engine stopped with brake
# 
# Brand: Harley
# Motorcycle engine started by kick-start
# Motorcycle stopped abruptly
```

#### Real-world Example: Payment System
```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    """Abstract payment method"""
    
    @abstractmethod
    def validate(self):
        pass
    
    @abstractmethod
    def process_payment(self, amount):
        pass
    
    def print_receipt(self, amount):
        print(f"Receipt: Payment processed for ${amount}")

class CreditCard(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number
    
    def validate(self):
        return len(self.card_number) == 16
    
    def process_payment(self, amount):
        if self.validate():
            print(f"Processing ${amount} via Credit Card {self.card_number[-4:]}")
            self.print_receipt(amount)
        else:
            print("Invalid card!")

class PayPal(PaymentMethod):
    def __init__(self, email):
        self.email = email
    
    def validate(self):
        return "@" in self.email
    
    def process_payment(self, amount):
        if self.validate():
            print(f"Processing ${amount} via PayPal ({self.email})")
            self.print_receipt(amount)
        else:
            print("Invalid email!")

class Bitcoin(PaymentMethod):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def validate(self):
        return len(self.wallet_address) > 20
    
    def process_payment(self, amount):
        if self.validate():
            print(f"Processing {amount} BTC via Blockchain ({self.wallet_address[:10]}...)")
            self.print_receipt(amount)
        else:
            print("Invalid wallet address!")

# Usage
print("=== Credit Card Payment ===")
card = CreditCard("1234567890123456")
card.process_payment(99.99)

print("\n=== PayPal Payment ===")
paypal = PayPal("user@example.com")
paypal.process_payment(49.99)

print("\n=== Bitcoin Payment ===")
bitcoin = Bitcoin("1A1z7agoat2GPFH3tCpxygFBAKD5x1royJ")
bitcoin.process_payment(0.001)
```

---

## 4. Working with Classes and Objects

### Class Structure
```python
class Book:
    """A class representing a book"""
    
    # Class variable (shared across all instances)
    total_books = 0
    
    def __init__(self, title, author, pages):
        """Constructor - called when object is created"""
        # Instance variables (unique to each object)
        self.title = title
        self.author = author
        self.pages = pages
        
        # Increment class variable
        Book.total_books += 1
    
    def __str__(self):
        """String representation when print() is called"""
        return f"'{self.title}' by {self.author}"
    
    def __repr__(self):
        """Official representation for debugging"""
        return f"Book('{self.title}', '{self.author}', {self.pages})"
    
    def read(self, pages_read):
        """Instance method"""
        if pages_read > self.pages:
            print(f"Can't read {pages_read} pages from a {self.pages}-page book!")
        else:
            print(f"Read {pages_read} pages of {self.title}")
    
    @classmethod
    def from_string(cls, book_string):
        """Class method - works with class itself, not instances"""
        title, author, pages = book_string.split(",")
        return cls(title, author, int(pages))
    
    @staticmethod
    def is_valid_pages(pages):
        """Static method - doesn't need instance or class"""
        return isinstance(pages, int) and pages > 0

# Instance creation and usage
book1 = Book("Python 101", "John Doe", 300)
book2 = Book("Advanced Python", "Jane Smith", 500)

print(book1)  # Uses __str__
print(repr(book1))  # Uses __repr__

book1.read(50)
Book.is_valid_pages(300)  # Call static method

print(f"Total books: {Book.total_books}")  # 2

# Using class method
book3 = Book.from_string("Data Science, Alex Brown, 450")
print(book3)
print(f"Total books: {Book.total_books}")  # 3
```

### Types of Methods

```python
class Calculator:
    pi = 3.14159  # Class variable
    
    def __init__(self, name):
        self.name = name  # Instance variable
    
    # Instance Method
    def add(self, a, b):
        """Works with instance data"""
        result = a + b
        print(f"{self.name} computed: {a} + {b} = {result}")
        return result
    
    # Class Method
    @classmethod
    def from_dict(cls, data):
        """Creates instance from dictionary"""
        return cls(data['name'])
    
    # Static Method
    @staticmethod
    def multiply(a, b):
        """Doesn't need instance or class data"""
        return a * b
    
    # Property
    @property
    def circle_area(self):
        """Computed property"""
        radius = 5
        return Calculator.pi * radius ** 2

# Usage
calc = Calculator("MyCalc")
calc.add(10, 20)

calc2 = Calculator.from_dict({'name': 'NewCalc'})
print(f"Multiply: {Calculator.multiply(5, 6)}")
print(f"Circle area: {calc.circle_area}")
```

---

# SESSION 2: Advanced Concepts & Real-world Applications

## 5. Multiple Inheritance

### Multiple Inheritance Basics
```python
class Animal:
    def eat(self):
        print("Animal is eating")

class Flyer:
    def fly(self):
        print("Flying in the sky")

class Swimmer:
    def swim(self):
        print("Swimming in water")

class Duck(Animal, Flyer, Swimmer):
    """Duck inherits from multiple classes"""
    def quack(self):
        print("Quack! Quack!")

duck = Duck()
duck.eat()    # From Animal
duck.fly()    # From Flyer
duck.swim()   # From Swimmer
duck.quack()  # Own method

# Output:
# Animal is eating
# Flying in the sky
# Swimming in water
# Quack! Quack!
```

### MRO (Method Resolution Order)
```python
class A:
    def method(self):
        print("From A")

class B(A):
    def method(self):
        print("From B")

class C(A):
    def method(self):
        print("From C")

class D(B, C):
    pass

obj = D()
obj.method()  # From B

# Check Method Resolution Order
print(D.mro())
# [<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>]

# Output:
# From B
```

---

## 6. Composition vs Inheritance

### When to Use Composition Instead of Inheritance

```python
# ❌ Bad inheritance example
class Car(Engine, Wheel, Seat):  # Weird! Car is not an Engine
    pass

# ✅ Good composition example
class Engine:
    def __init__(self, power):
        self.power = power
    
    def start(self):
        print(f"Engine with {self.power}HP starting")

class Wheel:
    def __init__(self, size):
        self.size = size
    
    def rotate(self):
        print(f"Wheel of {self.size} inches rotating")

class Car:
    """Car HAS-A Engine and Wheels (composition)"""
    
    def __init__(self, brand, engine_power, wheel_size):
        self.brand = brand
        self.engine = Engine(engine_power)  # Composition
        self.wheels = [Wheel(wheel_size) for _ in range(4)]  # Composition
    
    def start(self):
        self.engine.start()
        for wheel in self.wheels:
            wheel.rotate()
    
    def info(self):
        print(f"{self.brand} Car")
        print(f"Engine: {self.engine.power}HP")
        print(f"Wheels: {len(self.wheels)}")

car = Car("Toyota", 200, 18)
car.info()
car.start()

# Output:
# Toyota Car
# Engine: 200HP
# Wheels: 4
# Engine with 200HP starting
# Wheel of 18 inches rotating
# Wheel of 18 inches rotating
# Wheel of 18 inches rotating
# Wheel of 18 inches rotating
```

### Real-time Example: School Management System
```python
class Address:
    def __init__(self, street, city, zip_code):
        self.street = street
        self.city = city
        self.zip_code = zip_code
    
    def __str__(self):
        return f"{self.street}, {self.city} {self.zip_code}"

class Subject:
    def __init__(self, name, code):
        self.name = name
        self.code = code
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Teacher:
    def __init__(self, name, employee_id, specialization):
        self.name = name
        self.employee_id = employee_id
        self.specialization = specialization
    
    def teach(self, subject):
        print(f"{self.name} is teaching {subject}")

class Student:
    def __init__(self, name, student_id, address, teacher, subjects):
        self.name = name
        self.student_id = student_id
        self.address = address  # Composition
        self.teacher = teacher  # Composition
        self.subjects = subjects  # Composition
        self.grades = {}
    
    def add_grade(self, subject, grade):
        self.grades[subject.name] = grade
        print(f"Grade added: {subject.name} - {grade}")
    
    def display_info(self):
        print(f"\n=== Student Information ===")
        print(f"Name: {self.name}")
        print(f"ID: {self.student_id}")
        print(f"Address: {self.address}")
        print(f"Teacher: {self.teacher.name} ({self.teacher.specialization})")
        print(f"Subjects: {', '.join(str(s) for s in self.subjects)}")
        print(f"Grades: {self.grades}")

# Create composed objects
math_teacher = Teacher("Mr. Johnson", "T001", "Mathematics")
address = Address("123 Oak St", "Springfield", "12345")
subjects = [
    Subject("Mathematics", "MATH101"),
    Subject("English", "ENG101"),
    Subject("Science", "SCI101")
]

# Create student with composition
student = Student("Alice", "S001", address, math_teacher, subjects)
student.add_grade(subjects[0], "A")
student.add_grade(subjects[1], "B+")
student.display_info()

# Output:
# Grade added: Mathematics - A
# Grade added: English - B+
# 
# === Student Information ===
# Name: Alice
# ID: S001
# Address: 123 Oak St, Springfield 12345
# Teacher: Mr. Johnson (Mathematics)
# Subjects: Mathematics (MATH101), English (ENG101), Science (SCI101)
# Grades: {'Mathematics': 'A', 'English': 'B+'}
```

---

## 7. Special Methods (Magic Methods / Dunder Methods)

### Object Initialization and Representation

```python
class Person:
    def __init__(self, name, age):
        """Constructor"""
        self.name = name
        self.age = age
        print(f"Person object created: {self.name}")
    
    def __del__(self):
        """Destructor - called when object is deleted"""
        print(f"Person object deleted: {self.name}")
    
    def __str__(self):
        """User-friendly string representation"""
        return f"Person named {self.name}"
    
    def __repr__(self):
        """Developer-friendly representation"""
        return f"Person('{self.name}', {self.age})"
    
    def __len__(self):
        """Allows len() function"""
        return self.age
    
    def __eq__(self, other):
        """Equality comparison"""
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        return False
    
    def __lt__(self, other):
        """Less than comparison"""
        return self.age < other.age
    
    def __gt__(self, other):
        """Greater than comparison"""
        return self.age > other.age
    
    def __hash__(self):
        """Makes object hashable for use in sets/dicts"""
        return hash((self.name, self.age))

# Usage
p1 = Person("Alice", 25)
p2 = Person("Bob", 30)

print(str(p1))  # Uses __str__
print(repr(p1))  # Uses __repr__

print(len(p1))  # Uses __len__ - 25

print(p1 == p2)  # Uses __eq__ - False
print(p1 < p2)   # Uses __lt__ - True
print(p1 > p2)   # Uses __gt__ - False

# Can use in sets
people_set = {p1, p2}
print(f"Unique people: {len(people_set)}")

del p1  # Triggers __del__

# Output:
# Person object created: Alice
# Person object created: Bob
# Person named Alice
# Person(Alice, 25)
# 25
# False
# True
# False
# Unique people: 2
# Person object deleted: Alice
```

### Operator Overloading

```python
class Vector:
    """A 2D vector class"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        """Addition operator"""
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        """Subtraction operator"""
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Multiplication operator"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        """Division operator"""
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector(self.x / scalar, self.y / scalar)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

# Usage
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)      # Vector(4, 6)
print(v1 - v2)      # Vector(2, 2)
print(v1 * 2)       # Vector(6, 8)
print(v1 / 2)       # Vector(1.5, 2.0)

# Output:
# Vector(4, 6)
# Vector(2, 2)
# Vector(6, 8)
# Vector(1.5, 2.0)
```

### Container Magic Methods

```python
class Playlist:
    """A music playlist"""
    
    def __init__(self, name):
        self.name = name
        self.songs = []
    
    def __len__(self):
        """Number of songs in playlist"""
        return len(self.songs)
    
    def __getitem__(self, index):
        """Access song by index"""
        return self.songs[index]
    
    def __setitem__(self, index, song):
        """Set song at index"""
        self.songs[index] = song
    
    def __contains__(self, song):
        """Check if song is in playlist"""
        return song in self.songs
    
    def __iter__(self):
        """Iterate through songs"""
        return iter(self.songs)
    
    def add_song(self, song):
        self.songs.append(song)
    
    def __str__(self):
        return f"Playlist: {self.name} ({len(self)} songs)"

# Usage
playlist = Playlist("My Favorites")
playlist.add_song("Song A")
playlist.add_song("Song B")
playlist.add_song("Song C")

print(len(playlist))  # 3
print(playlist[0])    # Song A
print("Song B" in playlist)  # True

for song in playlist:
    print(f"  - {song}")

print(playlist)

# Output:
# 3
# Song A
# True
#   - Song A
#   - Song B
#   - Song C
# Playlist: My Favorites (3 songs)
```

---

## 8. Decorators and Descriptors

### Function Decorators

```python
def timing_decorator(func):
    """Decorator that measures function execution time"""
    import time
    
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    
    return wrapper

@timing_decorator
def slow_function():
    import time
    time.sleep(1)
    return "Done!"

result = slow_function()
print(result)

# Output:
# slow_function took 1.0005 seconds
# Done!
```

### Class Decorators

```python
def singleton(cls):
    """Decorator to make a class a singleton"""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    def __init__(self):
        self.connected = False
    
    def connect(self):
        self.connected = True
        print("Database connected")

# Only one instance exists
db1 = Database()
db2 = Database()

print(db1 is db2)  # True - Same object!
db1.connect()

# Output:
# True
# Database connected
```

---

## 9. Error Handling with Custom Exceptions

```python
# Define custom exceptions
class InsufficientFundsError(Exception):
    """Raised when account has insufficient funds"""
    pass

class InvalidAmountError(Exception):
    """Raised when amount is invalid"""
    pass

class BankAccount:
    def __init__(self, account_number, balance):
        self.account_number = account_number
        self.balance = balance
    
    def withdraw(self, amount):
        if amount < 0:
            raise InvalidAmountError("Amount cannot be negative")
        
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds! Available: ${self.balance}")
        
        self.balance -= amount
        print(f"Withdrew ${amount}. New balance: ${self.balance}")
    
    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be positive")
        
        self.balance += amount
        print(f"Deposited ${amount}. New balance: ${self.balance}")

# Usage with exception handling
account = BankAccount("123456", 1000)

try:
    account.withdraw(500)
    account.withdraw(600)  # Will raise InsufficientFundsError
except InsufficientFundsError as e:
    print(f"Error: {e}")
except InvalidAmountError as e:
    print(f"Error: {e}")
finally:
    print(f"Final balance: ${account.balance}")

# Output:
# Withdrew $500. New balance: $500
# Error: Insufficient funds! Available: $500
# Final balance: $500
```

---

## 10. Context Managers

```python
class DatabaseConnection:
    """Context manager for database connection"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        """Called when entering 'with' block"""
        print(f"Connecting to {self.db_name}...")
        self.connection = f"Connected to {self.db_name}"
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block"""
        print(f"Closing connection to {self.db_name}...")
        self.connection = None
        
        # Return True to suppress exceptions
        if exc_type:
            print(f"Exception occurred: {exc_type.__name__}: {exc_val}")
        return False

# Usage
with DatabaseConnection("MyDatabase") as conn:
    print(f"Using: {conn}")
    # Do database operations

# Output:
# Connecting to MyDatabase...
# Using: Connected to MyDatabase
# Closing connection to MyDatabase...
```

---

## 11. Metaclasses (Advanced)

```python
class SingletonMeta(type):
    """Metaclass that creates singleton classes"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    """Logger that only has one instance"""
    
    def __init__(self):
        self.logs = []
    
    def log(self, message):
        self.logs.append(message)
        print(f"[LOG] {message}")

# Test singleton
logger1 = Logger()
logger2 = Logger()

print(logger1 is logger2)  # True

logger1.log("Message 1")
logger2.log("Message 2")

print(f"Total logs: {len(logger1.logs)}")

# Output:
# True
# [LOG] Message 1
# [LOG] Message 2
# Total logs: 2
```

---

## 12. Complete Real-World Example: E-Commerce System

```python
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime

class OrderStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class Product:
    """Product in the store"""
    
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock
    
    def is_available(self, quantity):
        return self.stock >= quantity
    
    def reduce_stock(self, quantity):
        if self.is_available(quantity):
            self.stock -= quantity
            return True
        return False
    
    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

class CartItem:
    """Item in shopping cart"""
    
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
    
    def get_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class ShoppingCart:
    """Shopping cart with items"""
    
    def __init__(self):
        self.items = []
    
    def add_item(self, product, quantity):
        if product.is_available(quantity):
            self.items.append(CartItem(product, quantity))
            return True
        return False
    
    def remove_item(self, product_id):
        self.items = [item for item in self.items 
                      if item.product.product_id != product_id]
    
    def get_total(self):
        return sum(item.get_total() for item in self.items)
    
    def clear(self):
        self.items.clear()
    
    def __str__(self):
        return f"Cart with {len(self.items)} items"

class Order:
    """Customer order"""
    
    order_counter = 1000
    
    def __init__(self, customer_name, cart):
        self.order_id = Order.order_counter
        Order.order_counter += 1
        self.customer_name = customer_name
        self.items = cart.items.copy()
        self.total = cart.get_total()
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()
    
    def process_payment(self):
        """Simulate payment processing"""
        self.status = OrderStatus.PROCESSING
        print(f"Processing payment of ${self.total:.2f}")
    
    def ship(self):
        """Ship the order"""
        if self.status == OrderStatus.PROCESSING:
            self.status = OrderStatus.SHIPPED
            print(f"Order {self.order_id} shipped")
            return True
        return False
    
    def deliver(self):
        """Deliver the order"""
        if self.status == OrderStatus.SHIPPED:
            self.status = OrderStatus.DELIVERED
            print(f"Order {self.order_id} delivered to {self.customer_name}")
            return True
        return False
    
    def display_details(self):
        print(f"\n=== Order {self.order_id} ===")
        print(f"Customer: {self.customer_name}")
        print(f"Status: {self.status.value}")
        print(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Items:")
        for item in self.items:
            print(f"  - {item} = ${item.get_total():.2f}")
        print(f"Total: ${self.total:.2f}")

class Store:
    """The e-commerce store"""
    
    def __init__(self, name):
        self.name = name
        self.products = []
        self.orders = []
    
    def add_product(self, product):
        self.products.append(product)
    
    def get_product_by_id(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def create_order(self, customer_name, cart):
        order = Order(customer_name, cart)
        self.orders.append(order)
        
        # Reduce stock
        for item in order.items:
            item.product.reduce_stock(item.quantity)
        
        return order
    
    def display_catalog(self):
        print(f"\n=== {self.name} Catalog ===")
        for product in self.products:
            print(f"{product.product_id}: {product} (Stock: {product.stock})")

# Usage Example
if __name__ == "__main__":
    # Create store
    store = Store("Tech Store")
    
    # Add products
    laptop = Product("P001", "Laptop", 999.99, 10)
    mouse = Product("P002", "Wireless Mouse", 29.99, 50)
    keyboard = Product("P003", "Mechanical Keyboard", 129.99, 20)
    
    store.add_product(laptop)
    store.add_product(mouse)
    store.add_product(keyboard)
    
    store.display_catalog()
    
    # Customer 1: Place order
    print("\n--- Customer 1: Placing Order ---")
    cart1 = ShoppingCart()
    cart1.add_item(laptop, 1)
    cart1.add_item(mouse, 2)
    
    order1 = store.create_order("Alice Johnson", cart1)
    order1.display_details()
    
    order1.process_payment()
    order1.ship()
    order1.deliver()
    
    # Customer 2: Place order
    print("\n--- Customer 2: Placing Order ---")
    cart2 = ShoppingCart()
    cart2.add_item(keyboard, 1)
    cart2.add_item(mouse, 1)
    
    order2 = store.create_order("Bob Smith", cart2)
    order2.display_details()
    
    # Check updated inventory
    print("\n--- Updated Catalog ---")
    store.display_catalog()
    
    # Summary
    print(f"\nTotal Orders: {len(store.orders)}")
    print(f"Total Revenue: ${sum(order.total for order in store.orders):.2f}")
```

---

# MINI PROJECTS

## Project 1: Library Management System

```python
from datetime import datetime, timedelta

class Book:
    def __init__(self, isbn, title, author, genre):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre = genre
        self.is_available = True
        self.borrowed_by = None
        self.due_date = None
    
    def __str__(self):
        status = "Available" if self.is_available else f"Borrowed by {self.borrowed_by}"
        return f"{self.title} by {self.author} ({self.genre}) - {status}"

class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books = []
        self.membership_date = datetime.now()
    
    def __str__(self):
        return f"Member: {self.name} (ID: {self.member_id})"

class Library:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.books = []
        self.members = []
    
    def add_book(self, book):
        self.books.append(book)
        print(f"Added: {book.title}")
    
    def register_member(self, member):
        self.members.append(member)
        print(f"Registered: {member.name}")
    
    def borrow_book(self, member_id, isbn):
        member = self.find_member(member_id)
        book = self.find_book(isbn)
        
        if not member or not book:
            return False
        
        if not book.is_available:
            print(f"'{book.title}' is not available")
            return False
        
        book.is_available = False
        book.borrowed_by = member.name
        book.due_date = datetime.now() + timedelta(days=14)
        member.borrowed_books.append(book)
        
        print(f"{member.name} borrowed '{book.title}' - Due: {book.due_date.date()}")
        return True
    
    def return_book(self, member_id, isbn):
        member = self.find_member(member_id)
        book = self.find_book(isbn)
        
        if not member or not book or book.is_available:
            return False
        
        book.is_available = True
        book.borrowed_by = None
        book.due_date = None
        member.borrowed_books.remove(book)
        
        print(f"{member.name} returned '{book.title}'")
        return True
    
    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def find_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None
    
    def search_by_author(self, author):
        return [book for book in self.books if book.author.lower() == author.lower()]
    
    def search_by_genre(self, genre):
        return [book for book in self.books if book.genre.lower() == genre.lower()]
    
    def display_all_books(self):
        print(f"\n=== {self.name} - All Books ===")
        for book in self.books:
            print(f"  {book}")
    
    def display_available_books(self):
        available = [b for b in self.books if b.is_available]
        print(f"\n=== Available Books ===")
        for book in available:
            print(f"  {book}")

# Demo
if __name__ == "__main__":
    # Create library
    library = Library("City Library", "123 Main St")
    
    # Add books
    library.add_book(Book("978-0-123456-01-5", "Python Basics", "John Smith", "Programming"))
    library.add_book(Book("978-0-123456-02-2", "Advanced Python", "Jane Doe", "Programming"))
    library.add_book(Book("978-0-123456-03-9", "Python for Data Science", "Alex Brown", "Data Science"))
    library.add_book(Book("978-0-123456-04-6", "Fiction Novel", "Bob Wilson", "Fiction"))
    
    # Register members
    library.register_member(Member("M001", "Alice", "alice@email.com"))
    library.register_member(Member("M002", "Charlie", "charlie@email.com"))
    
    # Display books
    library.display_all_books()
    
    # Borrow books
    print("\n=== Borrowing Books ===")
    library.borrow_book("M001", "978-0-123456-01-5")
    library.borrow_book("M001", "978-0-123456-02-2")
    library.borrow_book("M002", "978-0-123456-03-9")
    
    # Display available books
    library.display_available_books()
    
    # Search
    print(f"\n=== Search Results ===")
    print("Books by John Smith:")
    for book in library.search_by_author("John Smith"):
        print(f"  {book}")
    
    # Return book
    print("\n=== Return Books ===")
    library.return_book("M001", "978-0-123456-01-5")
    
    # Display available again
    library.display_available_books()
```

---

## Project 2: Bank Account Management System

```python
from abc import ABC, abstractmethod
from datetime import datetime

class Account(ABC):
    """Abstract base class for bank accounts"""
    
    account_counter = 1000
    
    def __init__(self, owner, initial_balance):
        self.account_number = Account.account_counter
        Account.account_counter += 1
        self.owner = owner
        self.balance = initial_balance
        self.transactions = []
        self.created_date = datetime.now()
        self.add_transaction(f"Account created with ${initial_balance}")
    
    def add_transaction(self, description):
        self.transactions.append({
            'date': datetime.now(),
            'description': description,
            'balance': self.balance
        })
    
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive")
            return False
        
        self.balance += amount
        self.add_transaction(f"Deposit: +${amount:.2f}")
        print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
        return True
    
    @abstractmethod
    def withdraw(self, amount):
        pass
    
    @abstractmethod
    def get_interest(self):
        pass
    
    def display_statement(self):
        print(f"\n=== Account Statement - {self.__class__.__name__} ===")
        print(f"Account Number: {self.account_number}")
        print(f"Owner: {self.owner}")
        print(f"Balance: ${self.balance:.2f}")
        print(f"Created: {self.created_date.strftime('%Y-%m-%d')}")
        print(f"\nTransaction History:")
        for t in self.transactions:
            print(f"  {t['date'].strftime('%Y-%m-%d %H:%M')} - {t['description']} (Balance: ${t['balance']:.2f})")

class SavingsAccount(Account):
    """Savings account with interest"""
    
    def __init__(self, owner, initial_balance, interest_rate=2.5):
        super().__init__(owner, initial_balance)
        self.interest_rate = interest_rate
        self.withdrawal_limit = 3  # Limit withdrawals per month
        self.withdrawals_this_month = 0
    
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive")
            return False
        
        if amount > self.balance:
            print(f"Insufficient funds. Available: ${self.balance:.2f}")
            return False
        
        if self.withdrawals_this_month >= self.withdrawal_limit:
            print(f"Monthly withdrawal limit ({self.withdrawal_limit}) reached")
            return False
        
        self.balance -= amount
        self.withdrawals_this_month += 1
        self.add_transaction(f"Withdrawal: -${amount:.2f}")
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
        return True
    
    def get_interest(self):
        interest = self.balance * (self.interest_rate / 100) / 12
        self.balance += interest
        self.add_transaction(f"Monthly interest: +${interest:.2f}")
        print(f"Interest added: ${interest:.2f}")
        return interest

class CheckingAccount(Account):
    """Checking account with overdraft protection"""
    
    def __init__(self, owner, initial_balance, overdraft_limit=500):
        super().__init__(owner, initial_balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive")
            return False
        
        available = self.balance + self.overdraft_limit
        if amount > available:
            print(f"Insufficient funds. Available: ${available:.2f}")
            return False
        
        self.balance -= amount
        self.add_transaction(f"Withdrawal: -${amount:.2f}")
        print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
        return True
    
    def get_interest(self):
        # Checking accounts typically don't earn interest
        return 0

class Bank:
    """Bank managing multiple accounts"""
    
    def __init__(self, name):
        self.name = name
        self.accounts = []
    
    def create_savings_account(self, owner, initial_balance):
        account = SavingsAccount(owner, initial_balance)
        self.accounts.append(account)
        print(f"Savings account created for {owner}. Account #: {account.account_number}")
        return account
    
    def create_checking_account(self, owner, initial_balance):
        account = CheckingAccount(owner, initial_balance)
        self.accounts.append(account)
        print(f"Checking account created for {owner}. Account #: {account.account_number}")
        return account
    
    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        return None
    
    def display_all_accounts(self):
        print(f"\n=== {self.name} - All Accounts ===")
        for account in self.accounts:
            print(f"{account.account_number} ({account.__class__.__name__}): {account.owner} - ${account.balance:.2f}")

# Demo
if __name__ == "__main__":
    bank = Bank("First National Bank")
    
    # Create accounts
    savings = bank.create_savings_account("Alice", 5000)
    checking = bank.create_checking_account("Bob", 2000)
    
    # Perform transactions
    print("\n=== Transactions ===")
    savings.deposit(1000)
    savings.withdraw(500)
    savings.get_interest()
    
    checking.deposit(500)
    checking.withdraw(1000)
    checking.withdraw(2500)  # Using overdraft
    
    # Display statements
    savings.display_statement()
    checking.display_statement()
    
    # Display all accounts
    bank.display_all_accounts()
```

---

## Project 3: Social Media User System

```python
from datetime import datetime

class Post:
    def __init__(self, author, content):
        self.post_id = id(self)
        self.author = author
        self.content = content
        self.created_at = datetime.now()
        self.likes = 0
        self.comments = []
    
    def add_like(self):
        self.likes += 1
    
    def add_comment(self, user, text):
        self.comments.append({'user': user, 'text': text, 'time': datetime.now()})
    
    def __str__(self):
        return f"{self.author} - {self.content[:50]}... ({self.likes} likes, {len(self.comments)} comments)"

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.posts = []
        self.followers = []
        self.following = []
        self.created_at = datetime.now()
    
    def create_post(self, content):
        post = Post(self.username, content)
        self.posts.append(post)
        print(f"{self.username} posted: {content[:50]}...")
        return post
    
    def like_post(self, post):
        post.add_like()
        print(f"{self.username} liked {post.author}'s post")
    
    def comment_on_post(self, post, comment_text):
        post.add_comment(self.username, comment_text)
        print(f"{self.username} commented on {post.author}'s post")
    
    def follow(self, user):
        if user not in self.following and user != self:
            self.following.append(user)
            user.followers.append(self)
            print(f"{self.username} is now following {user.username}")
    
    def unfollow(self, user):
        if user in self.following:
            self.following.remove(user)
            user.followers.remove(self)
            print(f"{self.username} unfollowed {user.username}")
    
    def get_feed(self):
        """Get posts from users being followed"""
        feed = []
        for followed_user in self.following:
            feed.extend(followed_user.posts)
        return sorted(feed, key=lambda p: p.created_at, reverse=True)
    
    def display_profile(self):
        print(f"\n=== {self.username}'s Profile ===")
        print(f"Email: {self.email}")
        print(f"Joined: {self.created_at.strftime('%Y-%m-%d')}")
        print(f"Posts: {len(self.posts)}")
        print(f"Followers: {len(self.followers)}")
        print(f"Following: {len(self.following)}")
    
    def display_posts(self):
        print(f"\n=== {self.username}'s Posts ===")
        for post in sorted(self.posts, key=lambda p: p.created_at, reverse=True):
            print(f"  [{post.created_at.strftime('%H:%M')}] {post.content[:60]}...")
            print(f"     Likes: {post.likes}, Comments: {len(post.comments)}")

class SocialMedia:
    def __init__(self, name):
        self.name = name
        self.users = []
    
    def register_user(self, username, email):
        user = User(username, email)
        self.users.append(user)
        print(f"User {username} registered on {self.name}")
        return user
    
    def find_user(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def display_trending_posts(self, limit=5):
        all_posts = []
        for user in self.users:
            all_posts.extend(user.posts)
        
        trending = sorted(all_posts, key=lambda p: p.likes, reverse=True)[:limit]
        print(f"\n=== Trending on {self.name} ===")
        for i, post in enumerate(trending, 1):
            print(f"{i}. {post.author}: {post.content[:60]}... ({post.likes} likes)")

# Demo
if __name__ == "__main__":
    platform = SocialMedia("TechHub")
    
    # Register users
    alice = platform.register_user("alice_tech", "alice@email.com")
    bob = platform.register_user("bob_codes", "bob@email.com")
    charlie = platform.register_user("charlie_dev", "charlie@email.com")
    
    # Users follow each other
    print("\n=== Following ===")
    alice.follow(bob)
    alice.follow(charlie)
    bob.follow(charlie)
    
    # Create posts
    print("\n=== Creating Posts ===")
    post1 = alice.create_post("Just started learning Python OOP!")
    post2 = bob.create_post("Built an amazing web app today!")
    post3 = charlie.create_post("Python decorators are powerful!")
    
    # Interact with posts
    print("\n=== Interactions ===")
    bob.like_post(post1)
    charlie.like_post(post1)
    alice.like_post(post2)
    bob.comment_on_post(post3, "Great explanation!")
    alice.comment_on_post(post2, "Looks impressive!")
    
    # Display profiles
    alice.display_profile()
    bob.display_profile()
    
    # Display feeds
    print(f"\n=== {alice.username}'s Feed ===")
    for post in alice.get_feed():
        print(f"  {post.author}: {post.content[:60]}...")
    
    # Trending posts
    platform.display_trending_posts()
```

---

## Summary of Key Concepts

### Session 1
- ✅ Functions vs OOP
- ✅ Classes and Objects
- ✅ Encapsulation
- ✅ Inheritance
- ✅ Polymorphism
- ✅ Abstraction
- ✅ Methods and Attributes

### Session 2
- ✅ Multiple Inheritance
- ✅ Composition vs Inheritance
- ✅ Magic Methods
- ✅ Operator Overloading
- ✅ Decorators
- ✅ Context Managers
- ✅ Error Handling
- ✅ Real-world Applications

### Mini Projects
- ✅ Library Management System
- ✅ Bank Account Management
- ✅ Social Media Platform

---

## Best Practices

1. **Use descriptive names** for classes, methods, and variables
2. **Follow PEP 8** style guide
3. **Use inheritance wisely** - prefer composition when appropriate
4. **Encapsulate data** with properties and private attributes
5. **Document your code** with docstrings
6. **Handle exceptions gracefully** with custom exceptions
7. **Keep classes focused** on a single responsibility
8. **Use type hints** for better code clarity (Python 3.5+)
9. **Test your code** thoroughly
10. **Avoid deep inheritance hierarchies** - keep it simple

---