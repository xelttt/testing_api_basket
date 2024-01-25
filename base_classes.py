
import requests
import random
import string

BASE_URL = "http://localhost:8080/api"

class BaseApiMethods:

    def create_object_in_cart(self, value):
        response = requests.post(f"http://localhost:8080/api/Admin/create?value={value}")
        return response.json(), response.status_code

    def delete_all_products(self):
        response = requests.delete(f"{BASE_URL}/ShoppingCart/products")
        return response.json()

    def get_all_products(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/products")
        return response.json()

    def header(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/header")
        return response.json()

    def add_promo_code(self):
        response = requests.post(f"{BASE_URL}/ShoppingCart/discount")
        return response.json()

    def delete_promo_code(self):
        response = requests.delete(f"{BASE_URL}/ShoppingCart/discount")
        return response.status_code

    def get_baskedsummary(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/baskedsummary")
        return response.json()

    def generate_random_string(self, length):
        generate = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(generate) for _ in range(length))
        return random_string