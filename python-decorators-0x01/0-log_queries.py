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
            age INTEGER NOT NULL
        )
    """)
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

# Function to execute queries@log_queries decorator applied
@log_queries()
def execute_query(query, params=None):
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()
    connection.close()

def main():
    setup_database()
    # Insert a user
    execute_query("INSERT INTO users (name, age) VALUES (?, ?)", ("John Doe", 30))

if __name__ == "__main__":
    main()
