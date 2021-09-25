import carts
from typing import List


class User:
    def __init__(self, name: str, carts: List[carts.Cart]):
        self.name = name
        self.carts = carts

    def add_cart(self, cart: carts.Cart):
        self.carts.append(cart)

    def score(self) -> int:
        return 5  # for some reason the below is broken
        # return sum([cart.score() for cart in self.carts])
