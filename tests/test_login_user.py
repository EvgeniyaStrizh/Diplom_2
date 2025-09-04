import allure
import pytest
from utils.helpers import generate_random_string
from utils.data import STATUS_OK, STATUS_UNAUTHORIZED, SUCCESS_RESPONSES, RESPONSE_FIELDS


class TestLoginUser:
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user_success(self, api_client, registered_user):
        user_data, token = registered_user

        with allure.step("Выполнить логин с правильными credentials"):
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }
            response = api_client.post("/auth/login", json=login_data)

        with allure.step("Проверить успешный логин"):
            assert response.status_code == STATUS_OK
            assert response.json()[RESPONSE_FIELDS["SUCCESS"]] == SUCCESS_RESPONSES["SUCCESS_TRUE"]
            assert RESPONSE_FIELDS["ACCESS_TOKEN"] in response.json()

    @allure.title("Логин с неверными credentials")
    def test_login_wrong_credentials_fail(self, api_client, registered_user):
        user_data, token = registered_user

        with allure.step("Выполнить логин с неверным паролем"):
            wrong_login_data = {
                "email": user_data["email"],
                "password": generate_random_string(12)
            }
            response = api_client.post("/auth/login", json=wrong_login_data)

        with allure.step("Проверить ошибку аутентификации"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert response.json()[RESPONSE_FIELDS["SUCCESS"]] == SUCCESS_RESPONSES["SUCCESS_FALSE"]
            assert response.json()[RESPONSE_FIELDS["MESSAGE"]] == "email or password are incorrect"

    @allure.title("Логин с несуществующим email")
    def test_login_nonexistent_email_fail(self, api_client):
        with allure.step("Выполнить логин с несуществующим email"):
            login_data = {
                "email": f"nonexistent{generate_random_string(8)}@example.com",
                "password": generate_random_string(12)
            }
            response = api_client.post("/auth/login", json=login_data)

        with allure.step("Проверить ошибку аутентификации"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert response.json()[RESPONSE_FIELDS["SUCCESS"]] == SUCCESS_RESPONSES["SUCCESS_FALSE"]