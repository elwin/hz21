import csv
import json
import os

import users
import carts
import datetime

chips = carts.Product("Chips", 200, 5)
apple = carts.Product("Apple", 150, 3)
potatoes = carts.Product("Potatoes", 350, 1)

mock_carts = [
    carts.Cart(0, datetime.date(2021, 9, 1), [chips, apple]),
    carts.Cart(1, datetime.date(2021, 9, 2), [chips, potatoes]),
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
                    user_list[customer_id] = users.User(f"xyz_{customer_id}", [])
                user = user_list[customer_id]
                
                customers[customer_id] = user

                cart_id = int(row[2])
                if cart_id not in cart_list:
                    cart_list[cart_id] = carts.Cart(
                        cart_id,
                        datetime.datetime.strptime(row[6], "%Y-%m-%d"),
                        [],
                    )
                    user.add_cart(cart_list[cart_id])
                cart = cart_list[cart_id]

                product_id = int(row[8])
                if product_id not in product_list:
                    continue

                cart.add_product(product_list[product_id])

                # if customer_id not in shopping_data:
                #     shopping_data[customer_id] = []
                #     shopping_data[customer_id].append({
                #         "YYYYMM": int(row[0]),
                #         "KundeID": int(row[1]),
                #         "WarenkorbID": int(row[2]),
                #         "ProfitKSTID": int(row[3]),
                #         "ProfitKSTNameD": row[4],
                #         "GenossenschaftCode": row[5],
                #         "TransaktionDatumID": row[6],
                #         "TransaktionZeit": row[7],
                #         "ArtikelID": int(row[8]),
                #         "Menge": float(row[9]),
                #     })
            
            # sort cards
            for id, customer in customers.items():
                customer.carts = sorted(customer.carts, key=lambda cart: cart.date)
            print(0)

    return user_list


class FileStorage:
    def __init__(self, path: str):
        self.path = path
        self.user_list = read_data(path)
        return

    def users(self):
        return self.user_list

    def carts(self, user_id: int):
        return self.user_list[user_id].carts
