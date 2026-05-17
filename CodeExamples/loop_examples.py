## FOR Loops 

# Example 1: Looping through a iterable
'''
for item in iterable:
    # do something with item

iterable: a collection of items (like a list, tuple, string, etc.)
'''

# with a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# with a string
for char in "hello":
    print(char)

# with a tuple
numbers = (1, 2, 3, 4, 5)
for number in numbers:
    print(number)

# with a set
colors = {"red", "green", "blue"}
for color in colors:
    print(color)

# with a dictionary
person = {"name": "Alice", "age": 30, "city": "New York"}
for key in person:
    print(key, ":", person[key])

# Example 2: Looping with range()
'''
for i in range(start, stop, step):
    # do something with i

start: starting value (inclusive)
stop: ending value (exclusive)
step: increment (default is 1) 
'''

for i in range(1, 11, 2):  # odd numbers from 1 to 10
    print(i)

# Example 3: Reverse Looping with range()
for i in range(10, 0, -1):  # countdown from 10 to 1
    print(i)

for i in range(10, 0, 2):  
    print(i)


# Example 4: process api response 
import requests

api_url = "https://jsonplaceholder.typicode.com/posts"
try:
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an error for bad responses
    posts = response.json()

    for post in posts:
        print(f"Post ID: {post['id']}, Title: {post['title']}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


# Example 5: Nested FOR Loops
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
for row in matrix:
    for col in row:
        print(col)

# with range()
for i in range(3):
    for j in range(3):
        print(f"Element at ({i}, {j}): {matrix[i][j]}")


## WHILE Loops
# Example 1: Basic WHILE Loop
'''
while condition:
    # do something
'''

count = 0
while count < 5:
    print(count)
    count += 1

# Break: Stop the loop completely
count = 0
while True:
    if count >= 5:
        break
    print(count)
    count += 1

# Continue: Skip to the next iteration
count = 0
while count < 5:
    count += 1
    if count == 3:
        continue
    print(count)


# pass: Placeholder for future code
for i in range(5):
    pass  # TODO: implement this later


# For Loop with else: Executes when loop completes normally
for i in range(5):
    print(i)
else:
    print("Loop completed normally.")


for i in range(5):
    if i == 3:
        break
    print(i)
else:
    print("This will not print because the loop was broken.")


for i in range(5):
    if i == 2:
        continue
    print(i)
else:
    print("Loop completed normally with continue.")


# While Loop with else: Executes when loop completes normally
count = 0
while count < 5:
    print(count)
    count += 1
else:
    print("While loop completed normally.")


count = 0
while count < 5:
    if count == 3:
        break
    print(count)
    count += 1  
else:
    print("This will not print because the loop was broken.")


## List Comprehensions with Loops
# Example 1: Basic List Comprehension
squares = [x**2 for x in range(10)]
print(squares)

# Example 2: List Comprehension with Condition
evens = [x for x in range(10) if x % 2 == 0]
print(evens)

# Example 3: Nested List Comprehension
matrix = [[j for j in range(5)] for i in range(3)]
print(matrix)

## Dictionary Comprehensions with Loops
# Example 1: Basic Dictionary Comprehension
squared_dict = {x: x**2 for x in range(5)}
print(squared_dict)

# Example 2: Dictionary Comprehension with Condition
even_squared_dict = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squared_dict)

# Example 3: Nested Dictionary Comprehension
matrix_dict = {i: {j: i*j for j in range(3)} for i in range(3)}
print(matrix_dict)