import allure
import pytest
from utils.helpers import generate_random_string


class TestUpdateUser:
    @allure.title("Изменение данных пользователя с авторизацией")
    def test_update_user_with_auth_success(self, auth_api_client, user_data):
        new_name = f"Updated_{generate_random_string(6)}"
        new_email = f"updated_{generate_random_string(8)}@example.com"

        with allure.step("Обновить имя пользователя"):
            update_data = {"name": new_name}
            response = auth_api_client.patch("/auth/user", json=update_data)

            assert response.status_code == 200
            assert response.json()["success"] == True
            assert response.json()["user"]["name"] == new_name

        with allure.step("Обновить email пользователя"):
            update_data = {"email": new_email}
            response = auth_api_client.patch("/auth/user", json=update_data)

            assert response.status_code == 200
            assert response.json()["success"] == True
            assert response.json()["user"]["email"].lower() == new_email.lower()

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_without_auth_fail(self, api_client):
        with allure.step("Попытаться обновить данные без токена"):
            update_data = {"name": "UnauthorizedUpdate"}
            response = api_client.patch("/auth/user", json=update_data)

        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 401
            assert response.json()["success"] == False
            assert response.json()["message"] == "You should be authorised"