#!/usr/bin/env python3
"""
Holds a sub class UserSession from Base
"""

from models.base import Base


class UserSession(Base):
    """
    Create a new Authentication system based on a session ID
    stored in database
    """

    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
