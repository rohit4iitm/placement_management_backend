# controllers/internship_permission_controller.py

from models.internship_permission import InternshipPermission
from models.student import Student
from models.department_admin import DepartmentAdmin
from models import db
from datetime import datetime

def create_permission_request(data):
    """Create a new internship permission request by a student"""
    # Verify student exists
    student = Student.query.get(data['student_id'])
    if not student:
        return None, "Student not found"
    
    # Find appropriate department admin based on student's branch
    department_admin = DepartmentAdmin.query.filter_by(department=student.branch).first()
    if not department_admin:
        return None, "No department admin found for this branch"
    
    permission = InternshipPermission(
        student_id=data['student_id'],
        department_id=department_admin.department_admin_id,
        semester=data['semester'],
        internship_location=data['internship_location'],
        reason=data['reason'],
        start_date=datetime.fromisoformat(data['start_date']) if 'start_date' in data else None,
        end_date=datetime.fromisoformat(data['end_date']) if 'end_date' in data else None,
        status='pending'
    )
    
    db.session.add(permission)
    db.session.commit()
    return permission, "Permission request created successfully"

def get_permission_by_id(permission_id):
    """Get a specific permission request by ID"""
    return InternshipPermission.query.get(permission_id)

def get_student_permissions(student_id):
    """Get all permission requests for a specific student"""
    return InternshipPermission.query.filter_by(student_id=student_id).all()

def get_department_permissions(department_id):
    """Get all permission requests for a specific department"""
    return InternshipPermission.query.filter_by(department_id=department_id).all()

def get_all_permissions():
    """Get all permission requests (for admin)"""
    return InternshipPermission.query.all()

def update_permission_status(permission_id, status, updated_by):
    """Update the status of a permission request (approve/reject)"""
    permission = InternshipPermission.query.get(permission_id)
    
    if not permission:
        return None, "Permission request not found"
    
    # Check if the updater is authorized (either admin or the department admin for this request)
    if updated_by.get('role') == 'department_admin' and updated_by.get('id') != permission.department_id:
        return None, "You are not authorized to update this permission request"
    
    permission.status = status
    permission.updated_at = datetime.utcnow()
    
    db.session.commit()
    return permission, f"Permission request {status} successfully"

def update_permission_details(permission_id, data):
    """Update details of a permission request (by student before approval)"""
    permission = InternshipPermission.query.get(permission_id)
    
    if not permission:
        return None, "Permission request not found"
    
    # Only allow updates if status is still pending
    if permission.status != 'pending':
        return None, "Cannot update permission request that has already been processed"
    
    if 'semester' in data:
        permission.semester = data['semester']
    if 'internship_location' in data:
        permission.internship_location = data['internship_location']
    if 'reason' in data:
        permission.reason = data['reason']
    if 'start_date' in data:
        permission.start_date = datetime.fromisoformat(data['start_date'])
    if 'end_date' in data:
        permission.end_date = datetime.fromisoformat(data['end_date'])
    
    permission.updated_at = datetime.utcnow()
    
    db.session.commit()
    return permission, "Permission request updated successfully"

def delete_permission_request(permission_id, student_id):
    """Delete a permission request (only if pending and by the student who created it)"""
    permission = InternshipPermission.query.get(permission_id)
    
    if not permission:
        return False, "Permission request not found"
    
    # Verify the student is the one who created this request
    if permission.student_id != student_id:
        return False, "You are not authorized to delete this permission request"
    
    # Only allow deletion if status is still pending
    if permission.status != 'pending':
        return False, "Cannot delete permission request that has already been processed"
    
    db.session.delete(permission)
    db.session.commit()
    return True, "Permission request deleted successfully"
