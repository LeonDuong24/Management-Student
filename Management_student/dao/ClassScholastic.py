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



def get():
    student_id=1
    class_current=models.ClassScholasticStudent.query.filter_by(student_id=student_id).first()
    score=models.Score.query.filter_by(class_scholastic_student=class_current.id).all()
    type_test=models.TpyeTest.query.all()
    score={}
    for type in type_test:
        score[type]=''
    print(score)    
    #for i in score:
        
def end_class_scholastic():
    try:
        db.session.query(models.Student).update({models.Student.active: True})
        db.session.commit()
        return "Kết thúc năm học thnahf công"
    except:
        return "Không thành công do lỗi ngoại lệ"


def add_score(request,student_id):
    try:
        class_current=models.ClassScholasticStudent.query.filter_by(student_id=student_id,active=True).first()
        score = request.form['score']
        subject_score = request.form['subject_score']
        semester_score = request.form['semester_score']
        type_score = request.form['type_score']
        scores_in_subject=models.Score.query.filter_by(subject_id=subject_score,type_test_id=type_score,semester=semester_score,class_scholastic_student_id=class_current.id).all()
        type_test=models.TpyeTest.query.get(type_score)
        
        if len(scores_in_subject) +1 > type_test.max_test:
            print("Quá số lượng",len(scores_in_subject))
            return  "Thêm lớp thành công"
        
        score_class=models.Score(semester=semester_score,score=score,type_test_id=type_score,subject_id=subject_score,class_scholastic_student_id=class_current.id)
        db.session.add(score_class)
        db.session.commit()
        popup_content="Thêm lớp thành công"
        return  popup_content
    except Exception as e:
        print(e)
        popup_content="Thêm thất bại"
        return  popup_content
    

def add_grade(request):
    name = request.form['name']
    note = request.form['note']
    grade=models.Grade(name=name,note=note) 
    db.session.add(grade)
    db.session.commit()
    popup_content="Thêm khối thành công"
    return  popup_content
if __name__ == '__main__':
    get()