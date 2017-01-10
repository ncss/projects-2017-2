import sqlite3, os
from databases.Profiles import Profiles

# Ensure database does not exist already
if os.path.exists('databases/data.db'):
    os.remove('databases/data.db')
conn=sqlite3.connect('databases/data.db')
cursor=conn.cursor()

cursor.executescript(open("databases/create_database.sql").read())
cursor.executescript(open("databases/mock_data.sql").read())

# Hash all of the passwords
for r in cursor.execute("SELECT id,password FROM profiles;").fetchall():
    conn.execute("UPDATE profiles SET password = ? WHERE id = ?;", (Profiles._hash(r[1]), r[0]))

conn.commit()

conn.close()
