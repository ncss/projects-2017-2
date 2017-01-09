class Profiles(object):
    def __init__(self,pkid,user,email):
        self._id=pkid
        self.user=user
        self.email=email

    @classmethod
    def from_id(cls, pkid):
        """
         SELECT user, email
         FROM profiles
         WHERE id = ?
         """,(pkid)
        # SQL select statement to retrieve
        # the username and email
        
        return cls(pkid,user,email)

    @staticmethod
    def login(user,password):
        """
        SELECT id
        FROM profiles
        WHERE username = ? AND password = ?
        """,(user, password)
        """
        Takes username and password)
        Returns userid.
        This can then be used with Profiles.from_id
        to return a new Profile object.
        """
        # Hash teh password
        # SQL select statement to retrieve
        # the userid
        # Return None (or raise Error, you choose)
        # if there is no user matching
        # username and hashed password.
        return pkid
