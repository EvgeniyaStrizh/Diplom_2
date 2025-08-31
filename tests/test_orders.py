import allure
import pytest


class TestOrders:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients_success(self, auth_api_client):
        # Получаем список ингредиентов
        with allure.step("Получить список доступных ингредиентов"):
            ingredients_response = auth_api_client.get("/ingredients")
            assert ingredients_response.status_code == 200

            ingredients = ingredients_response.json()["data"]
            assert len(ingredients) > 0

            ingredient_ids = [ingredient["_id"] for ingredient in ingredients[:2]]

        with allure.step("Создать заказ с ингредиентами"):
            order_data = {"ingredients": ingredient_ids}
            response = auth_api_client.post("/orders", json=order_data)

        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200
            assert response.json()["success"] == True
            assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_success(self, api_client):
        # Получаем ингредиенты
        with allure.step("Получить ингредиенты для заказа"):
            ingredients_response = api_client.get("/ingredients")
            ingredients = ingredients_response.json()["data"]
            ingredient_ids = [ingredient["_id"] for ingredient in ingredients[:2]]

        with allure.step("Создать заказ без авторизации"):
            order_data = {"ingredients": ingredient_ids}
            response = api_client.post("/orders", json=order_data)

        with allure.step("Проверить создание заказа без авторизации"):
            assert response.status_code == 200
            assert response.json()["success"] == True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_fail(self, auth_api_client):
        with allure.step("Попытаться создать заказ без ингредиентов"):
            order_data = {"ingredients": []}
            response = auth_api_client.post("/orders", json=order_data)

        with allure.step("Проверить ошибку валидации"):
            assert response.status_code == 400
            assert response.json()["success"] == False
            assert "ingredient" in response.json()["message"].lower()

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fail(self, auth_api_client):
        with allure.step("Попытаться создать заказ с неверными хешами ингредиентов"):
            order_data = {"ingredients": ["invalid_hash_1", "invalid_hash_2"]}
            response = auth_api_client.post("/orders", json=order_data)

        with allure.step("Проверить ошибку валидации ингредиентов"):
            assert response.status_code == 500

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth_success(self, auth_api_client):
        with allure.step("Получить заказы пользователя"):
            response = auth_api_client.get("/orders")

        with allure.step("Проверить успешное получение заказов"):
            assert response.status_code == 200
            assert response.json()["success"] == True
            assert "orders" in response.json()

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_without_auth_fail(self, api_client):
        with allure.step("Попытаться получить заказы без авторизации"):
            response = api_client.get("/orders")

        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 401
            assert response.json()["success"] == False
            assert response.json()["message"] == "You should be authorised"