from flask import Flask, request, render_template, redirect, session
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
from datetime import timedelta
import html
import secrets
import MySQLdb

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
app.permanent_session_lifetime = timedelta(minutes=60)

def connect():
    con = MySQLdb.connect(
        host = "localhost",
        user = "root",
        password = "",
        db = "test",
        use_unicode = True,
        charset = "utf8")
    return con


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
        return render_template ("login.html")
    elif request.method == "POST":
        email = request.form["email"]
        passwd = request.form["passwd"] 
        con = connect ()
        cur = con.cursor()
        cur.execute("""
                    SELECT password,name,email,sex,DateofBirth,admin
                    FROM UserTable
                    WHERE email=%(email)s
                    """,{"email": email})
    data=[]
    for row in cur:
        data.append ([row[0],row[1],row[2],row[3],row[4],row[5]])
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
        return redirect("home")
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
                                    tel=html.escape (session["tel"]),
                                    admin="<a href=\"admin\">ユーザ情報一覧</a>")
        else:
            return render_template("success.html",
                                name=html.escape(session["name"]),
                                email=html.escape(session["email"]), 
                                tel=html.escape(session["tel"]))
    else:
        return redirect ("login")


@app.route("/admin")
def admin():
    if "admin" in session:
        if session["admin"] == 1:
            con = connect( )
            cur = con.cursor()
            cur.execute("""
                        SELECT name, email, tel
                        FROM users
                        """)
            res=""
            for row in cur:
                res = res + "<table border=\"1\" align=\"center\">\n"
                res = res + "\t<tr><td align=\"right\">名前</td><td>" + html.escape(row[0]) + "</td><td>\n"
                res = res + "\t<tr><td align=\"right\">メールアドレス</td><td>" + html.escape(row[1]) + "</td></tr>\n"
                res = res + "\t<tr><td align=\"right\">電話番号</td><td>" + + html.escape(row[2]) + "</td></tr>\n"
                res = res + "</table>"
            con.close()
            return res
        else:
            return redirect("home")
    else:
        return redirect("login")


if __name__ == "__main__":
    app.run(host="0.0.0.0")