import unittest
import json

from app import app
from app.models.base import db


class AuthLogoutTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.testing = True

        self.user_data = {
            "username": "john123",
            "email": "john123@john.com",
            "password": "john1234556",
        }

        with app.app_context():
            db.drop_all()
            db.create_all()

    def register_user(self):
        return self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )

    def login_user(self):
        return self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )

    def test_logout_user(self):
        reg = self.register_user()
        self.assertEqual(reg.status_code, 201)
        res = self.login_user()
        token = json.loads(res.data.decode())["access_token"]
        self.assertEqual(res.status_code, 200)
        result = self.app.post(
            "/api/v1/auth/logout",
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 200)
