

from . import db

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    linkedin = db.Column(db.String(100))
    github = db.Column(db.String(100))
    summary = db.Column(db.Text)
    
    # Relationships
    education = db.relationship("Education", back_populates="resume", cascade="all, delete-orphan")
    experience = db.relationship("Experience", back_populates="resume", cascade="all, delete-orphan")
    skills = db.relationship("Skill", back_populates="resume", cascade="all, delete-orphan")
    projects = db.relationship("Project", back_populates="resume", cascade="all, delete-orphan")
    certifications = db.relationship("Certification", back_populates="resume", cascade="all, delete-orphan")
    
    # Relationship to student
    student = db.relationship('Student', backref=db.backref('resumes', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'linkedin': self.linkedin,
            'github': self.github,
            'summary': self.summary,
            'education': [edu.to_dict() for edu in self.education],
            'experience': [exp.to_dict() for exp in self.experience],
            'skills': [skill.to_dict() for skill in self.skills],
            'projects': [proj.to_dict() for proj in self.projects],
            'certifications': [cert.to_dict() for cert in self.certifications]
        }


class Education(db.Model):
    __tablename__ = 'education'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    degree = db.Column(db.String(100))
    college = db.Column(db.String(100))
    location = db.Column(db.String(100))
    year = db.Column(db.String(20))
    
    resume = db.relationship("Resume", back_populates="education")
    
    def to_dict(self):
        return {
            'id': self.id,
            'degree': self.degree,
            'college': self.college,
            'location': self.location,
            'year': self.year
        }


class Experience(db.Model):
    __tablename__ = 'experience'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    duration = db.Column(db.String(50))
    description = db.Column(db.Text)
    
    resume = db.relationship("Resume", back_populates="experience")
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'duration': self.duration,
            'description': self.description
        }


class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    category = db.Column(db.String(100))
    items = db.Column(db.Text)
    
    resume = db.relationship("Resume", back_populates="skills")
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'items': self.items
        }


class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    title = db.Column(db.String(100))
    technologies = db.Column(db.String(200))
    description = db.Column(db.Text)
    
    resume = db.relationship("Resume", back_populates="projects")
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'technologies': self.technologies,
            'description': self.description
        }


class Certification(db.Model):
    __tablename__ = 'certifications'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    name = db.Column(db.String(100))
    issuer = db.Column(db.String(100))
    date = db.Column(db.String(50))
    
    resume = db.relationship("Resume", back_populates="certifications")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'issuer': self.issuer,
            'date': self.date
        }


