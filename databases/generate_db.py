import sqlite3
conn=sqlite3.connect('data.db')
cursor=conn.cursor()
f=open("create_database.sql")
cursor.execute(f.read())
