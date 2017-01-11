from databases.Profiles import Profiles
import databases.db
import sqlite3

sql = databases.db.db()

class BasicInfo():
    def __init__(self, user, *args):
        self.user = user
        self.contents = args[4]
        self.date = args[5]

    @classmethod
    def get(cls, id):
        sql.execute('''
        SELECT *
        FROM comments WHERE id=?
        ''', (id,))
        id = sql.fetchone()
        p = Profiles.from_id(id[1])
        return cls(p, *id)

if __name__ == "__main__":
    print(BasicInfo.get(1).contents)

