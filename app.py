import json
from sys import argv
from bottle import route,run,template, static_file,request,redirect,response,get



@get("/static/<styles:re:.*\.css>")
def css(styles):
    return static_file(styles, root="./static")

@get('/myndir/<mynd>')
def static(mynd):
    return static_file(mynd, root='./myndir')


@route("/")
def home():
    if request.get_cookie("visited"):
        hallo = request.get_cookie("visited")
        print(hallo)
        nota = hallo.split(";")
        global nafn
        global pas
        nafn = nota[0]
        pas = nota[1]
        return template("index3.tpl",a = "Cookie",n = nafn,p = pas)
    else:
        return template("index.tpl")

@route("/eyda")
def eyda():
    return '''
        <link rel="stylesheet" type="text/css" href="./static/style4.css">
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br> 
        <h1>Ertu Viss?</h1>
        <form action="/dele" method="POST">
        <input type = "submit" name = "login" value = "Eyða" />
        </form>
        <a href="/" title="Til baka" id="arrow">&#x21E7;</a>
</body>
    '''
@route("/dele", method = "POST")
def dele():
    with open("users.txt","r") as f:
        users = f.read()
        users = users.strip()
        users = users.split(",")
        global nafn
        global pas
        forU = users
        for a in forU:
            user = a.split(":")
            if nafn == user[0]:
                if pas == user[1]:
                    users.remove(nafn + ":" + pas)
    txt = ""
    tel = 0
    for a in users:
        tel += 1
        if tel == len(users):
            txt = txt + a
        else:
            txt = txt + a + ","
    with open("users.txt", "w") as f:
        f.write(txt)
    redirect("/del")
@route("/login", method = 'POST')
def index():

    username = request.forms.get('notendanafn')
    password = request.forms.get('lykilord')

    with open("users.txt","r") as f:
        users = f.read()
        users = users.strip()
        users = users.split(",")
        login = False
        for a in users:
            user = a.split(":")
            if username == user[0]:
                if password == user[1]:
                    global nafn
                    global pas
                    nafn = username
                    pas = password
                    login = True
        if login == True:
            nota = nafn+";"+pas
            response.set_cookie("visited",nota)
            return template("index3.tpl",a = "Login",n = nafn,p = pas)
        else:
            redirect('http://localhost:8080/')
@route("/del")
def delcookie():
    response.set_cookie("visited", "", expires=0)
    return '''<h1>Cookie deleted</h1>
    <a href="/">Go to Log in</a>'''
@route("/lykil")
def lykil():

    return template('index5.tpl')
@route("/skra", method = "POST")
def skra():

    username = request.forms.get('notendanafn')
    password = request.forms.get('lykilord')

    with open("users.txt", "a") as f:
        user = ","+username+":"+password
        f.write(user)
    return '''
        <h1>Notanda hefur verið bætt við</h1>
           <a href="/">Til baka</a>
    '''
@route("/not")
def notandi():
    return template('index4.tpl')

@route("/breyta")
def breyta():
    return  template('index5.tpl')
@route('/breyt',method = "POST")
def breyt():
    lykilord = request.forms.get('lykilord')
    with open("users.txt","r") as f:
        users = f.read()
        users = users.strip()
        users = users.split(",")
        forU = users
        for a in forU:
            user = a.split(":")
            if user[0] == nafn:
                if user[1] == pas:
                    users.remove(nafn+":"+pas)
                    users.append(nafn+":"+lykilord)
                    response.set_cookie("visited",nafn+";"+lykilord)

    txt = ""
    tel = 0
    for a in users:
        tel+=1
        if tel == len(users):
            txt=txt+a
        else:
            txt = txt+a+","
    print(users)
    with open("users.txt","w") as f:
        f.write(txt)
    return '''
        <h1>Notanda hefur verið breytt</h1>
           <a href="/">Til baka</a>
    '''


@route("/bilar",method = "GET")
def bilar():
    ioStream = open('myndir.json', 'r', encoding='utf-8')
    dData = json.load(ioStream)
    ioStream.close()
    return template('index2.tpl',gogn = dData)
"run(host='localhost', port=8080, debug=True, Realoader=True)"
#run(host='0.0.0.0', port=argv[1])
run()