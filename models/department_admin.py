# models/department_admin.py

from . import db

class DepartmentAdmin(db.Model):
    __tablename__ = 'department_admin'
    department_admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50))
    

    def to_dict(self):
        return {
            'department_admin_id': self.department_admin_id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
        }
