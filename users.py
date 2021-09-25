import carts
from typing import List


class User:
    def __init__(self, user_id: int, name: str, carts: List[carts.Cart]):
        self.id = user_id
        self.name = name
        self.carts = carts

    def add_cart(self, cart: carts.Cart):
        self.carts.append(cart)

    def score(self) -> int:
        return sum([cart.score() for cart in self.carts])
