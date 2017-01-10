from databases.BasicInfo import BasicInfo
from databases.Profiles import Profiles
import databases.db
import sqlite3

sql = databases.db.db()

class Comment(BasicInfo):
    def __init__(self, user, *args):
        super().__init__(user, *args)
        self.reply_to = args[2]

    @classmethod
    def CreateComment(self, comment_id, user_id, reply_to, image_id, contents, date):
        sql.execute('''
                INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?)
                ''', (comment_id, user_id, reply_to, image_id, contents, date,))
        comment = sql.fetchone()
        p = Profiles.from_id(user_id)
        return cls(p, *comment)

stub = ['1', '123', '4', 'NULL', 'Hello', '12/1/14' ]

print("hi".CreateComment(0).contents)