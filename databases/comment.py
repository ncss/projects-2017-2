from databases.basic_info import BasicInfo
from databases.profiles import Profiles

class Comment(BasicInfo):
    def __init__(self, user, *args):
        super().__init__(user, *args)

    def __repr__(self):
        return "Comment("+",".join(map(str,[self.id,self.user,self.reply_to,self.contents,self.date]))+")"

    @classmethod
    def create(cls, sql, user_id, reply_to, contents):
        sql.execute('''
                INSERT INTO comments
                (user_id, reply_id, contents)
                VALUES (?,?,?)
                ''', (user_id, reply_to, contents))
        pkid = sql.lastrowid
        sql.commit()

        sql.execute('''
               SELECT date
               FROM comments
               WHERE id=?''', (pkid,))
        date = sql.fetchone()[0]

        return cls(Profiles.from_id(sql, user_id), pkid, user_id, reply_to, contents, date)

    def get_replies(self, sql):
        sql.execute('''
          SELECT *
          FROM comments
          WHERE reply_id=?''', (self.id,))

        return [Comment(Profiles.from_id(sql, x[1]), *x) for x in sql.fetchall()]


#sql.open()
#print(Comment.create('18', '20520', '4', 'Hello', '12/1/14').contents)