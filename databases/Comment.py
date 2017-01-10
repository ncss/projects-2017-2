from databases.BasicInfo import BasicInfo

class Comment(BasicInfo):
    def __init__(self, user, *args):
        super().__init__(user, *args)
        self.reply_to = args[2]

print(Comment.get(2).reply_to)