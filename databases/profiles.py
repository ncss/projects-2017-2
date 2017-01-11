import sqlite3, hashlib, random

class Profiles(object):
    def __init__(self,pkid,user,hashed_pass,email):
        self.id=pkid
        self.user=user
        self.hashed_pass=hashed_pass
        self.email=email

    def __repr__(self):
        return "Profiles({},{},{},{})".format(self.id,self.user,repr(self.hashed_pass),self.email)

    def __str__(self):
        return "Profile id {} with username: {}, hashed pass: {}, email: {}".format(self.id,self.user,self.hashed_pass,self.email)

    @staticmethod
    def _hash(password):
        # Disable hashing
        # return password

        hash_object = hashlib.sha256(bytes(password,encoding="UTF-8"))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    @classmethod
    def from_id(cls, sql, pkid):
        # SQL select statement to retrieve
        # the username and email
        sql.execute("SELECT * FROM profiles WHERE id=?;",(str(pkid),))
        pkid, user, hashed_pass, email = sql.fetchone()
        return cls(pkid,user,hashed_pass,email)


    @classmethod
    def from_user(cls, sql, username):
        sql.execute("SELECT * FROM profiles WHERE username=?;",(username,))
        pkid,user,hashed_pass,email=sql.fetchone()
        return cls(pkid,user,hashed_pass,email)

    @classmethod
    def register(cls,sql,username,password,email):
        if sql.execute("SELECT * FROM profiles WHERE username=? LIMIT 1;", (username,)).fetchone():
            raise ValueError("Registration error: Username {} is already taken.".format(username))
        if sql.execute("SELECT * FROM profiles WHERE email=? LIMIT 1;", (email,)).fetchone():
            raise ValueError("Registration error: Email {} is already used.".format(email))

        pkid = sql.execute("INSERT INTO profiles (username, password, email) VALUES (?,?,?)", (username,cls._hash(password),email)).lastrowid
        sql.commit()

        return cls(pkid, username, cls._hash(password), email)

    @classmethod
    def login(cls,sql,username,password):
        userdata = sql.execute("SELECT id,username,email FROM profiles WHERE username=? AND password=? LIMIT 1;",(username,cls._hash(password))).fetchone()
        if userdata:
            return cls(userdata[0],userdata[1],cls._hash(password),userdata[2])
        else:
            raise ValueError("Username {} does not exist or password is incorrect.".format(username))

#print(Profiles.login(__import__('databases.db').db(),"lolmemes","PianoTuner"))