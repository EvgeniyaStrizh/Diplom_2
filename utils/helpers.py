import random
import string
from utils.api_client import ApiClient


def generate_random_string(length=10):
    """Генерирует случайную строку заданной длины"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_user_data():
    """Генерирует тестовые данные пользователя"""
    return {
        "email": f"{generate_random_string(8)}@example.com",
        "password": generate_random_string(12),
        "name": generate_random_string(8)
    }


def create_user(api_client, user_data):
    """Создает пользователя и возвращает данные и токен"""
    response = api_client.post("/auth/register", json=user_data)
    if response.status_code == 200:
        token = response.json().get("accessToken")
        return user_data, token
    return None, None


def delete_user(api_client, token):
    """Удаляет пользователя по токену"""
    if token:
        api_client.set_token(token)
        api_client.delete("/auth/user")
        api_client.clear_token()