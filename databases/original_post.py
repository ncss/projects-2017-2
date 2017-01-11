from databases.basic_info import BasicInfo
from databases.profiles import Profiles

class OriginalPost(BasicInfo):
    def __init__(self, user, *args):
        super().__init__(user, *args)
        self.image_id = args[3]

    @staticmethod
    def get_posts(sql,skip):
        sql.execute('''
        SELECT *
        FROM comments
        WHERE reply_id IS NULL;''')

        results = sql.fetchall()[skip:]
        original_post = []
        for a in results:
            p = Profiles.from_id(a[1])
            original_post.append(OriginalPost(p,*a))
        return original_post

#OriginalPost.get_posts(database object, 1)