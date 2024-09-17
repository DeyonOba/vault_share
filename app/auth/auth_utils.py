"""
Module contains functions needed for Authentication.
"""
import uuid


def _generate_uuid() -> str:
    """Generates a string representation of a new UUID."""
    return str(uuid.uuid4())
