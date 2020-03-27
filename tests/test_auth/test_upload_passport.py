import unittest
from unittest.mock import patch, Mock
from werkzeug.datastructures import FileStorage
import io
import json

from app import app
from app.models.base import db
from app.models.user import User

from app.auth.views import UserPassportphotoView
from app.auth import views


class AuthUploadPassportPhotoTestCase(unittest.TestCase):

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

    @patch.object(views.UserPassportphotoView, "post")
    def test_upload_passport_photo(self, mock_post):
        upload = UserPassportphotoView()
        mock_post.return_value.status_code = 200
        res = upload.post(
            "/api/v1/auth/upload",
            data=dict(file=(io.BytesIO(b"abcdef"), "test.jpg")),
            headers={"Content-Type": "multipart/form-data"},
        )
        self.assertEqual(res.status_code, 200)


    def test_upload_photo_with_non_allowed_ext(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]

        data = {"file": (io.BytesIO(b'my file contents'), 'hello.txt')}

        result = self.app.post(
            "/api/v1/auth/upload", buffered=True,
            headers={
                "Authorization": token,
                "Content-Type" : 'multipart/form-data',
            },
            data=data,
        )
        self.assertEqual(result.status_code, 400)


    def test_no_photo_upload(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]

        result = self.app.post(
            "/api/v1/auth/upload", buffered=True,
            headers={
                "Authorization": token,
                "Content-Type" : 'multipart/form-data',
            },
            data={},
        )
        self.assertEqual(result.status_code, 400)
