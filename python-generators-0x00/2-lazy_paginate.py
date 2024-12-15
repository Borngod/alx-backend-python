import mysql.connector
from mysql.connector import Error

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
            return connection
    except Error as e:
        print(f"Error while connecting to ALX_prodev: {e}")
        return None

def paginate_users(page_size, offset):
    """Fetch a page of users starting from the given offset."""
    connection = connect_to_prodev()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s;"
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching paginated data: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def lazy_paginate(page_size):
    """Generator function to lazily load pages of users."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# Example usage:
if __name__ == "__main__":
    page_size = 10
    for page in lazy_paginate(page_size):
        print(f"Page: {page}")
