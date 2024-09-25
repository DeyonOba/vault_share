"""
VaultShare Flask app module.
"""
import os
from .auth.auth import Auth
from flask import (
    Flask,
    jsonify,
    request,
    make_response,
    redirect,
    abort
)
from vaultShare.auth import Auth

auth = Auth()
app = Flask(__name__)
        

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
    payload = {"message": "Welcome"}
    return jsonify(payload)

@app.route("/signup", methods=['POST'], strict_slashes=False)
def login():
    """
    Handles user account creation.
    """
    auth = Auth()
    
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not username:
        # abort(400, description=f"Fill in your username")
        raise MissingFieldError("Fill in your <username>")
    
    if not email:
        abort(400, description=f"Fill in your <email>")
        
    if not password:
        abort(400, description=f"Fill in your <password>")
        
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
            "next_action": ["login", "create_workspace", "join_workspace"]
        }
        return jsonify(payload), 200
    
    except ValueError as e:
        abort(400)

@app.errorhandler(MissingFieldError)
def missing_field(e):
    print(f"{e=}")
    error = {"error": e.msg}
    return jsonify(error), 402

    
def run_app():
    app.run(host="0.0.0.0", port="5000", debug=True)
