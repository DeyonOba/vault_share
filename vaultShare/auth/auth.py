"""
Module contains class for Authentication.
"""
from .auth_utils import _generate_uuid, verify_password
from app.db.db import DB


class Auth:
    """
    Auth class interacts with the authenticated database.
    
    Attributes:
        _db (DB): Protected instance database object.
    """
    def __init__(self):
        self._db = DB()
