import os
import sqlite3
from flask import Flask , request
from flask_restful import  Api ,reqparse, Resource
from flask import jsonify
from security import authentication,identity
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import datetime




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=10)
app.secret_key = 'mahmoud'
jwt = JWT(app,authentication,identity)

#------------------------------------------------------------------

def check_plate(careplate):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    select_query = "SELECT * FROM users WHERE carplate=?"
    result = cursor.execute(select_query, (careplate,))
    row = result.fetchone()
    if row:
        return ("this plate is already excist"), 500
    connection.close()








@app.route('/regs',methods=['post'])
def registeration():  # the first thing in the registration is the number of careplate.
    request_data = request.get_json()
    if not check_plate(request_data['carplate']):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(insert_query, [request_data['id'], request_data['username'], request_data['password'], request_data['mail'], request_data['carplate'], request_data['phone']])
        connection.commit()
        connection.close()
        return jsonify({'user': request_data})

    else:
        return ("this plate is already excist"), 500






@app.route('/raspberry/carplates',methods=['GET'])
@jwt_required()
def get_slotes():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    select_query = "SELECT * FROM users"
    result = cursor.execute(select_query)
    rows = result.fetchall()
    if rows:
        carplates = []
        for row in rows:
            carplates.append(row[4])
        return jsonify({'carplates': carplates})
    else:
        return None



@app.route('/slote/free',methods=['GET'])
@jwt_required()
def get_free_slote():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    select_query = "SELECT * FROM slotes"
    result = cursor.execute(select_query)
    row = result.fetchone()
    if row:
        for i in range(4):
            if row[i] == -1:
                return jsonify({'free slote number': i})
        return ("No free slotes")
    #else:
    #   return jsonify({'message': None})




@app.route('/slote/userPosition/<string:id>',methods=['GET'])
@jwt_required()
def get_user_position(id):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    select_query = "SELECT * FROM slotes"
    result = cursor.execute(select_query)
    row = result.fetchone()
    if row:
        for i in range(4):
            if row[i] == int(id):
                return jsonify({'your position is': i})
            #return jsonify({'your': row, 'id':id})
        return jsonify({'message':'NO USER RELATED BY THIS ID'})
    #else:
    #    return jsonify({'message':None})


@app.route('/raspberry/slote',methods=['put'])
@jwt_required()
def update():
    params_data = request.get_json()
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    insert_query ="UPDATE slotes SET slote1=?, slote2=?, slote3=?, slote4=?"
    #result = cursor.execute(insert_query,(0,1,0,1))
    result = cursor.execute(insert_query,(params_data[0], params_data[1], params_data[2], params_data[3]))
    result.fetchall()
    select_query = "SELECT * FROM slotes"
    result1 = cursor.execute(select_query)
    row1 = result1.fetchone()
    newRow = []
    for i in range(4):
        #if row1[i] == 0:
        if int(params_data[i]) == 0:
            newRow.append(-1)
        else:
            newRow.append(row1[i])
    update_query = "UPDATE slotes SET slote1=?, slote2=?, slote3=?, slote4=?"  # insert the new values for the locations.
    cursor.execute(update_query,(newRow[0], newRow[1], newRow[2], newRow[3],))
    select_query = "SELECT * FROM slotes"
    result2 = cursor.execute(select_query)
    row2 = result2.fetchone()
    connection.commit()
    connection.close()
    return jsonify({'garage_slotes':row2})




@app.route('/slote',methods=['put'])
@jwt_required()
def accept_user_position():
    params_data = request.get_json()
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    select_query = "SELECT * FROM slotes"
    result = cursor.execute(select_query)
    row = result.fetchone()
    newRow = []
    for i in range(4):
        if int(params_data['sloteNumber']) == i:
            newRow.append(int(params_data['userId']))
        else:
            newRow.append(row[i])
    update_query = "UPDATE slotes SET slote1=?, slote2=?, slote3=?, slote4=?"  # insert the new values for the locations.
    result = cursor.execute(update_query,(newRow[0],newRow[1],newRow[2],newRow[3],))
    select_query = "SELECT * FROM slotes"
    result = cursor.execute(select_query)
    row = result.fetchone()
    connection.commit()
    connection.close()
    return jsonify({'garage_slotes':row})












@app.route('/users/remove',methods=['DELETE'])
@jwt_required()
def remove():
    request_data = request.get_json()
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    delete = "DELETE FROM users WHERE carplate=?"
    cursor.execute(delete,(str(request_data[0]),))                    #if plate only numbers-----> [plate number]
    #cursor.execute(delete,('A256',))                                 #if plate numbers and str ----->["plate number"]
    result = cursor.execute("SELECT * FROM users")
    row = result.fetchall()
    connection.commit()
    connection.close()
    return jsonify({'users':row})






#if __name__ == '__main__':                                        #If condition to run the app only from the main .
#    app.run(port=5000, debug=True)



if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)




