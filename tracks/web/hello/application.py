from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/")
def index():
    number = random.randint(1, 10)
    coin = random.randint(1,2)
    return render_template("index.html", name="Tangue", number=number, coin=coin)
@app.route("/goodbye")
def bye():
    return "GoodBye!"

@app.route("/hello")
def home():
    name = request.args.get("name")
    return render_template("hello.html", name=name)