import datetime
from typing import List, Tuple
import storage
from statistics import mean

class Product:
    def __init__(self, name: str, price: int, score: int,  img_link: str, related_ids: List[int]):
        self.name = name
        self.price = price
        self.score = score
        self.img_link = img_link
        self.related_ids = related_ids

    def related(self):
        return [storage.chips, storage.apple]

    def get_bg_color(self) -> str:
        if self.score >= 4:
            return "bg-success"
        if self.score >= 2:
            return "bg-warning"
        if self.score == 1:
            return "bg-danger"
        return "bg-secondary"


class Cart:
    def __init__(self, cart_id, date: datetime.date, location: str, products: List[Product]):
        self.id = cart_id
        self.date = date
        self.location = location
        self.products = products

    def score(self) -> int:
        print(len(self.products))
        return round(mean(product.score for product in self.products), 1)

    def score_sum(self) -> Tuple[int, int]:
        return sum(product.score for product in self.products), len(self.products)

    def add_product(self, product: Product):
        self.products.append(product)

    def get_bg_color(self) -> str:
        if self.score() >= 4:
            return "bg-success"
        if self.score() >= 2:
            return "bg-warning"
        if self.score() >= 1:
            return "bg-danger"
        return "bg-secondary"
