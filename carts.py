import datetime
from typing import List

import carts
import storage


class Product:
    def __init__(self, name: str, price: int, score: int):
        self.name = name
        self.price = price
        self.score = score

    def related(self):
        return [storage.chips, storage.apple]


class Cart:
    def __init__(self, cart_id: int, date: datetime.date, products: List[Product]):
        self.id = cart_id
        self.date = date
        self.products = products

    def score(self) -> int:
        return sum(product.score for product in self.products)

    def add_product(self, product: carts.Product):
        self.products.append(product)
