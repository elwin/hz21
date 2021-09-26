import datetime
import storage
import business
from flask import Flask, render_template
from carts import Cart

app = Flask(__name__)

me = 0  # 100688

# storage = storage.MockStorage()
storage = storage.FileStorage("resources/")

# shopping_list_cart = Cart(
#     cart_id=-1,
#     date=datetime.date.today(),
#     location="asdf",
#     products=[
#         # storage.products[110102500000],
#         # storage.products[130569400000],
#         # storage.products[110174000000],
#         # storage.products[109700200000]
#     ]
# )

shopping_list_cart = storage.get_cart(103708000001)


@app.route("/")
def index():
    return render_template("index.html",
                           user=storage.user(me),
                           carts=storage.get_carts(me),
                           timeline=business.get_timeline(
                               storage.user(me),
                               [storage.user(1), storage.user(2), storage.user(3), storage.user(4)],
                           ),
                           shopping_list=shopping_list_cart,
                           )


@app.route("/shopping_list")
def shopping_list():
    return render_template("shopping_list/show.html",
                           storage=storage,
                           shopping_list=shopping_list_cart
                           )


@app.route("/cart/<int:cart_id>")
def cart(cart_id: int):
    return render_template("cart/show.html",
                           cart=storage.get_cart(cart_id),
                           storage=storage,
                           )


@app.route("/leaderbord")
def leaderboard():
    return render_template("leaderboard/index.html", users=storage.users())


@app.route("/me")
def myprofile():
    return render_template("myprofile/index.html")  # logged-in user is hardcoded


@app.route("/purchase")
def purchase():
    current_cart = Cart(
        cart_id=-1,
        date=datetime.date.today(),
        location="asdf",
        products=[
            storage.products[131022500000],
            storage.products[109700200000],
            storage.products[111273500000],
            storage.products[131126100000],
            storage.products[204101500000],
            storage.products[130569400000],
            storage.products[105276800000],
            storage.products[204015800000],
        ]
    )

    return render_template("purchase/show.html", cart=current_cart)
