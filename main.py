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
                           current_cart=storage.get_cart(999999),
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
