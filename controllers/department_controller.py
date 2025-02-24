from models.department_admin import DepartmentAdmin
from models import db
from werkzeug.security import generate_password_hash, check_password_hash

def create_admin(data):
    password_hash = generate_password_hash(data['password'])
    admin = DepartmentAdmin(
        name=data['name'],
        email=data['email'],
        department= data['department'],
        password=password_hash
    )
    db.session.add(admin)
    db.session.commit()
    return admin

def login_admin(email, password):
    admin = DepartmentAdmin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password, password):
        return admin
    return None

def get_admin(admin_id):
    return DepartmentAdmin.query.get(admin_id)

