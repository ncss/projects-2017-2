from .BasicInfo import BasicInfo

class Comment(BasicInfo):
    def __init__(self, username, contents, date, reply_to):
        super().__init__(username, contents, date)
        self.reply_to = reply_to
