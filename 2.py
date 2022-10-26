import MySQLdb

con = MySQLdb.connect(
    host = "localhost",
    user = "root",
    password = "toaruKAGAKU",
    db = "test",
    use_unicode = True,
    charset = "utf8")

cur = con.cursor()

'''
cur.execute("""INSERT INTO UserTable
            (DateofBirth,sex,password)
            VALUES ('2002/2/8', 'M', '****')""")    
            
cur.execute("""INSERT INTO CreditTable
            (grade,semester,credit)
            VALUES (3, 'F', 114)""") 
'''

cur.execute("""INSERT INTO SubjectTable
            (subjectname,type,credit,grade)
            VALUES ('PBL', 'required', 2, 3)""")    

con.commit()

con.close()
