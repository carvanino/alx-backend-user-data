#!/usr/bin/env python3
"""
A Simple flask app
"""

from flask import Flask, jsonify, request, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def message():
    """
    Returns a Welcome message
    """
    return jsonify({"message": "Bienvenue"})


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
