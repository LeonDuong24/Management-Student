import hashlib
from Management_student.models import  User
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from Management_student import db,models,app, dao, admin,login


def get_user_by_id(user_id):
    return User.query.get(user_id)




def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    print('password',password)
    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()
def add_user(teacher_id, username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    #u = User(teacher_id=teacher_id, username=username, password=password)
    u = User(id=teacher_id, username=username, password=password)
    db.session.add(u)
    db.session.commit()