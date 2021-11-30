import sqlite3 
import werkzeug


# Создание базы данных и настройки
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
    print("Err table insert")
finally:
    con.close()


try:
    con = sqlite3.connect('database.db')
    cursor=con.cursor()
    types = cursor.execute(""" SELECT "type"  FROM "types" """).fetchall()
    types_link=['private','public']
    #print(types)
    if not types:
        for i in range(len(types_link)):
            cursor.execute(""" INSERT INTO "types" (type) VALUES (?)
            """,(types_link[i],))
            con.commit()
except sqlite3.Error:
    print("Err table insert")
finally:
    con.close()


	
# id в лич. кабинете
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


# Вход в систему
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

# Получение никнейма. 

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


# Обновление никнейма

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




# Регистрация пользователя

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


# Get Types from "Types"
def getLinkTypes():
    try:
        con = sqlite3.connect('database.db')
        cursor=con.cursor()
        types = cursor.execute(""" SELECT *  FROM "types" """).fetchall()
        return types
    except sqlite3.Error:
        print("Err table insert")
    finally:
        con.close()



# Insert into links
def insertLink(userid,normal,short,count,type):
    try:
        con = sqlite3.connect('database.db')
        cursor=con.cursor()
        cursor.execute(""" INSERT INTO "links" (user_id,normal,short,count,typelink_id) VALUES (?,?,?,?,?)
        """,(userid,normal,short,count,type))
        con.commit()
    except sqlite3.Error:
        print("Err table insert")
    finally:
        con.close()


#Выдать ссылки пользователя по id

def getLinkByUserId(userid):
    try:
        con = sqlite3.connect('database.db')
        cursor=con.cursor()
        GetLinks = cursor.execute(""" SELECT * FROM "links" where "user_id"=?  """,(userid,)).fetchall()
        return GetLinks
    except sqlite3.Error:
        print("Err table select")
    finally:
        con.close()   
	

# Проверить существует ли уже ссылка у пользователя
def hasAlreadyLink(userid,url):
    try:
        con = sqlite3.connect('database.db')
        cursor=con.cursor()
        GetLinks = cursor.execute(""" SELECT * FROM "links" where "user_id"=? and "normal"=? """,(userid,url)).fetchall()
        if len(GetLinks)>0:
            return False
        else:
            return True
    except sqlite3.Error:
        print("Err table select")
    finally:
        con.close() 


