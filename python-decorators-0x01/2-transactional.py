import sqlite3
import functools
from datetime import datetime

# Database setup
def setup_database():
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    # Create a users table for testing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT
        )
    """)

    # Insert a sample user
    cursor.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", ("John Doe", 30, "john.doe@example.com"))

    connection.commit()
    connection.close()

# Decorator to log queries
def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract SQL query from arguments (assuming the first arg is the query string)
            if args:
                query = args[0]
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Executing SQL Query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Decorator to handle database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect("test.db")
        try:
            return func(connection, *args, **kwargs)
        finally:
            connection.close()
    return wrapper

# Decorator to handle transactions
def transactional(func):
    @functools.wraps(func)
    def wrapper(connection, *args, **kwargs):
        try:
            result = func(connection, *args, **kwargs)
            connection.commit()
            return result
        except Exception as e:
            connection.rollback()
            print(f"Transaction rolled back due to: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

if __name__ == "__main__":
    setup_database()
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        user = get_user_by_id(user_id=1)
        print(user)
    except Exception as e:
        print(f"An error occurred: {e}")
