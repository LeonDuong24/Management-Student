from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary
from flask_babel import Babel
app = Flask(__name__)
babel = Babel(app)
app.secret_key = '#%^&(*$%^&(78678675$%&^&$^%*&^%&*^'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/ManagementStudent?charset=utf8mb4"\
                                        % quote('1234')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

cloudinary.config(cloud_name='dnufcykyv', api_key='133469853585953', api_secret='_-lsIbO4d-_vDGdf35fN6aq69xc')

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'my_login'