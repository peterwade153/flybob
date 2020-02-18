import unittest
from unittest.mock import patch, Mock
import io

from app.auth.views import UserPassportphotoView
from app.auth import views


class AuthUploadPassportPhotoTestCase(unittest.TestCase):

    @patch.object(views.UserPassportphotoView, "post")
    def test_upload_passport_photo(self, mock_post):
        upload = UserPassportphotoView()
        mock_post.return_value.status_code = 200
        res = upload.post(
            "/api/v1/upload",
            data=dict(file=(io.BytesIO(b"abcdef"), "test.jpg")),
            headers={"Content-Type": "multipart/form-data"},
        )
        self.assertEqual(res.status_code, 200)

    @patch.object(views.UserPassportphotoView, "post")
    def test_upload_photo_with_non_allowed_ext(self, mock_post):
        mock_post.return_value = Mock(status_code=400, json=lambda : {"message": "No image was uploaded", "status": "Failed"})
