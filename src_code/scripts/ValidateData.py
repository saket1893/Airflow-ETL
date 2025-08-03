import re

# Function to validate the generated data
def validate_data(data):
    validated_data = []
    
    for record in data:
        is_valid = True
        
        # Validate email format (basic validation)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", record['email']):
            print(f"Invalid email: {record['email']}")
            is_valid = False
        
        # Validate date of birth (ensure age is between 18 and 100)
        try:
            dob = datetime.strptime(record['date_of_birth'], '%Y-%m-%d')
            age = (datetime.now() - dob).days // 365
            if age < 18 or age > 100:
                print(f"Invalid age for date_of_birth: {record['date_of_birth']}")
                is_valid = False
        except ValueError:
            print(f"Invalid date format: {record['date_of_birth']}")
            is_valid = False
        
        # If data is valid, add to validated list
        if is_valid:
            validated_data.append(record)
    
    return validated_data

# Example usage
valid_data = validate_data(random_data)
print(valid_data)
