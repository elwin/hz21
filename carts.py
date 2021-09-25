import datetime
from typing import List
import storage


class Product:
    def __init__(self, name: str, price: int, score: int,  img_link: str, related_ids: List[int]):
        self.name = name
        self.price = price
        self.score = score
        self.img_link = img_link
        self.related_ids = related_ids

    def related(self):
        return [storage.chips, storage.apple]


class Cart:
    def __init__(self, cart_id: int, date: datetime.date, location: str, products: List[Product]):
        self.id = cart_id
        self.date = date
        self.location = location
        self.products = products

    def score(self) -> int:
        return sum(product.score for product in self.products)

    def add_product(self, product: Product):
        self.products.append(product)
