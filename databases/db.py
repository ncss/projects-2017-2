import sqlite3
import os
from databases.profiles import Profiles
class Database:
    def __init__(self,filepath):
        #Create a connection to the database file
        #Store it in a state E.G self.connection

        if not os.path.exists(filepath):
            conn = sqlite3.connect(filepath)
            cursor = conn.cursor()

            cursor.executescript(open("databases/create_database.sql").read())
            cursor.executescript(open("databases/mock_data.sql").read())

            # Hash all of the passwords
            for r in cursor.execute("SELECT id,password FROM profiles;").fetchall():
                conn.execute("UPDATE profiles SET password = ? WHERE id = ?;", (Profiles._hash(r[1]), r[0]))

            conn.commit()
            conn.close()
        self.conn = sqlite3.connect(filepath)
        self.cur  = self.conn.cursor()

    def __repr__(self):
        return "db()"

    def __str__(self):
        return "db object"

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __getattr__(self, item):
        return self.cur.__getattribute__(item)

    def __iter__(self):
        return self.cur.__iter__()

if __name__ == "__main__":
    x = Database('databases/data.db')
    # x.execute("INSERT INTO profiles VALUES (1234, 'testmeme', 'somesortofhashquestionmark', 'd@d.com');")

    print(x.execute("SELECT * FROM profiles").fetchall())

    for e in x:
        print(e)
    x.commit()
    x.close()