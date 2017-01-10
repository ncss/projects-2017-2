from databases.Comment import Comment

class Response(Comment):
    def __init__(self, username, *args):
        super().__init__(username, *args)
        self.image_data = args[3]