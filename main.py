from flask import Flask, render_template
import storage
import carts
import users

app = Flask(__name__)

storage = storage.MockStorage()

@app.route("/")
def index():
    return render_template("index.html", carts=storage.carts())


@app.route("/cart/<int:cart_id>")
def cart(cart_id: int):
    return render_template("cart/show.html", cart=storage.carts()[cart_id])


@app.route("/leaderbord")
def leaderboard():
    return render_template("leaderboard/index.html", users=storage.users())
