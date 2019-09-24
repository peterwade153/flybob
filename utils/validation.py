import os
import re


def validate_password(password):
    return re.match("^[A-Za-z0-9]{8,}", password)


def validate_email(email):
    return re.match("^[A-Za-z0-9.]+@[A-Za-z0-9]+\.[A-Za-z0-9.]{,100}$", email)


def allowed_image_extensions(image):
    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg"]
    name, ext = os.path.splitext(image.filename)
    return ext in (allowed_extensions)
