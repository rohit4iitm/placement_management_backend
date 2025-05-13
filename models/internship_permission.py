# models/internship_permission.py

from datetime import datetime
from . import db

class InternshipPermission(db.Model):
    __tablename__ = 'internship_permissions'

    permission_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department_admin.department_admin_id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    internship_location = db.Column(db.String(200), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Optional: Add start_date and end_date for the internship period
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    
    # Relationships
    student = db.relationship('Student', backref=db.backref('internship_permissions', lazy=True))
    department = db.relationship('DepartmentAdmin', backref=db.backref('internship_permissions', lazy=True))

    def to_dict(self):
        return {
            'permission_id': self.permission_id,
            'student_id': self.student_id,
            'student_name': self.student.name if self.student else None,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'semester': self.semester,
            'internship_location': self.internship_location,
            'reason': self.reason,
            'status': self.status,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
