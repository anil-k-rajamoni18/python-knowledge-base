# Tuple Basic Syntax
my_tuple = (1, 2, 3, "hello", 4.5)
print("Tuple:", my_tuple)

# Accessing Elements
print("First element:", my_tuple[0])
print("Last element:", my_tuple[-1])

# Slicing
print("Slice (1, 3):", my_tuple[1:4])

# Tuple Methods
print("Tuple Methods:", dir(my_tuple))

# 1. count(element): Returns the number of occurrences of an element in the tuple
count_of_element = my_tuple.count(2)
print("Count of 2:", count_of_element)


# 2. index(element): Returns the index of the first occurrence of an element
index_of_element = my_tuple.index("hello")
print("Index of 'hello':", index_of_element)

# unknown_element = my_tuple.index("world")  # Raises ValueError: tuple.index(x): x not in tuple
# print("Index of 'world':", unknown_element)

# Immutability Demonstration
# my_tuple[0] = 10  # Raises TypeError: 'tuple' object does not support item assignment

# Tuple Packing and Unpacking
packed_tuple = 1, 2, 3
print("Packed Tuple:", packed_tuple)

a, b, c = packed_tuple
print("Unpacked Values:", a, b, c)

# Nested Tuples
nested_tuple = (1, [2,3], (4, (5, 6)))
print("Nested Tuple:", nested_tuple)

nested_tuple[1][0] = 10  # Modifying mutable element inside tuple
print("Modified Nested Tuple:", nested_tuple)

# When to Use Tuples
# Use tuples when you need an immutable sequence of elements
# Use tuples as keys in dictionaries (if they contain only immutable elements)
# Use tuples to group related data together that should not change

# When not to Use Tuples
# Avoid using tuples when you need a mutable sequence of elements
# Avoid using tuples when you need to frequently add or remove elements

# Real-World Example
# Storing coordinates (latitude, longitude)
coordinates = (37.7749, -122.4194)

# Storing RGB color values
color = (255, 0, 0)  # Red color

# Storing fixed configuration settings
config = ("localhost", 8080, True)  # (host, port, debug_mode)

# Storing multiple return values from a function
def get_user_info():
    return ("Alice", 30, "New York")



# Time Complexity & Space Complexity
# Time Complexity:
# Accessing an element: O(1)
# Slicing: O(k) where k is the number of elements in the slice

# Space Complexity:
# The space complexity of a tuple is O(n), where n is the number of elements in the tuple.



# Named Tuple 
# Named tuples are a subclass of tuples that allow you to access elements by name instead of index. 
# They are defined using the namedtuple factory function from the collections module.

from collections import namedtuple

# Define a named tuple for a Point in 2D space
Point = namedtuple('Point', ['x', 'y']) # namedtuple(typename, field_names)

# Create an instance of the Point named tuple
p = Point(10, 20)

# Accessing elements by name
print("X coordinate:", p.x)
print("Y coordinate:", p.y)


Student = namedtuple('Student', ['name', 'age', 'grade'])
student1 = Student("Alice", 20, "A")

# Accessing elements by name
print("Student Name:", student1.name)
print("Student Age:", student1.age)
print("Student Grade:", student1.grade)
