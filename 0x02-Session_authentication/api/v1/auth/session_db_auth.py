#!/usr/bin/env python3
"""

"""

from flask import request
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Implement a Session Authetication with Database
    """

    def __init__(self) -> None:
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """
        Creates and stores new instance of UserSession and
        returns the Session ID
        """

        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        args = {}
        args['user_id'] = user_id
        args['session_id'] = session_id
        user_session = UserSession(**args)
        user_session.save()  # .db_USERSESSION.json
        # UserSession.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the User ID by requesting UserSession in the database based
        on session_id
        """
        if session_id is None:
            return None
        # This will instantiate the class with all objects in the file
        UserSession.load_from_file
        user_session_id = UserSession.search({'session_id': session_id})
        if not user_session_id:
            return None
        user_session_id = user_session_id[0]
        created_at = user_session_id.created_at
        if self.session_duration <= 0:
            return user_session_id.user_id
        duration_sec = timedelta(seconds=self.session_duration)
        if created_at + duration_sec < datetime.utcnow():
            return None
        return user_session_id.user_id

    def destroy_session(self, request: request = None):
        """
        Destroys the UserSession based on the Session ID from
        the request cookie
        """
        if request is None:
            return None
        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False
        UserSession.load_from_file
        user_session_id = UserSession.search({'session_id': sess_id})
        user_session_id = user_session_id[0]
        user_session_id.remove()
        user_session_id.save()
        return True
