from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from Management_student import app, db



admin = Admin(app, name='QUẢN TRỊ BÁN HÀNG', template_mode='bootstrap4')