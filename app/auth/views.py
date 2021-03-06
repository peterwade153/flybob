import os

from flask import request, jsonify
from flask.views import MethodView
import cloudinary.uploader

from app import app
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.auth.auth_utils import (
    check_for_all_fields_signup,
    check_for_all_fields_login,
    check_email_and_password_valid,
    check_wrong_password,
    check_image_is_valid,
)
from utils.validation import allowed_image_extensions, limit_content_length
from utils.auth_token import encode_auth_token, token_required, admin_required


class RegisterUserView(MethodView):
    """
    Registration of users
    params: Username, Email, Password
    """

    def post(self):

        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        fields_res = check_for_all_fields_signup(username, email, password)
        if fields_res:
            return fields_res

        invalid_res = check_email_and_password_valid(email, password)
        if invalid_res:
            return invalid_res

        user = User.get_by(email=email)
        if user:
            app.logger.info(
                "User with email " + email + " is already registered"
            )
            return (
                jsonify(
                    {
                        "message": "User with email: "
                        + email
                        + " already registered",
                        "status": "Failed",
                    }
                ),
                409,
            )

        try:
            new_user = User(username=username, email=email, password=password)
            new_user.save()

            # generate  access token
            access_token = encode_auth_token(user_id=new_user.id)

            return (
                jsonify(
                    {
                        "message": "User successfully registered",
                        "status": "Success",
                        "access_token": access_token.decode("UTF-8"),
                    }
                ),
                201,
            )

        except Exception as e:
            app.logger.error("User registration failed due this:- " + e)
            return (
                jsonify(
                    {
                        "message": "Registration failed. Please try again",
                        "status": "Failed",
                    }
                ),
                401,
            )


class LoginUserView(MethodView):
    """
    Login users
    params: Email, Password
    """

    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        fields_res = check_for_all_fields_login(email, password)
        if fields_res:
            return fields_res

        invalid_res = check_email_and_password_valid(email, password)
        if invalid_res:
            return invalid_res

        user = User.get_by(email=email)

        if not user:
            return (
                jsonify(
                    {
                        "message": "Please sign up to create an account",
                        "status": "Failed",
                    }
                ),
                400,
            )

        check_password_res = check_wrong_password(user.password, password)
        if check_password_res:
            app.logger.info("Failed login for user with email:- " + email)
            return check_password_res

        # generate  access token
        access_token = encode_auth_token(user_id=user.id)
        return (
            jsonify(
                {
                    "message": "Logged in successfully",
                    "status": "Success",
                    "access_token": access_token.decode("UTF-8"),
                }
            ),
            200,
        )


class LogoutView(MethodView):
    """
    Logs out user
    """

    decorators = [token_required]

    def post(self, current_user):
        token = request.headers["Authorization"]

        new_blacklist_token = TokenBlacklist(token=token)
        new_blacklist_token.save()
        return (
            jsonify(
                {"message": "Logged out successfully", "status": "Success"}
            ),
            200,
        )


class UserPassportphotoView(MethodView):
    """
    User upload passport photo to cloudinary
    params: image
    """

    decorators = [token_required, limit_content_length]

    def post(self, current_user):  
        if 'file' not in request.files:
            return (
                jsonify(
                    {"message": "No image was uploaded", "status": "Failed"}
                ),
                400,
            )
        image_file = request.files["file"]

        image_res = check_image_is_valid(image_file)
        if image_res:
            app.logger.info("Invalid file upload with wrong extension")
            return image_res

        user = User.get(id=current_user)
        try:
            upload_res = cloudinary.uploader.upload(image_file)
            stored_img_url = upload_res.get("url")
            if stored_img_url:
                user.update(passport_photo_url=stored_img_url)
                return (
                    jsonify(
                        {
                            "message": "Photo successfully uploaded",
                            "status": "Success",
                        }
                    ),
                    200,
                )
        except Exception as e:
            app.logger.error(
                "Photo upload failed for user:- "
                + user.email
                + " because of "
                + e
            )
            return (
                jsonify(
                    {
                        "message": "Passport photo upload failed, please try again",
                        "status": "Failed",
                    }
                ),
                400,
            )


class UpdateUserRole(MethodView):
    """
    Updates user role
    """

    decorators = [token_required, admin_required]

    def post(self, current_user, user_id):
        user = User.get(id=user_id)

        if not user.role:
            user.update(role=True)
            return (
                jsonify(
                    {
                        "message": "User role upgraded to Admin.",
                        "status": "Success",
                    }
                ),
                200,
            )
        # else down grade them to normal users
        user.update(role=False)
        return (
            jsonify(
                {
                    "message": "User role downgraded to normal user",
                    "status": "sucess",
                }
            ),
            200,
        )
