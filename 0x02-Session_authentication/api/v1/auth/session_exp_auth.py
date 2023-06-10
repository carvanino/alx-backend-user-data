#!/usr/bin/env python3
"""
Hold a sub class SessionExpAuth from SessionAuth
"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Implements an Authentication Session with Expiration
    """

    def __init__(self) -> None:
        """ Initializes the class """
        super().__init__()
        session_duration = os.getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Dictionary that keeps track of the user_id and
        updates the user_id_by_session_id dictionary with that dictionary
        Returns the user's Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user_id so long the session is not expired
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if 'created_at' not in session_dictionary:
            return None
        created_at = session_dictionary['created_at']
        duration_sec = timedelta(seconds=self.session_duration)
        if created_at + duration_sec < datetime.now():
            return None
        return session_dictionary.get('user_id')
