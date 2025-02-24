from models.admin import Admin
from models import db
from werkzeug.security import generate_password_hash, check_password_hash

def create_admin(data):
    password_hash = generate_password_hash(data['password'])
    admin = Admin(
        name=data['name'],
        email=data['email'],
        password=password_hash,
    )
    db.session.add(admin)
    db.session.commit()
    return admin

def login_admin(email, password):
    admin = Admin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password, password):
        return admin
    return None

def get_admin(admin_id):
    return Admin.query.get(admin_id)

