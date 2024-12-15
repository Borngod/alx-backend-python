import asyncio
import aiosqlite
import os

async def create_sample_database():
    """
    a sample SQLite database with user data for testing.
    """
    async with aiosqlite.connect('users.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        ''')
        
        # Sample user data
        users = [
            ('Alice', 35),
            ('Bob', 42),
            ('Charlie', 28),
            ('David', 45),
            ('Eve', 39),
            ('Frank', 50),
            ('Grace', 33)
        ]
        
        await db.executemany('INSERT OR REPLACE INTO users (name, age) VALUES (?, ?)', users)
        await db.commit()

async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.
    
    Returns:
        list: All users in the database
    """
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40.
    
    Returns:
        list: Users older than 40
    """
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    """
    Fetch users concurrently using asyncio.gather.
    
    Returns:
        tuple: Results of both concurrent queries
    """
    # Ensure the database exists with sample data
    await create_sample_database()
    
    # Use asyncio.gather to run both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    # Print results
    print("All Users:")
    for user in all_users:
        print(user)
    
    print("\nUsers Older than 40:")
    for user in older_users:
        print(user)
    
    return all_users, older_users

def main():
    """
    Main function to run the concurrent database queries.
    """
    # Run the concurrent fetch
    all_users, older_users = asyncio.run(fetch_concurrently())

if __name__ == '__main__':
    main()
