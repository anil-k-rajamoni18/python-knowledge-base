# age = input("Enter age: ") # str(data) => "data"
# print(age, type(age))


# age = int(input("Enter age: ")) # int(data) => converts data to integer
# print(age, type(age))

# salary = float(input("Enter salary: ")) # float(data) => converts data to float
# print(salary, type(salary))

# is_admin = bool(int(input("Are you admin? (1 for Yes, 0 for No): "))) # bool(data) => converts data to boolean
# print(is_admin, type(is_admin))

marks = []  # list with 3 elements initialized to 0 
for i in range(3):
    mark = float(input(f"Enter mark {i+1}: "))
    marks.append(mark)

# print(marks, type(marks))


num1, num2, num3 = list(map(int, input("Enter numbers separated by space: ").split()))
print(num1, num2, num3, type(num1), type(num2), type(num3))