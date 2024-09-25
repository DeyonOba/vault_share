"""
Module contains class for Authentication.
"""
from .auth_utils import _generate_uuid, verify_password, _hash_password
from vaultShare.db import DB, UserDB, WorkspaceDB
from vaultShare.db.models import User
from sqlalchemy.exc import NoResultFound
from ..exceptions import UserAlreadyExists


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
            raise UserAlreadyExists(f"User email '{email}' already exists")
        
        id_ = _generate_uuid()
        hashed_password = _hash_password(password)

        user = self._userdb.add_user(
            id=id_,
            username=username,
            email=email,
            password=hashed_password
        )
        return user
