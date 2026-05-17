
# 🧠 DAY 2 — Control Flow & Loops


## ✅ TOPIC 1 — if / elif / else (Decision Making)

### 🔍 What Are Conditionals?

Conditionals allow programs to "make decisions" based on conditions.

**🧠 Real-world analogy:**

When a user tries to log in:
- **IF** password is correct → login
- **ELSE** → show error

### 🏭 Real-World Uses

| Industry | Use Case |
|----------|----------|
| Banking | Validate transaction amount |
| E-commerce | Check stock before order |
| AI systems | Threshold decisions (probability scores) |
| Security | Permission checks |

### 🧱 Basic Structure

```python
if condition:
    # code
elif another_condition:
    # code
else:
    # fallback code
```

### 🧪 Example: Simple Authentication

```python
username = "admin"
password = "1234"

if password == "1234":
    print("Login Successful")
else:
    print("Invalid credentials")
```

### 💡 Important Concepts

✔ **Conditions must be True or False**

Python automatically evaluates expressions:
```python
if age >= 18:
```

✔ **Only first matching block runs**  
✔ **Use elif instead of multiple ifs**  
✔ **Avoid deeply nested code** (bad readability)

### 🏭 Industry Example — Fraud Detection Threshold

```python
score = 0.82

if score > 0.95:
    print("High fraud risk")
elif score > 0.75:
    print("Medium risk - manual review required")
else:
    print("Low risk")
```

### ⭐ Best Practices

- Keep conditions simple
- Use descriptive variable names
- Avoid multiple nested ifs → refactor using elif
- Compare values on left (preferred):
  ```python
  if user_score >= 80:
  ```

---

## ✅ TOPIC 2 — for / while Loops (Iteration Mechanisms)

Loops help execute code repeatedly.

### 🔁 FOR LOOP

Used when number of iterations is known.

**Structure:**
```python
for item in iterable:
```

**Iterable examples:**
- List
- String
- Range
- Tuple
- File

#### Example 1 — Loop through list

```python
for user in ["john", "sam", "alex"]:
    print(user)
```

#### Example 2 — Loop through range

```python
for i in range(1, 6):
    print(i)
```

### 🏭 Industry Example — Processing API responses

```python
for item in api_response["items"]:
    print(item["title"])
```

### 🔄 WHILE LOOP

Used when number of iterations is unknown.

**Structure:**
```python
while condition:
    # run
```

#### Example — Countdown

```python
count = 5

while count > 0:
    print(count)
    count -= 1
```

#### ⚠ Beware of infinite loops

```python
while True:
    print("runs forever")
```

### 🏭 Industry Example — Retrying Failed API Calls

```python
retries = 0

while retries < 3:
    print("Trying again...")
    retries += 1
```

### ⭐ Best Practices

- Use `for` when count is known
- Use `while` when waiting for condition
- Always ensure while loops have exit condition

---

## ✅ TOPIC 3 — break / continue / pass

These control loop behavior.

### 🛑 break — Stop the loop completely

```python
for num in range(1, 10):
    if num == 5:
        break
```

**Use cases:**
- Stop processing when target found
- Stop retry loop on success

### 🔁 continue — Skip current iteration

```python
for num in range(1, 6):
    if num == 3:
        continue
    print(num)
```

**Use cases:**
- Skip invalid data
- Skip empty values
- Skip weekends in automation script

### ⏭ pass — Do nothing (placeholder)

Used for future implementation.

```python
for i in range(5):
    pass
```

**Use cases:**
- Designing class structures
- Writing TODO code
- Avoiding syntax errors in empty blocks

### 🏭 Industry Example — Skip Bad API Items

```python
for record in records:
    if record["status"] == "invalid":
        continue
    process(record)
```

---

## ✅ TOPIC 4 — List Comprehensions (Intro)

List comprehensions are a short, Pythonic way to generate new lists.

**Structure:**
```python
new_list = [expression for item in iterable]
```

### Example 1 — Square numbers

```python
squares = [x*x for x in range(1, 6)]
```

### Example 2 — Convert to uppercase

```python
names = ["sam", "john", "alex"]
upper_names = [n.upper() for n in names]
```

### Example 3 — Filter even numbers

```python
evens = [n for n in range(20) if n % 2 == 0]
```

### 🏭 Industry Example — Extract Usernames from API

```python
usernames = [u["username"] for u in users]
```

### ⭐ Best Practices

- Keep comprehensions short
- Use normal loops for complex logic
- Good for transformation tasks

---

## 🧪 HANDS-ON EXERCISES (DAY 2)

### ✔ 1. Generate multiplication tables

**Input:** 5  
**Output:** 5 10 15 20 ... 50

### ✔ 2. FizzBuzz Variations

**Rules:**
- If divisible by 3 → Fizz
- If divisible by 5 → Buzz
- If both → FizzBuzz

**Add variations:**
- Replace numbers containing '3'
- Print special emoji instead of text

### ✔ 20 More Practice Tasks

#### if/elif/else
1. Check if number is positive/negative/zero.
2. Check if a person is child/teen/adult/senior.
3. Validate strong password rules.
4. Check if a year is leap year.

#### for Loop
5. Sum of first N numbers.
6. Print all vowels in a string.
7. Print star patterns (*, **, ***).
8. Count uppercase and lowercase letters.

#### while Loop
9. Reverse a number using while loop.
10. Take inputs until user types "exit".
11. Guess password until correct.

#### break/continue/pass
12. Print numbers 1 to 20, skipping multiples of 4.
13. Stop loop when number 13 appears.
14. Use pass to create empty function.

#### List Comprehensions
15. List of cubes for 1–10.
16. Extract words starting with "A".
17. Convert list of numbers to string list.
18. All even numbers from user-input list.

#### Combined Logic
19. Build a basic ATM menu (withdraw/deposit).
20. Build a simple login system with max 3 attempts.

---

## 🏆 MINI PROJECT — NUMBER GUESSING GAME

### 🎯 Features:

- ✔ Random number generation
- ✔ User attempts
- ✔ Feedback:
  - Too high
  - Too low
- ✔ Limit attempts
- ✔ Replay option

### 💻 Sample Implementation (Tutor-Optimized)

```python
import random

print("=== NUMBER GUESSING GAME ===")
secret = random.randint(1, 50)
attempts = 0
max_attempts = 7

while attempts < max_attempts:
    guess = int(input("Enter your guess (1–50): "))
    attempts += 1

    if guess == secret:
        print(f"🎉 Correct! You guessed it in {attempts} tries.")
        break
    elif guess < secret:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")

if attempts == max_attempts:
    print(f"❌ Out of attempts! The number was {secret}.")
```
```