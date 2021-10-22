import sqlite3
from flask import Flask,url_for,redirect
from flask import render_template
from flask import jsonify, request
conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
#configurar de la app
app = Flask(__name__)
cursorObj = conn.cursor()
@app.route('/login',methods=['POST'])
def login():
    conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
    content = request.get_json()
    email = content.get("email")
    password = content.get("password")
    status = content.get("status")
    sql_table(conn)
    if(status==1):
        info = (email)
        cursorObj.execute("SELECT * from users WHERE gmail == '"+email+"';")
        #Fetching 1st row from the table
        result = cursorObj.fetchone()
        try:
             if(result[3]==password and result[1]==email):
                 return jsonify({"information":result}),200        
        except:
            return jsonify({"ststus":False}),504    
    
        #Fetching 1st row from the table
        result = cursorObj.fetchall()
        #Commit your changes in the database
        conn.commit()
        return jsonify({"datos":True}),200
    else:
        sql_table(conn)
        inssert(conn,email,"na",email,"na",status)
        return jsonify({"data":True}),200 



        
@app.route('/registerUsers',methods=['POST'])
def registerUsers():
    content = request.get_json()
    email= content.get("email")
    type = content.get("type")
    name = content.get("name")
    password = content.get("password")
    status = content.get("status")
    sql_table(conn)
    inssert(conn,email,type,name,password,status)
    return jsonify({"datos":True}),200
@app.route('/')
def view():
    return render_template('index.html')

def sql_table(conn):
    try:
        cursorObj.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , gmail text, name text, password text ,type text,status int)")
        cursorObj.execute("CREATE TABLE IF NOT EXISTS ubication(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,long text,lant text)")
        cursorObj.execute("CREATE TABLE IF NOT EXISTS public(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,img text,nombre text,decription text,idUsuario,idUbication INTEGER)")
        cursorObj.execute("CREATE TABLE IF NOT EXISTS service(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,nombre text,decription text,valor text,idUbication INTEGER)")
        conn.commit()
    except:
        return jsonify({"error":"la tabla no se pudo crear"}),504

def inssert(conn,email,type,name,password,status):
    info=(email,name,password,type,status)
    cursorObj.execute('''INSERT INTO users (gmail,name,password,type,status) VALUES(?,?,?,?,?)''',info)
    conn.commit()
def innsertPublicidad(conn,information):    
    cursorObj.execute('''INSERT INTO  public(nombre,decription,valor,ubication) VALUES(?,?,?,?,?)''',information)
    conn.commit()


if __name__=="__main__":
    app.run(port=1406,debug=True,host='0.0.0.0')