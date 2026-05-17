from time import time


class Car:
    wheels = 4  # class attribute
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price


tata = Car("Tata", 500000)
print(tata, id(tata))
print(tata.brand, id(tata.brand))
print(tata.price, id(tata.price))
# print(tata.__dict__) # instance attributes
# print(Car.__dict__) # class attributes

tata2 = Car("Tata", 500000)
print(tata2, id(tata2))
print(tata2.brand, id(tata2.brand))
print(tata2.price, id(tata2.price))

class B:
    def __init__(self):
        print("B init") 

b1 = B()


"""
{
  "status": "OK",
  "code": 200,
  "locale": "en_US",
  "seed": None,
  "total": 1,
  "data": [
    {
      "id": 1,
      "street": "252 Lacy Canyon Apt. 281",
      "streetName": "Obie Mills",
      "buildingNumber": "76619",
      "city": "Port Tyraberg",
      "zipcode": "35239",
      "country": "Seychelles",
      "country_code": "SC",
      "latitude": 87.218288,
      "longitude": -42.630136
    }
  ]
}
"""

class AddressApiResponse:
    def __init__(self, status, code, locale, seed, total, data):
        self.status = status
        self.code = code
        self.locale = locale
        self.seed = seed
        self.total = total
        self.data = data
    class Address:
        def __init__(self, id, street, streetName, buildingNumber, city, zipcode, country, country_code, latitude, longitude):
            self.id = id
            self.street = street
            self.streetName = streetName
            self.buildingNumber = buildingNumber
            self.city = city
            self.zipcode = zipcode
            self.country = country
            self.country_code = country_code
            self.latitude = latitude
            self.longitude = longitude

    def __str__(self):
        return f"Status: {self.status}, Code: {self.code}, Locale: {self.locale}, Seed: {self.seed}, Total: {self.total}, Data: {self.data}"

    def address_list(self):
        return [self.Address(**address) for address in self.data]

api_response = {
  "status": "OK",
  "code": 200,
  "locale": "en_US",
  "seed": None,
  "total": 1,
  "data": [
    {
      "id": 1,
      "street": "252 Lacy Canyon Apt. 281",
      "streetName": "Obie Mills",
      "buildingNumber": "76619",
      "city": "Port Tyraberg",
      "zipcode": "35239",
      "country": "Seychelles",
      "country_code": "SC",
      "latitude": 87.218288,
      "longitude": -42.630136
    }
  ]
}

response = AddressApiResponse(**api_response)
print(response)



class Product:
    def multiply(self, a, b):
        prod = a * b
        return prod
    

    def multiply(self, a, b, c):  
        prod = a * b * c
        return prod


p = Product()
print(p.multiply(2, 3, 4))


####
class Dog:
    def speak(self):
        return "Bark"

class Human:
    def speak(self):
        return "Hello"

def make_sound(entity):
    # This function doesn't care about the type, only the 'speak' method
    print(entity.speak())

make_sound(Dog())  
make_sound(Human()) 




### 
print("********************")
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
p2 = Person("Alice", 25)

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


## 
print('********************')
# def timing_decorator(func):
#     """Decorator that measures function execution time"""
#     import time
    
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         result = func(*args, **kwargs)
#         end = time.time()
#         print(f"{func.__name__} took {end - start:.4f} seconds")
#         return result
    
#     return wrapper

# @timing_decorator
# def slow_function():
#     import time
#     time.sleep(10)
#     return "Done!"


# import sys 
# sys.set_int_max_str_digits(100000)

# @timing_decorator

def factorial(n: int) -> int:
    fact: int = 1
    for i in range(1, n + 1):
        fact *= i
    return fact

# result = slow_function()
# print(result)
start = time.time()
factorial_result = factorial(5000)
end = time.time()
print(f"Factorial of 5000 is: {factorial_result}")
print(f"Factorial calculation took {end - start:.4f} seconds")