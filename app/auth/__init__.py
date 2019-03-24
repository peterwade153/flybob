from flask import Blueprint

from app.auth.views import RegisterUserView, LoginUserView

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1')

user_registeration = RegisterUserView.as_view('register_user')
auth_blueprint.add_url_rule('/auth/register', 
                            view_func=user_registeration, 
                            methods=['POST'])

user_login = LoginUserView.as_view('login_user')
auth_blueprint.add_url_rule('/auth/login', 
                            view_func=user_login,
                            methods=['POST'])