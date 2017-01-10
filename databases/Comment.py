from databases.BasicInfo import BasicInfo
from databases.Profiles import Profiles
from databases.db import db

sql = db()

class Comment(BasicInfo):
    def __init__(self, user, *args):
        super().__init__(user, *args)
        self.reply_to = args[2]

    @classmethod
    def CreateComment(cls, comment_id, user_id, reply_to, image_id, contents, date):
        sql.execute('''
                INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?)
                ''', (comment_id, user_id, reply_to, image_id, contents, date,))
        p = Profiles.from_id(user_id)
        return cls(p, comment_id, user_id, reply_to, image_id, contents, date)


#print(Comment.CreateComment('18', '20520', '4', 'NULL', 'Hello', '12/1/14').contents)