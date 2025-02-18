import sqlite3

DATABASE = "users.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT NOT NULL,
        word_count INTEGER DEFAULT 0
    )
''')

conn.commit()
conn.close()
