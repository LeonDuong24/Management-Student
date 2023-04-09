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
    latest_record = models.RegulationAge.query.order_by(models.RegulationAge.update_date.desc()).first()
    print(latest_record)
    if check_age(birthdate,latest_record.min_age,latest_record.max_age) == False:
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

def get_all_student(page=1):
    page_size=5
    start = (page-1)*page_size
    end=start+page_size
    students=models.ClassScholasticStudent.query
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