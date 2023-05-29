#!/usr/bin/env python3
"""
Contains the Auth Class
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manage API authentication
    """

    def __init__(self) -> None:
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False
        """
        return False

    def authorization_header(self, request: request = None) -> str:
        """
        Returns None
        """
        return None

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        Returns None
        """
        return None
