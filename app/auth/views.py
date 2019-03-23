import os
import logging

from flask import Blueprint, request, jsonify
from flask.views import MethodView

from app.models.user import User
from utils.validation import validate_email, validate_password
from utils.auth_token import encode_auth_token, decode_auth_token


class RegisterUserView(MethodView):
    """
    Registration of users
    """
    def post(self):

        data =  request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, email, password]):
            return jsonify({
                'message' : 'All fields username, email or password are required',
                'status' : 'Failed'
            }), 400
        
        if not validate_email(email=email) or not validate_password(password=password):
            return jsonify({
                'message' : 'Please enter a valid email and password '
                            'not less than 8 charaters',
                'status'  : 'Failed'
            }), 400
        
        user = User.get_by(email=email)
        if user:
            return jsonify({
                'message' : 'User with email: '+email+' already registered',
                'status' : 'Failed'
            }), 409
        
        try:
            new_user = User(username=username, email=email, password=password)
            new_user.save()

            #generate  access token
            access_token = encode_auth_token(user_id=new_user.id)

            return jsonify({
                'message' : 'User successfully registered',
                'status' : 'Success',
                'access-token' : access_token.decode('UTF-8')
            }), 201

        except Exception as e:
            logging.error(f'An error {e} has occured')
            return jsonify({
                'message' : 'Registration failed. Please try again',
                'status' : 'Failed'
            }), 401
