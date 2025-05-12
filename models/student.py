# models/student.py

from . import db

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(50))
    branch = db.Column(db.String(50))
    section = db.Column(db.String(10))
    status = db.Column(db.String(20))
    batch = db.Column(db.String(50))
    prn = db.Column(db.String(8))
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'course': self.course,
            'branch': self.branch,
            'section': self.section,
            'status': self.status,
            'prn':self.prn,
            'batch':self.batch
        }
