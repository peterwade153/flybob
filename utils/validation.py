import os
import re

from functools import wraps
from flask import request, jsonify

from app import app


def validate_password(password):
    return re.match("^[A-Za-z0-9]{8,}", password)


def validate_email(email):
    return re.match("^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]{,100}$", email)


def allowed_image_extensions(image):
    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg"]
    name, ext = os.path.splitext(image.filename)
    return ext in (allowed_extensions)


def limit_content_length(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        content_length = request.content_length
        if (
            content_length
            and content_length > app.config["MAX_CONTENT_LENGTH"]
        ):
            return jsonify({"message": " File should not exceed 1 MB"}), 400
        return func(*args, **kwargs)

    return decorate
