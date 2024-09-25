"""Module contains custom Error classes."""


class MissingFieldError(ValueError):
    """Raises error when an important field is missing from a form-data.
    """
    msg=""
    def __init__(self, msg):
        self.msg = msg
