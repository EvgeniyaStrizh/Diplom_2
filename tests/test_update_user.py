import allure
import pytest
from utils.helpers import generate_random_string
from utils.data import STATUS_OK, STATUS_UNAUTHORIZED, SUCCESS_RESPONSES, ERROR_MESSAGES, RESPONSE_FIELDS


class TestUpdateUser:
    @allure.title("Изменение данных пользователя с авторизацией")
    def test_update_user_with_auth_success(self, auth_api_client):
        new_name = f"Updated_{generate_random_string(6)}"
        new_email = f"updated_{generate_random_string(8)}@example.com"

        with allure.step("Обновить имя пользователя"):
            update_data = {"name": new_name}
            response = auth_api_client.patch("/auth/user", json=update_data)

            assert response.status_code == STATUS_OK
            assert response.json()[RESPONSE_FIELDS["SUCCESS"]] == SUCCESS_RESPONSES["SUCCESS_TRUE"]
            assert response.json()[RESPONSE_FIELDS["USER"]]["name"] == new_name

        with allure.step("Обновить email пользователя"):
            update_data = {"email": new_email}
            response = auth_api_client.patch("/auth/user", json=update_data)

            assert response.status_code == STATUS_OK
            assert response.json()[RESPONSE_FIELDS["SUCCESS"]] == SUCCESS_RESPONSES["SUCCESS_TRUE"]
            assert response.json()[RESPONSE_FIELDS["USER"]]["email"].lower() == new_email.lower()

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_without_auth_fail(self, api_client):
        with allure.step("Попытаться обновить данные без токена"):
            update_data = {"name": "UnauthorizedUpdate"}
            response = api_client.patch("/auth/user", json=update_data)

        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert response.json()[RESPONSE_FIELDS["SUCCESS"]] == SUCCESS_RESPONSES["SUCCESS_FALSE"]
            assert response.json()[RESPONSE_FIELDS["MESSAGE"]] == ERROR_MESSAGES["YOU_SHOULD_BE_AUTHORISED"]