from flask import Flask, request, render_template, redirect, session, jsonify
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
from datetime import timedelta
import html
import secrets
import dicttoxml
import MySQLdb
import html
import json

def connect():
    con = MySQLdb.connect(
        host = "localhost",
        user = "root",
        password = "",
        db = "test",
        use_unicode = True,
        charset = "utf8")
    return con

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=60)

@app.route("/")
def one():
    return render_template("index.html")

@app.route("/make", methods=["GET", "POST"])
def make() :
    if request.method == "GET":
        return render_template("make.html")
    elif request.method == "POST":
        email = request.form["email"]
        passwd = request.form["passwd"]
        name = request.form["name"]
        sex = request.form["sex"]
        DateofBirth = request.form["DateofBirth"]
        hashpass = gph(passwd)
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT * FROM UserTable WHERE email=%(email)s 
                    """, {"email":email})
        data=[]
        for row in cur:
            data.append(row)
        if len(data)!=0:
            return render_template("make.html", msg="既に存在するメールアドレスです") 
        con.commit() 
        con.close()
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    INSERT INTO UserTable 
                    (email,password,name,sex,DateofBirth)
                    VALUES (%(email)s,%(hashpass)s,%(name)s,%(sex)s,%(DateofBirth)s)
                    """, {"email":email, "hashpass": hashpass, "sex":sex, "name": name, "DateofBirth":DateofBirth})
        con.commit()
        con.close()
        return render_template("info.html", email=email, passwd=passwd, name=name, sex=sex, DateofBirth=DateofBirth)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session.clear()
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form["email"]
        passwd = request.form["passwd"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT password,name,email,sex,DateofBirth,admin
                    FROM UserTable
                    WHERE email=%(email)s""",
                    {"email" : email})
        data=[]
        for row in cur:
            data.append([row[0],row[1],row[2],row[3],row[4],row[5]])
        if len(data)==0:
            con.close()
            return render_template("login.html", msg="IDが間違っています")
        if cph(data[0][0], passwd):
            session["name"] = data[0][1]
            session["email"] = data[0][2]
            session["sex"] = data[0][3]
            session["DateofBirth"] = data[0][4]
            session["admin"] = 0 if data[0][5] is None else data[0][5]
            con.close()
            return redirect("admin")
        else:
            con.close()
            return render_template("login.html", msg="パスワードが間違っています")
        
@app.route("/home")
def home():
    if "name" in session:
        if session["admin"] == 1:
            return render_template("success.html",
                                    name=html.escape(session ["name"]), 
                                    email=html.escape(session["email"]),
                                    sex=html.escape(session["sex"]),
                                    DateofBirth=html.escape(session["DateofBirth"]),
                                    admin="<a href=\"admin\">登録・検索</a>")
        else:
            return render_template("success.html",
                                name=html.escape(session["name"]),
                                email=html.escape(session["email"]), 
                                sex=html.escape(session["sex"]),
                                DateofBirth=html.escape(session["DateofBirth"]))
    else:
        return redirect("login")


@app.route("/admin")
def admin():
    if "admin" in session:
        if session["admin"] == 1:
            con = connect( )
            cur = con.cursor()
            cur.execute("""
                        SELECT name, email, sex, DateofBirth
                        FROM UserTable
                        """)
            res=""

            res = res + "<a href=\"makecredit\">合計所得単位登録</a>\n"
            res = res + "<a href=\"makesubject\">所得科目登録</a>\n"
            res = res + "<a href=\"webapi\">単位検索</a>\n"
            res = res + "<a href=\"webapi1\">科目検索</a>\n"
            
            for row in cur:
                res = res + "<table border=\"1\" align=\"center\">\n" 
                res = res + "\t<tr><td align=\"right\">名前</td><td>" + html.escape(row[0]) +"</td></tr>\n"
                res = res + "\t<tr><td align=\"right\">メールアドレス</td><td>" + html.escape(row[1]) +"</td></tr>\n"
                res = res + "\t<tr><td align=\"right\">性別</td><td>" + html.escape(row[2]) +"</td></tr>\n"
                res = res + "\t<tr><td align=\"right\">生年月日</td><td>" + html.escape(row[3]) +"</td></tr>\n"
                res = res + "</table>"

            con.close()
            return res
        else:
            return redirect("home")
    else:
        return redirect("login")


@app.route("/makecredit", methods=["GET", "POST"])
def makecredit() :
    if request.method == "GET":
        return render_template("makecredit.html")
    elif request.method == "POST":
        name=session["name"]
        grade = request.form["grade"]
        semester = request.form["semester"]
        credit = request.form["credit"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    INSERT INTO CreditTable 
                    (grade,semester,credit,name)
                    VALUES (%(grade)s,%(semester)s,%(credit)s,%(name)s)
                    """, {"grade":grade,"semester":semester,"credit":credit,"name":name})
        con.commit()
        con.close()
        return render_template("makecredit.html", msg="完了")

@app.route("/makesubject", methods=["GET", "POST"])
def makesubject() :
    if request.method == "GET":
        return render_template("makesubject.html")
    elif request.method == "POST":
        name=session["name"]
        subjectname = request.form["subjectname"]
        type = request.form["type"]
        credit = request.form["credit"]
        grade = request.form["grade"]
        semester = request.form["semester"]
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    INSERT INTO SubjectTable 
                    (subjectname,type,credit,grade,semester,name)
                    VALUES (%(subjectname)s,%(type)s,%(credit)s,%(grade)s,%(semester)s,%(name)s)""", 
                    {"subjectname":subjectname,"type":type,"credit":credit,"grade":grade,"semester":semester,"name":name})
        con.commit()
        con.close()
        return render_template("makesubject.html", msg="完了")

@app.route("/webapi")
def webapi2():
    return render_template("search.html")

@app.route("/webapi1")
def webapi3():
    return render_template("search1.html")

@app.route("/api")
def api2():
    num = request.args.get("name")
    form = request.args.get("format")
    con = connect()
    cur = con.cursor()
    cur.execute("""
                SELECT grade,semester,credit
                FROM credittable
                WHERE name=%(id)s
                """,{"id" : num})

    res = {}
    tmpa=[]
    for row in cur:
        tmpd={}
        tmpd["grade"] = row[0]
        tmpd["semester"] = row[1]
        tmpd["credit"] = row[2]
        tmpa.append(tmpd)

    res["content"] = tmpa
    if form == "XML":
        xml = dicttoxml.dicttoxml(res)
        resp = app.make_response(xml)
        resp.mimetype = "text/xml"
        return resp
    else:
        res = json.dumps(res,indent=2,ensure_ascii=False)
        return res

@app.route("/api1")
def api3():
    name = request.args.get("name")
    form = request.args.get("format")
    con = connect()
    cur = con.cursor()
    cur = con.cursor()
    cur.execute("""
                SELECT name,subjectname,type,credit,grade,semester
                FROM subjecttable
                WHERE name=%(id)s
                """,{"id" : name})

    res = {}
    tmpa=[]
    for row in cur:
        tmpd = {}
        tmpd["name"] = row[0]
        tmpd["subjectname"] = row[1]
        tmpd["type"] = row[2]
        tmpd["credit"] = row[3]
        tmpd["grade"] = row[4]  
        tmpd["semester"] = row[5]  
        tmpa.append(tmpd)

    res["content"] = tmpa
    if form == "XML":
        xml = dicttoxml.dicttoxml(res)
        resp = app.make_response(xml)
        resp.mimetype = "text/xml"
        return resp
    else:
        res = json.dumps(res,indent=2,ensure_ascii=False)
        return res


@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0")