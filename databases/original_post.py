from databases.basic_info import BasicInfo
from databases.profiles import Profiles
from databases.response import Response
import os
import re

class OriginalPost(BasicInfo):
    def __init__(self, user, *args):
        super(OriginalPost, self).__init__(user, *args)

    def __repr__(self):
        return "OriginalPost("+",".join(map(str,[self.id,self.user,self.reply_to,self.contents,self.date]))+")"

    @staticmethod
    def get_posts(sql,skip=0):
        sql.execute('''
        SELECT *
        FROM comments
        WHERE reply_id IS NULL
        ORDER BY date DESC;''')

        results = sql.fetchall()[skip:]
        original_post = []
        for a in results:
            p = Profiles.from_id(sql,a[1])
            original_post.append(OriginalPost(p,*a))
        return original_post

    @staticmethod
    def get_posts_by_user(sql, username, skip=0):
        sql.execute('''
        SELECT *
        FROM comments
        INNER JOIN profiles ON comments.user_id = profiles.id
        WHERE reply_id IS NULL AND username=?
        ORDER BY date;''', (username,))

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

    @staticmethod
    def get_posts_with_category(sql, category_name, skip=0):
        sql.execute('''
        SELECT *
        FROM comments
        WHERE id in (
            SELECT comment_id
            FROM categorylink
            WHERE category_name = ?
        )
        ORDER BY date DESC
        ''', (category_name,))

        results = sql.fetchall()[skip:]
        posts = []
        for row in results:
            profile = Profiles.from_id(sql, row[1])
            posts.append(OriginalPost(profile, *row))
        return posts

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

    @staticmethod
    def make_category_links(sql, comment_id, categories):
        for category in categories:
            sql.execute(
                '''
                    INSERT INTO categorylink
                    (category_name, comment_id)
                    VALUES (?, ?)
                ''',
                (category, comment_id)
            )
            sql.commit()

    def get_image_path(self):
        for file in os.listdir('static/images/'):
            ext = re.match(str(self.id)+'(\..*)',file)
            if ext:
                return 'static/images/'+str(self.id)+ext.group(1)

