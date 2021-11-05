import sqlite3 

try:
    con = sqlite3.connect('database.db')
    cursor=con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
	    "id"	INTEGER NOT NULL,
	    "email"	TEXT NOT NULL,
        "password"	TEXT NOT NULL,
	    PRIMARY KEY("id" AUTOINCREMENT)
        );
        """)
    con.commit()
except sqlite3.Error:
    print("Err table create")
finally:
    con.close()


def selectUser(email,password):
    try:
        con = sqlite3.connect("database.db")
        
        cursor=con.cursor()

        GetUser = cursor.execute(""" SELECT "email" FROM "users" where "email"=? AND "password"=? """,(email,password,)).fetchall()
        if(len(GetUser)>0):
            return 1
        else:
            return -1       
    except sqlite3.Error:
        print("No")
    finally:
        con.close() 


def insertUser(email,password):
    try:
        con = sqlite3.connect("database.db")
        
        cursor=con.cursor()
        print('good')
        GetUser = cursor.execute(""" SELECT "email" FROM "users" where "email"=?  """,(email,)).fetchall()
        
        if(len(GetUser)==0):
            cursor.execute(""" INSERT INTO "users" (email,password) VALUES (?,?)
            """,(email,password))
            con.commit()
            return 1
        else:
            return -1
    except sqlite3.Error:
        print("No")
    finally:
        con.close() 



#print(insertUser("dj@.gmail.com","ASD"))