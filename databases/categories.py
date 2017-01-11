from databases.Profiles import Profiles

class Categories():
    def __init__(self, category_name, category_id, image_id):
        self.category_name = category_name
        self.category_id = category_id
        self.image_id = image_id

    @classmethod
    def get(cls, sql,):
        sql.execute('''
            SELECT category_name
            FROM categories
            ''')
        return cls(category_name)