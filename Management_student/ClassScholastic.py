import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from Management_student import db,models


    

def add_class(request):
    name = request.form['name']
    note = request.form['note']
    year = request.form['year']
    grade = request.form['grade']
    size = request.form['size']
    class_Scholastic=models.ClassScholastic(grade_id=grade,name=name,note=note,scholastic=year,max_size=size)
    db.session.add(class_Scholastic)
    db.session.commit()
    popup_content="Thêm lớp thành công"
    return  popup_content 

def add_grade(request):
    name = request.form['name']
    note = request.form['note']
    grade=models.Grade(name=name,note=note) 
    db.session.add(grade)
    db.session.commit()
    popup_content="Thêm khối thành công"
    return  popup_content