#!/usr/bin/env python3
"""
Integration test for app
"""

import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    Test the Signup functionality of app
    """
    payload = {"email": email, "password": password}
    expected_res = {"email": email, "message": "user created"}
    res = requests.post(BASE_URL + "/users", data=payload)
    assert res.json() == expected_res


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test authenticating feature of app with wrong password
    """
    payload = {"email": email, "password": password}
    res = requests.post(BASE_URL + "/sessions", data=payload)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test authentication feature of app
    """
    payload = {"email": email, "password": password}
    res = requests.post(BASE_URL + "/sessions", data=payload)
    expected_res = {"email": email, "message": "logged in"}
    assert res.json() == expected_res
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Tests users authorization with unauthorized user
    """
    res = requests.get(BASE_URL + '/profile')
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Tests users authorization with authorized user
    """
    cookies = {"session_id": session_id}
    res = requests.get(BASE_URL + '/profile', cookies=cookies)
    # print("Line 58 of profile_logged()", res.status_code)
    expected_res = {"email": EMAIL}
    assert res.json() == expected_res


def log_out(session_id: str) -> None:
    """
    Tests the log_out feature
    """
    cookies = {"session_id": session_id}
    res = requests.delete(BASE_URL + '/sessions', cookies=cookies)
    # print(res.url)
    assert res.url == BASE_URL + '/'


def reset_password_token(email: str) -> str:
    """
    Test the reset password token feature
    """
    data = {"email": email}
    res = requests.post(BASE_URL + '/reset_password', data=data)
    reset_token = res.json().get('reset_token')
    expected_res = {"email": email, "reset_token": reset_token}
    assert res.json() == expected_res
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test the update password feature
    """
    payload = {"email": email, "reset_token": reset_token,
               "new_password": new_password}
    res = requests.put(BASE_URL + '/reset_password', data=payload)
    expected_res = {"email": email, "message": "Password updated"}
    assert res.json() == expected_res


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
