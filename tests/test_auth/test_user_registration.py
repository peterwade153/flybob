import unittest
import json

from app import app
from app.models.base import db


class AuthTestCase(unittest.TestCase):
    

    def setUp(self):
        self.app = app.test_client()
        app.testing = True

        self.user_data = {
            'username':'john123',
            'email':'john123@john.com',
            'password':'john1234556'
        }

        with app.app_context():
            db.drop_all()
            db.create_all()


    def test_register_user(self):
        reg = self.app.post('/api/v1/auth/register', data=json.dumps(self.user_data),
                            headers={'Content-Type':'application/json'})
        self.assertEqual(reg.status_code, 201)
    
    def test_same_user_registration(self):
        reg = self.app.post('/api/v1/auth/register', data=json.dumps(self.user_data),
                            headers={'Content-Type':'application/json'})
        self.assertEqual(reg.status_code, 201)
        sec_reg = self.app.post('/api/v1/auth/register', data=json.dumps(self.user_data),
                            headers={'Content-Type':'application/json'})
        self.assertEqual(sec_reg.status_code, 409)

    def tests_user_registering_with_invalid_data(self):
        users_data = {'username':'#$@#mo', 'email':'teste.com', 'password':'@##103'}
        reg = self.app.post('/api/v1/auth/register', data=json.dumps(users_data), 
                            content_type='application/json')
        self.assertEqual(reg.status_code, 400)

    def tests_user_registering_with_no_data(self):
        users_data = {}
        reg = self.app.post('/api/v1/auth/register', data=json.dumps(users_data), 
                            content_type='application/json')
        self.assertEqual(reg.status_code, 400)


