import requests
import allure


class ApiClient:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"

    def __init__(self):
        self.session = requests.Session()
        self.token = None

    @allure.step("Установить токен авторизации")
    def set_token(self, token):
        self.token = token
        self.session.headers.update({'Authorization': token})

    @allure.step("Очистить токен авторизации")
    def clear_token(self):
        self.token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']

    @allure.step("Выполнить POST запрос к {endpoint}")
    def post(self, endpoint, json=None):
        return self.session.post(f"{self.BASE_URL}{endpoint}", json=json)

    @allure.step("Выполнить GET запрос к {endpoint}")
    def get(self, endpoint):
        return self.session.get(f"{self.BASE_URL}{endpoint}")

    @allure.step("Выполнить PATCH запрос к {endpoint}")
    def patch(self, endpoint, json=None):
        return self.session.patch(f"{self.BASE_URL}{endpoint}", json=json)

    @allure.step("Выполнить DELETE запрос к {endpoint}")
    def delete(self, endpoint):
        return self.session.delete(f"{self.BASE_URL}{endpoint}")
