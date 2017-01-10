import sqlite3

conn = None
isopen = False

def open():
    global conn,isopen
    conn = sqlite3.connect("data.db")
    isopen = True

def close():
    global conn
    conn.close()

class db():
    def __init__(self):
        if isopen is False:
            open()
        self.cur = conn.cursor()

    def commit(self):
        conn.commit()

    def __getattr__(self, item):
        return self.cur.__getattribute__(item)

    def __iter__(self):
        return self.cur.__iter__()

if __name__ == "__main__":
    x = db()
    x.execute("INSERT INTO profiles VALUES (1234, 'testmeme', 'somesortofhashquestionmark', 'd@d.com');")
    print(x.execute("SELECT * FROM profiles").fetchall())
    for e in x:
        print(e)
    x.commit()
    x.close()