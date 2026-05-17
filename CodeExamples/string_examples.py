"""
string: collection of characters
characters: letters, numbers, symbols, spaces
example: "Hello, World!", 'Python3.8'

Creating Strings:
- Using single quotes: 'Hello'
- Using double quotes: "Hello"
- Using triple quotes for multi-line strings: '''Hello'''
"""

# Why 3 types of quotes?
single_quote_str = 'Hello, World!'
double_quote_str = "Hello, World!"
triple_quote_str = '''Hello, World!'''

print(single_quote_str)
print(double_quote_str)
print(triple_quote_str)

example_str = "It's a beautiful day!"

## How Strings store data?
# Strings are immutable (cannot be changed after creation)
immutable_str = "Hello"
# immutable_str[0] = 'h'  # This will raise an error

## String Operations
# Concatenation
str1 = "Hello, "
str2 = "World!"
result = str1 + str2
print("Concatenation:", result)

# Repetition
repeated_str = "Ha" * 3
print("Repetition:", repeated_str)

# Indexing
sample_str = "Python"
print("First character:", sample_str[0])
print("Last character:", sample_str[-1])

# Slicing
# [start:end:step] 
# default start is 0, default end is length of string, default step is 1
# end index is exclusive
print("Substring (0-2):", sample_str[0:3])  # 'Pyt'
print("Substring (2-end):", sample_str[2:])   # 'thon'
print("Substring (start-3):", sample_str[:4])  # 'Pyth'
print("Every second character:", sample_str[::2])  # 'Pto'

# String Methods
original_str = "  Hello, World!  "
print("Original String:", repr(original_str))
print("Lowercase:", original_str.lower())
print("Uppercase:", original_str.upper())
print("Stripped:", original_str.strip())
print("Replaced:", original_str.replace("World", "Python"))
print("Split:", original_str.split(","))
print("Length:", len(original_str))
print("Find 'World':", original_str.find("World"))
print("Count 'l':", original_str.count("l"))
print("Starts with '  He':", original_str.startswith("  He"))
print("Ends with '!  ':", original_str.endswith("!  "))
print("Is alphanumeric:", original_str.isalnum())
print("Is alphabetic:", original_str.isalpha())
print("Is digit:", original_str.isdigit())

# Formatted Strings
name = "Alice"
age = 30

# Using f-strings (Python 3.6+)
formatted_str_f = f"My name is {name} and I am {age} years old."
print("Formatted String (f-string):", formatted_str_f)

# Using str.format() method
formatted_str_format = "My name is {} and I am {} years old.".format(name, age)
print("Formatted String (str.format):", formatted_str_format)

# Using % operator
formatted_str_percent = "My name is %s and I am %d years old." % (name, age)
print("Formatted String (% operator):", formatted_str_percent)