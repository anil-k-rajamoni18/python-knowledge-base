# Example - 1
fruits = {"apple", "banana", "cherry", "apple", "date", "cherry"}
print(fruits)
print("Number of unique fruits:", len(fruits))

# Example - 2
numbers = {1, 2, 3, 4, 5, 2, 3, 4}
print(numbers)
print("Number of unique numbers:", len(numbers))

# Example - 3: Find the duplicates in a list using set
nums = [1, 2, 3, 4, 5, 2, 3, 4]
unique_nums = set()
duplicates = set()
for num in nums:
    if num in unique_nums:
        duplicates.add(num)
    unique_nums.add(num)
print("Duplicate numbers found:", duplicates)

# Example - 4: Find unique characters in a string using set
text = "hello world bye"
unique_chars = set(text)
print("Unique characters found:", unique_chars)

# Set Methods Examples

# 1. add(obj)
fruits = {"apple", "banana", "cherry"}
fruits.add("date")
fruits.add("apple")  # Adding a duplicate element
print("After adding an element:", fruits)

# 2. remove(obj)
fruits.remove("banana")
print("After removing an element:", fruits)

# remove() will raise a KeyError if the element is not found
# fruits.remove("kiwi")  # Uncommenting this line will raise an error

# 3. discard(obj)
fruits.discard("cherry")
print("After discarding an element:", fruits)

# discard() will not raise an error if the element is not found
fruits.discard("kiwi")  # No error raised


# 4. pop() : Removes and returns an arbitrary element from the set
popped_element = fruits.pop()
print("Popped element:", popped_element)
print("After popping an element:", fruits)

# 5. clear() : Removes all elements from the set
fruits.clear()
print("After clearing the set:", fruits)

# 6. union(set) : Returns a new set with elements from both sets
fruits = {"apple", "banana", "cherry"}
citrus = {"orange", "lemon"}
all_fruits = fruits.union(citrus) # | alternative: all_fruits = fruits | citrus
print("All fruits:", all_fruits)


# 7. intersection(set) : Returns a new set with elements common to both sets
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}
common_elements = set1.intersection(set2) # & alternative: common_elements = set1 & set2
print("Common elements found:", common_elements)

# 8. difference(set) : Returns a new set with elements in the first set but not in the second
unique_to_set1 = set1.difference(set2) # - alternative: unique_to_set1 = set1 - set2
print("Elements unique to set1:", unique_to_set1)


# 9. symmetric_difference(set) : Returns a new set with elements in either set but not in both
sym_diff = set1.symmetric_difference(set2) # ^ alternative: sym_diff = set1 ^ set2
print("Symmetric difference between set1 and set2:", sym_diff)

# 10. issubset(set) : Returns True if the set is a subset of another set
subset = {1, 2}
is_subset = subset.issubset(set1) # alternative: is_subset = subset <= set1
print("Is subset a subset of set1?", is_subset)


# 11. issuperset(set) : Returns True if the set is a superset of another set
is_superset = set1.issuperset(subset) # alternative: is_superset = set1 >= subset
print("Is set1 a superset of subset?", is_superset)

# 12. copy() : Returns a shallow copy of the set
set_copy = set1.copy()
print("Copy of set1:", set_copy)

# 13. disjoint(set) : Returns True if two sets have no elements in common
set3 = {7, 8, 9}
is_disjoint = set1.isdisjoint(set3) # alternative: is_disjoint = not set1 & set3
print("Is set1 disjoint with set3?", is_disjoint)

# 14. update(set) : Updates the set with elements from another set
set1.update(set2)
print("After updating set1 with set2:", set1)


# Explore 
# intersection_update(), difference_update(), symmetric_difference_update()


# When to Use Sets
# Use sets when you need to store unique items and perform operations like union, intersection, and difference efficiently.
# Sets are particularly useful for membership testing and eliminating duplicates from a collection.
# Sets are unordered, so they do not maintain the order of elements.
# Sets can only contain immutable (hashable) types, such as numbers, strings, and tuples.
# Sets are not indexed, so you cannot access elements by position.
# Sets are mutable, meaning you can add or remove elements after creation.

# When Not to Use Sets
# Avoid using sets when you need to maintain the order of elements, as sets are unordered collections.
# If you need to access elements by index or position, consider using lists or tuples instead.
# If you need to store duplicate items, sets are not suitable since they only store unique elements.  


# Time Complexity & Space Complexity
# Time Complexity:
# Adding an element: O(1) on average
# Removing an element: O(1) on average

# Membership testing: O(1) on average
# Set operations (union, intersection, difference): O(min(len(s), len(t))) where s and t are the sets involved

# Space Complexity:
# The space complexity of a set is O(n), where n is the number of elements in the set.