class Comments(object):
    def __init__(self,pkid,poster_id,reply_to,image_id,contents,date=None):
        self.pkid=pkid
        self.poster_id=poster_id
        self.reply_to=reply_to
        self.image_id=image_id
        self.contents=contents
        self.date=date
    
