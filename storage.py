import csv
import json
import os
import names
import users
import carts
import datetime


def read_data(path: str):
    product_list = {}
    product_path = path + "products/"
    for filename in os.listdir(product_path)[:5000]:
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
