import mysql.connector
from mysql.connector import Error

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='password',  # Replace with your MySQL password
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None

def stream_users_in_batches(batch_size):
    """Fetch rows in batches from the user_data table using a generator."""
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def batch_processing(batch_size):
    """Process each batch to filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 25]
        yield filtered_users

# Example usage:
if __name__ == "__main__":
    batch_size = 10
    for processed_batch in batch_processing(batch_size):
        print(f"Processed batch: {processed_batch}")
