import os
import bd
import shorteners as shortURL
from flask import Flask,request,render_template, session,url_for,redirect,jsonify
import werkzeug





app = Flask(__name__,template_folder='templates')
app.secret_key="session_start"
@app.route("/")
def hello_world():
    auth=False
    if "id" in session and "auth":
        auth=True
    return render_template("index.html",auth=auth)

@app.route("/protoShort")
def ProtoPage():
    auth=False
    if "id" in session and "auth":
        auth=True
    return render_template("proto.html",auth=auth)

@app.route('/protoShort', methods=['POST'])
def proto():
    shorty=""
    auth=False
    if "id" in session and "auth":
        auth=True
    if request.method == 'POST':
            a = request.form.get('url')
            url=str(a).replace(" ","")
            if len(url)>8:
                resp=shortURL.getShortURL(url)
                if resp:
                    shorty= f"{resp}"
                else: shorty="К сожалению произошла ошибка. И ссылку не удалось отработать"
            else: shorty="Ссылка очень маленькая. Она должна быть больше 8 символов"
            
    return render_template("proto.html",link=shorty,auth=auth)
    



@app.route("/enter")
def AuthPage():
    AuthErr=""
    email=""
    password=""
    return render_template("auth.html",email=email,password=password,error=AuthErr)

@app.route("/enter",  methods=['POST'])
def auth():
    request_data = request.get_json()
    if request_data:
        if 'email' in request_data:
            email = request_data['email']

        if 'password' in request_data:
            password = request_data['password']

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hasUser= bd.selectUser(email,password)
        print(hasUser)
        if hasUser:
            session["auth"]=True
            session["id"]=bd.selectUserID(email)
            return redirect(url_for("DeskPage"))
        else:
            session.pop("auth",None)
            AuthErr="Не правильно веден пароль или почта"
            return render_template('auth.html',email=email,password=password,error=AuthErr)
    else:
        session.pop("auth",None)
        AuthErr="Простите. Но произошла ошибка."
        return render_template('auth.html',email="",password="",error=AuthErr)


@app.route("/regin")
def ReginPage():
    ReginErr=""
    email=""
    password=""
    return render_template("regin.html",email=email,password=password,error=ReginErr)

@app.route("/regin",  methods=['POST'])
def regin():
    request_data = request.get_json()
    if request_data:
        if 'email' in request_data:
            email = request_data['email']

        if 'password' in request_data:
            password = request_data['password']

    if request.method == 'POST':
        email = request.form.get('email')
        password_v = request.form.get('password')
        password = werkzeug.security.generate_password_hash(password_v, method='pbkdf2:sha256', salt_length=16)
        insertUser= bd.insertUser(email,password," ")
        print(insertUser)
        if insertUser:
            session["auth"]=True
            return redirect(url_for("DeskPage"))
        else:
            ReginErr="Пользователь с такой почтой уже есть в сети."
            return render_template('regin.html',email="",password="",error=ReginErr)
    else:
        ReginErr="Простите. Но произошла ошибка."
        return render_template('regin.html',email="",password="",error=ReginErr)




@app.route("/answer")
def AnswerPage():
    auth=False
    if "id" in session and "auth":
        auth=True
    return render_template("answer.html",auth=auth)


@app.route('/seetings')
def SettingsPage():
    nickname=""
    if "id" in session:
        nickname=bd.getUserName(session["id"])
    
    return render_template("settings.html",nickname=nickname)


@app.route('/seetings', methods=['POST'])
def changeNick():
    request_data = request.get_json()
    if request_data:
        if 'nick' in request_data:
            nick = request_data['nick']

    if request.method == 'POST':
        nick = request.form.get('nick')
        if "id" in session:
            bd.updateNick(session["id"],nick)
            return redirect(url_for("DeskPage"))
    else:
        return render_template("settings.html",nickname="")



@app.route('/desktop')
def DeskPage():
    nickname=""
    links=False
    if "id" in session and "auth" in session and session["auth"]:
        links=bd.getLinkByUserId(session["id"])
        nickname=bd.getUserName(session["id"])
        #print(nickname)
        return render_template("start.html",nickname=nickname,linksHas=links)
    else: 
        return redirect(url_for("AuthPage"))
    


 

@app.route('/shortlink')
def ShortPage():
    if "auth" in session and session["auth"]:
        types=bd.getLinkTypes()

        return render_template("short.html",len=len(types), types=types,res=None,link=None,errors=None)
    else:
        return redirect(url_for("AuthPage"))


		
