import sqlite3, os

# Ensure database does not exist already
os.remove('data.db')
conn=sqlite3.connect('data.db')
cursor=conn.cursor()

cursor.executescript(open("create_database.sql").read())
cursor.executescript(open("mock_data.sql").read())

conn.close()