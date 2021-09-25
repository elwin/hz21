import carts
from typing import List


class User:
    def __init__(self, user_id: int, name: str, carts: List[carts.Cart]):
        self.id = user_id
        self.name = name
        self.carts = carts
        self.friends = []

    def add_friend(self, friend):
        self.friends.append(friend)

    def add_cart(self, cart: carts.Cart):
        self.carts.append(cart)

    def score(self) -> int:
        if len(self.carts) == 0:
            return 0

        score = sum(cart.score_sum()[0] for cart in self.carts)
        num = sum(cart.score_sum()[1] for cart in self.carts)

        return round(score / num, 1)
