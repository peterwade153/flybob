import unittest
import json

from app import app
from app.models.base import db
from app.models.user import User


class AuthUpdateRoleTestCase(unittest.TestCase):
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

            # create admin user
            user = User(
                username="john123",
                email="john123@john.com",
                password="john1234556",
                role=True,
            )
            user.save()
            # admin 2 whose role will be downgraded
            admin2 = User(
                username="admin123",
                email="admin123@john.com",
                password="admin1234556",
                role=True,
            )
            admin2.save()

    def test_user_update_role(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]
        new_user = {
            "username": "test123",
            "email": "test123@john.com",
            "password": "test1234567",
        }
        res = self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(new_user),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(res.status_code, 201)
        result = self.app.post(
            "/api/v1/auth/update-role/3",
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 200)

    def test_admin_user_update_role_to_default_user(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]
        result = self.app.post(
            "/api/v1/auth/update-role/2",
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 200)

    def test_non_admin_user_attempt_to_update_role(self):
        user_data = {
            "username": "badguy123",
            "email": "badguy123@john.com",
            "password": "badguy123456",
        }
        res = self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]

        new_data = {
            "username": "guy123",
            "email": "guy123@john.com",
            "password": "guy1234567",
        }
        rev = self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(new_data),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(rev.status_code, 201)
        result = self.app.post(
            "/api/v1/auth/update-role/2",
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 401)
