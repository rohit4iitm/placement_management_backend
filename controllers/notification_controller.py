# controllers/notification_controller.py

from datetime import datetime
from operator import and_, or_

from flask import jsonify
from models.notifications import Notification, NotificationRead
from models import db
from models.student import Student 

def create_notification(data):
    # Process expiration date if provided
    expires_at = None
    if data.get('expires_at'):
        try:
            expires_at = datetime.fromisoformat(data.get('expires_at'))
        except ValueError:
            return None
    
    # Create new notification
    notification = Notification(
        title=data.get('title'),
        message=data.get('message'),
        category=data.get('category')['value'],
        priority=data.get('priority', 'normal')['value'],
        expires_at=expires_at,
        company_id=data.get('company_id'),
        target_batch=data.get('target_batch'),
        target_department=data.get('target_department')
    )
    
    db.session.add(notification)
    db.session.commit()
    return notification 

def get_all_notifications(page, per_page, category,is_active):
    
    if is_active is not None:
        is_active = is_active.lower() == 'true'
    
    # Build query with filters
    query = Notification.query
    
    if category:
        query = query.filter(Notification.category == category)
    
    if is_active is not None:
        query = query.filter(Notification.is_active == is_active)
    
    # Order by created_at (newest first)
    query = query.order_by(Notification.created_at.desc())
    
    # Paginate results
    notifications_page = query.paginate(page=page, per_page=per_page)
    
    result = {
        "notifications": [n.to_dict() for n in notifications_page.items],
        "total": notifications_page.total,
        "pages": notifications_page.pages,
        "current_page": page
    }
    return result 

def get_notification(notification_id):
    result = Notification.query.get(notification_id) 
    return result 

def update_notification(notification_id, data):
    notification = Notification.query.get_or_404(notification_id)
    
    # Update fields if provided
    if 'title' in data:
        notification.title = data['title']
    if 'message' in data:
        notification.message = data['message']
    if 'category' in data:
        notification.category = data['category']['value']
    if 'priority' in data:
        notification.priority = data['priority']['value']
    if 'is_active' in data:
        notification.is_active = data['is_active']
    if 'expires_at' in data:
        if data['expires_at']:
            try:
                notification.expires_at = datetime.fromisoformat(data['expires_at'])
            except ValueError:
                return None
        else:
            notification.expires_at = None
    if 'company_id' in data:
        notification.company_id = data['company_id']
    if 'target_batch' in data:
        notification.target_batch = data['target_batch']
    if 'target_department' in data:
        notification.target_department = data['target_department']
    db.session.add(notification)
    db.session.commit()
    return notification
    
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    
    db.session.delete(notification)
    db.session.commit()
    return None 

def get_notification_student(page,per_page,unread_only,category,student_id):
    now = datetime.now()
    student = Student.query.get(student_id)
    # Base query for active notifications that are either not expired or have no expiration
    query = Notification.query.filter(
        Notification.is_active == True,
        or_(
            Notification.expires_at == None,
            Notification.expires_at > now
        )
    )
    
    # Filter by category if specified
    if category:
        query = query.filter(Notification.category == category)
    
    # Filter for targeted notifications
    # Include notifications that are either not targeted or targeted to this student's batch/department
    query = query.filter(
        or_(
            and_(Notification.target_batch == None, Notification.target_department == None),
            and_(
                or_(Notification.target_batch == None, Notification.target_batch == student.batch),
                or_(Notification.target_department == None, Notification.target_department == student.branch)
            )
        )
    )
    
    # Filter for unread notifications if requested
    if unread_only:
        # Get IDs of notifications the student has already read
        read_notification_ids = db.session.query(NotificationRead.notification_id).filter(
            NotificationRead.student_id == student_id
        ).all()
        read_notification_ids = [id[0] for id in read_notification_ids]
        
        # Exclude read notifications
        if read_notification_ids:
            query = query.filter(~Notification.notification_id.in_(read_notification_ids))
    
    # Order by priority (high first) and then by creation date (newest first)
    query = query.order_by(
        # Custom ordering for priority
        db.case(
            (Notification.priority == 'high', 1),
            (Notification.priority == 'normal', 2),
            else_=3
        ),
        Notification.created_at.desc()
    )
    
    # Paginate results
    notifications_page = query.paginate(page=page, per_page=per_page)
    
    # Get read status for each notification
    notification_list = []
    for notification in notifications_page.items:
        notification_dict = notification.to_dict()
        
        # Check if this notification has been read by the student
        read_record = NotificationRead.query.filter_by(
            notification_id=notification.notification_id,
            student_id=student_id
        ).first()
        
        notification_dict['is_read'] = read_record is not None
        if read_record:
            notification_dict['read_at'] = read_record.read_at.isoformat()
        
        notification_list.append(notification_dict)
    
    result = {
        "notifications": notification_list,
        "total": notifications_page.total,
        "pages": notifications_page.pages,
        "current_page": page
    }
    return result 

