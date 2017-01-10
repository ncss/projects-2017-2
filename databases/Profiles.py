import sqlite3
class Profiles(object):
    def __init__(self,pkid,user,email):
        self._id=pkid
        self.user=user
        self.email=email

    @classmethod
    def from_id(cls, pkid):
        # SQL select statement to retrieve
        # the username and email
        conn=sqlite3.connect("data.db");
        cur=conn.cursor();
        cur.execute("SELECT * FROM profiles WHERE id="+str(pkid));
        row=cur.fetchone();
        print(row)
        conn.close()
        pkid,user,email=(i for i in row)
        return Profiles(pkid,user,email)


    @classmethod
    def from_user(cls, username):
        conn=sqlite3.connect("data.db");
        cur=conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE user="+str(username));
        row=cur.fetchone()
        conn.close()
        pkid,user,email=(i for i in row)
        return Profiles(pkid,user,email);

p=Profiles(1,"Viney","vineyk24@gmail.com");

p.from_id(1);

