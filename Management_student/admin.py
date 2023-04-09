import os
import sys
current_dir = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from Management_student import app, db
from Management_student import models
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect



admin = Admin(app, name='QUẢN TRỊ BÁN HÀNG', template_mode='bootstrap4')
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")
class GradeView(ModelView):
    column_list = ['id', 'name']

class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
    
admin.add_view(GradeView(models.Grade, db.session))
admin.add_view(ModelView(models.ClassScholasticStudent, db.session))
admin.add_view(ModelView(models.Student, db.session))

# admin.add_view(AdminView(Category, db.session))
# admin.add_view(AdminView(Product, db.session))
