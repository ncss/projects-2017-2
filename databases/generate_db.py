import sqlite3, os

# Ensure database does not exist already
os.remove('data.db')
conn=sqlite3.connect('data.db')
cursor=conn.cursor()
for statement in open("create_database.sql").read().split('--STATEMENT-DELIM'):
    print(statement)
    cursor.execute(statement)

for statement in open("mock_data.sql").read().split('--STATEMENT-DELIM'):
    print(statement)
    cursor.execute(statement)

conn.close()