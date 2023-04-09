import math
from flask import Flask, jsonify, request, render_template, session,send_file,redirect,url_for,make_response,flash
from flask_login import login_user, logout_user,login_required
import sys
import os
from datetime import datetime
import cloudinary.uploader


current_dir = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
#print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#sys.path.append(r"C:\Users\Alpaca\Desktop\Management-Student")

from dao import teacher,user,student,ClassScholastic,subject
from Management_student import app, admin,login,models


@app.route('/chart', methods=['GET', 'POST'])
def chart():
    return render_template('chart.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/all_students')
def all_students():
    page=request.args.get('page',1)
    
    students=student.get_all_student(int(page))
    return render_template('all_students.html',students=students,pages=math.ceil(len(students)/5))

 
@app.route('/students')
def students():
    page=request.args.get('page',1) 
    students=student.get_students_active(int(page))
    return render_template('students.html',students=students,pages=math.ceil(len(students)/5))

@app.route('/teachers')
def teachers():
    subject_id = request.args.get('subject')
    name_teacher = request.args.get('name_teacher')
    page=request.args.get('page',1)
    print(subject_id)
    print(name_teacher)
    teachers=teacher.get_all_teacher(subject_id,name_teacher,int(page))
    subject=models.Subject.query.all()
    #teachers=teacher.get_all_teacher(int(page))
    for i in teachers:
        print(i.name)
    
    return render_template('teachers.html',teachers=teachers,pages=math.ceil(len(teachers)/5),subject=subject)

@app.route('/add_grade', methods=['GET','POST'])
def process_add_grade():
    if request.method == 'POST':
        popup_content=ClassScholastic.add_grade(request)
        return render_template('add_grade.html',popup_content=popup_content)
    else: 
        return render_template('add_grade.html')

@app.route('/add_subject', methods=['GET','POST'])
def process_add_subject():
    if request.method == 'POST':
        popup_content=subject.add_subject(request)
        return render_template('add_subject.html',popup_content=popup_content)
    else: 
        return render_template('add_subject.html')    
    
@app.route('/add_class', methods=['GET','POST'])
def process_add_class():
    grade=models.Grade.query.all()
    if request.method == 'POST':
        popup_content=subject.add_class(request)
        return render_template('add_class.html',popup_content=popup_content,grade=grade)
    else: 
        return render_template('add_class.html',grade=grade)    
    
@app.route('/add_student', methods=['POST'])
def process_add_student():
    popup_content=student.get_student(request)
    print(popup_content)
    return render_template('add_student.html',popup_content=popup_content)

@app.route('/add_student')
@login_required
def add_student():
    grade=models.Grade.query.all()
    classes=models.ClassScholastic.query.all()
    return render_template('add_student.html',grade=grade,classes=classes)

@app.route('/add_score/<int:id>', methods=['POST'])
def process_add_score(id):
    pop=ClassScholastic.add_score(request,id)
        #student.update_student(request,id)
        #return render_template('add_student.html')
    return redirect(url_for('student_profile', student_id=id))

@app.route('/update_student/<int:id>', methods=['POST'])
def process_update_student(id):
        student.update_student(request,id)
        #return render_template('add_student.html')
        return redirect(url_for('student_profile', student_id=id))
    
@app.route('/update_teacher/<int:id>', methods=['POST'])
def process_update_teacher(id):
        teacher.update_teacher(request,id)
        #return render_template('add_student.html')
        return redirect(url_for('teacher_profile', id=id))
  

@app.route('/add_teacher', methods=['GET','POST'])
def process_add_teacher():
    subject=models.Subject.query.all()
    if request.method == 'POST':
        popup_content=teacher.add_teacher(request)
        return render_template('add_teacher.html',popup_content=popup_content,subject=subject)
    else: 
        return render_template('add_teacher.html',subject=subject)


@app.route('/login')
def my_login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def my_login_process():
    username = request.form['username']
    password = request.form['password']
    u = user.auth_user(username, password)
    
    if u:
        login_user(user=u)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else '/')

    return render_template('login.html')

@app.route("/logout")
def my_logout():
    logout_user()
    return redirect("/login")

@app.route('/query_students')
def query_students():
    # Lấy tiêu chí truy vấn từ yêu cầu GET gửi từ máy khách
    criteria = request.args.get('criteria')
    # Thực hiện truy vấn cơ sở dữ liệu để lấy danh sách học sinh phù hợp với tiêu chí
    students = models.Student.query.filter(criteria).all()
    # Trả về danh sách học sinh dưới dạng JSON
    return jsonify([student.to_dict() for student in students])


@app.route('/teacher_profile/<int:id>', methods=['GET','POST'])
def teacher_profile(id):
    if request.method == 'GET':
        teacher_profile=models.Teacher.query.get(id)
        dob_str = teacher_profile.date_of_birth.strftime('%d-%m-%Y')
        subject=models.Subject.query.all() 
        return render_template('teacher_profile.html',teacher_profile=teacher_profile,dob_str=dob_str,subject=subject)


@app.route('/student_profile/<int:student_id>', methods=['GET','POST'])
def student_profile(student_id):
    if request.method == 'GET':
        grade=models.Grade.query.all()
        classes=models.ClassScholastic.query.all()
        class_current=models.ClassScholasticStudent.query.filter_by(student_id=student_id).first()
        type_test=models.TpyeTest.query.all()
        #subject=models.Subject_grade.query.get()
        student_profile=student.get_student_by_id(student_id)
        #dob = datetime.strptime(student_profile.date_of_birth, '%Y-%m-%d')
        dob_str = student_profile.date_of_birth.strftime('%Y-%m-%d')
        semesterI={}
        semesterII={}
        for type in type_test:
            semesterI[type.id]=[]
            semesterII[type.id]=[]
        if class_current:
            subject_current=models.Subject_grade.query.filter_by(grade_id=class_current.class_scholastic.grade_id).all()
            score=models.Score.query.filter_by(class_scholastic_student=class_current.id).all()
            for sc in score:
                #print(sc.class_scholastic_student.class_scholastic.grade_id)
                if(sc.semester==1):
                    semesterI[sc.type_test_id].append(sc.score)
                elif (sc.semester==2):
                    semesterII[sc.type_test_id].append(sc.score)
            score_grade={'1':semesterI,'2':semesterII}
            print(score_grade)
    
            #score=models.Score.query.all()
            return render_template('student_profile.html',student_profile=student_profile,
                                   dob_str=dob_str, grade=grade, classes=classes, 
                                   subject_current=subject_current, score=score, type_test=type_test,semesterI=semesterI,score_grade=score_grade)
        return render_template('student_profile.html',student_profile=student_profile,dob_str=dob_str,grade=grade,classes=classes, type_test=type_test)




@app.route("/register")
def my_register():
    return render_template('register.html')

@app.route("/register", methods=['post'])
def my_register_process():
    data = request.form
    password = data['password']
    confirm = data['confirm']
    

    if password.__eq__(confirm):
       
        username = data['username']
        #res = cloudinary.uploader.upload(request.files['avatar'])
        teacher_id = data['teacher_id']
        try:
            user.add_user(teacher_id=teacher_id, username=username, password=password)
            return redirect("/login")
        except Exception as ex:
            msg = str(ex)
            print(ex)
    else:
        msg = 'Password does not match!!!'

    return render_template('register.html', msg=msg)


@login.user_loader
def get_user(user_id):
    return user.get_user_by_id(user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
