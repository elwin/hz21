import datetime
from typing import List


class Product:
    def __init__(self, name: str, price: int, score: int):
        self.name = name
        self.price = price
        self.score = score

    def related(self):
        return [chips, apple]


chips = Product("Chips", 200, 5)
apple = Product("Apple", 150, 3)
potatoes = Product("Potatoes", 350, 1)


class Cart:
    def __init__(self, cart_id: int, date: datetime.date, score: int, products: List[Product]):
        self.id = cart_id
        self.date = date
        self.products = products

    def score(self) -> int:
        return sum(product.score for product in self.products)


def get_cards():
    return {
        0: Cart(0, datetime.date(2021, 9, 1), 5, [chips, apple]),
        1: Cart(1, datetime.date(2021, 9, 2), 9, [chips, potatoes]),
    }
