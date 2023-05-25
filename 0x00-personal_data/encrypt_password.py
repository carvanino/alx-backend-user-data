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
