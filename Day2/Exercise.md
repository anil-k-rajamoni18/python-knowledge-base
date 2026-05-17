## 🧪 REALTIME HANDS-ON EXERCISES — DAY 2
### (Control Flow, Loops, Break/Continue, List Comprehensions)

---

## SECTION 1 — Industry-Driven if/elif/else Exercises

### 1. Login System with Lockout

Simulate login:
- User enters username/password
- If entered incorrectly 3 times → lock the account

### 2. Bank Transaction Validator

**Input:** withdrawal amount, balance  
**Output:**
- "Transaction successful" if amount ≤ balance
- "Insufficient balance" otherwise

### 3. Shipping Cost Calculator

**Rules:**
- Weight < 1kg → ₹50
- 1–5kg → ₹100
- \>5kg → ₹200

### 4. Employee Bonus Eligibility

**Inputs:**
- Years of experience
- Rating (1–5)

**Rules:**
- If experience > 5 AND rating ≥ 4 → 20% bonus
- Else → 10% bonus

### 5. Movie Ticket Pricing

**Rules:**
- Children (<13) → ₹100
- Adults (13–60) → ₹200
- Seniors (>60) → ₹150

### 6. Smart Traffic Light Rule Engine

**Input:** light color: "red", "yellow", "green"  
**Output:** corresponding driving instruction.

### 7. Fraud Score Classification

Given fraud probability score (0–1):
- \>0.9 → "High risk"
- \>0.6 → "Medium risk"
- else → "Low risk"

### 8. Temperature Alert System

**Input:** temperature  
**Print:**
- "Normal"
- "Warning"
- "Critical"

Used in DevOps, IoT systems.

### 9. Discount Engine for E-commerce

**Inputs:**
- Product price
- Customer type (new/regular/premium)

**Logic:**
- premium → 20% discount
- regular → 10%
- new → 5%

### 10. Student Grade Calculator

Convert marks to grade A/B/C/D/F.

---

## SECTION 2 — Realtime for Loops Exercises

### 11. Generate Employee IDs

Given 5 employees, generate IDs:
```
EMP001  
EMP002  
EMP003 ...
```

### 12. Process List of Orders

Given list:
```python
orders = [450, 1200, 300, 999, 1450]
```

Print:
- "High-value order" if >1000
- else "Normal order"

### 13. Print Logs with Line Numbers

**Input:** list of log messages  
**Output:**
```
1. initializing system  
2. loading model  
3. model ready
```

### 14. Count Vowels in a Company Name

Loop through string and count vowels.

### 15. API Retry Logic Simulation

Run a loop 5 times:
- If response code == 200 → break
- Else retry

### 16. Print Multiplication Table (1–20)

But only print values ending in digit "5".

### 17. Data Cleaning — Remove Empty Strings

Given list:
```python
["john", "", "sam", "", "alex"]
```

Skip empty strings and print others.

### 18. Temperature Sensor Data Summary

Given 24 hourly readings:
- Find min, max, average
- (without using min/max/sum built-ins)

### 19. Password Strength Checker

Loop through characters → ensure:
- at least 1 uppercase
- 1 digit
- 1 special character

### 20. Inventory Validation

Given stock list:
```python
stock = [12, 0, 4, 7, 0, 33]
```

Print "Out of stock" where value is 0.

---

## SECTION 3 — While Loops in Real Life

### 21. ATM Withdrawal — Continue Asking

Users enter withdrawal amount until:
- they enter 0
- OR amount < balance

### 22. 2FA Verification Simulation

Ask OTP until correct OTP is entered or attempts reach 3.

### 23. Menu-Driven CLI App

Display menu inside a while loop:
```
1. Add Task  
2. Delete Task  
3. Show Tasks  
4. Exit
```

### 24. Number Reversal (No Strings)

Use while loop to reverse digits.

### 25. Keep Taking Inputs Until "exit"

Used in chatbots / CLI tools.

### 26. Find First Number Divisible by Both 3 and 7

Using `while True`, break when found.

### 27. Count Login Attempts

While loop to count attempts until password is correct.

### 28. CPU Threshold Monitor Simulation

Generate random CPU usage until cpu < 70, else keep watching.

### 29. Random Dice Rolling Game

Roll dice until user types "stop".

### 30. Sum of Digits of a Number

Using while loop (no conversion to string).

---

## SECTION 4 — break / continue / pass (Applied)

### 31. Skip Invalid Transactions

Transaction list:
```python
txn = [230, -1, 450, 0, 990, -4]
```

Skip negatives and zeros.

### 32. Stop Processing When Fraud Transaction Found

Stop loop when any amount > 10,000.

### 33. Skip Emails Without '@'

List of user emails, skip invalid ones.

### 34. Placeholder Functions using pass

Create class with methods:
- `login()`
- `logout()`
- `reset_password()`

Use `pass` in each.

### 35. Print Even Numbers But Stop at 50

Use both `continue` and `break` in same loop.

---

## SECTION 5 — List Comprehension (Realtime Intro)

### 36. Convert Product Names to Uppercase

```python
products = ["macbook", "airpods", "iphone"]
```

### 37. Extract Prices Above 500

```python
prices = [120, 450, 899, 1500, 300]
```

### 38. Clean Email List

Remove empty emails:
```python
emails = ["a@gmail.com", "", "test@yahoo.com", None, "sam@test.com"]
```

### 39. Generate List of Even Numbers (1–200)

Using comprehension.

### 40. Extract First Letter of Each Name

```python
names = ["Alice", "Bob", "Charlie", "David"]
```
```