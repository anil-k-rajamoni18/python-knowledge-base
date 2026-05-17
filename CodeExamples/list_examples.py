# Example 1:
fruits = ["Apple", "banana", "cherry", "date", "elderberry", "apple"]
print(fruits)

# First Element
print("First fruit:", fruits[0])  # Outputs: Apple

# Last Element
print("Last fruit:", fruits[-1])  # Outputs: elderberry

# Unknown Element
# print(fruits[10])  # Raises IndexError: list index out of range

# Mutablity
fruits[1] = "Blueberry"

# Methods 

print("List Methods:", dir([]))  # Lists all available methods for list objects

## 1. append(element): Adds an element to the end of the list
fruits.append("fig")
fruits.append("cherry")

# fruits.append("grape", "honeydew")  # Raises TypeError: append() takes exactly one argument (2 given)

print(fruits)
# 2. extend(iterable): Extends the list by appending elements from an iterable (like another list)
fruits.extend(["grape", "honeydew"])
print(fruits)

# 3. insert(index, element): Inserts an element at a specified index
fruits.insert(1, "dragonfruit")
print(fruits)

# Invalid Positive Index
fruits.insert(20, "kiwi")  # Inserts at the end if index is greater than length
print(fruits)

# Invalid Negative Index
fruits.insert(-20, "lemon")  # Inserts at the start if negative index is less than -length
print(fruits)


# 4. remove(element): Removes the first occurrence of an element
removed_fruit = fruits.remove("date")
print(removed_fruit)  
print(fruits)

# fruits.remove("mango")  # Raises ValueError: list.remove(x): x not in list

# 5. pop(index): Removes and returns the element at the specified index (default is the last element)
popped_fruit = fruits.pop()
print("Popped fruit:", popped_fruit)
print(fruits)

popped_fruit_index = fruits.pop(2)
print("Popped fruit at index 2:", popped_fruit_index)
print(fruits)

# Invalid Index with pop
# fruits.pop(10)  # Raises IndexError: pop index out of range

# 6. index(element): Returns the index of the first occurrence of an element
index_of_fruit = fruits.index("fig")
print("Index of 'fig':", index_of_fruit)

# fruits.index("mango")  # Raises ValueError: 'mango' is not in list

# 7. count(element): Returns the number of occurrences of an element
count_of_fruit = fruits.count("cherry")
print("Count of 'cherry':", count_of_fruit)


count_of_fruit_not_present = fruits.count("mango")
print("Count of 'mango':", count_of_fruit_not_present)  # Outputs: 0

# 8. sort(): Sorts the list in ascending order
fruits.sort() # in place sorting
print("Sorted fruits:", fruits)

# descending order with sort(reverse=True)
fruits.sort(reverse=True)
print("Sorted fruits (descending):", fruits)

# 9. reverse(): Reverses the elements of the list in place
fruits.reverse()
print("Reversed fruits:", fruits)

# 10. copy(): Returns a shallow copy of the list
fruits_copy = fruits.copy()
print("Copied fruits:", fruits_copy)
print(id(fruits), id(fruits_copy))  # Different memory addresses
print(id(fruits[0]), id(fruits_copy[0]))  # Same memory addresses for elements
print("Are fruits and fruits_copy the same object?", fruits is fruits_copy)  # Outputs: False

# 11. clear(): Removes all elements from the list
fruits.clear()
print("Fruits after clear():", fruits)



## When to Use Lists
# - When you need an ordered collection of items
# - When you need to modify the collection (add, remove, change items)  
# - When you need to store duplicate items
# - When you need to access items by their index
# - When you need to perform operations like sorting or reversing the collection
# - When you need to iterate over the collection multiple times

# ## When Not to Use Lists
# - When you need an immutable collection (use tuples instead)
# - When you need to store unique items only (use sets instead)
# - When you need to associate keys with values (use dictionaries instead)
# - When performance is critical and you need faster lookups (consider sets or dictionaries)

## Real-World Examples
# - Storing a list of user names in a web application
# - Keeping track of items in a shopping cart
# - Managing a playlist of songs in a music app
# - Collecting survey responses
# - Storing coordinates of points in a 2D space
# - Maintaining a list of tasks in a to-do application


# Time Complexity & Space Complexity
# Time Complexity:
# - Accessing an element by index: O(1)
# - Appending an element: O(1) on average
# - Removing an element: O(n) in the worst case
# - Inserting an element: O(n) in the worst case

# Space Complexity:
# The space complexity of a list is O(n), where n is the number of elements in the list.