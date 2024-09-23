"""
Module contains class for Authentication.
"""
from .auth_utils import _generate_uuid, verify_password
from vaultShare.db import DB, UserDB, WorkspaceDB
from vaultShare.db.models import User


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
            raise ValueError(f"User {username} already exists")
        
        try:
            user = self._userdb.find_user(email=email)
        except NoResultFound:
            user = None
            
        if user:
            raise ValueError(f"User {email} already exists")

        hashed_password = _hash_password(password)

        user = self._userdb.add_user(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        return user
