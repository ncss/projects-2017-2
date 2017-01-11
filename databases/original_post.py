from databases.basic_info import BasicInfo
from databases.profiles import Profiles
from databases.response import Response
import os
import re

class OriginalPost(BasicInfo):
    def __init__(self, user, *args):
        super().__init__(user, *args)

    def __repr__(self):
        return "OriginalPost("+",".join(map(str,[self.id,self.user,self.reply_to,self.contents,self.date]))+")"

    @staticmethod
    def get_posts(sql,skip=0):
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

    def get_replies(self, sql):
        sql.execute('''
        SELECT *
        FROM comments
        WHERE reply_id=?''', (self.id,))

        return [Response(Profiles.from_id(sql,x[1]),*x) for x in sql.fetchall()]

    @classmethod
    def create(cls,sql,user_id,contents):
        sql.execute('''
        INSERT INTO comments
        (user_id, contents)
        VALUES (?,?)''',(user_id,contents))
        pkid = sql.lastrowid
        sql.commit()

        sql.execute('''
        SELECT date
        FROM comments
        WHERE id=?''',(pkid,))
        date = sql.fetchone()[0]
        # print(Profiles.from_id(sql,user_id),pkid,user_id,None,contents,date)
        return cls(Profiles.from_id(sql,user_id),pkid,user_id,None,contents,date)

    def get_image_path(self):
        for file in os.listdir('static/images/'):
            ext = re.match(str(self.id)+'(\..*)',file)
            if ext:
                return 'static/images/'+str(self.id)+ext.group(1)