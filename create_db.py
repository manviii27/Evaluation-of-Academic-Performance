import sqlite3 #in-built library to create a database without 3rd party software
def create_db():
    con=sqlite3.connect(database="rms.db")
    cur=con.cursor()
    cur.execute("Create Table if not exists course(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, sem INTEGER, charges text, desc text)")
    con.commit()
    cur.execute("Create Table if not exists student(id INTEGER PRIMARY KEY AUTOINCREMENT, sid text, name text, rollno text, email text, gender text, dob date, course text, sem integer)")
    con.commit()
    cur.execute("Create Table if not exists subject(id INTEGER PRIMARY KEY AUTOINCREMENT, subid text, name text, sem INTEGER, course text)")
    con.commit()
    cur.execute("Create Table if not exists result(id INTEGER PRIMARY KEY AUTOINCREMENT, rollno text, name text, subid text, cname text, marks INTEGER)")
    con.commit()
create_db()