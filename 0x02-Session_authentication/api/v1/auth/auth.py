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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            # if '*' in excluded_path:
            if excluded_path.endswith('*'):
                pattern = excluded_path[:-1]
                if path.startswith(pattern):
                    return False
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request: request = None) -> str:
        """
        Returns None
        """
        if request is None:
            return None
        # if request.headers.get('Authorization'):
        if 'Authorization' in request.headers:
            # print(request.headers)
            return request.headers.get('Authorization')
        return None

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        Returns None
        """
        return None
