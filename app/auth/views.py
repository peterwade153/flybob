import os

from flask import request, jsonify
from flask.views import MethodView
from werkzeug.security import check_password_hash
import cloudinary.uploader

from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from utils.validation import validate_email, validate_password, allowed_image_extensions
from utils.auth_token import encode_auth_token, token_required, admin_required


class RegisterUserView(MethodView):
    """
    Registration of users
    params: Username, Email, Password
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
                'access_token' : access_token.decode('UTF-8')
            }), 201

        except:
            return jsonify({
                'message' : 'Registration failed. Please try again',
                'status' : 'Failed'
            }), 401


class LoginUserView(MethodView):
    """
    Login users
    params: Email, Password
    """

    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return jsonify({
                'message' : 'Username and password are required',
                'status' : 'Failed'
            }), 400
        if not validate_password(password) or not validate_email(email):
            return jsonify({
                'message' : 'Password should have 8 or more characters' 
                            'and email should be valid',
                'status ' : 'Failed'
            }), 400

        user = User.get_by(email=email)
        if not user:
            return jsonify({
                'message' : 'User not registered, please register',
                'status' : 'Failed'
            }), 404
        if not check_password_hash(user.password, password):
            return jsonify({'Message':'An error occured,please try again!',
                            'Status':'Failed'}), 401
        #generate  access token
        access_token = encode_auth_token(user_id=user.id)
        return jsonify({
            'message' : 'Logged in successfully',
            'status' : 'Success',
            'access_token' : access_token.decode('UTF-8')
        }), 200


class LogoutView(MethodView):
    """
    Logs out user
    """
    decorators = [token_required]

    def post(self, current_user):
        token = request.headers['Authorization']

        new_blacklist_token = TokenBlacklist(token=token)
        new_blacklist_token.save()
        return jsonify({
            'message':'Logged out successfully',
            'status':'Success'
        }), 200


class UserPassportphotoView(MethodView):
    """
    User upload passport photo to cloudinary
    params: image
    """

    decorators = [token_required]

    def post(self, current_user):

        image_file = request.files['image']
        if not image_file:
            return jsonify({
                'message' : 'No image was uploaded',
                'status' : 'Failed'
            }), 400
        if not allowed_image_extensions(image_file):
            return jsonify({
                'message' : 'Only images are allowed',
                'status' : 'Failed'
            }), 400
        user = User.get(id=current_user)
        try:
            upload_res = cloudinary.uploader.upload(image_file)
            stored_img_url = upload_res.get('url')
            if stored_img_url:
                user.update(passport_photo_url=stored_img_url)
                return jsonify({
                    'message':'Photo successfully uploaded',
                    'status':'Success'
                }), 200
        except:
            return jsonify({
                'message' : 'Passport photo upload failed, please try again',
                'status' : 'Failed'
            }), 400


class UpdateUserRole(MethodView):
    """
    Updates user role
    """
    decorators = [token_required, admin_required]

    def post(self, current_user, user_id):
        user = User.get(id=user_id)

        if not user.role:
            user.update(role=True)
            return jsonify({
                'message': "User role upgraded to Admin.",
                'status' : "Success"
            }), 200
        #else down grade them to normal users
        user.update(role=False)
        return jsonify({
            'message':"User role downgraded to normal user",
            'status':'sucess'
        }), 200
