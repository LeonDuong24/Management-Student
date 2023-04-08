from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from Management_student import db, app
from flask_login import UserMixin


class Base(db.Model):
    __abstract__=True
    id = Column(Integer, primary_key=True, autoincrement=True)
    update_date= Column(DateTime,default=datetime.now() )
    user_update= Column(String(100) )
    note = Column(String(100))

# #Định nghĩa model cho bảng 'teachers'
class Teacher(Base):
    __tablename__ = 'teachers'
    name = Column(String(50))
    address = Column(String(100))
    date_of_birth = Column(DateTime)
    phone_number = Column(String(100))
    email = Column(String(100))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    image = Column(String(100))
    gender = Column(String(100))


# #Định nghĩa model cho bảng 'students'
class Student(Base):
    __tablename__ = 'students'
    name = Column(String(50))
    address = Column(String(100))
    date_of_birth = Column(DateTime)
    phone_number = Column(String(100))
    email = Column(String(100))
    image = Column(String(100))
    gender = Column(String(100))

# # Định nghĩa model cho bảng 'classes'

class Grade(Base):
    __tablename__ = 'grades'
    name = Column(String(100), nullable=False)

class Subject_grade():
    __tablename__ = 'subjects_grade'
    grade_id = Column(Integer, ForeignKey('grades.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
    update_date= Column(DateTime,default=datetime.now() )
    
class RegulationAge(Base):
    __tablename__ = 'regulation_age'
    max_age = Column(Integer,default=20)
    min_age = Column(Integer,default=15)
    

# class Class(Base):
#     __tablename__ = 'classes'
#     name = Column(String(100), nullable=False)
#     #grade = relationship('grade', backref='grades', lazy=True)
#     grade_id=Column(Integer, ForeignKey('grades.id'), nullable=False)
    
class ClassScholastic(Base):
    __tablename__ = 'class_scholastic'
    grade_id=Column(Integer, ForeignKey('grades.id'), nullable=False)
    name=Column(String(100))
    scholastic=Column(String(100))
    regulation_age=Column(Integer, ForeignKey('regulation_age.id'))
    max_size = Column(Integer,default=40)
    
    
# class ClassStudentHis(Base):
#     __tablename__ = 'class_scholastic_his'
#     class_id = Column(Integer)
#     student_id = Column(Integer)
#     note = Column(String(100))
#     scholastic=Column(String(100))
#     max_size = Column(Integer,default=40)
#     max_age = Column(Integer,default=20)
#     min_age = Column(Integer,default=15)

# # # Định nghĩa model cho bảng 'class_student'
class ClassScholasticStudent(Base):
    __tablename__ = 'class_scholastic_student'
    class_scholastic_id = Column(Integer, ForeignKey('class_scholastic.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    class_scholastic = relationship('ClassScholastic', backref='class_scholastic_student', lazy=True)
    #student = relationship('Student', backref='class_scholastic', lazy=True)
    student = relationship('Student', backref='class_scholastic_student', lazy=True)
# # # Định nghĩa model cho bảng 'scores'

class Score(Base):
    __tablename__ = 'scores'
    class_scholastic_student= Column(Integer, ForeignKey('class_scholastic_student.id'), nullable=False)
    #student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    semester = Column(Integer)
    type_test = Column(String(100))
    score = Column(Float, nullable=False)
    
class Subject(Base):
    __tablename__ = 'subjects'
    subject = Column(String(100), nullable=False)

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    avatar = Column(String(100))
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    user_role = Column(String(20), default='USER')

    def __str__(self):
        return self.name
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # import hashlib
        # u = User(username='demo', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          name='ABC DEF',
        #          avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg')
        # db.session.add(u)
        # db.session.commit()