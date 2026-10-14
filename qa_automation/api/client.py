import os
import secrets
import string

import requests


class DemoQAApi:
    def __init__(self, base_url=None):
        self.base_url = (base_url or os.getenv("DEMOQA_BASE_URL", "https://demoqa.com")).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method, path, **kwargs):
        response = self.session.request(method, f"{self.base_url}{path}", timeout=30, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def new_credentials():
        username = "qa_" + secrets.token_hex(5)
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = "Qa1!" + "".join(secrets.choice(alphabet) for _ in range(12))
        return username, password

    def create_user(self, username, password):
        response = self._request(
            "POST", "/Account/v1/User", json={"userName": username, "password": password}
        )
        return response.json()

    def generate_token(self, username, password):
        response = self._request(
            "POST", "/Account/v1/GenerateToken", json={"userName": username, "password": password}
        )
        return response.json()

    def is_authorized(self, username, password):
        response = self._request(
            "POST", "/Account/v1/Authorized", json={"userName": username, "password": password}
        )
        return response.json()

    def list_books(self):
        response = self._request("GET", "/BookStore/v1/Books")
        return response.json()["books"]

    def borrow_books(self, user_id, token, isbns):
        response = self._request(
            "POST",
            "/BookStore/v1/Books",
            headers={"Authorization": f"Bearer {token}"},
            json={"userId": user_id, "collectionOfIsbns": [{"isbn": isbn} for isbn in isbns]},
        )
        return response.json()

    def get_user(self, user_id, token):
        response = self._request(
            "GET", f"/Account/v1/User/{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        return response.json()
