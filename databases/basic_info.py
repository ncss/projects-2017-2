from databases.profiles import Profiles

class BasicInfo:
    def __init__(self, pkid, user, *args):
        self.id = pkid
        self.user = user
        self.contents = args[1]
        self.date=args[2]



    @classmethod
    def from_id(cls, sql, id):
        sql.execute('''
        SELECT *
        FROM comments WHERE id=?
        ''', (id,))
        x = sql.fetchone()
        p = Profiles.from_id(sql,x[1])
        return cls(id, p, *x)

#print(BasicInfo.get(some database object, 1).contents)

