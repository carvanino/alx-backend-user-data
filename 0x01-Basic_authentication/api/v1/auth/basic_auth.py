#!/usr/bin/env python3
"""
Contains the sub class BasicAuth, inherited from Auth
"""


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    The BasicAuth class
    """

    def __init__(self) -> None:
        super().__init__()

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the endoded credentials from the authorization header
        """
        if authorization_header and isinstance(
                authorization_header,
                str) and authorization_header.startswith('Basic '):
            encoded = authorization_header.split()
            return encoded[1]
        return None
