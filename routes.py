from flask import Blueprint, request, jsonify
from controllers import (
    student_controller, 
    company_controller, 
    job_application_controller, 
    placement_controller,
    login_controller,
    policy_controller,
    password_change_history_controller,
    company_management_controller,
    admin_controller, 
    department_controller,
    resume_controller
)
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models.resume import Resume, Education, Experience, Skill, Project, Certification

api = Blueprint('api', __name__)

# Student Routes
@api.route('/students/register', methods=['POST'])
def register_student():
    data = request.get_json()
    student = student_controller.create_student(data)
    return jsonify({"student_id": student.student_id, "message": "Student registered successfully"}), 201

@api.route('/students/login', methods=['POST'])
def student_login():
    data = request.get_json()
    student = student_controller.login_student(data['email'], data['password'])
    if student:
        # Generate JWT token
        access_token = create_access_token(identity=student.student_id)
        return jsonify({"access_token": access_token,"id": student.student_id, "message": "Login successful", "user_type":"student"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@api.route('/student/password_change/<int:student_id>', methods=['PUT'])
def students_password_change(student_id):
    data = request.get_json()
    student = student_controller.change_password(data,student_id)
    if student is not None:
        return jsonify({"student_id":student.student_id, "message": "Password changes successfully"}), 201
    return jsonify({"student_id":"N/A", "message":"Password change unsuccessful"}), 301                                                       

@api.route('/students/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    student = student_controller.get_student(student_id)
    if student:
        return jsonify(student.to_dict()), 200
    return jsonify({"error": "Student not found"}), 404

@api.route('/students/total',methods=["GET"])
@jwt_required()
def get_total_students():
    students = student_controller.get_all_student()
    student_count = 0
    for i in students:
        student_count+=1
    return jsonify({"student_count":student_count}),200

@api.route('/student/profile/update/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = student_controller.change_profile(data,student_id)
    if student is not None:
        return jsonify({"student_id":student.student_id, "message": "Password changes successfully"}), 201
    return jsonify({"student_id":"N/A", "message":"Password change unsuccessful"}), 301     
    

# Admin Routes 
@api.route('/admin/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    admin = admin_controller.create_admin(data)
    return jsonify({"admin_id": admin.admin_id, "message": "Admin registered successfully"}), 201

@api.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    admin = admin_controller.login_admin(data['email'],data['password'])
    if admin:
        access_token = create_access_token(identity=admin.admin_id)
        return jsonify({"access_token":access_token,"id":admin.admin_id, "message":"Login successful", "user_type":"admin"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@api.route('/admin/password_change/<int:admin_id>', methods=['PUT'])
def admin_password_change(admin_id):
    data = request.get_json()
    admin = admin_controller.change_password(data,admin_id)
    if admin is not None:
        return jsonify({"admin_id":admin.admin_id, "message": "Password changes successfully"}), 201 
    return jsonify({"admin_id":"N/A", "message":"Password change unsuccessful"}), 301

@api.route('/admin/profile/update/<int:admin_id>', methods=['PUT'])
def admin_profile_change(admin_id):
    data = request.get_json()
    admin = admin_controller.change_profile(data,admin_id)
    if admin is not None:
        return jsonify({"admin_id":admin.admin_id, "message": "Profile changes successfully"}), 201 
    return jsonify({"admin_id":"N/A", "message":"Profile change unsuccessful"}), 301

@api.route('/admin/<int:admin_id>', methods=['GET'])
@jwt_required()
def get_admin(admin_id):
    admin = admin_controller.get_admin(admin_id)
    if admin:
        return jsonify(admin.to_dict()), 200
    return jsonify({"error": "Student not found"}), 404

# Department admin routes 
@api.route('/department/register', methods=['POST'])
def register_department_admin():
    data = request.get_json()
    dept_admin = department_controller.create_admin(data)
    return jsonify({"admin_id": dept_admin.department_admin_id, "message": "Admin registered successfully"}), 201 

@api.route('/department/login', methods=['POST'])
def department_login():
    data = request.get_json()
    admin = department_controller.login_admin(data['email'],data['password'])
    if admin:
        access_token = create_access_token(identity=admin.department_admin_id)
        return jsonify({"access_token":access_token,"id":admin.department_admin_id, "message":"Login successful", "user_type":"department", "branch":admin.department}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@api.route('/department/password_change/<int:department_id>', methods=['PUT'])
def department_password_change(department_id):
    data = request.get_json()
    department = department_controller.change_password(data,department_id)
    if department is not None: 
        return jsonify({"department_id":department.department_admin_id, "message":"Password changes successfully"}), 201 
    return jsonify({"department_id":"N/A", "message":"Password change unsuccessful"}), 301

@api.route('/department/profile/update/<int:department_id>', methods=['PUT'])
def department_profile_change(department_id):
    data = request.get_json()
    department = department_controller.change_profile(data,department_id)
    if department is not None:
        return jsonify({"admin_id":department.department_admin_id, "message": "Profile changes successfully"}), 201 
    return jsonify({"admin_id":"N/A", "message":"Profile change unsuccessful"}), 301

@api.route('/department/<int:admin_id>', methods=['GET'])
@jwt_required()
def get_department_admin(admin_id):
    admin = department_controller.get_admin(admin_id)
    if admin:
        return jsonify(admin.to_dict()), 200
    return jsonify({"error": "Student not found"}), 404

# Company Routes
@api.route('/companies', methods=['POST'])
@jwt_required()
def create_company():
    data = request.get_json()
    company = company_controller.create_company(data)
    return jsonify({"company_id": company.company_id, "message": "Company created successfully"}), 201

@api.route('/companies/<int:company_id>', methods=['GET', 'DELETE', 'PUT'])
@jwt_required()
def handle_company(company_id):
    if request.method == 'GET':
        company = company_controller.get_company(company_id)
        if company:
            return jsonify(company.to_dict()), 200
        return jsonify({"error": "Company not found"}), 404
    
    if request.method == 'DELETE':
        result, status_code = company_controller.delete_company(company_id)
        return jsonify(result), status_code
    
    if request.method == "PUT":
        data = request.get_json()
        company = company_controller.edit_company(company_id, data)
        if company:
            return jsonify(company.to_dict()),200
        return jsonify({"error": "Company not found"}), 404


@api.route('/companies', methods=['GET'])
def get_companies():
    search_query = request.args.get('search', '').strip().lower()

    if search_query:
        companies = company_controller.search_companies(search_query)
    else:
        companies = company_controller.get_all_companies()

    return jsonify([company.to_dict() for company in companies]), 200


# Job Application Routes
@api.route('/students/<int:student_id>/apply', methods=['POST'])
@jwt_required()
def apply_job(student_id):
    data = request.get_json()
    student_application = job_application_controller.get_student_applications(student_id=student_id)
    for _ in student_application:
        if _.company_id == data['company_id']:
            return jsonify({"application_id":"N/A", "status":"Application already submitted"}), 201
    job_application = job_application_controller.apply_for_job(student_id, data['company_id'])
    if job_application is not None:
        return jsonify({"application_id": job_application.application_id, "status": "Application submitted"}), 201
    else:
        return jsonify({"application_id": "N/A", "status":"Application could not be placed. You are already placed"}), 201
    
@api.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    applications = job_application_controller.get_applications()
    if applications:
        return jsonify([application.to_dict() for application in applications]), 200
    return jsonify({"error": "Application not found"}), 404

@api.route('/applications/<int:application_id>', methods=['GET'])
@jwt_required()
def get_application(application_id):
    application = job_application_controller.get_application(application_id)
    if application:
        return jsonify(application.to_dict()), 200
    return jsonify({"error": "Application not found"}), 404

@api.route('/applications/student/<int:student_id>',methods=['GET'])
@jwt_required()
def get_student_applications(student_id):
    student_applications = job_application_controller.get_student_applications(student_id)
    if student_applications:
        return jsonify([student_application.to_dict() for student_application in student_applications]),200
    return jsonify({"error":"Application not found"}), 404

# Placement Routes
@api.route('/placements/record', methods=['POST'])
@jwt_required()
def record_placement_route():
    data = request.get_json()
    placement = placement_controller.record_placement(data['student_id'], data['company_id'], data['offer_letter'])
    if placement is not None:
        return jsonify({"placement_id": placement.placement_id, "message": "Placement recorded"}), 201
    else:
        return jsonify({"placement_id": "N/A", "message":"Student is already placed"}), 301

@api.route('/placements', methods=['GET'])
@jwt_required()
def get_all_placements():
    placements = placement_controller.get_all_placements()
    return jsonify([placement.to_dict() for placement in placements]), 200

@api.route('/placements/total',methods=["GET"])
@jwt_required()
def get_total_placement():
    placements = placement_controller.get_all_placements()
    placement_count = 0
    for i in placements:
        placement_count+=1
    return jsonify({"placement_count":placement_count}),200

@api.route('/placements/<int:placement_id>', methods=['GET'])
@jwt_required()
def get_placement(placement_id):
    placement = placement_controller.get_placement(placement_id)
    if placement:
        return jsonify(placement.to_dict()), 200
    return jsonify({"error": "Placement not found"}), 404

# Policy Routes
@api.route('/policies',methods=['POST'])
@jwt_required()
def create_policy():
    data = request.get_json()
    policy = policy_controller.create_policy(data['policy_text'])
    return jsonify({"application_id": policy.policy_id, "status": "Policy Created"}), 201

@api.route('/policies', methods=['GET'])
@jwt_required()
def get_policies():
    policies = policy_controller.get_policies()
    return jsonify([policy.to_dict() for policy in policies]), 200

@api.route('/policies/<int:policy_id>', methods=['GET'])
@jwt_required()
def get_policy(policy_id):
    policy = policy_controller.get_policy(policy_id)
    if policy:
        return jsonify(policy.to_dict()), 200
    return jsonify({"error": "Policy not found"}), 404

# Login Routes
@api.route('/logins', methods=['GET'])
@jwt_required()
def get_logins():
    logins = login_controller.get_all_logins()
    return jsonify([login.to_dict() for login in logins]), 200

@api.route('/logins/<int:login_id>', methods=['GET'])
@jwt_required()
def get_login(login_id):
    login = login_controller.get_user_login_history(login_id)
    if login:
        return jsonify(login.to_dict()), 200
    return jsonify({"error": "Login not found"}), 404

# Password Change History Routes
@api.route('/password_changes/<int:student_id>', methods=['GET'])
@jwt_required()
def get_password_changes(student_id):
    changes = password_change_history_controller.get_password_change_history(student_id)
    return jsonify([change.to_dict() for change in changes]), 200

# Company Management Routes
@api.route('/company_management/actions', methods=['GET'])
@jwt_required()
def get_company_actions():
    actions = company_management_controller.get_all_actions()
    return jsonify([action.to_dict() for action in actions]), 200

@api.route('/company_management/actions/<int:company_id>', methods=['GET'])
@jwt_required()
def get_company_actions_for_company(company_id):
    actions = company_management_controller.get_company_actions(company_id)
    return jsonify([action.to_dict() for action in actions]), 200

# Get all resumes
@api.route('/resumes', methods=['GET'])
def get_all_resumes():
    resumes = resume_controller.get_resumes()
    result = [resume.to_dict() for resume in resumes]
    return jsonify(result)

# Get a specific resume
@api.route('/resumes/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    resume = resume_controller.get_resume(resume_id)
    
    if resume is None:
        return jsonify({"error": "Resume not found"}), 404
    
    result = resume.to_dict()
    return jsonify(result)

# Create a new resume
@api.route('/resumes', methods=['POST'])
def create_resume():
    data = request.get_json()
    
    try:
        resume = resume_controller.create_resume(data)
        result = resume.to_dict()
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update an existing resume
@api.route('/resumes/<int:resume_id>', methods=['PUT'])
def update_resume(resume_id):
    data = request.json
    
    try:
        resume = resume_controller.get_resume(resume_id)
        
        if resume is None:
            return jsonify({"error": "Resume not found"}), 404
        
        resume = resume_controller.create_resume(data, resume)
        
        result = resume.to_dict()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a resume
@api.route('/resumes/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    
    try:
        resume = resume_controller.get_resume(resume_id)
        
        if resume is None:
            return jsonify({"error": "Resume not found"}), 404
        
        return jsonify({"message": "Resume deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
