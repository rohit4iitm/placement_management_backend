# models/login.py

from . import db

class Login(db.Model):
    __tablename__ = 'logins'
    login_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    login_time = db.Column(db.DateTime)
    logout_time = db.Column(db.DateTime)
    user_type = db.Column(db.String(20))

    def to_dict(self):
        return {
            "login_id" : self.login_id,
            "user_id" : self.user_id,
            "login_time" : self.login_time,
            "logout_time" : self.logout_time,
            "user_type" : self.user_type
        }

