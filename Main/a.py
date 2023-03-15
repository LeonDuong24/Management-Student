from flask import Flask, request, render_template, session,send_file,redirect,url_for,make_response,flash
from flask_login import login_user, logout_user
import sys
import os
current_dir = os.getcwd()

print(sys.path)
sys.path.append(os.path.join(current_dir,'Main'))

#from Main import app, dao#, admin
#from Main import login
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/login')
def my_login():
    return render_template('login.html')

@app.route("/login", methods=['post'])
def my_login_process():
    email = request.form['email']
    password = request.form['password']
    u = dao.auth_user(email, password)
    if u:
        login_user(user=u)
        return redirect('/')

    return render_template('login.html')

@app.route("/logout")
def my_logout():
    logout_user()
    return redirect("/login")

@app.route('/student_profile')
def student_profile():
    return render_template('student-profile.html')
@app.route('/test')
def test():
    return render_template('test.html')


@app.route("/register")
def my_register():
    return render_template('register.html')


# @login.user_loader
# def get_user(user_id):
#     return dao.get_user_by_id(user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)