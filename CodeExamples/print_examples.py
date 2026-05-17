print("Hello, World!")  # print(values, ..., sep=' ', end='\n', file=sys.stdout, flush=False)

name = "Alice"
age = 30
print(name)
print(age)

print(name, age)

# Using sep parameter
print("Alice", "Bob", "Charlie", sep="->")

# Using end parameter
print("Hello,", end=" ")
print("World!")

# Using file parameter
with open("output.txt", "w") as f:
    print("This will be written to a file.", file=f)\
    

# Using flush parameter
# Flase by default; when set to True, the output buffer is flushed immediately
import time
print("This is a message.", flush=True) # flushes the output buffer immediately
time.sleep(2) # main program sleeps for 2 seconds
print("This is another message.", flush=True) # flushes the output buffer immediately


# Normal formatting
pi = 3.14159
print("The value of pi is:", pi)
# Using f-strings (Python 3.6+)
print(f"The value of pi is: {pi}")

# Using str.format() method
print("The value of pi is: {}".format(pi))

# Using % operator
print("The value of pi is: %.2f" % pi)  # formats pi