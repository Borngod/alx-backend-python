import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        # Open the database connection
        self.connection = sqlite3.connect(self.db_name)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the database connection
        if self.connection:
            if exc_type is None:
                # Commit changes if no exception occurred
                self.connection.commit()
            else:
                # Rollback changes if an exception occurred
                self.connection.rollback()
            self.connection.close()

# Example usage:
if __name__ == "__main__":
    # Using the context manager to perform a query
    with DatabaseConnection('user.db') as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
    # Print the query results
    for row in results:
        print(row)
