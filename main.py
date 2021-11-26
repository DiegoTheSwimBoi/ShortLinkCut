import os
import bd
import shorteners as shortURL
from flask import Flask,request,render_template, session,url_for,redirect,jsonify
import werkzeug



app = Flask(__name__,template_folder='templates')
app.secret_key="session_start"
@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/protoShort")
def ProtoPage():
    return render_template("proto.html")

@app.route('/protoShort', methods=['POST'])
def proto():
    request_data = request.get_json()
    if request_data:
        if 'url' in request_data:
            url = request_data['url']

            print(url)

        if request.method == 'POST':
            a = request.form.get('url')
            url=str(a).replace(" ","")
            if len(url)>8:
                resp=shortURL.getShortURL(url)
                if resp:
                    session["responsed"]= f"{resp}"
                else: session["responsed"]="К сожалению произошла ошибка. И ссылку не удалось отработать"
            else: session["responsed"]="Ссылка очень маленькая. Она должна быть больше 8 символов"
            
    return render_template("proto.html",link=session["responsed"])



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
        if int(hasUser)>0:
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
        if insertUser>0:
            session["auth"]=True
            return redirect(url_for("DeskPage"))
    else:
        ReginErr="Простите. Но произошла ошибка."
        return render_template('regin.html',email="",password="",error=ReginErr)




@app.route("/answer")
def AnswerPage():
    return render_template("answer.html")


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
    if "id" in session and "auth" in session and session["auth"]:
        nickname=bd.getUserName(session["id"])
        #print(nickname)
        return render_template("start.html",nickname=nickname)
    else: 
        return redirect(url_for("AuthPage"))
    

 

@app.route('/shortlink')
def ShortPage():
    if "auth" in session and session["auth"]:
        return render_template("short.html")
    else:
        return redirect(url_for("AuthPage"))

@app.route('/shortlink', methods=['POST'])
def Page():
    request_data = request.get_json()
    if request_data:
        if 'url' in request_data:
            url = request_data['url']

            print(url)

        if request.method == 'POST':
            a = request.form.get('url')
            url=str(a).replace(" ","")
            if len(url)>8:
                resp=shortURL.getShortURL(url)
                if resp:
                    session["responsed"]= f"{resp}"
                else: session["responsed"]="К сожалению произошла ошибка. И ссылку не удалось отработать"
            else: session["responsed"]="Ссылка очень маленькая. Она должна быть больше 8 символов"
            
    return render_template("short.html",link=session["responsed"])


if __name__=="__main__":       
    app.run(debug=True,port=5002)
