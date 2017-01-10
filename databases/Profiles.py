import sqlite3, hashlib, random
import db

class Profiles(object):
    def __init__(self,pkid,user,hashed_pass,email):
        self._id=pkid
        self.user=user
        self.hashed_pass=hashed_pass
        self.email=email

    def __repr__(self):
        return "Profiles({},{},{},{})".format(self._id,self.user,self.hashed_pass,self.email)

    def __str__(self):
        return "Profile id {} with username: {}, hashed pass: {}, email: {}".format(self._id,self.user,self.hashed_pass,self.email)

    @staticmethod
    def _hash(password):
        # Disable hashing
        # return password

        hash_object = hashlib.sha256(bytes(password,encoding="UTF-8"))
        hex_dig = hash_object.hexdigest()
        return hex_dig;

    @classmethod
    def from_id(cls, pkid):
        # SQL select statement to retrieve
        # the username and email
        conn=sqlite3.connect("data.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE id=?;",(str(pkid),))
        pkid, user, hashed_pass, email = cur.fetchone()
        conn.close()
        return cls(pkid,user,hashed_pass,email)


    @classmethod
    def from_user(cls, username):
        conn=sqlite3.connect("data.db");
        cur=conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE username=?;",(username,))
        row=cur.fetchone()
        conn.close()
        pkid,user,hashed_pass,email=row
        return cls(pkid,user,hashed_pass,email)

    @classmethod
    def register(cls,username,password,email):
        conn=sqlite3.connect("data.db");
        cur=conn.cursor()
        if cur.execute("SELECT * FROM profiles WHERE username=? LIMIT 1;", (username,)).fetchone():
            raise ValueError("Registration error: Username {} is already taken.".format(username))
        if cur.execute("SELECT * FROM profiles WHERE email=? LIMIT 1;", (email,)).fetchone():
            raise ValueError("Registration error: Email {} is already used.".format(email))

        pkid = random.getrandbits(32)
        while cur.execute("SELECT * FROM profiles WHERE id=?", (pkid,)).fetchone():
            pkid = random.getrandbits(32)
        cur.execute("INSERT INTO profiles VALUES (?,?,?,?)", (pkid,username,cls._hash(password),email))
        conn.commit()
        conn.close()

        return cls(pkid, username, cls._hash(password), email)

    @classmethod
    def login(cls,username,password):
        conn=sqlite3.connect("data.db")
        cur=conn.cursor()
        userdata = cur.execute("SELECT id,username,email FROM profiles WHERE username=? AND password=? LIMIT 1;",(username,cls._hash(password))).fetchone()
        if userdata:
            return cls(userdata[0],userdata[1],cls._hash(password),userdata[2])
        else:
            raise ValueError("Username {} does not exist or password is incorrect.".format(username));