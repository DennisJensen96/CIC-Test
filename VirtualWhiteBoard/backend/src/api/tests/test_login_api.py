# standard library
import unittest
import os
import json

# This component
from api.api import setup_api


class TestLoginApi(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.app = setup_api().test_client()

    @classmethod
    def tearDownClass(self) -> None:
        os.remove("./data/data.db")

    def test_create_user(self):
        payload = json.dumps({
            "user_name": "test_user_10",
            "email": "test_email",
            "password": "test_password"
        })

        response = self.app.post(
            '/users', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_authentication(self):
        payload = json.dumps({
            "user_name": "test_user_11",
            "password": "test_password"
        })

        response = self.app.post(
            '/users', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(response.status_code, 200)

        response = self.app.post(
            "/user/authentication", headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(response.status_code, 200)

    def test_reset_password(self):
        payload = json.dumps({
            "user_name": "test_user_12",
            "password": "test_password"
        })

        response = self.app.post(
            '/users', headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(response.status_code,
                         200), "Was not able to create user"
        payload = json.loads(payload)
        payload["new_password"] = "test_password_2"
        payload = json.dumps(payload)

        print(payload)
        response = self.app.post(
            "/user/password_reset", headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(response.status_code,
                         200), "Did not change password succesfully"
        payload = json.loads(payload)
        payload["password"] = "test_password_2"
        payload = json.dumps(payload)

        response = self.app.post(
            "/user/authentication", headers={"Content-Type": "application/json"}, data=payload)

        self.assertEqual(response.status_code, 200), "Authentication failed"
