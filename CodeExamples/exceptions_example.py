from datetime import date
import requests

print("Welcome to Exception Handling")

try:
    num1 = int(input("Enter Num1:"))
    num2 = int(input("Enter Num2:"))
    print(f"Division Of {num1}/{num2} = {num1/num2}")
except (ValueError, ZeroDivisionError) as e:
    print("Exception Handled..", e)

print(f"Today: ", date.today())
print("Division Operation Completed")


api_endpoint = "https://open-weather13.r.rapidapi.com/CITY"
headers = {"x-rapidapi-host" : "open-weather13.p.rapidapi.com" ,
"x-rapidapi-key" : "bfa73a12a8msh0fd2368b057d757p19201ajsnd017d538d45b"
}

payload = {"city" : "gwalior",
"lang" : "EN"
}
try:
    response = requests.get(url=api_endpoint, headers=headers, params=payload)
    print(f"status code: {response.status_code}")
    print(f"weather data: {response.json()}")
except Exception as e:
    print({"error": "API failed"})
    print(f"Exception: {e}")

print("End")


class InvalidAgeError(Exception):
    pass

def register(age):
    if age < 18:
        raise InvalidAgeError("Age must be 18+")
    print("registered")

register(18)
try:
    register(11)
except InvalidAgeError as e:
    print(e, "Please pass valid age")



def process_user_records(records):
    valid = []
    invalid = []
    
    for i, record in enumerate(records):
        try:
            # Try to convert age
            age = int(record.get("age", ""))
            
            # Validate email exists
            if "email" not in record:
                raise KeyError("email field missing")
            
            # Validate age range
            if age < 18 or age > 120:
                raise ValueError(f"Age {age} out of valid range")
            
            valid.append(record)
            
        except ValueError as e:
            invalid.append({"index": i, "error": f"Invalid value: {e}"})
        except KeyError as e:
            invalid.append({"index": i, "error": f"Missing field: {e}"})
        except Exception as e:
            invalid.append({"index": i, "error": f"Unknown error: {e}"})
    
    return valid, invalid

# Test
records = [
    {"name": "John", "age": "25", "email": "john@email.com"},
    {"name": "Jane", "age": "abc", "email": "jane@email.com"},  # Invalid age
    {"name": "Bob", "age": "30"},  # Missing email
    {"name": "Alice", "age": "150", "email": "alice@email.com"},  # Age out of range
]

valid, invalid = process_user_records(records)
print(f"Valid records: {len(valid)}")
print(f"Invalid records: {len(invalid)}")
for inv in invalid:
    print(f"  Record {inv['index']}: {inv['error']}")



####
try:
    api_key = input("Enter API key: ")
    endpoint = input("Enter endpoint: ")
    
    try:
        response = requests.get(
            f"https://api.example.com/{endpoint}",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        try:
            data = response.json()
            print(f"Data received: {len(data)} records")
        except json.JSONDecodeError:
            print("Response is not valid JSON")
            
    except requests.ConnectionError:
        print("Network connection failed")
    except requests.Timeout:
        print("Request timed out")
        
except KeyboardInterrupt:
    print("User cancelled operation")