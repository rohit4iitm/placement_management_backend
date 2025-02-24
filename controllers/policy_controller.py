# controllers/policy_controller.py

from models.policy import Policy
from models import db

def create_policy(policy_text):
    policy = Policy(policy_text=policy_text)
    db.session.add(policy)
    db.session.commit()
    return policy

def get_policies():
    return Policy.query.all()

def get_policy(policy_id):
    return Policy.query.get(policy_id)

def update_policy(policy_id, policy_text):
    policy = Policy.query.get(policy_id)
    if policy:
        policy.policy_text = policy_text
        db.session.commit()
    return policy

def delete_policy(policy_id):
    policy = Policy.query.get(policy_id)
    if policy:
        db.session.delete(policy)
        db.session.commit()
    return policy
