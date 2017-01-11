from databases.comment import Comment

class Response(Comment):
    def __init__(self, pkid, user_id, *args):
        super().__init__(pkid, user_id, *args)