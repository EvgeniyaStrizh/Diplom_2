import random
import string
import requests


class ApiClient:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"

    def __init__(self):
        self.session = requests.Session()
        self.token = None

    def set_token(self, token):
        self.token = token
        self.session.headers.update({'Authorization': token})

    def clear_token(self):
        self.token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']

    def post(self, endpoint, json=None):
        return self.session.post(f"{self.BASE_URL}{endpoint}", json=json)

    def get(self, endpoint):
        return self.session.get(f"{self.BASE_URL}{endpoint}")

    def patch(self, endpoint, json=None):
        return self.session.patch(f"{self.BASE_URL}{endpoint}", json=json)

    def delete(self, endpoint):
        return self.session.delete(f"{self.BASE_URL}{endpoint}")


def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_user_data():
    return {
        "email": f"{generate_random_string(8)}@example.com",
        "password": generate_random_string(12),
        "name": generate_random_string(8)
    }