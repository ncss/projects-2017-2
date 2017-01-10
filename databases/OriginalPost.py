from databases.BasicInfo import BasicInfo

class OriginalPost(BasicInfo):
    def __init__(self, username, contents, date, image_data):
        super().__init__(username, contents, date)
        self.image_data = image_data