import sqlite3

class ExecuteQuery:
    """
    A context manager for executing SQL queries with automatic connection management.
    
    This class provides a reusable way to execute SQL queries with proper 
    connection opening, query execution, and connection closing.
    
    Attributes:
        db_name (str): Path to the SQLite database file
        query (str): SQL query to be executed
        params (tuple, optional): Parameters for parameterized queries
    """
    def __init__(self, db_name, query, params=None):
        """
        Initialize the ExecuteQuery context manager.
        
        Args:
            db_name (str): Path to the SQLite database file
            query (str): SQL query to be executed
            params (tuple, optional): Parameters for the query. Defaults to None.
        """
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """
        Open database connection and execute the query.
        
        Returns:
            list: Results of the query execution
        """
        # Open the database connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
        # Execute the query with parameters
        self.cursor.execute(self.query, self.params)
        
        # Fetch all results
        self.results = self.cursor.fetchall()
        
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the database connection, committing or rolling back as needed.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_value: Exception value if an exception occurred
            traceback: Traceback if an exception occurred
        """
        if self.connection:
            if exc_type is None:
                # Commit changes if no exception occurred
                self.connection.commit()
            else:
                # Rollback changes if an exception occurred
                self.connection.rollback()
            
            # Close the cursor and connection
            self.cursor.close()
            self.connection.close()

# Example usage
if __name__ == "__main__":

    import sqlite3
    
    # Create a sample database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER
        )
    ''')
    
    # Insert some sample data
    sample_users = [
        ('Alice', 30),
        ('Bob', 25),
        ('Charlie', 35),
        ('David', 22)
    ]
    cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', sample_users)
    conn.commit()
    conn.close()
    
    # Demonstrate usage of ExecuteQuery context manager
    # Fetch users older than 25
    with ExecuteQuery('example.db', 'SELECT * FROM users WHERE age > ?', (25,)) as results:
        print("Users older than 25:")
        for user in results:
            print(user)
