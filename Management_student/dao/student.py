import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from Management_student import db,models
from sqlalchemy import desc
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
    print(request.form['class'])
    #class_scholastic_st=models.ClassScholasticStudent(student_id=student_id,class_scholastic_id= request.form['class'])
    student = models.Student.query.get(student_id)
    student.name = request.form['name']
    student.address = request.form['address']
    #username = request.form['username']
    student.phone_number = request.form['mobile_no']
    student.email = request.form['email']
    student.date_of_birth = request.form['birthdate']
    student.note = request.form['note']
    img=request.files['image']
    #student.class_id = request.form['class_id']
    student.gender = request.form['gender']
    if img:
        res = cloudinary.uploader.upload(request.files['image'])
        student.image=res['secure_url']
    #student.image = request.form['image']
    if student != False:
        #db.session.add(class_scholastic_st)
        db.session.commit()

    

def get_student(request):
    name = request.form['name']
    address = request.form['address']
    #username = request.form['username']
    mobile_no = request.form['mobile_no']
    email = request.form['email']
    birthdate = request.form['birthdate']
    note = request.form['note']
    #class_id = request.form['class_id']
    gender = request.form['gender']
    img=request.files['image']
    #age=models.RegulationAge
    regulation_age = models.RegulationAge.query.filter(models.RegulationAge.active.__eq__(True)).first()
    print(regulation_age)
    if check_age(birthdate,regulation_age.min_age,regulation_age.max_age) == False:
        popup_content="Độ tuổi không phù hợp"
        return  popup_content
    if img:
        res = cloudinary.uploader.upload(request.files['image'])
        student=models.Student(name=name, gender=gender, note=note, email=email, date_of_birth=birthdate, phone_number=mobile_no,image=res['secure_url'])
    student=models.Student(name=name, gender=gender, note=note, email=email, date_of_birth=birthdate, phone_number=mobile_no)
    db.session.add(student)
    db.session.commit()
    popup_content="Thêm học sinh thành công"
    return  popup_content



def get_score_class(class_scholastic_student):
    semesterI={}
    semesterII={}
    type_test=models.TpyeTest.query.all()
    subject_grade=models.Subject_grade.query.filter_by(grade_id=class_scholastic_student.class_scholastic.grade_id).all()
    score_subject={}
    for subject in subject_grade:
        score_subject[subject.subject.name]={}
    # for type in type_test:
    #     semesterI[type.id]=[]
    #     semesterII[type.id]=[]
    scores=models.Score.query.filter_by(class_scholastic_student=class_scholastic_student.id).all()
    for sc in scores:
        if(sc.semester==1):
            semesterI[sc.subject.name][sc.type_test_id].append(sc.score)
        elif (sc.semester==2):
            semesterII[sc.type_test_id].append(sc.score)
    score_grade={'1':semesterI,'2':semesterII}
    return score_grade

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

def get_students_active(page=1):
    page_size=5
    start = (page-1)*page_size
    end=start+page_size
    students=models.ClassScholasticStudent.query.filter(models.ClassScholasticStudent.active.__eq__(True))
    return students.slice(start,end).all()
    #return models.ClassScholasticStudent.slice(start,end).all()
    #return models.Student.slice(start,end).all()


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