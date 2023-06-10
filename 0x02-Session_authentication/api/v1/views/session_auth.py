#!/usr/bin/env python3
"""
Handles all route for Session Authentication
"""

from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Authenticates a user with an email address
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    # print(user)
    if user is None or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if user.is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 401
    user_id = user.id
    from api.v1.app import auth
    session_id = auth.create_session(user_id)
    _my_session_id = os.getenv('SESSION_NAME')
    out = jsonify(user.to_json())
    out.set_cookie(_my_session_id, session_id)
    return out


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Deletes a users authenticated session, thereby implementing a
    logout feature
    """
    from api.v1.app import auth
    is_alive = auth.destroy_session(request)
    if not is_alive:
        abort(404)
    return jsonify({}), 200
