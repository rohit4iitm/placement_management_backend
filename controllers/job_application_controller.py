# controllers/job_application_controller.py

from models.student import Student
from models.job_application import JobApplication
from models import db

def apply_for_job(student_id, company_id,resume_id):
    student = Student.query.get(student_id)
    if student.status == "inactive":
        return None
    job_application = JobApplication(
        student_id=student_id,
        company_id=company_id,
        resume_id=resume_id,
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
