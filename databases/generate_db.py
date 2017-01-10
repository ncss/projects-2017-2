import sqlite3, os, Profiles

# Ensure database does not exist already
os.remove('data.db')
conn=sqlite3.connect('data.db')
cursor=conn.cursor()

cursor.executescript(open("create_database.sql").read())
cursor.executescript(open("mock_data.sql").read())

for r in cursor.execute("SELECT id,password FROM profiles;").fetchall():
    conn.execute("UPDATE profiles SET password = ? WHERE id = ?;", (Profiles.Profiles._hash(r[1]), r[0]))


conn.commit()

conn.close()