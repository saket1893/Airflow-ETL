import random
import string
import re
import mysql.connector
from datetime import datetime
from mysql.connector import Error

# Function to generate random user data
def generate_data(num_records: int):
    """
    Generate random user data (name, email, address, date_of_birth).
    """
    data = []
    
    for _ in range(num_records):
        name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=8))
        email = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@gmail.com"
        address = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits + " ,.-", k=50))
        date_of_birth = datetime(1970, 1, 1) + (datetime.now() - datetime(1970, 1, 1)) * random.random()
        
        data.append({
            'name': name,
            'email': email,
            'address': address,
            'date_of_birth': date_of_birth.strftime('%Y-%m-%d')
        })
    
    return data

# Function to validate the generated data
def validate_data(data):
    """
    Validate the data (check email format, date of birth, etc.).
    """
    validated_data = []
    
    for record in data:
        is_valid = True
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", record['email']):
            print(f"Invalid email: {record['email']}")
            is_valid = False
        
        # Validate date of birth (age must be between 18 and 100)
        try:
            dob = datetime.strptime(record['date_of_birth'], '%Y-%m-%d')
            age = (datetime.now() - dob).days // 365
            if age < 18 or age > 100:
                print(f"Invalid age for date_of_birth: {record['date_of_birth']}")
                is_valid = False
        except ValueError:
            print(f"Invalid date format: {record['date_of_birth']}")
            is_valid = False
        
        # If valid, add to list
        if is_valid:
            validated_data.append(record)
    
    return validated_data

# Function to load data into MySQL
def load_data(host: str, port: int, database: str, user: str, password: str, data):
    """
    Load validated data into MySQL database via host and URL.
    """
    try:
        # Establish MySQL connection
        connection = mysql.connector.connect(
            host=host,        # MySQL host (docker service name)
            port=port,        # Port (3306 for MySQL)
            database=database,  # Database name
            user=user,          # MySQL username
            password=password   # MySQL password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Prepare SQL insert query
            insert_query = """INSERT INTO users (name, email, address, date_of_birth) 
                              VALUES (%s, %s, %s, %s)"""
            
            # Insert each record
            for record in data:
                cursor.execute(insert_query, (record['name'], record['email'], record['address'], record['date_of_birth']))
            
            # Commit the transaction
            connection.commit()
            print(f"{cursor.rowcount} records inserted into MySQL.")
    
    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage
if __name__ == "__main__":
    # Step 1: Generate random data
    generated_data = generate_data(5)  # Generate 5 records
    
    # Step 2: Validate data
    validated_data = validate_data(generated_data)
    
    # Step 3: Load data into MySQL
    load_data(
        host='mysql',            # Service name for MySQL in Docker Compose
        port=3306,               # Default MySQL port
        database='airflow',      # Database name
        user='airflow',          # MySQL user
        password='airflowpassword',  # MySQL password
        data=validated_data      # The validated data
    )
