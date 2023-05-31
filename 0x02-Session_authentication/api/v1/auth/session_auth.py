#!/usr/bin/env python3
"""
Holds the sub class SessionAuth from Auth
"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    A Session Authentication mechanism
    """

    def __init__(self) -> None:
        super().__init__()
        pass
