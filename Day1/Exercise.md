# 🧪 DAY-1 — Hands-On Exercise Questions (With Real-World Context)

**Total: 40 exercises**  
✔ Beginner – 15 | ✔ Intermediate – 15 | ✔ Advanced – 10

---

## BEGINNER EXERCISES (FOUNDATIONAL)

### 1. Installation & Environment

1. Print the installed Python version using terminal.
2. Open a Python file in VS Code and run `"Hello Python"`.
3. Create a virtual environment and activate it.

### 2. Variables, Data Types, Input/Output

1. Create variables using all basic types (int, float, str, bool, None).
2. Create a variable `temperature` and print:
   - current temperature
   - temperature type (`type()` function)
3. Write a script that takes name and age from input and prints: `Hello John, you are 20 years old.`
4. Write a script that asks for two numbers and prints the sum.
5. Store your city name in a variable and print it in uppercase.
6. Convert a string number `"45"` to an integer and multiply by 2.
7. Ask user for years of experience and print: `"Junior" if <2 years else "Senior"`.

### 3. Operators

1. Calculate the area of a circle (radius from user).
2. Convert Celsius to Fahrenheit using formula.
3. Print remainder when a user enters a number divided by 7.
4. Ask user for age and check if they are eligible to vote (>18).
5. Evaluate and print result of: `3 + 4 * 2 - 5 / 2`.

### 4. Strings

1. Ask for a name and print the first & last character.
2. Slice a string `"PYTHONPROGRAMMING"` to print `"PROGRAM"`.
3. Ask for a sentence and print number of characters.
4. Replace all spaces in a sentence with hyphens.
5. Ask for a filename (e.g., `"data.csv"`) → print the extension.

---

## INTERMEDIATE EXERCISES (INDUSTRY LEVEL)

### Variables, I/O, Expressions

1. Build a script that asks:
   - name
   - department
   - employee id  
   And prints formatted ID card-style output.
2. Accept 3 numbers and print the largest (without using max()).
3. Create 3 variables and swap their values (a→b, b→c, c→a).
4. Create a BMI calculator: BMI = weight / (height * height).
5. Given an amount & tax rate, calculate final bill.

### Strings

1. Check if a user's email contains `"@"` and `"."`.
2. Ask for a full name and generate initials (e.g., `"John A Doe"` → `"J.A.D."`).
3. Turn `"hello world"` into `"Hello World"` without using `.title()`.
4. Reverse a string using slicing.
5. Extract domain from email (`"user@gmail.com"` → `"gmail.com"`).

### Operators (Real Use Cases)

1. Create a simple salary increment calculator:
   - Ask for salary
   - Ask for increment %
   - Print updated salary
2. Ask a user for test scores (3 numbers) and print average.
3. Given distance (km) & fuel consumption, print mileage.
4. Evaluate: `(a**2 + b**2) / (a+b)` using user inputs.
5. Build a script that calculates monthly loan EMI (simple formula).

---

## ADVANCED EXERCISES (LOGIC-DRIVEN)

### Deep Input/Output + Expressions

1. Create a script that takes a date in format `"DD-MM-YYYY"` and prints:
   - Day
   - Month
   - Year  
   using slicing.

### String Manipulation Challenges

1. Ask user for a paragraph and output:
   - total words
   - total characters
   - longest word  
   *(Real use case: log analysis, NLP pre-processing)*

2. Ask user for a phone number and validate:
   - exactly 10 digits
   - only numeric

### Applied Operator Logic

1. Create an electricity bill calculator:
   ```
   0-100 units → ₹5/unit  
   101-200 units → ₹7/unit  
   200+ units → ₹10/unit  
   ```

2. Build a simple authentication simulation:
   - Ask for username + password
   - Check against stored values
   - Print success/failure  
   *(Real-world: Login flow basics)*