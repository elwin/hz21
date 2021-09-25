import users
import carts
import datetime

chips = carts.Product("Chips", 200, 5)
apple = carts.Product("Apple", 150, 3)
potatoes = carts.Product("Potatoes", 350, 1)

mock_carts = [
    carts.Cart(0, datetime.date(2021, 9, 1), 5, [chips, apple]),
    carts.Cart(1, datetime.date(2021, 9, 2), 9, [chips, potatoes]),
]


class MockStorage:
    def __init__(self):
        return

    def users(self):
        return [
            users.User("Dani", self.carts()),
            users.User("Leon", self.carts()),
            users.User("Till", self.carts()),
            users.User("Elwin", self.carts()),
        ]

    def carts(self):
        return {
            0: mock_carts[0],
            1: mock_carts[1],
        }
