from databases.comment import Comment

class Response(Comment):
    def __init__(self, username, *args):
        super().__init__(username, *args)
        self.image_id = args[3]