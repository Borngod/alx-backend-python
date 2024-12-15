import csv
import uuid
import mysql.connector
from mysql.connector import Error

def connect_db():
    """Connect to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password=' ' 
        )
        if connection.is_connected():
            print("Connected to MySQL server.")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created or already exists.")
    except Error as e:
        print(f"Error while creating database: {e}")

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='',  
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database.")
        return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Create the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3, 0) NOT NULL,
                INDEX (user_id)
            );
        ''')
        print("Table user_data created or already exists.")
    except Error as e:
        print(f"Error while creating table: {e}")

def insert_data(connection, data):
    """Insert data into the user_data table."""
    try:
        cursor = connection.cursor()
        insert_query = '''
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                email = VALUES(email),
                age = VALUES(age);
        '''
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"Inserted {cursor.rowcount} rows into user_data table.")
    except Error as e:
        print(f"Error while inserting data: {e}")

def read_csv(file_path):
    """Read user data from a CSV file."""
    data = []
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append((str(uuid.uuid4()), row['name'], row['email'], row['age']))
        print(f"Read {len(data)} rows from CSV file.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return data

def main():
    # Step 1: Connect to the MySQL server
    connection = connect_db()
    if not connection:
        return

    # Step 2: Create the ALX_prodev database
    create_database(connection)
    connection.close()

    # Step 3: Connect to the ALX_prodev database
    prodev_connection = connect_to_prodev()
    if not prodev_connection:
        return

    # Step 4: Create the user_data table
    create_table(prodev_connection)

    # Step 5: Read data from the CSV file
    data = read_csv('user_data.csv')

    # Step 6: Insert data into the database
    insert_data(prodev_connection, data)

    # Step 7: Close the database connection
    prodev_connection.close()

if __name__ == "__main__":
    main()
