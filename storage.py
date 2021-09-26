import csv
import json
import os
import names
import users
import carts
import datetime


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
                product_id = int(data['id'])
                product_list[product_id] = carts.Product(
                    product_id=product_id,
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

    #   CARTS AND CUSTOMERS

    shopping_cart_path = path + "shopping_cart_new/"

    for filename in os.listdir(shopping_cart_path)[:2]:
        with open(shopping_cart_path + filename) as f:
            r = csv.reader(f, delimiter=',')
            for i, row in enumerate(r):

                if i == 0:
                    continue  # header

                # if i == 500:  # TODO: Remove
                #     break

                user_id = int(row[1])

                # register new users
                if user_id not in user_list:

                    # only register 5 users
                    if len(user_list) == 5:  # only take 5 users for now
                        continue

                    user_list[user_id] = users.User(
                        user_id=user_id,
                        name=['Elwin', 'Daniela', 'Till', 'Leon', 'Ueli'][len(user_list)],  # f"xyz_{customer_id}"
                        cart_list=[]
                    )

                user = user_list[user_id]

                cart_id = 1000000 * user_id + int(row[2])

                product_id = int(row[8])
                product = product_list.get(product_id)

                # not all products might be registered
                if product is None:
                    continue

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

    def get_related_higher(self, product: carts.Product):
        return [p for p in self.get_related(product) if p.score > product.score]

    def get_max_score(self, cart: carts.Cart) -> int:
        score = 0

        for product in cart.products:
            related = self.get_related_higher(product)
            if len(related) > 0:
                score += related[0].score
            else:
                score += product.score

        return score
