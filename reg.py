@app.route("/make", methods=["GET", "POST"])
def make() :
    if request.method == "GET":
        return render_template("make.html")
    elif request.method == "POST":
        email = request.form["email"]
        passwd = request. form[ "passwd" ]
        name = request.form[ "name" ]
        tel = request. form["tel"]
        hashpass = gph(passwd)
        con = connect()
        cur = con.cursor()
        cur.execute("""
                    SELECT * FROM users WHERE email=%(email)s 
                    """, {"email":email})

data=[]
for row in cur:
    data.append(row)
if len(data)!=0:
    return render_template("make.htmI", msg="既に存在するメールアドレスです") 
con.commit() 
con.close()
con = connect()
cur = con.cursor()
cur.execute("""
            INSERT INTO users 
            (email, passwd, tel, name)
            VALUES (%(email)s,%(hashpass)s,%(tel)s,%(name)s)
            """, {"email":email, "hashpass": hashpass, "tel":tel, "name": name})
con.commit()
con.close()
return render_template("info.html", email=email, passwd=passwd, name=name, tel=tel)