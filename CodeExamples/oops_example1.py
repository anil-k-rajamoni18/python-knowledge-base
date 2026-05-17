class Car:
    """A blueprint for car objects"""
    pass

tataev = Car()

tataev.engineType = "1.2L"
tataev.model = "x1"
tataev.price="790000"

print(tataev.__dict__)  

##
class Parent:
    data = 1029
    def __init__(self):
        print("Parent __init__")
        self.name = "Surya"
    
    def display_name(self):
        print(f"Name: {self.name}")


class Child(Parent):
    def __init__(self):
        super().__init__()
        print("Child __init__")
        self.age = 20
    
    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")

ch = Child()
print(ch.__dict__)
print(ch.display_info())

### 
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


####
class Animal:
    def eat(self):
        print("Animal is eating")

class Flyer:
    def fly(self):
        print("Flying in the sky")
    
    def eat(self):
        print("Flyer is eating")

class Swimmer:
    def swim(self):
        print("Swimming in water")

class Duck(Flyer, Animal, Swimmer):
    """Duck inherits from multiple classes"""
    def quack(self):
        print("Quack! Quack!")

duck = Duck()
duck.eat()    # From Animal
duck.fly()    # From Flyer
duck.swim()   # From Swimmer
duck.quack()  # Own method
