from databases.comment import Comment

class Response(Comment):
    def __init__(self, user, *args):
        super().__init__(user, *args)