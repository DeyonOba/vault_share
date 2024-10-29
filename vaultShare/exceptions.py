"""Module contains custom Error classes."""


class MissingFieldError(ValueError):
    """Raises error when an important field is missing from a form-data.
    """
    msg = ""
    def __init__(self, msg):
        self.msg = msg


class InvalidFieldType(ValueError):
    """
    Raises error when data passed in the form-data field is not accepted by
    database schema datatype outlined.
    """
    msg = ""
    def __init__(self, msg):
        self.msg = msg


class UserAlreadyExists(ValueError):
    """
    Raises error when a registered user already has the given
    credentials passed during new user registration.
    """
    msg = ""
    def __init__(self, msg):
        self.msg = msg
        
class NoUserFound(ValueError):
    msg=""
    def __init__(self, msg):
        self.msg = msg