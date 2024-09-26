"""
Module contains class for Authentication.
"""
from .auth_utils import _generate_uuid, verify_password, _hash_password
from vaultShare.db import DB, UserDB, WorkspaceDB
from vaultShare.db.models import User
from sqlalchemy.exc import NoResultFound


class Auth:
    """
    Auth class interacts with the authenticated database.
    
    Attributes:
        _db (DB): Protected instance database object.
    """
    def __init__(self):
        self._db = DB()
        self._userdb = UserDB()
        
    def register_user(self, username: str, email: str, password: str) -> User:
        """
        Use the email and password given to register a user.

        Args:
            username(str): Account username to be registed
            email(str): Acount user email
            password(str): Account user password

        Returns:
            user(User): User object.

        Raises:
            ValueError: If username or email already exists in db.
        """
        try:
            user = self._userdb.find_user(username=username)
        except NoResultFound:
            user = None

        if user:
            raise ValueError(f"Username '{username}' already exists")
        
        try:
            user = self._userdb.find_user(email=email)
        except NoResultFound:
            user = None
            
        if user:
            raise ValueError(f"User email '{email}' already exists")
        
        id_ = _generate_uuid()
        hashed_password = _hash_password(password)

        user = self._userdb.add_user(
            id=id_,
            username=username,
            email=email,
            password=hashed_password
        )
        return user

    def valid_login(self, password: str, username: str=None, email: str=None) -> User:
        """
        Finds user in the database using either the email or username, then
        checks if the hashed password is a match with the given password.
        
        Args:
            password (str): User password
            email (str): User email. Optional
            username (str): Username. Optional
        
        Return:
            user (User): User object of verified user.
            
        Raises:
            ValueError: If username or email is not found, or if the password
            is not a match
        """
        if email and not username:
            try:
                user = self._userdb.find_user(email=email)
                self._userdb.update_user({"email": email}, session_id=_generate_uuid())
            except NoResultFound:
                raise ValueError("Enter a registered <email>")
            
        elif username and not email:
            try:
                user = self._userdb.find_user(username=username)
                self._userdb.update_user({"username": username}, session_id=_generate_uuid())
            except NoResultFound:
                raise ValueError("Enter a registered <username>")
            
        if not verify_password(password, user.hashed_password):
            raise ValueError("Enter a valid <password>")
        
        return user
    
    def find_user_by_sessionid(self, session_id: str) -> User:
        """
        Finds user using the sessionid passed.
        """
        try:
            user = self._userdb.find_user(session_id=session_id)
        except NoResultFound:
            user = None
            
        return user
