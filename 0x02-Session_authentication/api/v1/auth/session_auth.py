#!/usr/bin/env python3
"""
Holds the sub class SessionAuth from Auth
"""

from typing import TypeVar
from flask import request
from api.v1.auth.auth import Auth
from api.v1.views.users import User
import uuid


class SessionAuth(Auth):
    """
    A Session Authentication mechanism
    """
    user_id_by_session_id = {}

    def __init__(self) -> None:
        super().__init__()
        pass

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for an existing user
        Args:
            user_id (str): ID of a user
        Return (str): The session ID of the user
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        Returns a User instance based on the cookie value
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)
