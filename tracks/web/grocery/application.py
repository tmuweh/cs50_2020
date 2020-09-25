from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["get", "post"])
def add():
    return render_template("add.html")