from flask import Flask, render_template
import storage
import business

app = Flask(__name__)

me = 34390  # 100688

# storage = storage.MockStorage()
storage = storage.FileStorage("resources/")


@app.route("/")
def index():
    return render_template("index.html",
                           carts=storage.get_carts(me),
                           timeline=business.get_timeline(storage.user(me)),
                           current_cart=storage.get_cart(list(storage.cart_list.keys())[-1]),
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
    return render_template("myprofile/index.html") # logged-in user is hardcoded

@app.route("/purchase")
def purchase():
    products = [
        storage.products[131022500000],
        storage.products[130569400000],
        storage.products[204101500000],
        storage.products[109700200000],
        storage.products[111273500000],
        storage.products[131126100000],
        storage.products[105276800000],
        storage.products[204015800000],
    ]

    return render_template("purchase/show.html", products=products)