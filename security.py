import sqlite3
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from user import userModel

def authentication(username,password):                   #FILTER BY THE CARE PLTE BECAUSE IT NEVER REPEAT.
    user = userModel.find_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user
    return {'message': 'user not available'}


def identity(payload):
     user_id = payload['identity']
     return userModel.find_by_id(user_id)





