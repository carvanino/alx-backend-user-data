#!/usr/bin/env python3
"""
Holds a hash_password function
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bycrpyt
    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Uses bycrpt to validate that the provided password matches the hatched
    password
    Args:
        password (str): The password
        hashed_password (bytes): A hashed password
    Returns:
        bool: True or False
    """
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False
