from models.resume import Resume, Education, Experience, Skill, Project, Certification
from models import db
def create_resume(data, resume=None):
    if resume is None:
        resume = Resume()
    
    # Set main resume attributes
    resume.name = data.get('name')
    resume.email = data.get('email')
    resume.phone = data.get('phone')
    resume.linkedin = data.get('linkedin')
    resume.github = data.get('github')
    resume.summary = data.get('summary')
    
    # Clear existing related items if updating
    if resume.id:
        # We'll clear and recreate related items
        resume.education.clear()
        resume.experience.clear()
        resume.skills.clear()
        resume.projects.clear()
        resume.certifications.clear()
    
    # Education
    for edu_data in data.get('education', []):
        if edu_data.get('degree') or edu_data.get('college'):  # Only add non-empty items
            education = Education(
                degree=edu_data.get('degree'),
                college=edu_data.get('college'),
                location=edu_data.get('location'),
                year=edu_data.get('year')
            )
            resume.education.append(education)
    
    # Experience
    for exp_data in data.get('experience', []):
        if exp_data.get('title') or exp_data.get('company') or exp_data.get('description'):
            experience = Experience(
                title=exp_data.get('title'),
                company=exp_data.get('company'),
                location=exp_data.get('location'),
                duration=exp_data.get('duration'),
                description=exp_data.get('description')
            )
            resume.experience.append(experience)
    
    # Skills
    for skill_data in data.get('skills', []):
        if skill_data.get('category') and skill_data.get('items'):
            skill = Skill(
                category=skill_data.get('category'),
                items=skill_data.get('items')
            )
            resume.skills.append(skill)
    
    # Projects
    for proj_data in data.get('projects', []):
        if proj_data.get('title') or proj_data.get('description'):
            project = Project(
                title=proj_data.get('title'),
                technologies=proj_data.get('technologies'),
                description=proj_data.get('description')
            )
            resume.projects.append(project)
    
    # Certifications
    for cert_data in data.get('certifications', []):
        if cert_data.get('name'):
            certification = Certification(
                name=cert_data.get('name'),
                issuer=cert_data.get('issuer'),
                date=cert_data.get('date')
            )
            resume.certifications.append(certification)
    
    db.session.add(resume)
    db.session.commit()
    return resume

def get_resumes():
    return Resume.query.all()

def get_resume(resume_id):
    return Resume.query.get(resume_id)

 