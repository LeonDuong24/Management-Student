from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from sqlalchemy import Column, DateTime, String, Integer, Float, ForeignKey, Text,Boolean
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
    subject = relationship('Subject', backref='teachers', lazy=True)
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

class Subject_grade(Base):
    __tablename__ = 'subjects_grade'
    grade_id = Column(Integer, ForeignKey('grades.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    subject = relationship('Subject', backref='subjects_grade', lazy=True)
    
class RegulationAge(Base):
    __tablename__ = 'regulation_age'
    max_age = Column(Integer,default=20)
    min_age = Column(Integer,default=15)
    active=Column(Boolean, default=True)
    
class ClassScholastic(Base):
    __tablename__ = 'class_scholastic'
    grade_id=Column(Integer, ForeignKey('grades.id'), nullable=False)
    grade = relationship('Grade', backref='class_scholastic', lazy=True)
    name=Column(String(100))
    regulation_age=Column(Integer, ForeignKey('regulation_age.id'))
    max_size = Column(Integer,default=40)
    

# # # Định nghĩa model cho bảng 'class_student'
class ClassScholasticStudent(Base):
    __tablename__ = 'class_scholastic_student'
    class_scholastic_id = Column(Integer, ForeignKey('class_scholastic.id'))
    scholastic=Column(String(100))
    student_id = Column(Integer, ForeignKey('students.id'))
    class_scholastic = relationship('ClassScholastic', backref='class_scholastic_student', lazy=True)
    student = relationship('Student', backref='class_scholastic_student', lazy=True)
    active=Column(Boolean, default=True)
# # # Định nghĩa model cho bảng 'scores'

class Score(Base):
    __tablename__ = 'scores'
    class_scholastic_student_id= Column(Integer, ForeignKey('class_scholastic_student.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    semester = Column(Integer, nullable=False)
    subject = relationship('Subject', backref='scores', lazy=True)
    type_test = relationship('TpyeTest', backref='scores', lazy=True)
    class_scholastic_student=relationship('ClassScholasticStudent', backref='scores', lazy=True)
    type_test_id= Column(Integer, ForeignKey('type_test.id'), nullable=False)
    score = Column(Float, nullable=False)
    
class TpyeTest(Base):
    __tablename__ = 'type_test'
    name = Column(String(100), nullable=False)
    min_test = Column(Integer, nullable=False)
    max_test = Column(Integer,nullable=False)
    coefficient=Column(Float)
    
    
class Subject(Base):
    __tablename__ = 'subjects'
    name = Column(String(100), nullable=False)
  
class User(db.Model, UserMixin):
    #id = Column(Integer, primary_key=True, autoincrement=True)
    #name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    user_role = Column(String(20), default='USER')
    teacher_id=Column(Integer, ForeignKey('teachers.id'), nullable=False,primary_key=True)
    teacher = relationship('Teacher', backref='user', lazy=True)
    

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