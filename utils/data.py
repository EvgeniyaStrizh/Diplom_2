"""
Модуль для хранения констант и текстов ответов API
"""

# HTTP статус коды
STATUS_OK = 200
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_INTERNAL_SERVER_ERROR = 500

# Сообщения об ошибках API
ERROR_MESSAGES = {
    "USER_ALREADY_EXISTS": "User already exists",
    "YOU_SHOULD_BE_AUTHORISED": "You should be authorised",
    "INGREDIENT_IDS_MUST_BE_PROVIDED": "Ingredient ids must be provided"
}

# Успешные ответы
SUCCESS_RESPONSES = {
    "SUCCESS_TRUE": True,
    "SUCCESS_FALSE": False
}

# Поля ответов
RESPONSE_FIELDS = {
    "ACCESS_TOKEN": "accessToken",
    "SUCCESS": "success",
    "MESSAGE": "message",
    "USER": "user",
    "ORDER": "order",
    "ORDERS": "orders",
    "DATA": "data"
}
