import allure
import pytest
from utils.helpers import generate_user_data, generate_random_string


class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, api_client, user_data):
        with allure.step("Создать уникального пользователя"):
            response = api_client.post("/auth/register", json=user_data)

        with allure.step("Проверить успешное создание"):
            assert response.status_code == 200
            assert response.json()["success"] == True
            assert "accessToken" in response.json()

        # Cleanup
        token = response.json()["accessToken"]
        api_client.set_token(token)
        api_client.delete("/auth/user")

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user_fail(self, api_client, registered_user):
        user_data, token = registered_user

        with allure.step("Попытаться создать пользователя с существующими данными"):
            response = api_client.post("/auth/register", json=user_data)

        with allure.step("Проверить ошибку создания"):
            assert response.status_code == 403
            assert response.json()["success"] == False
            assert response.json()["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_fail(self, api_client, user_data, missing_field):
        invalid_data = user_data.copy()
        invalid_data[missing_field] = ""

        with allure.step(f"Создать пользователя без поля {missing_field}"):
            response = api_client.post("/auth/register", json=invalid_data)

        with allure.step("Проверить ошибку валидации"):
            assert response.status_code == 403
            assert response.json()["success"] == False