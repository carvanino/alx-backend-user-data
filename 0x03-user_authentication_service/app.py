#!/usr/bin/env python3
"""
A Simple flask app
"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def message():
    """
    Returns a Welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/profile')
def profile():
    """
    Rereives a users based on the session_id and return user email
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": "{}".format(user.email)}), 200
    abort(403)


@app.route('/users', methods=['POST'])
def users():
    """
    Implements the Sign_up route for the app
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": "{}".format(
            email), "message": "user created"})


@app.route('/sessions', methods=['POST'])
def login():
    """
    Implements the login route for the app
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        session_id = AUTH.create_session(email)
        out = jsonify({"email": email, "message": "logged in"})
        out.set_cookie("session_id", session_id)
        return out
    abort(401)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Reset a password with a reset token
    """
    try:
        email = request.form.get('email')
    except KeyError:
        abort(403)
    reset_token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Updates password end-point
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "message": "password updated"}), 200


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Deletes a users session Implemeting a logout route for the app
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
