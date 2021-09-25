import carts
from typing import List


class User:
    def __init__(self, name: str, carts: List[carts.Cart]):
        self.name = name
        self.carts = carts
