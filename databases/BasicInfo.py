from databases.Profiles import Profiles

import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()

class BasicInfo():

    def __init__(self, user, contents, date):
        self.user = user
        self.contents = contents
        self.date = date

    @classmethod
    def get(cls, id):
        cur.execute('''
        SELECT *
        FROM comments WHERE id=?
        ''', (id,))
        id = cur.fetchone()
        p = Profiles.from_id(id[1])
        return cls(p, id[4], id[5])

print(BasicInfo.get(1).user)

