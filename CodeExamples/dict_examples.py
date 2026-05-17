# Example-1

user = {
    "name": "Alice", 
    "age": 30, 
    "city": "New York", 
    "name": "Bob"
}

print(user)

# len() 
print("Number of key-value pairs:", len(user))  # Outputs: 3

# Mutability
user["age"] = 31 # Modifying an existing value
user["email"] = "alice@example.com" # Adding a new key-value pair
print(user)

# Keys must be immutable
# invalid_dict = {
#     [1, 2, 3]: "This will cause an error"  # List as a key (not allowed)
# }
# print(invalid_dict)

valid_dict = {
    (1, 2, 3): "This is allowed"  # Tuple as a key (allowed)
}
print(valid_dict)


# Methods
employee = {
    "name": "Charlie",
    "position": "Developer",
    "salary": 70000, 
    "department": "IT",
    "address": {
        "street": "123 Main St",
        "city": "San Francisco",
        "zip": "94105"
    },
    "skills": ["Python", "JavaScript"]
}

# 1. get(): Retrieve value for a given key
print("Employee Name:", employee.get("name"))
print("Employee Age:", employee.get("age", "Keys doesn't exist"))  # Default value if key doesn't exist

# 2. keys(): Get all keys in the dictionary
print("Employee Keys:", employee.keys()) # [keys...]

# 3. values(): Get all values in the dictionary
print("Employee Values:", employee.values()) # [values...]

# 4. items(): Get all key-value pairs in the dictionary
print("Employee Items:", employee.items()) # [(key, value), ...]

# 5. pop(): Remove a key-value pair and return the value
popped_data = employee.pop("salary") # Removes and returns the value for the specified key
print("Removed data:", popped_data)

print("Employee after pop:", employee)

# 6. popitem(): Remove and return the last inserted key-value pair
last_item = employee.popitem()
print("Last inserted item removed:", last_item)
print("Employee after popitem:", employee)

# 7. update(): Update the dictionary with key-value pairs from another dictionary
employee.update({"position": "Senior Developer", "salary": 90000})
print("Employee after update:", employee)


# 8. copy(): Create a shallow copy of the dictionary
employee_copy = employee.copy()
print("Employee Copy:", employee_copy)
print("Is employee and employee_copy the same object?", employee is employee_copy)  # Outputs: False

# 9. fromkeys(): Create a new dictionary with specified keys and a default value
keys = ["id", "name", "role"]
new_dict = dict.fromkeys(keys, "Unknown")
print("New Dictionary from keys:", new_dict)  # Outputs: {'id': 'Unknown', 'name': 'Unknown', 'role': 'Unknown'}

# 10. setdefault(): Get the value of a key, and if it doesn't exist, set it to a default value
role = employee.setdefault("role", "Engineer")
print("Employee Role:", role)
print("Employee after setdefault:", employee)

# 11. clear(): Remove all items from the dictionary
employee.clear()
print("Employee after clear:", employee)  # Outputs: {}

# Nested Dictionaries
company = {
    "departments": {
        "IT": {
            "employees": 50,
            "budget": 1000000
        },
        "HR": {
            "employees": 10,
            "budget": 200000
        }
    },
    "location": "New York"
}

print(company["departments"]["HR"]["budget"])  # Outputs: 200000

# get(key, default)  vs dict[key]
# if key exists in the dictionary
print(company.get("departments").get("HR").get("budget", 0))  # Outputs: 200000
print(company["departments"]["HR"]["budget"])  # Outputs: 200000

# Unknown key
# print(company["departments"]["HR"]["revenue"])  # Outputs: KeyError

# When to use Dictionaries
# 1. When you need to associate values with unique keys.
# 2. When you need fast lookups, insertions, and deletions based on keys.
# 3. When you need to represent structured data, such as records or objects.
# 4. When you need to group related data together.
# 5. When you need to implement mappings, such as a phone book or a configuration settings.

# When not to use Dictionaries
# 1. When order matters and you need to maintain the order of elements (consider using lists or OrderedDict).
# 2. When you need to store duplicate keys (consider using lists or sets).
# 3. When you need to perform mathematical operations on the data (consider using lists, tuples, or NumPy arrays).
# 4. When memory usage is a concern and you need a more compact data structure (consider using lists or arrays).

# Time Complexity of Dictionary Operations
# 1. Accessing an element by key: O(1) on average
# 2. Inserting or updating an element: O(1) on average
# 3. Deleting an element: O(1) on average
# 4. Checking if a key exists: O(1) on average
# 5. Iterating over all keys or values: O(n), where n is the number of items in the dictionary
# 6. Copying a dictionary: O(n), where n is the number of items in the dictionary

# Note: In the worst-case scenario, some operations may degrade to O(n) due to hash collisions, but this is rare with a good hash function and proper resizing of the hash table.

# Space Complexity
# 1. The space complexity of a dictionary is O(n), where n is the number of key-value pairs stored in the dictionary. This is because each key-value pair requires additional memory to store both the key and the value.
# 2. Additionally, dictionaries may use extra space for internal data structures, such as hash tables and linked lists, to handle collisions and maintain performance.



## Defaultdict Example

from collections import defaultdict

# Create a defaultdict with a default value of 0
word_count = defaultdict(int)
normal_dict_word_count = {}
# Count the frequency of words in a list
words = ["apple", "banana", "apple", "orange", "banana", "apple"]

# using normal dict
for word in words:
    if word in normal_dict_word_count:
        normal_dict_word_count[word] += 1
    else:
        normal_dict_word_count[word] = 1

for word in words:
    word_count[word] += 1

print("Word Count:", dict(word_count))
print("Unknown key access in defaultdict:", word_count["grape"])  # Outputs: 0 (default value)
print("Normal Dict Word Count:", normal_dict_word_count)