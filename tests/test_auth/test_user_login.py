import unittest
import json

from app import app
from app.models.base import db


class AuthLoginTestCase(unittest.TestCase):
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

    def register_user(
        self,
        username="john123",
        email="john123@john.com",
        password="john1234556",
    ):
        user_data = {
            "username": username,
            "email": email,
            "password": password,
        }
        return self.app.post(
            "/api/v1/auth/register",
            data=json.dumps(user_data),
            headers={"Content-Type": "application/json"},
        )

    def test_login_user(self):
        reg = self.register_user()
        self.assertEqual(reg.status_code, 201)
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(res.status_code, 200)

    def tests_user_login_with_invalid_data(self):
        reg = self.register_user()
        self.assertEqual(reg.status_code, 201)
        users_data = {"email": "teste.com", "password": "@##103"}
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(users_data),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)

    def tests_unregistered_user_login(self):
        reg = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            content_type="application/json",
        )
        self.assertEqual(reg.status_code, 404)

    def tests_user_login_with_no_data(self):
        users_data = {}
        reg = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(users_data),
            content_type="application/json",
        )
        self.assertEqual(reg.status_code, 400)

    def tests_user_login_with_invalid_password(self):
        reg = self.register_user()
        self.assertEqual(reg.status_code, 201)
        users_data = {"email": "john123@john.com", "password": "10343443345"}
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(users_data),
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 401)
