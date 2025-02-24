# models/company_management.py

from . import db

class CompanyManagement(db.Model):
    __tablename__ = 'company_management'
    management_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    admin_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50))
    action_date = db.Column(db.Date)

    def to_dict(self):
        return {
            "company_id": self.company_id,
            "management_id": self.management_id,
            "admin_id": self.admin_id,
            "action": self.action,
            "action_date": self.action_date
        }