import random
import string
from datetime import datetime

# Function to generate random user data
def generate_random_data(num_records: int):
    data = []
    
    for _ in range(num_records):
        name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=8))  # Random name
        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@gmail.com"  # Random email
        address = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + " ,.-", k=50))  # Random address
        date_of_birth = datetime(1970, 1, 1) + (datetime.now() - datetime(1970, 1, 1)) * random.random()  # Random date of birth
        
        data.append({
            'name': name,
            'email': email,
            'address': address,
            'date_of_birth': date_of_birth.strftime('%Y-%m-%d')
        })
    
    return data

# Example usage
random_data = generate_random_data(5)  # Generate 5 random records
print(random_data)
