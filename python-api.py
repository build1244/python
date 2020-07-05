from flask import Flask
from flask import Response
from flask import request
from datetime import datetime
import os
import json
import MySQLdb
import time

checkdb = 0
while checkdb == 0:
    try:
        db = MySQLdb.Connect(os.environ['MYSQL_SERVER'],"root","password")
    except:
        time.sleep(2)
#	continue
    else:
        checkdb = 1

#print(os.environ)
mysql = db.cursor()
#mysql.execute("CREATE DATABASE IF NOT EXISTS {}".format(os.environ['DB_NAME']))
mysql.execute("show databases")
databases = mysql.fetchall()
print(databases)
try:
    mysql.execute("USE {}".format(os.environ['DB_NAME']))
except:
    print("create db")
#    print("CREATE DATABASE {}".format(os.environ['DB_NAME']))
    mysql.execute("CREATE DATABASE {}".format(os.environ['DB_NAME']))
    mysql.execute("USE "+str(os.environ['DB_NAME']))
    sql = """CREATE TABLE person (
    ID int,
    firstname varchar(255),
    lastname varchar(255),
    age varchar(10)
    )"""
    mysql.execute(sql)
    db.commit()

app = Flask(__name__)

@app.route('/')
def welcome():
    return '''
	<h1>Hello welcome to the site</h1><br>
        <p>Timestamp: {}</p>
	'''.format(datetime.now())

@app.route('/add_info', methods=['POST'])
def add_info_person():
    data = request.get_json()
   # print("INSERT INTO %s.person (ID, firstname, lastname, age) VALUES (%s,%s,%s)",(str(os.environ['DB_NAME']), data['id'], data['firstname'], data['lastname'], data['age']))
    mysql.execute("SELECT * FROM {}.person WHERE ID={}".format(os.environ['DB_NAME'], data['id']))
    result = mysql.fetchone()
    if result:
        mysql.execute("UPDATE {}.person SET firstname=%s, lastname=%s, age=%s WHERE id={}".format(os.environ['DB_NAME'],data['id']),(data['firstname'],data['lastname'],data['age']))
        db.commit()
        return Response('Personal info updated', status=200, mimetype='application/json')
    else:
        insert = "INSERT INTO {}.person (ID, firstname, lastname, age) VALUES (%s,%s,%s,%s)".format(os.environ['DB_NAME'])
   # mysql.execute("USE {}".format(os.environ['DB_NAME']))
        mysql.execute(insert, (data['id'], data['firstname'], data['lastname'], data['age']))
        db.commit()
        return Response('Personal info added', status=200, mimetype='application/json')

@app.route('/person/<id>')
def show_person(id):
   # select = 'SELECT * FROM {}.person WHERE ID=%s'.format(os.environ['DB_NAME'])
    mysql.execute('SELECT * FROM {}.person WHERE ID={}'.format(os.environ['DB_NAME'], str(id)))
    result = mysql.fetchone()
    if result:
        return Response("""
        <h1>Record FOUND!!</h1><br>
        <p>ID: {}<br>
        firstname: {}<br>
        lastname: {}<br>
        age: {}<br></p>
        """.format(result[0],result[1],result[2],result[3]), status=200)
    else:
        return "Record not found"

@app.route('/delete/<id>')
def delete(id):
    mysql.execute('SELECT * FROM {}.person WHERE ID={}'.format(os.environ['DB_NAME'], str(id)))
    result = mysql.fetchone()
    if result:
        mysql.execute('DELETE FROM {}.person WHERE ID={}'.format(os.environ['DB_NAME'],str(id)))
        db.commit()
        return Response('Personal info removed', status=200, mimetype='application/json')
    else:
        return Response('Invalid id', status=400, mimetype='application/json')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9000, debug=True)
