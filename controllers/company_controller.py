# controllers/company_controller.py

from datetime import datetime
from models.company import Company
from models import db

def create_company(data):
    recruitment_date = datetime.strptime(data['recruitment_date'], '%Y-%m-%d').date()
    company = Company(
        job_description=data['job_description'],
        recruitment_date=recruitment_date,  # Use the converted date object
        company_name=data['company_name'],
        criteria=data['criteria'],
        eligibility=data['eligibility'],
        category=data['category']
    )
    
    db.session.add(company)
    db.session.commit()
    return company

def get_all_companies():
    return Company.query.all()

def get_company(company_id):
    return Company.query.filter(Company.company_id == company_id).first()

def delete_company(company_id):
    company = Company.query.filter(Company.company_id == company_id).first()
    
    if not company:
        return {"error": "Company not found"}, 404
    
    db.session.delete(company)
    db.session.commit()
    
    return {"message": f"Company with ID {company_id} deleted successfully."}, 200

def search_companies(search_query):
    return Company.query.filter(Company.company_name.ilike(f"%{search_query}%")).all()
