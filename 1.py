import MySQLdb

def connect():
    con = MySQLdb.connect(
        host = "localhost",
        user = "root",
        password = "toaruKAGAKU",
        db = "test",
        use_unicode = True,
        charset = "utf8")
    return con

con = connect()

cur = con.cursor()

'''
cur.execute("""
            CREATE TABLE test.UserTable
            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
            DateofBirth VARCHAR(30),
            sex CHAR(1),
            password VARCHAR(30),
            PRIMARY KEY(id))
            """)        


cur.execute("""
            CREATE TABLE test.CreditTable
            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
            grade int(1),
            semester char(1),
            credit int(3),
            PRIMARY KEY(id))
            """)

cur.execute("""
            CREATE TABLE test.SubjectTable
            (id MEDIUMINT NOT NULL AUTO_INCREMENT,
            subjectname VARCHAR(30),
            type VARCHAR(10),
            credit int(1),
            grade int(1),
            PRIMARY KEY(id))
            """)
'''

con.commit()

con.close()
