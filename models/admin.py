# models/department_admin.py

from . import db

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    

    def to_dict(self):
        return {
            'admin_id': self.admin_id,
            'name': self.name,
            'email': self.email,
        }
