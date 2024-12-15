# Alx-backend-python
### 0\. Getting started with python generators


**Objective: create a generator that streams rows from an SQL database one by one.**

**Instructions:**

- Write a python script that `seed.py`:
    
    - Set up the MySQL database, `ALX_prodev` with the table user\_data with the following fields:
    - `user_id(Primary Key, UUID, Indexed)`
    - `name (VARCHAR, NOT NULL)`
    - `email (VARCHAR, NOT NULL)`
    - `age (DECIMAL,NOT NULL)`
    - Populate the database with the sample data from this [user\_data.csv](https://intranet.alxswe.com/rltoken/kPrtJ_hN0TXKgEfwKY4vHg "user_data.csv")
        - Prototypes:
    - `def connect_db()` :- connects to the mysql database server
    - `def create_database(connection)`:- creates the database `ALX_prodev` if it does not exist
    - `def connect_to_prodev()` connects the the ALX\_prodev database in MYSQL
    - `def create_table(connection)`:- creates a table user\_data if it does not exists with the required fields
    - `def insert_data(connection, data)`:- inserts data in the database if it does not exist

```
faithokoth@ubuntu:python-generators-0x00 % cat 0-main.py
#!/usr/bin/python3

seed = __import__('seed')

connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print(f"connection successful")

    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()

faithokoth@ubuntu:python-generators-0x00 % ./0-main.py
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119), ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49), ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22), ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102)]

faithokoth@h@ubuntu:python-generators-0x00 % 

```

**Repo:**

- GitHub repository: `alx-backend-python`
- Directory: `python-generators-0x00`
- File: `seed.py, README.md`
