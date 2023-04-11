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



admin = Admin(app, name='QUẢN TRỊ HỆ THỐNG TRƯỜNG', template_mode='bootstrap4')
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")
class GradeView(ModelView):
    form_columns = ['name', 'note']
    column_labels = {
        'name': 'Tên khối',
        'note': 'Ghi chú',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật',
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")

class RegulationAge(ModelView):
    form_columns = ['max_age', 'note','min_age']
    column_labels = {
        'note': 'Ghi chú',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật',
        'max_age':'Tuổi tối đa',
       'min_age':'Tuổi tối thiểu'
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")
    
    
class ClassScholasticStudent(ModelView):
    form_columns = [ 'note','active', 'note','scholastic']
    column_labels = {
        'note': 'Ghi chú',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật',
        'active': 'Còn học',
        'scholastic':'Năm học',
        'class_scholastic':"Lớp",
        'student':'Học sinh'
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")

class Students(ModelView):
    form_columns = ['name', 'note','address','date_of_birth', 'phone_number','email','image','gender']
    column_labels = {
        'name': 'Tên',
        'note': 'Ghi chú',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật',
        'address': 'Địa chỉ',
        'date_of_birth': 'Ngày sinh',
        'phone_number':'SĐT',
        'email':'Email',
        'image': 'Ảnh đại diện',
        'gender':'Giới tính'
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")
class Teachers(ModelView):
    form_columns = ['name', 'note','address','date_of_birth', 'phone_number','email','image','gender']
    column_labels = {
        'name': 'Tên',
        'note': 'Ghi chú',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật',
        'address': 'Địa chỉ',
        'date_of_birth': 'Ngày sinh',
        'phone_number':'SĐT',
        'email':'Email',
        'image': 'Ảnh đại diện',
        'gender':'Giới tính'
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")

class Subject(ModelView):
    form_columns = ['name', 'note']
    column_labels = {
        'name': 'Tên',
        'note': 'Ghi chú',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật'   
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")

class SubjectGrade(ModelView):
    form_columns = ['id','subject_id', 'note','grade_id','subject']
    form_ajax_refs = {
        'subject': {
            'fields': ['name']
        }
    }
    column_labels = {
        'subject':'Môn học',
        'id': 'Mã',
        'subject_id': 'Mã môn học',
        'grade_id': 'Mã khối',
        'note': 'Ghi chú',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật'   
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")
class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
class Classes(ModelView):
    form_columns = ['name', 'note','regulation_age', 'max_size']
    column_labels = {
        'name': 'Tên lớp',
        'note': 'Ghi chú',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật',
        'name': 'Tên lớp',
        'regulation_age': 'Quy định tuổi',
        'max_size':'Sỉ số tối đa'
        
    }
  
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")

class Users(ModelView):
    form_columns = ['username', 'password','user_role', 'id']
    column_labels = {
        'username': 'Tài khoản',
        'password': 'Mật khẩu',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật',
        'user_role': 'Quyền hạn',
        'id': 'Mã giáo viên',
        
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")

class TypeTest(ModelView):
    form_columns = ['name', 'min_test','max_test', 'coefficient']
    column_labels = {
        'name': 'Loại kiểm tra',
        'min_test': 'Số bài kiểm tra tối thiểu',
        'update_date':'Ngày cập nhật',
        'user_update':'Tài khoản cập nhật',
        'max_test': 'Số bài kiểm tra tối đa',
        'coefficient': 'Hệ số',
        
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__("ADMIN")


admin.add_view(GradeView(models.Grade, db.session,name='Quản lý khối'))
admin.add_view(ClassScholasticStudent(models.ClassScholasticStudent, db.session,name='Quản lý học sinh theo lớp'))
admin.add_view(RegulationAge(models.RegulationAge, db.session,name='Quản lý quy định tuổi'))
admin.add_view(Students(models.Student, db.session,name='Quản lý học sinh'))
admin.add_view(Teachers(models.Teacher, db.session,name='Quản lý giáo viên'))
admin.add_view(Subject(models.Subject, db.session,name='Quản lý môn học'))
admin.add_view(SubjectGrade(models.Subject_grade, db.session,name='Quản lý môn học cho khối lớp'))
admin.add_view(Classes(models.ClassScholastic, db.session,name='Quản lý lớp học'))
admin.add_view(Users(models.User, db.session,name='Quản lý tài khoản'))
admin.add_view(TypeTest(models.TpyeTest, db.session,name='Quản lý loại kiểm tra'))
