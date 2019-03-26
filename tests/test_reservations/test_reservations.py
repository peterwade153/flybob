import unittest
import json

from app import app
from app.models.base import db
from app.models.user import User
from app.models.flights import Flight


class ReservationsTestCase(unittest.TestCase):
    

    def setUp(self):
        self.app = app.test_client()
        app.testing = True

        self.user_data = {
            'username':'john123',
            'email':'john123@john.com',
            'password':'john1234556'
        }

        self.reservation_data = {
            'flight_id': 1,
            'seats_booked': 2
        }

        with app.app_context():
            db.drop_all()
            db.create_all()

            #create admin user
            user = User(username='john123', email='john123@john.com', password='john1234556', role=True)
            user.save()
            flight = Flight(name='KQ-FTK123', origin='JFK-NAIROBI', destination='LGN-BST Boston', duration='8hrs',
                            departure='2019-04-25T18:30:49-0300', capacity=233, arrive='2019-04-26T18:30:49-0300',
                            aircraft="Boeing 8 max", status='scheduled', created_by=1)
            flight.save()
    
    def test_add_reservations(self):
        res = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_data),
                        headers={'Content-Type':'application/json'})
        token = json.loads(res.data.decode())['access_token']
        result = self.app.post('/api/v1/reservations', data=json.dumps(self.reservation_data), headers={
                    'Content-Type':'application/json',
                    'Authorization':token})
        self.assertEqual(result.status_code, 201)
    
    def test_add_reservations_for_non_existant_flight(self):
        res = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_data),
                        headers={'Content-Type':'application/json'})
        token = json.loads(res.data.decode())['access_token']
        non_existant_data = {
            'flight_id': 6,
            'seats_booked': 2
        }
        result = self.app.post('/api/v1/reservations', data=json.dumps(non_existant_data), headers={
                    'Content-Type':'application/json',
                    'Authorization':token})
        self.assertEqual(result.status_code, 404)

    def test_add_reservations_for_with_wrong_data(self):
        res = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_data),
                        headers={'Content-Type':'application/json'})
        token = json.loads(res.data.decode())['access_token']
        invalid_data = {
            'flight_iddfty': 6,
            'seats_bookedjhbjhb': 2
        }
        result = self.app.post('/api/v1/reservations', data=json.dumps(invalid_data), headers={
                    'Content-Type':'application/json',
                    'Authorization':token})
        self.assertEqual(result.status_code, 400)
    
    def test_get_all_reservations(self):
        res = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_data),
                        headers={'Content-Type':'application/json'})
        token = json.loads(res.data.decode())['access_token']
        result = self.app.get('/api/v1/reservations', headers={
                    'Content-Type':'application/json',
                    'Authorization':token})
        self.assertEqual(result.status_code, 200)
    
    def test_get_a_reservations(self):
        res = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_data),
                        headers={'Content-Type':'application/json'})
        token = json.loads(res.data.decode())['access_token']
        self.app.post('/api/v1/reservations', data=json.dumps(self.reservation_data), headers={
                    'Content-Type':'application/json','Authorization':token})
        result = self.app.get('/api/v1/reservations/1', headers={
                    'Content-Type':'application/json',
                    'Authorization':token})
        self.assertEqual(result.status_code, 200)
    
    def test_get_a_non_existant_reservations(self):
        res = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_data),
                        headers={'Content-Type':'application/json'})
        token = json.loads(res.data.decode())['access_token']
        result = self.app.get('/api/v1/reservations/1', headers={
                    'Content-Type':'application/json',
                    'Authorization':token})
        self.assertEqual(result.status_code, 404)
    
    def test_update_a_non_existant_reservations(self):
        res = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_data),
                        headers={'Content-Type':'application/json'})
        token = json.loads(res.data.decode())['access_token']
        update_data = {
            'seats_booked': 2,
            'status':'cancelled'
        }
        result = self.app.put('/api/v1/reservations/1', data=json.dumps(update_data), headers={
                    'Content-Type':'application/json',
                    'Authorization':token})
        self.assertEqual(result.status_code, 404)
    
    def test_update_a_reservations(self):
        res = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_data),
                        headers={'Content-Type':'application/json'})
        token = json.loads(res.data.decode())['access_token']
        self.app.post('/api/v1/reservations', data=json.dumps(self.reservation_data), headers={
                    'Content-Type':'application/json','Authorization':token})
        update_data = {
            'seats_booked': 2,
            'status':'cancelled'
        }
        result = self.app.put('/api/v1/reservations/1', data=json.dumps(update_data), headers={
                    'Content-Type':'application/json',
                    'Authorization':token})
        self.assertEqual(result.status_code, 200)
    
    def test_update_a_reservations_with_invalid_data(self):
        res = self.app.post('/api/v1/auth/login', data=json.dumps(self.user_data),
                        headers={'Content-Type':'application/json'})
        token = json.loads(res.data.decode())['access_token']
        self.app.post('/api/v1/reservations', data=json.dumps(self.reservation_data), headers={
                    'Content-Type':'application/json','Authorization':token})
        update_data = {
            'flight_booked': 2,
            'status':'cancelled'
        }
        result = self.app.put('/api/v1/reservations/1', data=json.dumps(update_data), headers={
                    'Content-Type':'application/json',
                    'Authorization':token})
        self.assertEqual(result.status_code, 400)
    
