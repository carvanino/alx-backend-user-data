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
        if path is not None and path[-1] != "/":
            path = path + '/'
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False
        if path not in excluded_paths:
            return True

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
