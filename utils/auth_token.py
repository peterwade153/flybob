import os
import logging
import datetime

import jwt
from functools import wraps
from flask import request, jsonify

from app.models.user import User


def encode_auth_token(user_id):
    """
    Generate auth tokens
    """
    try:
        payload = {
            'exp':datetime.datetime.utcnow() + datetime.timedelta(days=5),
            'iat':datetime.datetime.utcnow(),
            'sub':user_id
        }
        return jwt.encode(
            payload,
            os.getenv('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return(f"an error {e} occurred while encoding the token")

def decode_auth_token(auth_token):
    """
    Decode the authentication token
    """

    try:
        payload = jwt.decode(auth_token, os.getenv('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignature:
        return (f"Token  expired, please log in again.")
    except jwt.InvalidTokenError:
        return (f"Invalid token, please log in again")

def token_required(f):

    @wraps(f)
    def decorate(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        
        if not token:
            return jsonify({
                'message' : 'Token missing, please login to get an access_token',}), 403
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'))
            current_user = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message' : 'Token expired, please login!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message' : 'Invalid token:'}), 403

        return f(current_user, *args, **kwargs)
    
    return decorate

def admin_required(f):

    @wraps(f)
    def admin_check(current_user, *args, **kwargs):
        user_id = current_user
        try:
            user = User.get(id=user_id)
            if not user.role:
                return jsonify({
                    'message':'Unauthorized action, Admins only'
                }), 401
        except Exception as e:
            logging.error(f"An error:-> {e}")
            return jsonify({
                'message': 'Action failed, please try again'
            }), 400
        return f(*args, **kwargs)
    return admin_check
