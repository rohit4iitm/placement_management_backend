# models/password_change_history.py

from . import db

class PasswordChangeHistory(db.Model):
    __tablename__ = 'password_change_history'
    change_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    change_date = db.Column(db.Date)
    
    def to_dict(self):
        return {
            "change_id":self.change_id,
            "student_id":self.student_id,
            "change_date":self.change_date
        }
