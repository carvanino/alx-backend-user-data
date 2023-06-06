#!/usr/bin/env python3
"""
Defines a function that hashes a password
"""

from db import DB
from sqlalchemy.orm.exc import NoResultFound
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
    hashed_password = hashpw(password.encode(), gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """
    Returns a string representation of a new UUID
    """
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """
        Generates a session ID for a new user and returns the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return None
        else:
            session_id = _generate_uuid()
            # user.session_id = session_id
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves a User by session_id
        Args:
            session_id (str): users session_id
        Returns:
            (User | None): A user object or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Implements a Logout feature, by deleting users session
        """
        try:
            self._db.find_user_by(id=user_id)
        except Exception:
            return None
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset token for password
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Resets and update a users password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
