from flask import Flask, abort
from flask import make_response
from flask import request
from flask_jsonpify import jsonify
import pymysql

app = Flask(__name__)


###############  DB   ################

conn = pymysql.connect(host='172.31.31.129', port=3306, user='root', passwd='Test_123', db='mydb')
cur = conn.cursor()

###############################

@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def badRequest(error):
    return make_response(jsonify({'error': 'Bad Request'}), 404)

@app.route('/')
def default():
    return 'How are you ! This is a User management Restful service. Please have fun with  this. Thank you'

@app.route('/users')
def getUsers():
    # list all
    cur.execute("SELECT * FROM users")
    ret = ''
    for row in cur:
        ret = ret + 'ID : ' + str(row[0]) + ", Name : " + row[1] + ", Sex : " + row[2] + ", Role : " + row[3]
    return ret

@app.route('/users/<int:user_id>')
def getUser(user_id):
    cur.execute("SELECT * FROM users WHERE user_id = %d" %user_id)
    ret = ''
    for row in cur:
        ret = ret + 'ID : ' + str(row[0]) + ", Name : " + row[1] + ", Sex : " + row[2] + ", Role : " + row[3]
    return ret

@app.route('/users/create',methods = ['POST'])
def createUser():
    if not request.json:
        abort(400)
    print(request.json)
 
    try:
        sql = "INSERT INTO `users` (`name`, `sex`, `role`) VALUES (%s, %s, %s)"
        cur.execute(sql, (request.json['name'], request.json['sex'], request.json['role']))
        conn.commit()
        return make_response(jsonify({'result': 'Success'}), 200)
    except err:
        return make_response(jsonify({'result': err}), 200)

@app.route('/users/delete', methods=['DELETE'])
def deleteUser():
    try:
        sql = "Delete from users where user_id= %d " % request.json['user_id']
        cur.execute(sql)
        conn.commit()
        return make_response(jsonify({'result': 'Success'}), 200)
    except :
        return make_response(jsonify({'result': err}), 200)
    return jsonify({'result': 'error'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8088)
    cur.close()
    conn.close()    
