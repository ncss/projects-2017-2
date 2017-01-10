import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()

class BasicInfo():
    def __init__(self, username, contents, date):
        self.username = username
        self.contents = contents
        self.date = date

    @classmethod
    def get(cls, id):
        cur.execute('''
        SELECT *
        FROM comments WHERE id=?
        ''', (id,))
        print(cur.fetchone())
        return cls()

BasicInfo.get(1)

cur.execute('''
        SELECT username
        FROM profiles WHERE id=?
        ''', (id,))