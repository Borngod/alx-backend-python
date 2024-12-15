## Tasks

### 0\. Logging database Queries


**Objective:** create a decorator that logs database queries executed by any function

**Instructions:**

- Complete the code below by writing a decorator `log_queries` that logs the SQL query before executing it.
    
- Prototype: `def log_queries()`
    

```
import sqlite3
import functools

#### decorator to lof SQL queries

 """ YOUR CODE GOES HERE"""

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
```

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `python-decorators-0x01`
- File: `0-log_queries.py`


### 1\. Handle Database Connections with a Decorator


**Objective:** create a decorator that automatically handles opening and closing database connections

**Instructions:**

- Complete the script below by Implementing a decorator `with_db_connection` that opens a database connection, passes it to the function and closes it afterword

```
import sqlite3 
import functools

def with_db_connection(func):
    """ your code goes here""" 

@with_db_connection 
def get_user_by_id(conn, user_id): 
cursor = conn.cursor() 
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)
```

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `python-decorators-0x01`
- File: `1-with_db_connection.py`



### 2\. Transaction Management Decorator


**Objective:** create a decorator that manages database transactions by automatically committing or rolling back changes

**Instructions:**

- Complete the script below by writing a decorator `transactional(func)` that ensures a function running a database operation is wrapped inside a transaction.If the function raises an error, rollback; otherwise commit the transaction.
    
- Copy the `with_db_connection` created in the previous task into the script
    

```
import sqlite3 
import functools

"""your code goes here"""

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
```

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `python-decorators-0x01`
- File: `2-transactional.py`



### 3\. Using Decorators to retry database queries


**Objective:** create a decorator that retries database operations if they fail due to transient errors

**Instructions:**

- Complete the script below by implementing a `retry_on_failure(retries=3, delay=2)` decorator that retries the function of a certain number of times if it raises an exception

```
import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
```

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `python-decorators-0x01`
- File: `3-retry_on_failure.py`



### 4\. Using decorators to cache Database Queries


**Objective:** create a decorator that caches the results of a database queries inorder to avoid redundant calls

**Instructions:**

- Complete the code below by implementing a decorator `cache_query(func)` that caches query results based on the SQL query string

```
import time
import sqlite3 
import functools


query_cache = {}

"""your code goes here"""

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
```

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `python-decorators-0x01`
- File: `4-cache_query.py`
