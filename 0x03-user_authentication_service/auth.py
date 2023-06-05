#!/usr/bin/env python3
"""
Defines a function that hashes a password
"""

from db import DB
from sqlalchemy.exc import NoResultFound
from user import User
from bcrypt import hashpw, gensalt, checkpw
from uuid import uuid4


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


def _generate_uuid() -> str:
    """
    Returns a string representation of a new UUID
    """
    return str(uuid4)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Implements a Sign_up feature
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
        else:
            raise ValueError("User {} already exists".format(email))
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates and Authenticates a user during login
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        if checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        return False
