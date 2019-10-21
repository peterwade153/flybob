import unittest
import json

from app import app
from app.models.base import db
from app.models.user import User


class AuthTokenTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.testing = True

        self.flight_data = {}

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
            )
            user.save()

    def test_invalid_admin_token(self):

        token = f"blah blah"
        result = self.app.post(
            "/api/v1/flights",
            data=json.dumps(self.flight_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 400)

    def test_non_admin_token(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]
        result = self.app.post(
            "/api/v1/flights",
            data=json.dumps(self.flight_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 401)
    
    def test_no_token_passed(self):

        result = self.app.get(
            "/api/v1/flights",
            headers={
                "Content-Type": "application/json",
            },
        )
        self.assertEqual(result.status_code, 403)