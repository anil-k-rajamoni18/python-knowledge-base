## realtime senario examples of conditional statements in Python

# Example 1: User Authentication
username = input("Enter username: ").strip()  
password = input("Enter password: ").strip()

if username == "admin" and password == "password123":
    print("Access granted.")
else:
    print("Access denied.")


# Example 2: Grading System
score = float(input("Enter your score (0-100): ").strip()) 
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'

print(f"Your grade is: {grade}")

## Example 3: Discount Calculation
purchase_amount = float(input("Enter purchase amount: ").strip())
if purchase_amount > 1000:
    discount = 0.1
elif purchase_amount > 500:
    discount = 0.05
else:
    discount = 0

final_price = purchase_amount - (purchase_amount * discount)
print(f"Final price after discount: {final_price}")


# Example 4: multiple if statements
temperature = float(input("Enter the temperature in Celsius: ").strip())
if temperature > 30:
    print("It's a hot day.")
if temperature < 10:
    print("It's a cold day.")
if 10 <= temperature <= 30:
    print("It's a moderate day.")
else:
    print("Invalid temperature input.")


# Example 5: Nested if statements Casting Vote Eligibility
age = int(input("Enter your age: ").strip())
citizenship = input("Are you a Indian citizen? (yes/no): ").strip().lower()
has_id = input("Do you have a valid ID? (yes/no): ").strip().lower()

if age >= 18:
    if citizenship == "yes":
        if has_id == "yes":
            print("You are eligible to vote.")
        else:
            print("You need a valid ID to vote.")
    else:
        print("Only Indian citizens are eligible to vote.")

else:
    print("You must be at least 18 years old to vote.")


# Example 6: if conditions with bool values and bool function 
is_raining_input = input("Is it raining? (yes/no): ").strip().lower()

is_raining = True if is_raining_input == "yes" else False

if is_raining:
    print("Don't forget your umbrella!")
else:
    print("Enjoy your day!")


# Example 7: Tricky

users = []
if users:
    print("This will not print because an empty list is considered False.")
else:
    print("This will print because the condition is False.")


users = ["Alice", "Bob", "Charlie"]
if users:
    print("User list is not empty.")
else:
    print("User list is empty.")


if 10 + 20:
    print("This will print because 10 + 20 evaluates to 30, which is considered True.")
else:
    print("This will not print.")