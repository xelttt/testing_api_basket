import random
import requests
from jsonschema import validate
from schemas.schemas import HEADER_SCHEMA, PRODUCTS_SCHEMA, DELETED_SCHEMA, BASKEDSUMMARY_SCHEMA
from base_classes import BASE_URL, BaseApiMethods
from enums.global_enums import GlobalErrorMessages


class TestApiMethods(BaseApiMethods):

    def test_admin_create(self):
        response = self.create_object_in_cart(random.randint(2, 9))
        assert response[0] == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert response[1] == True

    def test_shopping_cart_header(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/header")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        validate(response.json(), HEADER_SCHEMA)


    def test_shopping_cart_products(self):
        self.create_object_in_cart(1)
        response = requests.get(f"{BASE_URL}/ShoppingCart/products")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        validate(response.json(), PRODUCTS_SCHEMA)

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

    def test_shopping_cart_product(self):
        self.create_object_in_cart(value=1)
        get_products = self.get_all_products()
        products_list = get_products[1]
        product_id = products_list[0].get("Id")
        get_header = self.header()
        user_guid = get_header.get("UserGuid")
        data = {"ProductId": product_id, "UserGuid": user_guid}
        deleted = requests.delete(f"{BASE_URL}/ShoppingCart/products", json=data)
        assert deleted.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert "Ваша корзина удалена" in deleted.text

    def test_shopping_cart_baskedsummary(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/baskedsummary")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        validate(response.json(), BASKEDSUMMARY_SCHEMA)

    def test_shopping_cart_viewed_list(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/viewedList")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        validate(response.json(), PRODUCTS_SCHEMA)

    def test_shopping_cart_quantityinc(self):
        self.create_object_in_cart(1)
        get_products = self.get_all_products()
        products_list = get_products[1]
        product_id = products_list[0].get("Id")
        get_header = self.header()
        user_guid = get_header.get("UserGuid")
        data = {"ProductId": product_id,
                "UserGuid": user_guid}
        response = requests.post(f"{BASE_URL}/ShoppingCart/quantityinc", json=data)
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value

    def test_shopping_cart_quantitydec(self):
        self.create_object_in_cart(1)
        get_products = self.get_all_products()
        products_list = get_products[1]
        product_id = products_list[0].get("Id")
        get_header = self.header()
        user_guid = get_header.get("UserGuid")
        data = {"ProductId": product_id,
                "UserGuid": user_guid}
        response = requests.post(f"{BASE_URL}/ShoppingCart/quantityinc", json=data)
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value

    def test_shopping_cart_change_quantity(self):
        self.create_object_in_cart(1)
        get_products = self.get_all_products()
        products_list = get_products[1]
        product_id = products_list[0].get("Id")
        user_guid = self.header().get("UserGuid")
        value = 10
        data = {"ProductId": product_id,
                "UserGuid": user_guid,
                "Value": value}
        response = requests.post(f"{BASE_URL}/ShoppingCart/changequantity", json=data)
        check_quantity = self.get_all_products()
        quantity_list = check_quantity[1]
        quantity = quantity_list[0].get("Quantity")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert quantity == value

    def test_shopping_cart_discount(self):
        self.create_object_in_cart(1)
        used_guid = self.header().get("UsedGuid")
        promo_code = "hawkingbros"
        data = {"DiscountName": promo_code, "UsedGuid": used_guid}
        response = requests.post(f"{BASE_URL}ShoppingCart/discount", json=data)
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert "Промокод успешно применен" in response.text

    def test_delete_shopping_cart_discount(self):
        response = requests.delete(f"{BASE_URL}ShoppingCart/discount")
        assert response.status_code == 200, GlobalErrorMessages.WRONG_STATUS_CODE.value
        assert "Промокод успешно отменен" in response.text