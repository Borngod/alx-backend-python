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

def stream_user_ages():
    """Generator function to yield user ages one by one."""
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data;")
        for (age,) in cursor:
            yield age
    except Error as e:
        print(f"Error fetching user ages: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def calculate_average_age():
    """Calculate the average age of users using the stream_user_ages generator."""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")

# Example usage:
if __name__ == "__main__":
    calculate_average_age()
