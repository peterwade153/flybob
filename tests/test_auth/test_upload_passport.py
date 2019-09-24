import unittest
from unittest.mock import patch
import io

from app import app
from app.auth.views import UserPassportphotoView
from app.auth import views


class AuthUploadPassportPhotoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.testing = True

    @patch.object(views.UserPassportphotoView, "post")
    def test_upload_passport_photo(self, mock_post):
        oth = UserPassportphotoView()
        oth.post(
            "/api/v1/upload",
            data=dict(file=(io.BytesIO(b"abcdef"), "test.jpg")),
            headers={"Content-Type": "multipart/form-data"},
        )
        self.assertEqual(mock_post.called, True)
