from databases.basic_info import BasicInfo
from databases.profiles import Profiles

class OriginalPost(BasicInfo):
    def __init__(self, pkid, user, *args):
        super().__init__(pkid, user, *args)

    def __repr__(self):
        return "OriginalPost("+",".join(map(str,[self.id,self.user,self.reply_to,self.contents,self.date]))+")"

    @staticmethod
    def get_posts(sql,skip):
        sql.execute('''
        SELECT *
        FROM comments
        WHERE reply_id IS NULL
        ORDER BY date;''')

        results = sql.fetchall()[skip:]
        original_post = []
        for a in results:
            p = Profiles.from_id(sql,a[1])
            original_post.append(OriginalPost(p,*a))
        return original_post

    @classmethod
    def create(cls,sql,user_id,contents):
        sql.execute('''
        INSERT INTO comments
        (user_id, contents)
        VALUES (?,?)''',(user_id,contents))
        pkid = sql.lastrowid
        sql.commit()

        date = sql.execute('''
        SELECT date
        FROM comments
        WHERE id=?''',(pkid,)).fetchone()[0]
        print(pkid,user_id,None,contents,date)
        return cls(pkid,user_id,None,contents,date)