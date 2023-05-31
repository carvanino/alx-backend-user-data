#!/usr/bin/env python3
"""
Holds the sub class SessionAuth from Auth
"""

from api.v1.auth.auth import Auth
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
