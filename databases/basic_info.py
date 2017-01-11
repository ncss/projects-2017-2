from databases.profiles import Profiles

class BasicInfo:
    def __init__(self, user, *args):
        self.user = user
        self.contents = args[4]
        self.date = args[5]

    @classmethod
    def get(cls, sql, id):
        sql.execute('''
        SELECT *
        FROM comments WHERE id=?
        ''', (id,))
        id = sql.fetchone()
        p = Profiles.from_id(id[1])
        return cls(p, *id)

#print(BasicInfo.get(1).contents)

