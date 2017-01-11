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

#print(BasicInfo.get(some database object, 1).contents)
