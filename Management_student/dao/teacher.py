import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from Management_student import db,models
import cloudinary.uploader

def get_teacher(request):
    name = request.form['name']
    address = request.form['address']
    #username = request.form['username']
    mobile_no = request.form['mobile_no']
    email = request.form['email']
    birthdate = request.form['birthdate']
    note = request.form['note']
    subject = request.form['subject']
    gender = request.form['gender']
    if gender==str(0):
        gender="Nam"
    elif gender==str(1):
        gender="Nữ"
    


def update_teacher(request,id):
    teacher = models.Teacher.query.get(id)
    teacher.name = request.form['name']
    teacher.address = request.form['address']
    teacher.phone_number = request.form['mobile_no']
    teacher.email = request.form['email']
    teacher.date_of_birth = request.form['birthdate']
    teacher.note = request.form['note']
    img=request.files['image']
    #teacher.class_id = request.form['class_id']
    teacher.gender = request.form['gender']
    if img:
        res = cloudinary.uploader.upload(request.files['image'])
        teacher.image=res['secure_url']
    if teacher != False:
        #db.session.add(class_scholastic_st)
        db.session.commit()

def add_teacher(request):
    name = request.form['name']
    address = request.form['address']
    mobile_no = request.form['mobile_no']
    email = request.form['email']
    birthdate = request.form['birthdate']
    note = request.form['note']
    gender = request.form['gender']
    subject = request.form['subject']
    if gender==str(0):
        gender="Nam"
    elif gender==str(1):
        gender="Nữ"
    #age=models.RegulationAge
    # if check_age(birthdate,15,20) == False:
    #     popup_content="Độ tuổi không phù hợp"
    #     return  popup_content
    teacher=models.Teacher(name=name, gender=gender, note=note, email=email, date_of_birth=birthdate, phone_number=mobile_no,subject_id=subject) #, address=address
    db.session.add(teacher)
    db.session.commit()
    popup_content="Thêm giáo viên thành công"
    return  popup_content

def get_all_teacher(subject_id=None,name_teacher=None,page=1):
    query = models.Teacher.query
    if subject_id:
        query=models.Teacher.query.filter(models.Teacher.subject_id.__eq__(subject_id) )
    if name_teacher:
        query = query.filter(models.Teacher.name.contains(name_teacher))
    page_size=5
    start = (page-1)*page_size
    end=start+page_size
    #teachers=models.Teacher.query
    return query.slice(start,end).all()

def check_age(birthdate, age_min, age_max):
    today = datetime.date.today()
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