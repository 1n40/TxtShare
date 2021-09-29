from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import hashlib
app = Flask(__name__)



# API for master page where an identification hash is passed
@app.route('/master', methods=['GET'])
def master():
    co = request.headers.get('Cookie')
    if co[co.find("id="):co.find("id=")+67].replace("id=","") == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918":        # Hash of admin password
        con = sqlite3.connect('sug.db')
        cur = con.cursor()
        cur.execute('insert into status(id, stat) values("8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918","NO");')
        con.commit()
        con.close()
        return render_template('master.htm')
    else:
        return render_template('index.htm')



# API for user page
@app.route('/user', methods=['GET'])
def user():
    return render_template('user.htm')



# Login Page with initilalization of tables; users, status and suggestions
@app.route('/')
def home():
    con = sqlite3.connect("sug.db")
    cur = con.cursor()
    cur.execute("""create table if not exists sug(name varchar(10) NOT NULL, mes varchar(2000) NOT NULL);""")
    cur.execute("""create table if not exists users(id varchar(10) NOT NULL, pass varchar(256) NOT NULL);""")
    cur.execute('create table if not exists status(stat varchar(3) NOT NULL);')
    con.commit()
    con.close()
    return render_template('index.htm')



# Authentication API
@app.route('/auth', methods=['POST'])
def aut():
    if request.method == "POST":
        nos = request.data.decode()   # id&passwd
        print(nos)
        cred = nos.split("&")
        print(cred)
        
        usr = cred[0]
        passwd = cred[-1]
        passwd = str(hashlib.sha256(passwd.encode()).hexdigest())
        
        print(passwd)
        con = sqlite3.connect("sug.db")
        cur = con.cursor()
        try:
            cur.execute("select id from users where pass=:pas;",{"pas": passwd})
            
            ans = cur.fetchone()[0]
            con.close()
            
            if ans == usr:
                if usr == "admin":
                    return passwd+"master"
                else:
                    return passwd+"user"
            else:
                return "false"
        except TypeError:
            print("Oops!")



# A read API to get the data from the document.
@app.route('/read', methods=['GET'])
def docu():
    ro = os.getcwd() + "\\project1\\doc.txt"
    x = ""
    with open(ro, "r") as fil:
        x = fil.read()
    return x



# API to update the resource. (MASTER)
@app.route('/update', methods=['POST','GET'])
def upd():
    if request.method == 'POST':
        he = request.data.decode()
        ro = os.getcwd() + "\\project1\\doc.txt"
        x = ""
        with open(ro, "w") as fil:
            x = fil.write(he)
        return "successfull!"
    else:
        return docu()


# API for suggestions for edit (USER)
@app.route('/suggest', methods=['POST'])
def sug():
    try:
        req = request.data.decode().split("&")
        name = req[0]
        ed = req[1]
        print(name, ed)
        
        con = sqlite3.connect("sug.db")
        cur = con.cursor()
        cur.execute("select * from sug where mes=:na",{"na":ed})
        if not len(cur.fetchall()):
            cur.execute("insert into sug (name, mes) values(:na, :ma);", {"na": name, "ma": ed})
            con.commit()
            cur.execute("select * from sug;")
            print(cur.fetchall())
        con.close()
        
        return "success"
    except:
        return "boo"



# API sugestions read (MASTER)
@app.route('/getsuggestions', methods=['GET'])
def get():
    try:
        con = sqlite3.connect("sug.db")
        cur = con.cursor()
        cur.execute("select * from sug;")
        res = cur.fetchall()
        print(res[-1][-1])      # Get latest suggestions
        con.close()
        
        return res[-1][-1]
    except:
        print("Oops!")



# API to delete the suggestions (MASTER)
@app.route('/delsug', methods=['POST'])
def de():
    try:
        req = request.data.decode()     # The content (suggestions)
        con = sqlite3.connect("sug.db")
        cur = con.cursor()
        cur.execute("delete from sug where mes=:re;",{"re":req})
        con.commit()
        con.close()
        return 'success'
    except TypeError:
        return 'No suggestions at the moment!'



# Sign of document by MASTER/USER
@app.route('/lock', methods=['POST'])
def lock():
    if request.method == 'POST':
        au = request.data.decode()
        ro = os.getcwd() + "\\project1\\doc.txt"
        x = ""
        with open(ro, "a") as fil:
            x = fil.write("\n\n\n Signed by:\n"+au)


# API to display document
@app.route('/doc', methods=['GET'])
def buf():
    return docu()



if __name__=="__main__":
    app.run(debug=True)