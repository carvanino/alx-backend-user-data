#!/usr/bin/env python3
"""
Contains the sub class BasicAuth, inherited from Auth
"""


from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User
from flask import request


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
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Get the users email and password from a decoded string
        """
        email, password = None, None
        if decoded_base64_authorization_header and isinstance(
                decoded_base64_authorization_header,
                str) and ':' in decoded_base64_authorization_header:
            user_credential = decoded_base64_authorization_header.split(':', 1)
            # print(user_credential)
            email = user_credential[0]
            password = user_credential[1]
            return (email, password)
        return (email, password)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Returns an instance of User based on the email and password provided
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({"email": user_email})
        except KeyError:
            return None
        # print(user)
        if not user:
            return None
        # else:
        if user[0].is_valid_password(user_pwd):
            return user[0]
        return None

    def current_user(self, request: request = None) -> TypeVar('User'):
        """
        A complete Basic authentication
        Overloads Auth and retrieves the User instance for a request
        """
        authorization_header = self.authorization_header(request)
        encoded_str = self.extract_base64_authorization_header(
            authorization_header)
        decoded_str = self.decode_base64_authorization_header(encoded_str)
        user_credentials = self.extract_user_credentials(decoded_str)
        # print("User =", user_credentials)
        user_email = user_credentials[0]
        user_pwd = user_credentials[1]
        return self.user_object_from_credentials(user_email, user_pwd)
        # return self.user_object_from_credentials(*user_credentials)
