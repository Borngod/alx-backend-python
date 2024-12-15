import mysql.connector
from mysql.connector import Error

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password=' ', 
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None

def stream_users():
    """Fetch rows one by one from the user_data table using a generator."""
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage:
if __name__ == "__main__":
    for user in stream_users():
        print(user)
