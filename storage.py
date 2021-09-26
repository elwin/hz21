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

    shopping_cart_path = path + "shopping_cart/"

    for filename in ["Abverkaufdaten_trx_202001.csv", "Abverkaufdaten_trx_202002.csv"]:
        with open(shopping_cart_path + filename) as f:
            r = csv.reader(f, delimiter=',')
            for i, row in enumerate(r):

                if i == 0:
                    continue  # header

                # if i == 500:  # TODO: Remove
                #     break

                user_id = int(row[1])
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

                cart = cart_list[cart_id]

                # skip repetitions
                if product in cart.products:
                    continue

                cart.add_product(product)

    user_list = {
        0: users.User(0, "Dani", [
            cart_list[107748000001],
            cart_list[108928000006],
            cart_list[106563000002],
            cart_list[102111000004],
        ]),
        1: users.User(1, "Till", [
            cart_list[108204000004],
            cart_list[103080000001],
            cart_list[107421000005],
            cart_list[103436000003],
        ]),
        2: users.User(2, "Leon", [
            cart_list[103466000004],
            cart_list[108646000006],
            cart_list[105367000001],
            cart_list[105367000003],
        ]),
        3: users.User(3, "Elwin", [
            cart_list[107480000006],
            cart_list[102186000004],
            cart_list[102745000002],
        ]),
        4: users.User(4, "Ueli", [
            cart_list[109221000008],
            cart_list[109091000003],
            cart_list[108928000001],
            cart_list[104180000002],
        ]),
    }

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
