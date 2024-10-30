from flask import Blueprint, request, jsonify
from vaultShare.db import UserDB
from vaultShare.exceptions import NoUserFound
from sqlalchemy.exc import NoResultFound

user_db = UserDB()
# Create a user route blueprint
users_bp = Blueprint('users', __name__)

def process_user_details(user_obj):
    user = {
        'id': user_obj.get('id'),
        'username': user_obj.get('username'),
        'email': user_obj.get('email'),
        'role': user_obj.get('role'),
        'created_at': user_obj.get('created_at'),
        'memory_allocated': user_obj.get('memory_allocated'),
        'memory_used': user_obj.get('memory_used')
    }
    return user

@users_bp.route('/', methods=['GET'])
def app_users_details():
    limit = request.args.get('limit')
    users_obj = user_db.find_all_users(limit=limit)
    users = [process_user_details(user.__dict__) for user in users_obj]
    
    return jsonify(users)

@users_bp.route('/<username>', methods=['GET'])
def app_user_detail(username: str):
    try:
        obj = user_db.find_user(username=username)
        user = process_user_details(obj.__dict__)
    except NoResultFound:
        raise NoUserFound(f"No user {username} found.")
    return process_user_details(user)

@users_bp.route('/<username>', methods=['PUT'])
def update_user_details(username: str):
    """
    Update specified user details
    
    Only details like username, and email can be updated using this
    route
    """
    new_username = request.form.get('username')
    new_email = request.form.get('email')
    
    try:
        user = user_db.find_user(username=username)
    except NoResultFound:
        raise NoUserFound(f"No user {username} found.")
    
    update_filter = {"username": user.username}
    fields_updated = 0
    if new_username:
        fields_updated += user_db.update_user(update_filter, username=new_username)
    if new_email:
        fields_updated += user_db.update_user(update_filter, email=new_email)
    
    message = {"message": f"{fields_updated} fields were updated" if fields_updated else "No field has been updated"}  
    return jsonify(message)