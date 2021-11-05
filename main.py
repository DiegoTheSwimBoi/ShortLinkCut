import bd
import shorteners as shortURL
from flask import Flask,request,render_template, session,url_for,redirect,jsonify



app = Flask(__name__,template_folder='templates')
app.secret_key="session_start"
@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/enter")
def AuthPage():
    return render_template("auth.html")

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
        if hasUser>0:
            session["auth"]=True
            return render_template('start.html')
        else:
            session.pop("auth",None)
            return render_template('auth.html')
    else:
        session.pop("auth",None)
        return render_template('auth.html')


@app.route("/regin")
def ReginPage():
    return render_template("regin.html")

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
        password = request.form.get('password')
        insertUser= bd.insertUser(email,password)
        print(insertUser)
        if insertUser>0:
            session["auth"]=True
            return render_template('start.html')
        else:
            return render_template('regin.html')
    else:
        return render_template('regin.html')




@app.route("/answer")
def AnswerPage():
    return render_template("answer.html")


@app.route("/response", methods=['POST','GET'])
def response():
    s=""
    if "auth" in session:
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
            
            return redirect(f"responsed")
                



@app.route('/responsed')
def responsed():
    if "responsed" in session:
        resp=session["responsed"]
        return f"<h1>{resp}</h1>"


if __name__=="__main__":       
    app.run(debug=True,port=5002)
