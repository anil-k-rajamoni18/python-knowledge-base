# 1. Arithmetic Operators
# results are numerical values
a = 10
b = 3

print("Addition:", a + b)          # Addition
print("Subtraction:", a - b)       # Subtraction
print("Multiplication:", a * b)    # Multiplication
print("Division:", a / b)          # Division
print("Floor Division:", a // b)   # Floor Division
print("Modulus:", a % b)           # Modulus
print("Exponentiation:", a ** b)   # Exponentiation

# Observations on % Operator
print(10 % 3)  # Outputs: 1
print(3 % 10)  # Outputs: 3
print(5 % 5)   # Outputs: 0

# negative numbers with % operator
# formula: a % b = a - (b * floor(dividend / divisor))
# dividend / divisor
# sign of the result is the same as the sign of the divisor (b)

print(-10 % 3)  # Outputs: 2
# Explanation: -10 - (3 * floor(-10 / 3)) = -10 - (3 * -4) = -10 + 12 = 2
print(10 % -3)  # Outputs: -2
print(-10 % -3) # Outputs: -1 

# floor and ceil functions
# floor(x): returns the largest integer less than or equal to x
# ceil(x): returns the smallest integer greater than or equal to x

import math
print("Floor of 10 / 3:", math.floor(10 / 3))   # Outputs: 3
print("Ceil of 10 / 3:", math.ceil(10 / 3))     # Outputs: 4
#########################################################################################

## 2. Comparison Operators
# results are boolean values: True or False
x = 5
y = 10
print("Equal:", x == y)              # Equal
print("Not Equal:", x != y)          # Not Equal
print("Greater:", x > y)            # Greater
print("Less:", x < y)               # Less
print("Greater or Equal:", x >= y)  # Greater or Equal
print("Less or Equal:", x <= y)     # Less or Equal

#########################################################################################

## 3. Logical Operators
# results are boolean values: True or False
p = True
q = False
print("AND:", p and q)              # AND
print("OR:", p or q)                # OR
print("NOT:", not p)                # NOT

username = "admin"
password = "1234"

is_authenticated = (username == "admin") and (password == "1234")
print("Is Authenticated:", is_authenticated)  # Outputs: True

#########################################################################################

## 4. Assignment Operators
# used to assign values to variables
x = 5
y = 10
z = x + y
print("Z:", z)  # Outputs: 15

x += 3  # x = x + 3
print("X after += 3:", x)  # Outputs: 8

y *= 2  # y = y * 2
print("Y after *= 2:", y)  # Outputs: 20

z -= 5  # z = z - 5
print("Z after -= 5:", z)  # Outputs: 10

x //= 2  # x = x // 2
print("X after //= 2:", x)  # Outputs: 4

y %= 6  # y = y % 6
print("Y after %= 6:", y)  # Outputs: 2

## 5. Ternary Operator
# syntax: value_if_true if condition else value_if_false

age = 20
status = "Adult" if age >= 18 else "Minor" 
print("Status:", status)  # Outputs: Adult

#########################################################################################
## 6. Bitwise Operators
# results are numerical values
# Binary, Octal, Hexadecimal representations

# binary => base 2 (0, 1) prefix: 0b or 0B, method: bin()
# octal  => base 8 (0-7) prefix: 0o or 0O   , method: oct()
# hexadecimal => base 16 (0-9, A-F) prefix: 0x or 0X , method: hex()


# operates on binary representations of integers
a = 5      # Binary: 0101
b = 3      # Binary: 0011
print("AND:", a & b)    # Outputs: 1  (Binary: 0001)
print("OR:", a | b)     # Outputs: 7  (Binary: 0111)
print("XOR:", a ^ b)    # Outputs: 6  (Binary: 0110)
print("NOT:", ~a)       # Outputs: -6 (Binary: 1010)
print("Left Shift:", a << 1)  # Outputs: 10 (Binary: 1010)
print("Right Shift:", a >> 1) # Outputs: 2  (Binary: 0010)

#########################################################################################
## 7. Membership Operators
# results are boolean values: True or False
fruits = ["apple", "banana", "cherry"]
print("Is 'banana' in fruits?", "banana" in fruits)  # Outputs: True
print("Is 'grape' in fruits?", "grape" in fruits)    # Outputs: False

print("Is 'grape' not in fruits?", "grape" not in fruits)  # Outputs: True
print("Is 'apple' not in fruits?", "apple" not in fruits)  # Outputs: False

#########################################################################################
## 8. Identity Operators 
# compare memory locations of two objects
# results are boolean values: True or False
x = ["apple", "banana", "cherry"]
y = ["apple", "banana", "cherry"]
z = x

print("Is x is y?", x is y)      # Outputs: False
print("Is x is z?", x is z)      # Outputs: True
print("Is x is not y?", x is not y)  # Outputs: True
print("Is x is not z?", x is not z)  # Outputs: False

#########################################################################################
## 9. Operator Precedence  and Associativity
# Precedence determines the order of operations

result = 10 + 3 * 2  # Multiplication has higher precedence than addition
print("Result of 10 + 3 * 2:", result)  # Outputs: 16

## Using parentheses to change precedence
result = (10 + 3) * 2  # Parentheses change the order of operations
print("Result of (10 + 3) * 2:", result)  # Outputs: 26

## Using logical operators with precedence
a = True
b = False
c = True

result = a or b and c  # AND has higher precedence than OR
print("Result of a or b and c:", result)  # Outputs: True

result = (a or b) and c  # Parentheses change the order of operations
print("Result of (a or b) and c:", result)  # Outputs: True