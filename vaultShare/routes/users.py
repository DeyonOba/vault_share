from flask import Blueprint, request, jsonify
from vaultShare.db import UserDB

user_db = UserDB()
# Create a user route blueprint
users_bp = Blueprint('users', __name__)

def process_user_details(user_obj):
    user = {
        'id': user_obj.id,
        'username': user_obj.username,
        'email': user_obj.email,
        'role': user_obj.role,
        'created_at': user_obj.created_at,
        'memory_allocated': user_obj.memory_allocated,
        'memory_used': user_obj.memory_used
    }
    return user

@users_bp.route('/', methods=['GET'])
def app_users_details():
    limit = request.args.get('limit')
    users_obj = user_db.find_all_users(limit=limit)
    users = [process_user_details(user) for user in users_obj]
    
    return jsonify(users)

@users_bp.route('/<username>', methods=['GET'])
def app_user_detail(username: str):
    return process_user_details(user_db.find_user(username=username))


