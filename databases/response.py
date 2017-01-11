from databases.comment import Comment
from databases.profiles import Profiles

class Response(Comment):
    def __init__(self, user, *args):
        super().__init__(user, *args)

    def __repr__(self):
        return "Response("+",".join(map(str,[self.id,self.user,self.reply_to,self.contents,self.date]))+")"

    def get_replies(self, sql):
        sql.execute('''
        SELECT *
        FROM comments
        WHERE reply_id=?''', (self.id,))

        return [Comment(Profiles.from_id(sql,x[1]),*x) for x in sql.fetchall()]