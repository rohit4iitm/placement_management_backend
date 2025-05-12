from . import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    notification_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50)) 
    priority = db.Column(db.String(20), default='normal') 
    created_at = db.Column(db.DateTime, default=datetime.now)
    expires_at = db.Column(db.DateTime, nullable=True) 
    is_active = db.Column(db.Boolean, default=True)
    
    # Optional: Link to a company if the notification is about a recruitment
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=True)
    company = db.relationship('Company', backref=db.backref('notifications', lazy=True))
    target_batch = db.Column(db.String(50), nullable=True)  # e.g., '2022-2026'
    target_department = db.Column(db.String(100), nullable=True)  # e.g., 'Computer Science'
    # For tracking which students have read the notification
    reads = db.relationship('NotificationRead', back_populates='notification', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "title": self.title,
            "message": self.message,
            "category": self.category,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active,
            "company_id": self.company_id,
            "company_name": self.company.company_name if self.company else None,
        }

class NotificationRead(db.Model):
    __tablename__ = 'notification_reads'
    
    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.notification_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    read_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    notification = db.relationship('Notification', back_populates='reads')
    student = db.relationship('Student')
    
    # Ensure a student can only mark a notification as read once
    __table_args__ = (db.UniqueConstraint('notification_id', 'student_id', name='unique_notification_read'),)
    
    def to_dict(self):
        return {
            "id": self.id,
            "notification_id": self.notification_id,
            "student_id": self.student_id,
            "read_at": self.read_at.isoformat()
        }


