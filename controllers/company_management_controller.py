# controllers/company_management_controller.py

from models.company_management import CompanyManagement
from models import db

def record_company_action(company_id, admin_id, action):
    company_action = CompanyManagement(
        company_id=company_id,
        admin_id=admin_id,
        action=action,
        action_date=db.func.current_date()
    )
    db.session.add(company_action)
    db.session.commit()
    return company_action

def get_company_actions(company_id):
    return CompanyManagement.query.filter_by(company_id=company_id).all()
