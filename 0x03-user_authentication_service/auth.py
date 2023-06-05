#!/usr/bin/env python3
"""
Defines a function that hashes a password
"""


from bcrypt import hashpw, gensalt

def _hash_password(password: str) -> bytes:
    """
    Hashes a password
    Args:
        password (str): The string to hash
    Return:
        (bytes): The hashed string
    """
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    return hashed_password