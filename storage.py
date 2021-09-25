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
    carts.Cart((0, 0), datetime.date(2021, 9, 1), [chips, apple], "MM Sarnen-Center"),
    carts.Cart((1, 0), datetime.date(2021, 9, 2), [chips, potatoes], "M Schöftland"),
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

    user_list = {}
    cart_list = {}
    product_list = {}

    #   PRODUCTS

    product_path = path + "products/"

    for filename in os.listdir(product_path)[:5000]:
        with open(product_path + filename, encoding="utf-8") as f:
            data = json.loads(f.read())
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
            # except ValueError:
            #     pass

    #   CARTS AND CUSTOMERS

    shopping_cart_path = path + "shopping_cart_new/"

    for filename in os.listdir(shopping_cart_path)[:2]:
        with open(shopping_cart_path + filename) as f:
            r = csv.reader(f, delimiter=',')
            for i, row in enumerate(r):

                if i == 0: continue  # header

                user_id = int(row[1])

                # register new users
                if user_id not in user_list:

                    # only register 5 users
                    if len(user_list) == 5:  # only take 5 users for now
                        continue

                    user_list[user_id] = users.User(
                        user_id=user_id,
                        name=['Elwin', 'Daniela', 'Till', 'Leon', 'Ueli'][len(user_list)],  # f"xyz_{customer_id}"
                        carts=[]
                    )

                user = user_list[user_id]

                cart_id = 1000000*user_id+int(row[2])

                # register new carts
                if cart_id not in cart_list:
                    cart_list[cart_id] = carts.Cart(
                        cart_id=cart_id,
                        date=datetime.datetime.strptime(row[6], "%Y-%m-%d"),
                        location=row[4][3:],  # exclude canton abbreviation
                        products=[],
                    )
                    user.add_cart(cart_list[cart_id])

                cart = cart_list[cart_id]

                product_id = int(row[8])
                product = product_list.get(product_id)

                # not all products might be registered
                if product is None:
                    continue

                # skip repetitions
                if product in cart.products:
                    continue

                cart.add_product(product)

            # # sort carts
            # for id, customer in user_list.items():
            #     customer.carts = sorted(customer.carts, key=lambda cart: cart.date)

    # add friends
    for id1, u1 in user_list.items():
        for id2, u2 in user_list.items():
            if id1 != id2:
                u1.friends.append(u2)

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
