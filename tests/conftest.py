import pytest
import allure
from utils.helpers import ApiClient, generate_user_data, generate_random_string


@pytest.fixture
def api_client():
    return ApiClient()


@pytest.fixture
def user_data():
    return generate_user_data()


@pytest.fixture
def registered_user(api_client, user_data):
    # Создаем пользователя
    response = api_client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    token = response.json().get("accessToken")

    yield user_data, token

    # Удаляем пользователя после теста
    if token:
        api_client.set_token(token)
        api_client.delete("/auth/user")
        api_client.clear_token()


@pytest.fixture
def auth_api_client(registered_user):
    user_data, token = registered_user
    client = ApiClient()
    client.set_token(token)
    return client