# controllers/student_controller.py

from models.student import Student
from models import db
from werkzeug.security import generate_password_hash, check_password_hash

def create_student(data):
    password_hash = generate_password_hash(data['password'])
    student = Student(
        name=data['name'],
        email=data['email'],
        password=password_hash,
        course=data['course'],
        branch=data['branch'],
        section=data['section'],
        prn = data['prn'],
        batch = data['batch'],
        status=data.get('status', 'active')
    )
    db.session.add(student)
    db.session.commit()
    return student

def login_student(email, password):
    student = Student.query.filter_by(email=email).first()
    if student and check_password_hash(student.password, password):
        return student
    return None

def get_student(student_id):
    return Student.query.get(student_id)

def get_all_student():
    return Student.query.all()

def change_password(data, student_id):
    student = Student.query.get(student_id)
    if student and check_password_hash(student.password, data['password_current']):
        password_hash = generate_password_hash(data['password'])
        student.password = password_hash
        db.session.add(student)
        db.session.commit()
        return student
    else:
        return None
    
def change_profile(data, student_id):
    student = Student.query.get(student_id)
    if student:
        student.name = data['name']
        student.email = data['email']
        student.batch = data['batch']
        student.prn = data['prn']
        db.session.add(student)
        db.session.commit()
        return student
    else:
        return None