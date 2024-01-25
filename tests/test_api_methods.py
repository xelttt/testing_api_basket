from jsonschema import validate
import random
import requests
from schemas.schemas import HEADER_SCHEMA, PRODUCTS_SCHEMA, DELETED_SCHEMA, BASKEDSUMMARY_SCHEMA
from base_classes import BASE_URL, BaseApiMethods
from enums.global_enums import GlobalErrorMessages

class TestApiMethods(BaseApiMethods):

    def test_admin_create(self):
        response = self.create_object_in_cart(random.randint(2, 9))
        assert response[1] == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert response[0] == True

    def test_negative_value_admin_create(self):
        response = self.create_object_in_cart(-1)
        assert response[1] == 400, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert response[0] == False, "Некорректное значение value"

    def test_check_count_of_items_in_cart(self):
        self.delete_all_products()
        x = random.randint(1, 10)
        self.create_object_in_cart(x)
        products = self.get_all_products()
        product = set(item["Id"] for item in products)
        count = len(product)
        assert x == count, 'Количество товаров не соответствует числу, указанному при генерации корзины'

    def test_shopping_cart_header(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/header")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        validate(response.json(), HEADER_SCHEMA)

    def test_check_user_guid_in_response_body(self):
        response = self.header()
        user_guid = "UserGuid"
        assert user_guid in response, 'Ключ "UserGuid" отсутствует в теле ответа'

    def test_shopping_cart_products(self):
        self.create_object_in_cart(1)
        response = requests.get(f"{BASE_URL}/ShoppingCart/products")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        validate(response, PRODUCTS_SCHEMA)

    def test_deleted_shopping_cart_products(self):
        self.create_object_in_cart(random.randint(2, 5))
        response = requests.delete(f"{BASE_URL}/ShoppingCart/products")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        validate(response.json(), DELETED_SCHEMA)
        result = response.json()
        description = result.get("Description")
        assert description == "Ваша корзина удалена"

    def test_check_no_content(self):
        self.delete_all_products()
        response = requests.get(f"{BASE_URL}/ShoppingCart/products")
        assert response.status_code == 204, GlobalErrorMessages.WRONG_STATUS_CODE.value

    def test_deleted_shopping_cart_product(self):
        self.delete_all_products()
        self.create_object_in_cart(1)
        get_products = self.get_all_products()
        product_id = get_products[0]["Id"]
        get_header = self.header()
        used_guid = get_header["UsedGuid"]
        data = {"ProductId": product_id, "UserGuid": used_guid}
        response = requests.delete(f"{BASE_URL}/ShoppingCart/product", json=data)
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert "Товар удален" in response.text

    def test_deleted_product_negative_data(self):
        self.create_object_in_cart(1)
        product_id = random.randint(1, 9999999999)
        user_guid = self.generate_random_string(36)
        data = {"ProductId": product_id, "UsedGuid": user_guid}
        response = requests.delete(f"{BASE_URL}/ShoppingCart/product", json=data)
        assert response.status_code == 400, GlobalErrorMessages.WRONG_STATUS_CODE.value

    def test_shopping_cart_baskedsummary(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/baskedsummary")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        validate(response.json(), BASKEDSUMMARY_SCHEMA)

    def test_check_info_total_products(self):
        self.delete_all_products()
        self.create_object_in_cart(random.randint(2, 9))
        products_info = self.get_all_products()
        quantity = []
        for x in products_info:
            quantity.append(x["Quantity"])
        response = self.get_baskedsummary()
        total_products = response["TotalProducts"]
        assert sum(quantity) == total_products, GlobalErrorMessages.BASKED_SUMMARY_INFO.value

    def test_check_total_price_products(self):
        self.delete_all_products()
        self.create_object_in_cart(random.randint(2, 9))
        products_info = self.get_all_products()
        total_prices = [x["Quantity"] * x["Price"] for x in products_info]
        response = self.get_baskedsummary()
        total = response["Total"]
        assert total == sum(total_prices), "Итоговая сумма заказа некорректна"

    def test_check_discount_baskedsummary(self):
        self.delete_all_products()
        self.create_object_in_cart(random.randint(2, 9))
        data = {"DiscountName": "hawkingbros", "UsedGuid": self.header()["UsedGuid"]}
        promo_code = requests.post(f"{BASE_URL}/ShoppingCart/discount", json=data)
        products_info = self.get_all_products()
        discounted_price = [x["Quantity"] * x["DiscountedPrice"] for x in products_info]
        discount = self.get_baskedsummary()["Discount"]
        assert promo_code.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert discount == sum(discounted_price), 'Некорректно рассчитывается итоговая сумма скидки'

    def test_shopping_cart_viewed_list(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/viewedList")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        validate(response.json(), PRODUCTS_SCHEMA)

    def test_shopping_cart_quantityinc(self):
        self.delete_all_products()
        self.create_object_in_cart(1)
        get_products = self.get_all_products()
        product_id = get_products[0]["Id"]
        get_header = self.header()
        user_guid = get_header["UsedGuid"]
        data = {"ProductId": product_id,
                "UserGuid": user_guid}
        response = requests.post(f"{BASE_URL}/ShoppingCart/quantityinc", json=data)
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert "Количество товара было увеличено" in response.text

    def test_shopping_cart_quantitydec(self):
        self.create_object_in_cart(1)
        get_products = self.get_all_products()
        product_id = get_products[0]["Id"]
        get_header = self.header()
        user_guid = get_header["UsedGuid"]
        data = {"ProductId": product_id,
                "UserGuid": user_guid}
        response = requests.post(f"{BASE_URL}/ShoppingCart/quantitydec", json=data)
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert "Количество товара было уменьшено" in response.text

    def test_shopping_cart_change_quantity(self):
        self.create_object_in_cart(1)
        get_products = self.get_all_products()
        product_id = get_products[0]["Id"]
        user_guid = self.header()["UsedGuid"]
        value = random.randint(2, 10)
        data = {"ProductId": product_id,
                "UserGuid": user_guid,
                "Value": value}
        response = requests.post(f"{BASE_URL}/ShoppingCart/changequantity", json=data)
        check_quantity = self.get_all_products()
        quantity = check_quantity[0]["Quantity"]
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert quantity == value, 'Количество товара отличается от указанного в запросе'

    def test_shopping_cart_discount(self):
        self.create_object_in_cart(1)
        used_guid = self.header()["UsedGuid"]
        promo_code = "hawkingbros"
        data = {"DiscountName": promo_code, "UsedGuid": used_guid}
        response = requests.post(f"{BASE_URL}/ShoppingCart/discount", json=data)
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert "Промокод успешно применен" in response.text

    def test_delete_shopping_cart_discount(self):
        response = requests.delete(f"{BASE_URL}/ShoppingCart/discount")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert "Промокод успешно отменен" in response.text