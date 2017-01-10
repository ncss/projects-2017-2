import sqlite3
conn = None
cur  = None
def open():
    global conn,cur
    conn=sqlite3.connect("data.db")
    cur=conn.cursor();
    return cur

def close():
    global conn,cur
    conn.close();
    return

def execute(s,args=()):
    return cur.execute(s,args)

if __name__=="__main__":
    open()
    execute("INSERT INTO profiles VALUES (1234, 'testmeme', 'somesortofhashquestionmark', 'd@d.com');")
    print(execute("SELECT * FROM profiles").fetchall())