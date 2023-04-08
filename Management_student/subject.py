import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from Management_student import db,models


def add_subject(request):
    try:
        subject = request.form['subject']
        note = request.form['note']
        subject=models.Subject(subject=subject,note=note)
        db.session.add(subject)
        db.session.commit()
        popup_content="Thêm môn học thành công"
        
    except:
        popup_content="Thêm môn học thất bại"
    return  popup_content 