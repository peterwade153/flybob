import os
import logging
import datetime

import jwt
from functools import wraps
from flask import request, jsonify

from app import app
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist


def encode_auth_token(user_id):
    """
    Generate auth tokens
    """
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=5),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")
    except Exception as e:
        app.logger.error("Encoding token failed due to:- "+e)
        return f"an error {e} occurred while encoding the token"


def token_required(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                token = auth_header
        else:
            app.logger.info("Token required")
            return jsonify({"message": "Token missing"}), 403

        # check if token is not blacklisted
        is_blacklisted = TokenBlacklist.get_by(token=token)
        if is_blacklisted:
            return jsonify({"message": "Invalid token, please login!"}), 403

        try:
            payload = jwt.decode(token, os.environ.get("SECRET_KEY"))
            current_user = payload["sub"]
        except jwt.ExpiredSignatureError:
            app.logger.error("Token expired")
            return jsonify({"message": "Token expired, please login!"}), 403
        except jwt.InvalidTokenError:
            app.logger.error("Token invalid")
            return jsonify({"message": "Invalid token"}), 403

        return func(current_user, *args, **kwargs)

    return decorate


def admin_required(func):
    @wraps(func)
    def admin_check(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                token = auth_header

        try:
            payload = jwt.decode(token, os.environ.get("SECRET_KEY"))
            user_id = payload["sub"]

            user = User.get(id=user_id)
            if not user.role:
                app.logger.info('Admin access required.')
                return (
                    jsonify({"message": "Unauthorized action, Admins only"}),
                    401,
                )
        except Exception as e:
            app.logger.error("Admin token invalid or expired")
            return jsonify({"message": "Action failed, please try again"}), 400
        return func(*args, **kwargs)

    return admin_check
