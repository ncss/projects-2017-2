import os

import re

from databases.profiles import Profiles

class BasicInfo:
    def __init__(self, user, *args):
        self.user = user
        self.id = args[0]
        self.reply_to = args[2]
        self.contents = args[3]
        self.date=args[4]

    @classmethod
    def from_id(cls, sql, id):
        sql.execute('''
        SELECT *
        FROM comments WHERE id=?
        ''', (id,))
        x = sql.fetchone()
        p = Profiles.from_id(sql,x[1])
        return cls(p, *x)


    def get_image_path(self):
        for file in os.listdir('static/images/'):
            ext = re.match(str(self.id)+'(\..*)',file)
            if ext:
                return 'static/images/'+str(self.id)+ext.group(1)
#print(BasicInfo.get(some database object, 1).contents)
