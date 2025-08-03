import mysql.connector
from mysql.connector import Error

def load_data(host: str, port: int, database: str, user: str, password: str, data):
    """
    Load validated data into MySQL database.
    :param host: The hostname of the MySQL server
    :param port: The port number (usually 3306)
    :param database: The database name
    :param user: The MySQL username
    :param password: The MySQL password
    :param data: The validated data to insert
    """
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        # Check if the connection is successful
        if connection.is_connected():
            print(f"Successfully connected to the database: {database}")
            
            # Create a cursor to execute SQL queries
            cursor = connection.cursor()

            # SQL Insert query to insert data into the 'users' table
            insert_query = """INSERT INTO users (name, email, address, date_of_birth)
                              VALUES (%s, %s, %s, %s)"""

            # Loop through each validated record and insert it into the database
            for record in data:
                cursor.execute(insert_query, (record['name'], record['email'], record['address'], record['date_of_birth']))
            
            # Commit the transaction to make sure the data is saved
            connection.commit()
            print(f"{cursor.rowcount} records inserted into MySQL.")
        
    except Error as e:
        # Handle any error that occurs during the process
        print(f"Error: {e}")
    
    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")
