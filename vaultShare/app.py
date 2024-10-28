"""
VaultShare Flask app module.
"""
import os
from .auth.auth import Auth
from .exceptions import MissingFieldError, InvalidFieldType, UserAlreadyExists
from flask import (
    Flask,
    jsonify,
    request,
    make_response,
    redirect,
    abort
)
from pathvalidate import is_valid_filename
from .routes.users import users_bp

auth = Auth()
app = Flask(__name__)
app.register_blueprint(users_bp, url_prefix="/users")       

@app.route("/", methods=['GET'], strict_slashes=False)
def index():
    """
    Root endpoint
    
        GET "/"
        
        If user is logged in (i.e. has a session) then redirect user to account
        info page, else display VaultShare capability page.
        
        Returns:
            response: {"message": <content>}
    """
    payload = {"message": "Welcome to VaultShare"}
    return jsonify(payload)

@app.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Status endpoint.
    """
    return jsonify({"status": "OK"}), 200

@app.route("/signup", methods=['POST'], strict_slashes=False)
def register():
    """
    Handles user account creation.
    """
    auth = Auth()
    
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not username:
        raise MissingFieldError("Fill in your <username>")
    
    if not email:
        raise MissingFieldError("Fill in your <email>")
        
    if not password:
        raise MissingFieldError("Fill in your <password>")
    
    if type(username) is not str:
        raise InvalidFieldType(f"Invalid username <{username}> passed, username must be text")
    
    if type(email) is not str:
        raise InvalidFieldType(f"Invalid email <{email}> passed, email must be text")

    if type(password) is not str:
        raise InvalidFieldType(f"Invalid password <{password}> passed, password must be text")
    
    if not is_valid_filename(username):
        raise InvalidFieldType(f"Username <{username}> can't be use as workspace folder name")
    
    try:
        user = auth.register_user(username, email, password)
        payload = {
            "message": f"Awesome! {user.username} you are now a member of VaultShare family",
            "account_detail": {
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "created_at": user.created_at
            },
            "recommended_actions": ["login", "create_workspace", "join_workspace"]
        }
        return jsonify(payload), 201
    except ValueError as e:
        raise UserAlreadyExists(e.args[0])
    
@app.route("/login", methods=["POST"], strict_slashes=False)
def login():
    """
    Handles user account login.
    """
    user = None
    session_id = request.cookies.get("session_id")
    
    if session_id:
        user = auth.find_user_by_sessionid(session_id)
        
    if user:
        return jsonify({"message": "You have already logged in"}), 200
    
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not password:
        raise MissingFieldError("Fill in your <password>")
    
    if email and not username:
        try:
            user = auth.valid_login(password, email=email)
        except ValueError as e:
            raise InvalidFieldType(e.args[0])
    elif username and not email:
        try:
            user = auth.valid_login(password, username=username)
        except ValueError as e:
            raise InvalidFieldType(e.args[0])
    else:
        raise MissingFieldError("Enter a valid <email> or <username> to login")
    
    payload = {
        "message": f"Welcome back {user.username} to VaultShare",
        "session_id": user.session_id,
        "recommend_actions": ["checkNotification", "creatWorkspace", "joinWorkspace"]
    }
    return jsonify(payload), 200

@app.route("/logout", methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Endpoint handles user loggout.
    
    Request: DELETE "/sessions"

    Find the user with the requested session ID. If the user exists
    destroy the session and redirect the user to "GET '/'".
    If the user does not exist respond with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        abort(403)
        
    user = auth.find_user_by_sessionid(session_id=session_id)

    if not user:
        abort(403)

    if not auth.destroy_session(user.session_id):
        abort(422)
    return redirect("/")

@app.errorhandler(403)
def unauthorized_access(e):
    error = {"error": "Unauthorized access"}
    return jsonify(error), 403
  
@app.errorhandler(MissingFieldError)
def missing_field(e):
    error = {"error": e.msg}
    return jsonify(error), 402

@app.errorhandler(InvalidFieldType)
def missing_field(e):
    error = {"error": e.msg}
    return jsonify(error), 422

@app.errorhandler(ValueError)
def missing_field(e):
    error = {"error": e.msg}
    return jsonify(error), 400
   
def run_app():
    app.run(host="0.0.0.0", port="5000", debug=True)
