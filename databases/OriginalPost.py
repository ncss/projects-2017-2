from databases.BasicInfo import BasicInfo
from databases.Profiles import Profiles
import sqlite3
conn = sqlite3.connect('data.db')
cur = conn.cursor()


class OriginalPost(BasicInfo):
    def __init__(self, user, *args):
        super().__init__(user, *args)
        self.image_data = args[3]

    @staticmethod
    def GetPosts(skip):
        cur.execute('''
        SELECT *
        FROM comments
        WHERE reply_id IS NULL;''')

        results = cur.fetchall()[skip:]
        original_post  = []
        for a in results:
            p = Profiles.from_id(a[1])
            original_post.append(OriginalPost(p,*a))
        return original_post
OriginalPost.GetPosts(1)