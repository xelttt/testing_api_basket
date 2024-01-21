import unittest
import requests
import random

BASE_URL = "http://localhost:8080/api"

class BaseApiMethods(unittest.TestCase):

    def create_object_in_cart(self, value):
        response = requests.post(f"http://localhost:8080/api/Admin/create?value={value}")
        return response.status_code, response.json()

    def delete_all_products(self):
        response = requests.delete(f"{BASE_URL}/ShoppingCart/products")
        return response.status_code, response.json()

    def get_all_products(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/products")
        return response.status_code, response.json()

    def header(self):
        response = requests.get(f"{BASE_URL}/ShoppingCart/header")
        return response.json()

    def delete_promo_code(self):
        response = requests.delete(f"{BASE_URL}/ShoppingCart/discount")
        return response.status_code
