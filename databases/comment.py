from databases.basic_info import BasicInfo
from databases.profiles import Profiles

class Comment(BasicInfo):
    def __init__(self, user, *args):
        super().__init__(user, *args)

    @classmethod
    def create(cls, sql, user_id, reply_to, contents):
        pkid = sql.execute('''
                INSERT INTO comments
                (user_id, reply_id, contents)
                VALUES (?,?,?)
                ''', (user_id, reply_to, contents)).lastrowid
        sql.commit()

        date = sql.execute('''
               SELECT date
               FROM comments
               WHERE id=?''', (pkid,)).fetchone()[0]

        return cls(Profiles.from_id(sql, user_id), pkid, user_id, reply_to, contents, date)


#sql.open()
#print(Comment.create('18', '20520', '4', 'Hello', '12/1/14').contents)