import os
import datetime

import jwt


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

