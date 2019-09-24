import unittest
import json

from app import app
from app.models.base import db
from app.models.user import User


class FlightTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.testing = True

        self.user_data = {
            "username": "john123",
            "email": "john123@john.com",
            "password": "john1234556",
        }
        self.flight_data = {
            "name": "KQ-FTK123",
            "origin": "JFK-NAIROBI",
            "destination": "LGN-BST Boston",
            "departure": "2019-04-25T18:30:49-0300",
            "arrive": "2019-04-26T18:30:49-0300",
            "duration": "8hrs",
            "capacity": "200",
            "status": "scheduled",
            "aircraft": "Boeing 8 max",
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

    def test_register_flight(self):
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
        self.assertEqual(result.status_code, 201)

    def test_register_flight_with_incomplete_data(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]
        incomplete_data = {
            "name": "KQ-FTK123",
            "origin": "JFK-NAIROBI",
            "destination": "LGN-BST Boston",
            "departure": "2019-04-25T18:30:49-0300",
        }
        result = self.app.post(
            "/api/v1/flights",
            data=json.dumps(incomplete_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 400)

    def test_get_all_flights(self):
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
        self.assertEqual(result.status_code, 201)
        res = self.app.get(
            "/api/v1/flights",
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(res.status_code, 200)

    def test_update_flight(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]
        self.app.post(
            "/api/v1/flights",
            data=json.dumps(self.flight_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        update_data = {
            "name": "KQ-FTK123",
            "origin": "JFK-NAIROBI",
            "destination": "LGN-BST Boston",
            "departure": "2019-04-25T18:30:49-0300",
        }
        result = self.app.put(
            "/api/v1/flights/1",
            data=json.dumps(update_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 200)

    def test_update_non_existing_flight(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]
        update_data = {
            "name": "KQ-FTK123",
            "origin": "JFK-NAIROBI",
            "destination": "LGN-BST Boston",
            "departure": "2019-04-25T18:30:49-0300",
        }
        result = self.app.put(
            "/api/v1/flights/3",
            data=json.dumps(update_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 404)

    def test_update_flight_with_invalid_data(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]
        self.app.post(
            "/api/v1/flights",
            data=json.dumps(self.flight_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        update_data = {
            "namejumbo": "KQ-FTK123",
            "origin": "JFK-NAIROBI",
            "destination": "LGN-BST Boston",
            "departure": "2019-04-25T18:30:49-0300",
        }
        result = self.app.put(
            "/api/v1/flights/1",
            data=json.dumps(update_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 400)

    def test_delete_flight(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]
        self.app.post(
            "/api/v1/flights",
            data=json.dumps(self.flight_data),
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        result = self.app.delete(
            "/api/v1/flights/1",
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 200)

    def test_delete_non_existing_flight(self):
        res = self.app.post(
            "/api/v1/auth/login",
            data=json.dumps(self.user_data),
            headers={"Content-Type": "application/json"},
        )
        token = json.loads(res.data.decode())["access_token"]
        result = self.app.delete(
            "/api/v1/flights/6",
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(result.status_code, 404)

    def test_get_flight(self):
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
        self.assertEqual(result.status_code, 201)
        res = self.app.get(
            "/api/v1/flights/1",
            headers={
                "Content-Type": "application/json",
                "Authorization": token,
            },
        )
        self.assertEqual(res.status_code, 200)
