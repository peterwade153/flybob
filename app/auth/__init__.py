from flask import Blueprint

from app.auth.views import (
    RegisterUserView,
    LoginUserView,
    UserPassportphotoView,
    LogoutView,
    UpdateUserRole,
)

auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/v1")

user_registeration = RegisterUserView.as_view("register_user")
auth_blueprint.add_url_rule(
    "/auth/register", view_func=user_registeration, methods=["POST"]
)

user_login = LoginUserView.as_view("login_user")
auth_blueprint.add_url_rule(
    "/auth/login", view_func=user_login, methods=["POST"]
)

user_passportphoto = UserPassportphotoView.as_view("user_photo")
auth_blueprint.add_url_rule(
    "/auth/upload", view_func=user_passportphoto, methods=["POST"]
)

user_logout = LogoutView.as_view("logout_user")
auth_blueprint.add_url_rule(
    "/auth/logout", view_func=user_logout, methods=["POST"]
)

user_role = UpdateUserRole.as_view("update_role")
auth_blueprint.add_url_rule(
    "/auth/update-role/<user_id>", view_func=user_role, methods=["POST"]
)
