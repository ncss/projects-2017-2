from databases.Comment import Comment

class Response(Comment):
    def __init__(self, username, contents, date, reply_to, image_data):
        super().__init__(username, contents, date, reply_to)
        self.image_data = image_data