import pytest
import allure
from utils.api_client import ApiClient
from utils.helpers import create_user, delete_user


@pytest.fixture
def api_client():
    """Фикстура для создания API клиента"""
    return ApiClient()


@pytest.fixture
def registered_user(api_client):
    """Фикстура для создания зарегистрированного пользователя с предусловиями и постусловиями"""
    from utils.helpers import generate_user_data
    
    # Предусловие: генерируем данные пользователя
    user_data = generate_user_data()
    
    # Создаем пользователя
    user_data, token = create_user(api_client, user_data)
    
    yield user_data, token

    # Постусловие: удаляем пользователя после теста
    delete_user(api_client, token)


@pytest.fixture
def auth_api_client(registered_user):
    """Фикстура для создания авторизованного API клиента"""
    user_data, token = registered_user
    client = ApiClient()
    client.set_token(token)
    return client