def mark_notification_read(notification_id, student_id):
    # Check if notification exists
    notification = Notification.query.get_or_404(notification_id)
    
    # Check if already marked as read
    existing_read = NotificationRead.query.filter_by(
        notification_id=notification_id,
        student_id=student_id
    ).first()
    
    if existing_read:
        return jsonify({"message": "Notification already marked as read", "read_at": existing_read.read_at.isoformat()}), 200
    
    # Mark as read
    read_record = NotificationRead(
        notification_id=notification_id,
        student_id=student_id
    )
    
    db.session.add(read_record)
    db.session.commit()
    return read_record

def mark_all_notifications_read(student_id):
    # Get student info for targeting
    student = Student.query.get_or_404(student_id)
    
    # Current time for checking expiration
    now = datetime.now()
    
    # Get all active, non-expired notifications for this student
    notifications = Notification.query.filter(
        Notification.is_active == True,
        or_(
            Notification.expires_at == None,
            Notification.expires_at > now
        ),
        or_(
            and_(Notification.target_batch == None, Notification.target_department == None),
            and_(
                or_(Notification.target_batch == None, Notification.target_batch == student.batch),
                or_(Notification.target_department == None, Notification.target_department == student.branch)
            )
        )
    ).all()
    
    # Get IDs of notifications already read
    read_notification_ids = db.session.query(NotificationRead.notification_id).filter(
        NotificationRead.student_id == student_id
    ).all()
    read_notification_ids = [id[0] for id in read_notification_ids]
    
    # Mark unread notifications as read
    count = 0
    for notification in notifications:
        if notification.notification_id not in read_notification_ids:
            read_record = NotificationRead(
                notification_id=notification.notification_id,
                student_id=student_id
            )
            db.session.add(read_record)
            count += 1
    
    db.session.commit()
    return count 

def get_notification_analytics(notification_id):
    if notification_id:
        # Analytics for a specific notification
        notification = Notification.query.get_or_404(notification_id)
        
        # Count total reads
        read_count = NotificationRead.query.filter_by(notification_id=notification_id).count()
        
        # Get total eligible students (based on targeting)
        student_query = Student.query
        if notification.target_batch:
            student_query = student_query.filter(Student.batch == notification.target_batch)
        if notification.target_department:
            student_query = student_query.filter(Student.branch == notification.target_department)
        
        total_students = student_query.count()
        
        # Calculate read percentage
        read_percentage = (read_count / total_students * 100) if total_students > 0 else 0
        
        # Get recent reads
        recent_reads = NotificationRead.query.filter_by(notification_id=notification_id).order_by(
            NotificationRead.read_at.desc()
        ).limit(10).all()
        
        result = {
            "notification": notification.to_dict(),
            "analytics": {
                "read_count": read_count,
                "total_students": total_students,
                "read_percentage": round(read_percentage, 2),
                "recent_reads": [
                    {
                        "student_id": read.student_id,
                        "read_at": read.read_at.isoformat()
                    } for read in recent_reads
                ]
            }
        }
        return result
    else:
        # Overall analytics
        total_notifications = Notification.query.count()
        active_notifications = Notification.query.filter_by(is_active=True).count()
        total_reads = NotificationRead.query.count()
        
        # Most read notifications
        most_read_subquery = db.session.query(
            NotificationRead.notification_id,
            db.func.count(NotificationRead.id).label('read_count')
        ).group_by(NotificationRead.notification_id).subquery()
        
        most_read = db.session.query(
            Notification,
            most_read_subquery.c.read_count
        ).join(
            most_read_subquery,
            Notification.notification_id == most_read_subquery.c.notification_id
        ).order_by(most_read_subquery.c.read_count.desc()).limit(5).all()
        
        result = {
            "total_notifications": total_notifications,
            "active_notifications": active_notifications,
            "total_reads": total_reads,
            "most_read_notifications": [
                {
                    "notification": notification.to_dict(),
                    "read_count": read_count
                } for notification, read_count in most_read
            ]
        }
        return result