from flask import Flask, request, render_template, session,send_file,redirect,url_for,make_response,flash
from flask_login import login_user, logout_user
import sys
import os
from datetime import datetime
current_dir = os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
#print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#sys.path.append(r"C:\Users\Alpaca\Desktop\Management-Student")


from Management_student import app, dao, admin,login,student,ClassScholastic,models,subject,teacher


@app.route('/chart', methods=['GET', 'POST'])
def chart():
    return render_template('chart.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/student')
def students():
    #page=request.args.get('page')
    students=student.get_all_student()
    return render_template('student.html',students=students)

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
def add_student():
    
    return render_template('add_student.html')

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
    u = dao.auth_user(username, password)
    print("u",u)
    
    if u:
        login_user(user=u)
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route("/logout")
def my_logout():
    logout_user()
    return redirect("/login")

@app.route('/student_profile/<int:student_id>')
def student_profile(student_id):
    student_profile=student.get_student_by_id(student_id)
    #dob = datetime.strptime(student_profile.date_of_birth, '%Y-%m-%d')
    dob_str = student_profile.date_of_birth.strftime('%Y-%m-%d')
    return render_template('student_profile.html',student_profile=student_profile,dob_str=dob_str)



@app.route("/register")
def my_register():
    return render_template('register.html')


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)
