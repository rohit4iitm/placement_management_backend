# controllers/password_change_history_controller.py

from models.password_change_history import PasswordChangeHistory
from models import db

def log_password_change(student_id):
    change_record = PasswordChangeHistory(
        student_id=student_id,
        change_date=db.func.current_date()
    )
    db.session.add(change_record)
    db.session.commit()
    return change_record

def get_password_change_history(student_id):
    return PasswordChangeHistory.query.filter_by(student_id=student_id).all()
