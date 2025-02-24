from . import db

class Company(db.Model):
    __tablename__ = 'companies'
    
    company_id = db.Column(db.Integer, primary_key=True)
    job_description = db.Column(db.Text)
    recruitment_date = db.Column(db.Date)
    company_name = db.Column(db.String(100))
    criteria = db.Column(db.String(200))
    eligibility = db.Column(db.String(200))
    category = db.Column(db.String(20))

    def to_dict(self):
        return {
            "company_id": self.company_id,
            "job_description": self.job_description,
            "recruitment_date": self.recruitment_date.isoformat() if self.recruitment_date else None,
            "company_name": self.company_name,
            "criteria": self.criteria,
            "eligibility": self.eligibility,
            "category": self.category
        }
