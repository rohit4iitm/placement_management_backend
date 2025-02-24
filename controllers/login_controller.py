# controllers/login_controller.py

from models.login import Login
from models import db

def log_user_login(user_id, user_type):
    login = Login(
        user_id=user_id,
        user_type=user_type,
        login_time=db.func.current_timestamp()
    )
    db.session.add(login)
    db.session.commit()
    return login

def log_user_logout(login_id):
    login = Login.query.get(login_id)
    if login:
        login.logout_time = db.func.current_timestamp()
        db.session.commit()
    return login

def get_user_login_history(user_id):
    return Login.query.filter_by(user_id=user_id).all()

def get_all_logins():
    return Login.query.all()