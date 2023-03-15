from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from Main import db, app
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    avatar = Column(String(100))
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    user_role = Column(String(20), default='USER')

    def __str__(self):
        return self.name
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        import hashlib
        u = User(username='demo', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 name='ABC DEF',
                 avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg')
        db.session.add(u)
        db.session.commit()