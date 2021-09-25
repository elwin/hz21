from flask import Flask, render_template
import storage
import business

app = Flask(__name__)

# storage = storage.MockStorage()
storage = storage.FileStorage("resources/")


@app.route("/")
def index():
    return render_template("index.html", carts=storage.carts(100688), timeline=business.get_timeline(storage.users()))  # TODO


@app.route("/cart/<int:cart_id>")
def cart(cart_id: int):
    return render_template("cart/show.html", cart=storage.carts(cart_id))


@app.route("/leaderbord")
def leaderboard():
    return render_template("leaderboard/index.html", users=storage.users())
