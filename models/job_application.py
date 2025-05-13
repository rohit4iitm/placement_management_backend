# models/job_application.py

from . import db

class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    application_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    application_date = db.Column(db.Date)
    status = db.Column(db.String(20))

    def to_dict(self):
        return {
            "application_id": self.application_date,
            "student_id": self.student_id,
            "company_id": self.company_id,
            "resume_id": self.resume_id,
            "application_date": self.application_date,
            "status": self.status
        }

