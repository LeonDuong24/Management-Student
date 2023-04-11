import copy
import datetime
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from Management_student import db,models
from sqlalchemy import desc, and_
import cloudinary.uploader

def get_student_from_UI(request):
    name = request.form['name']
    address = request.form['address']
    #username = request.form['username']
    mobile_no = request.form['mobile_no']
    email = request.form['email']
    birthdate = request.form['birthdate']
    note = request.form['note']
    #class_id = request.form['class_id']
    gender = request.form['gender']
    latest_record = models.RegulationAge.query.order_by(models.RegulationAge.update_date.desc()).first()
    # if check_age(birthdate,latest_record.min_age,latest_record.max_age) == False:
    #     popup_content="Độ tuổi không phù hợp"
    #     return  False
    student=models.Student(name=name, gender=gender, note=note, email=email, date_of_birth=birthdate, phone_number=mobile_no,address=address) #, address=address
    return student

def update_student(request,student_id):
    class_current=models.ClassScholasticStudent.query.filter_by(active=True,student_id=student_id).first()
    student = models.Student.query.get(student_id)
    student.name = request.form['name']
    student.address = request.form['address']
    student.phone_number = request.form['mobile_no']
    student.email = request.form['email']
    student.date_of_birth = request.form['birthdate']
    student.note = request.form['note']
    img=request.files['image']
    change_class=request.form['class']
    student.gender = request.form['gender']
    if img:
        res = cloudinary.uploader.upload(request.files['image'])
        student.image=res['secure_url']
    if change_class:
        if class_current:
            class_current.class_scholastic_id=change_class
        else:
            class_scholastic_st=models.ClassScholasticStudent(student_id=student_id,class_scholastic_id= change_class)
            if check_size_class(change_class) :
                db.session.add(class_scholastic_st)
            else:
                return "Sỉ số lớp đã tới hạn" 
    if student != False:
        db.session.commit()

def check_size_class(class_id):
    size_class_cur= len(models.ClassScholasticStudent.query.filter_by(active=True,class_scholastic_id=class_id).all())
    class_cur=models.ClassScholastic.query.get(class_id)
    if (size_class_cur>class_cur.max_size):
        return False
    else:
        return True

def get_student(request):
    try:
        name = request.form['name']
        address = request.form['address']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        birthdate = request.form['birthdate']
        note = request.form['note']
        class_id = request.form['class']
        gender = request.form['gender']
        img=request.files['image']
        regulation_age = models.RegulationAge.query.filter(models.RegulationAge.active.__eq__(True)).first()
        if check_age(birthdate,regulation_age.min_age,regulation_age.max_age) == False:
            return  "Độ tuổi học sinh không phù hợp"
        if img:
            res = cloudinary.uploader.upload(request.files['image'])
            student=models.Student(address=address,name=name, gender=gender, note=note, email=email, date_of_birth=birthdate, phone_number=mobile_no,image=res['secure_url']) 
        student=models.Student(address=address,name=name, gender=gender, note=note, email=email, date_of_birth=birthdate, phone_number=mobile_no)
        db.session.add(student)
        db.session.commit()
        print(student.id)
        print(class_id)
        if class_id:
            class_scholastic_st=models.ClassScholasticStudent(student_id=student.id,class_scholastic_id=class_id)
            if check_size_class(class_id) :
                db.session.add(class_scholastic_st)
                db.session.commit()
            else:
                return "Sỉ số lớp đã tới hạn"
        return "Thêm học sinh thành công"
    except Exception as e:
        print(e)
        return  "Thêm thất bại vì lý do ngoại lệ"



def get_score_class(class_scholastic_student):
    #{1:{"Toán":{{ 15p:[1,2,3]    }}}}
    semester={}
    type_test=models.TpyeTest.query.all()
    subject_grade=models.Subject_grade.query.filter_by(grade_id=class_scholastic_student.class_scholastic.grade_id).all()
    score_subject={}
    type={}
    for ty in type_test:
            type[ty.id]=[]
    for subject in subject_grade:
        score_subject[subject.subject.id]=copy.deepcopy(type)
    semester[1]=copy.deepcopy(score_subject)
    semester[2]=copy.deepcopy(score_subject)
    print(semester)
    #semesterII=score_subject.copy()
    scores2 = models.Score.query.filter_by(class_scholastic_student_id=class_scholastic_student.id).order_by(and_(models.Score.update_date,models.Score.type_test_id)).all()
    for sc in scores2:
        semester[sc.semester][sc.subject_id][sc.type_test_id].append(sc.score)
    # for sem in semester.values():
    #     for subject in sem.values():
    #         total=0
    #         coff=0
    #         for test_type in subject.values():
    #             type_score = sum(test_type)/len(subject.values())
    #             total+=type_score
    #             coff+=
    #         test_type.append(total_score)
    return semester

def get_his_class(student_id):
    try:
        score_his={}
        grades=models.ClassScholasticStudent.query.filter_by(student_id=student_id,activity=False).all()
        for class_grade in grades:
            score_class=get_score_class(class_grade)
            score_his[class_grade.class_scholastic.name]=score_class
        return score_his
    except:
        return None

def get_students_active(page=1,class_student=None,name_student=None):
    query = models.ClassScholasticStudent.query.filter(models.ClassScholasticStudent.active.__eq__(True))
    if class_student:
        query=models.ClassScholasticStudent.query.filter(models.ClassScholasticStudent.class_scholastic_id.__eq__(class_student),models.ClassScholasticStudent.active.__eq__(True) )
    if name_student:
        query = query.join(models.ClassScholasticStudent.student).filter(models.Student.name.contains(name_student),models.ClassScholasticStudent.active.__eq__(True))
    page_size=5
    start = (page-1)*page_size
    end=start+page_size
    #students=models.ClassScholasticStudent.query.filter(models.ClassScholasticStudent.active.__eq__(True))
    return query.slice(start,end).all()



def get_all_student(page=1):
    page_size=5
    start = (page-1)*page_size
    end=start+page_size
    students=models.Student.query
    return students.slice(start,end).all()
    #return models.ClassScholasticStudent.slice(start,end).all()
    #return models.Student.slice(start,end).all()
def get_student_by_id(student_id):
    return models.Student.query.get(student_id)

# def check_can_join_class(numStudent):
#     pass

def check_age(birthdate, age_min, age_max):
    today = datetime.date.today()
    birthdate=datetime.datetime.strptime(birthdate,'%Y-%m-%d')
    age = today.year - birthdate.year
    if age >= age_min and age <= age_max:
        return True
    else:
        return False
if __name__ == '__main__':
    dob = datetime.date(2009, 3, 28)
    age_min = 18
    age_max = 25

    if check_age(dob, age_min, age_max):
        print("Ngày sinh nằm trong khoảng độ tuổi cho phép.")
    else:
        print("Ngày sinh không nằm trong khoảng độ tuổi cho phép.")