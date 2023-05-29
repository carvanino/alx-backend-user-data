#!/usr/bin/env python3
"""
Contains the sub class BasicAuth, inherited from Auth
"""


from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string
        Args:
            base64_authorization_header (str): A Base64 String to be decoded
        Returns:
            (str): The decoded value of base64_authorization_header
        """
        if base64_authorization_header and isinstance(
                base64_authorization_header, str):
            try:
                decoded_string = base64.b64decode(base64_authorization_header)
            except base64.binascii.Error:
                return None
            return decoded_string.decode('utf-8')
        return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Get the users email and password from a decoded string
        """
        email, password = None, None
        if decoded_base64_authorization_header and isinstance(
                decoded_base64_authorization_header,
                str) and ':' in decoded_base64_authorization_header:
            user_credential = decoded_base64_authorization_header.split(':')
            email = user_credential[0]
            password = user_credential[1]
            return (email, password)
        return (email, password)
