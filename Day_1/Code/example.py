## input() 
'''
input() is a built-in function in Python that allows you to take input from the user. When you call input(), the program will pause and wait for the user to enter some data. 
Once the user presses Enter, the input() function will return the entered data as a string.
when there is type conversion failure, it will raise a ValueError. For example, if you try to convert a non-numeric string to an integer using int(), it will raise a ValueError.
'''
name = input("Enter your name: ")
print(f"Hello, {name}!")

# for reading other data types, we can use type conversion functions like int(), float(), etc.
name = input("Enter your name: ")
age = int(input("Enter your age: "))
salary = float(input("Enter your salary: "))
is_employed = bool(input("Are you employed? (True/False): "))


## print()
'''
print() is a built-in function in Python that allows you to output text to the console. 
It can take multiple arguments, which will be printed with a space in between by default.
'''

# syntax: print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

## sep = This will change the default separator between values from a space to a hyphen.
print("Hello", "World", sep="-")

## end = This will change the default end character from a newline to a space, so the next print statement will continue on the same line.
print("Hi", end = " ")
print("Welcome to Python")

## file - This will create a file named output.txt and write the string to it. If the file already exists, it will append the string to the end of the file instead of overwriting it.
print("Hello Hi Welcome to Python Learning", file = open("output.txt", mode='a'))
