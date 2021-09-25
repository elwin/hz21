import csv
import json
import os

import names
import users
import carts
import datetime

chips = carts.Product("Chips", 200, 5,
                      "https://image.migros.ch/2017-large/fa352f7d033713ba58e96e7e05c4b04060f7fe9f/m-classic-xl-chips-nature-400g.jpg",
                      [])
apple = carts.Product("Apple", 150, 3,
                      "https://image.migros.ch/2017-large/c86784443644854787947603e2c054b0f9927605/aepfel-jazz.jpg", [])
potatoes = carts.Product("Potatoes", 350, 1,
                         "https://image.migros.ch/2017-large/5b73957e3e40f7f4ba5eafb0eefa1c87683798fa/kartoffeln-baked-potatoes.jpg",
                         [])

mock_carts = [
    carts.Cart(0, datetime.date(2021, 9, 1), [chips, apple], "MM Sarnen-Center"),
    carts.Cart(1, datetime.date(2021, 9, 2), [chips, potatoes], "M Schöftland"),
]


class MockStorage:
    def __init__(self):
        return

    def users(self):
        return [
            users.User(0, "Dani", self.carts()),
            users.User(1, "Leon", self.carts()),
            users.User(2, "Till", self.carts()),
            users.User(3, "Elwin", self.carts()),
        ]

    def carts(self, user_id: int = 0):
        return {
            0: mock_carts[0],
            1: mock_carts[1],
        }


def read_data(path: str):
    product_list = {}
    product_path = path + "products/"
    for filename in os.listdir(product_path)[:2000]:
        with open(product_path + filename) as f:
            data = json.load(f)
            try:
                product_list[int(data['id'])] = carts.Product(
                    name=data['name'],
                    price=int(data['price']['item']['price'] * 100),
                    score=int(data['m_check2']['carbon_footprint']['ground_and_sea_cargo']['rating']),
                    related_ids=list(map(int, data['related_products']['purchase_recommendations']['product_ids'])),
                    img_link=data['image']['original']
                )
            except KeyError:
                pass
            except ValueError:
                pass

    user_list = {}
    cart_list = {}

    shopping_path = path + "shopping_cart/"

    for filename in os.listdir(shopping_path)[:10]:
        with open(shopping_path + filename) as f:
            r = csv.reader(f, delimiter=',')

            customers = {}

            for i, row in enumerate(r):
                if i == 0:
                    continue

                if i == 1000:
                    break

                customer_id = int(row[1])
                if customer_id not in user_list:
                    user_list[customer_id] = users.User(customer_id, names.get_random(), [])
                user = user_list[customer_id]

                customers[customer_id] = user

                cart_id = int(row[0])
                if cart_id not in cart_list:
                    cart_list[cart_id] = carts.Cart(
                        cart_id,
                        datetime.datetime.strptime(row[6], "%Y-%m-%d"),
                        row[4][3:],  # exclude canton abbreviation
                        [],
                    )
                    user.add_cart(cart_list[cart_id])
                cart = cart_list[cart_id]

                product_id = int(row[8])
                if product_id not in product_list:
                    continue

                cart.add_product(product_list[product_id])

            # sort cards
            for id, customer in customers.items():
                customer.carts = sorted(customer.carts, key=lambda cart: cart.date)

    user_list = {k: user_list[k] for k in list(user_list)[:10]}

    return user_list, cart_list, product_list


class FileStorage:
    def __init__(self, path: str):
        self.path = path
        self.user_list, self.cart_list, self.products = read_data(path)

        return

    def users(self):
        return self.user_list

    def user(self, user_id: int):
        return self.user_list[user_id]

    def get_carts(self, user_id: int):
        return self.user_list[user_id].carts

    def get_cart(self, cart_id: int):
        return self.cart_list[cart_id]

    def get_related(self, product: carts.Product):
        return [self.products.get(key) for key in product.related_ids if key in self.products]
