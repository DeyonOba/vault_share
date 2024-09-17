#!/usr/bin/env python3
"""
Module contains functions needed for Authentication.
"""
import uuid
import hashlib
import os


def _generate_uuid() -> str:
    """Generates a string representation of a new UUID."""
    return str(uuid.uuid4())

def _hash_password(password: str) -> str:
    """
    Generates a hashed user password.
    
    Args:
        password (str): User password
        
    Returns:
        str: hashed password
        
    REFERENCE:
        i. https://docs.python.org/3/library/os.html#os.urandom
        ii. https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac
    """
    # Generate salt of 16 bytes as recommended in the documentation
    salt: bytes = os.urandom(16)
    pwd: bytes = password.encode('utf-8')

    hash_pwd: bytes = hashlib.pbkdf2_hmac('sha256', pwd, salt, 100_000)
    # Add salt to the begining of the hashed password to ensure easy
    # password decyrption/validation
    return salt.hex() + hash_pwd.hex()
    
if __name__ == "__main__":
    print(f"Try generation UUID: {_generate_uuid()}")
    
    password = "BestPwd"
    print(f"{password=}")
    hashed_password = _hash_password(password)
    print(f"Try hashing password (hex): <{hashed_password}>")