from databases.Profiles import Profiles

class Categories():
    def __init__(self, name, category_id, image_id):
        self.name = name
        self.category_id = category_id
        self.image_id = image_id

    @classmethod
    def get(cls, sql, id):
        sql.execute('''
            SELECT *
            FROM comments WHERE id=?
            ''', (id,))
        id = sql.fetchone()
        p = Profiles.from_id(id[1])
        return cls(p, *id)