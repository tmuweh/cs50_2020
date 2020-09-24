from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello, World!</h1>"
@app.route("/goodbye")
def bye():
    return "GoodBye!"

@app.route("/hello")
def home():
    return "Hello, World!"