@app.route('/shortlink', methods=['POST'])
def Page():
    shorty=""
    resText=""
    error=""
    name=bd.getUserName(session["id"])
    types=bd.getLinkTypes()
    if request.method == 'POST':
        a = request.form.get('url')
        type = request.form.get('type')
        save = request.form.get('isSave')
            
        url=str(a).replace(" ","")
        if len(url)>8:
            resp=shortURL.getShortURL(url)
            if resp:
                shorty=resp
                if not bd.hasAlreadyLink(session["id"],url) and save:               
                    bd.insertLink(session["id"],url,shorty,0,type)
                    getlink=bd.hasAlreadyLink(session["id"],url)
                    #print(private)
                    Links=f"http://127.0.0.1:5002/checker/{getlink[0][0]}"
                    shorty=shortURL.getShortURL(Links)
                    resText=shorty
                    shorty=shorty+f":{name}"
                else:
                    shorty=shortURL.getShortURL(f"http://127.0.0.1:5002/checkerNotSaved/{resp[-8:]}+{type}")
                    resText=shorty
            else: error="К сожалению произошла ошибка. И ссылку не удалось отработать"
        else: error="Ссылка очень маленькая. Она должна быть больше 8 символов"
    return render_template("short.html",len=len(types), types=types,res=resText,link=shorty,errors=error)


@app.route('/links')
def LinksPage():
    name=bd.getUserName(session["id"])
    fakelink=[]
    if "auth" in session and session["auth"]:
        types=bd.getLinkTypes()
        links=bd.getLinkByUserId(session["id"])
        if len(links)>0:
            for i in range(len(links)):
                fakelink.append(shortURL.getShortURL(f"http://127.0.0.1:5002/checker/{links[i][0]}"))
            return render_template("links.html",len=len(links),linkname=fakelink,links=links,types=types,name=name)
        else: 
            return redirect(url_for('DeskPage'))
    else:
        return redirect(url_for("AuthPage"))


@app.route('/links', methods=['POST'])
def DeleteLink():
    if "auth" in session and session["auth"]:
        if request.method == 'POST':
            id = request.form.get('id')
            bd.deleteLink(id,session["id"])
            return redirect(url_for('LinksPage'))
    else:
        return redirect(url_for("AuthPage"))


@app.route('/checker/<int:id>')
def SavedLinks(id):
    link=bd.getLinkById(id)
    print(link)
    if link[0]==1 or link[0]==3:
        if "auth" in session and session["auth"]:
            count=int(link[2])+1
            bd.updateLinkCountStatus(id,count)
            return redirect(link[1])
        else:
            return redirect(url_for("AuthPage"))
    elif link[0]==2:
        count=int(link[2])+1
        bd.updateLinkCountStatus(id,count)
        return redirect(link[1])

@app.route('/checkerNotSaved/<string>')
def notSavedLinks(string):
    inter = int(string[9])
    link=f"https://tinyurl.com/{string[0:8]}"
    if inter==1 or inter==3:
        if "auth" in session and session["auth"]:
            return redirect(link)
        else:
            return redirect(url_for("AuthPage"))
    else:
        return redirect(link)

@app.route('/edit/<id>')
def EditLinkPage(id):
    if "auth" in session and session["auth"] and bd.getLinkByUserId(session["id"]):
        types=bd.getLinkTypes()
        link=bd.getLinkById(id)
        checked=[]
        for i in range(len(types)):
            if link[0]== types[i][0]:
                checked.append("checked")
            else: checked.append("")

        print(bd.getLinkById(id))
        return render_template("edit.html",len=len(types),original=link[3],checked=checked,types=types,res=None,link=None,errors=None)
    else:
        return redirect(url_for("Out"))

		
@app.route('/edit/<id>', methods=['POST'])
def EditLink(id):
    shorty=""
    resText=""
    error=""
    count=0
    checked=[]
    name=bd.getUserName(session["id"])
    types=bd.getLinkTypes()
    if request.method == 'POST':
        a = request.form.get('url')
        type = request.form.get('type')

        
            
        url=str(a).replace(" ","")

        if  bd.hasAlreadyLink(session["id"],url):
            count=int(bd.getLinkById(id)[2])

        if len(url)>8:
            resp=shortURL.getShortURL(url)
            print(url)
            if resp:
                shorty=resp
                               
                bd.updateLink(id,url,shorty,type,count)
                Links=f"http://127.0.0.1:5002/checker/{id}"
                shorty=shortURL.getShortURL(Links)
                resText=shorty
                shorty=shorty+f":{name}"
                link=bd.getLinkById(id)
                for i in range(len(types)):
                    if link[0]== types[i][0]:
                        checked.append("checked")
                    else: checked.append(" ")
                
            else: error="К сожалению произошла ошибка. И ссылку не удалось отработать"
        else: error="Ссылка очень маленькая. Она должна быть больше 8 символов"
    return render_template("edit.html",len=len(types),original=url,checked=checked,types=types,res=resText,link=shorty,errors=error)




@app.route('/out')
def Out():
    session.clear()
    return redirect(url_for("hello_world"))


if __name__=="__main__":       
    app.run(debug=True,port=5002)
