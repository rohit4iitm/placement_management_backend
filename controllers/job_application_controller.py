# controllers/job_application_controller.py

from models.job_application import JobApplication
from models import db

def apply_for_job(student_id, company_id):
    job_application = JobApplication(
        student_id=student_id,
        company_id=company_id,
        application_date=db.func.current_date(),
        status="applied"
    )
    db.session.add(job_application)
    db.session.commit()
    return job_application

def get_application(application_id):
    return JobApplication.query.get(application_id)

def get_student_applications(student_id):
    return JobApplication.query.filter_by(student_id=student_id).all()

def get_applications():
    return JobApplication.query.all()
