from flask import jsonify
from werkzeug.security import check_password_hash

from utils.validation import (
    validate_email,
    validate_password,
    allowed_image_extensions,
)


def check_for_all_fields_signup(username, email, password):
    """
    Returns an error if any of the fields is missing
    params: username, email, password
    """

    if not all([username, email, password]):
        return (
            jsonify(
                {
                    "message": "All fields username, email or password are required",
                    "status": "Failed",
                }
            ),
            400,
        )


def check_for_all_fields_login(email, password):
    """
    Returns an error if any of the fields is missing
    params: username, email, password
    """

    if not all([email, password]):
        return (
            jsonify(
                {
                    "message": "Username and password are required",
                    "status": "Failed",
                }
            ),
            400,
        )


def check_email_and_password_valid(email, password):
    """
    Return an error if the email or password is in valid
    params: email, password
    """
    if not validate_email(email) or not validate_password(password):
        return (
            jsonify(
                {
                    "message": "Please enter a valid email and password "
                    "not less than 8 charaters",
                    "status": "Failed",
                }
            ),
            400,
        )


def check_wrong_password(password, input_password):
    """
    Returns an error response when the input password is incorrect
    params: user_password, input_password
    """
    if not check_password_hash(password, input_password):
        return (
            jsonify(
                {
                    "Message": "Login failed, please try again!",
                    "Status": "Failed",
                }
            ),
            401,
        )


def check_image_is_valid(image_file):
    """
    Returns error response if invalid image file is received
    params: image_file
    """
    if not allowed_image_extensions(image_file):
        return (
            jsonify(
                {"message": "Only images are allowed", "status": "Failed"}
            ),
            400,
        )
