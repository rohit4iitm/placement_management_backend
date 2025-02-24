# models/policy.py

from . import db

class Policy(db.Model):
    __tablename__ = 'policies'
    policy_id = db.Column(db.Integer, primary_key=True)
    policy_text = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return{
            "policy_id":self.policy_id,
            "policy_text":self.policy_text 
        }