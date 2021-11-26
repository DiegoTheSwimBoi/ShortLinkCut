import sqlite3 
import werkzeug

try:
    con = sqlite3.connect('database.db')
    cursor=con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
	    "id"	INTEGER NOT NULL,
	    "email"	TEXT NOT NULL,
        "password"	TEXT NOT NULL,
        "nickname" TEXT NOT NULL,
	    PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)
    con.commit()
except sqlite3.Error:
    print("Err table create")
finally:
    con.close()

	

try:
    con = sqlite3.connect('database.db')
    cursor=con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "links" (
	    "id"	INTEGER NOT NULL,
        "user_id"	INTEGER NOT NULL,
	    "normal"	TEXT NOT NULL,
        "short"	TEXT NOT NULL,
        "count"	INTEGER NOT NULL,
		"typelink_id"	INTEGER NOT NULL,
	    PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)
    con.commit()
except sqlite3.Error:
    print("Err table create")
finally:
    con.close()
	

try:
    con = sqlite3.connect('database.db')
    cursor=con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "types" (
	    "id"	INTEGER NOT NULL,
	    "type"	TEXT NOT NULL,
	    PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)
    con.commit()
except sqlite3.Error:
    print("Err table create")
finally:
    con.close()

	

def selectUserID(email):
    try:
        con = sqlite3.connect("database.db")
        
        cursor=con.cursor()

        UserId = cursor.execute(""" SELECT "id" FROM "users" where "email"=? """,(email,)).fetchone()
        if(len(UserId)>0):
            return UserId[0]
        else:
            return 0       
    except sqlite3.Error:
        return 0
    finally:
        con.close() 

def selectUser(email,password):
    try:
        con = sqlite3.connect("database.db")
        
        cursor=con.cursor()

        GetPassword=cursor.execute(""" SELECT "password" FROM "users" where "email"=? """,(email,)).fetchone()
        print(werkzeug.security.check_password_hash(GetPassword[0], password))
        if (werkzeug.security.check_password_hash(GetPassword[0], password)):
            return 1
        else:
            return -1       
    except sqlite3.Error:
        print("No")
        return -2
    finally:
        con.close() 

def getUserName(id):
    try:
        con = sqlite3.connect("database.db")
        
        cursor=con.cursor()
        print('good')
        nick = cursor.execute(""" SELECT "nickname" FROM "users" where "id"=?  """,(id,)).fetchone()
        
        return nick[0]
    except sqlite3.Error:
        return -1
    finally:
        con.close() 


def updateNick(id,nickname):
    try:
        con = sqlite3.connect("database.db")
        
        cursor=con.cursor()
        #print('good')

        cursor.execute(""" UPDATE "users" SET "nickname"=? where "id"=?  """,(nickname,id))

        con.commit()
    except sqlite3.Error:
        return -1
    finally:
        con.close() 

def insertUser(email,password,nick):
    try:
        con = sqlite3.connect("database.db")
        
        cursor=con.cursor()
        print('good')
        GetUser = cursor.execute(""" SELECT "email" FROM "users" where "email"=?  """,(email,)).fetchall()
        print("Arr len")
        print(len(GetUser))
        if(len(GetUser)==0):
            cursor.execute(""" INSERT INTO "users" (email,password,nickname) VALUES (?,?,?)
            """,(email,password,nick))
            con.commit()
            return 1
        else:
            return -1
    except sqlite3.Error:
        return -2
    finally:
        con.close() 




