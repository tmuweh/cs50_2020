from flask import Flask, request, redirect, render_template, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    # create session variable grocies to store list of grocies
    if "grocies" not in session:
        session["grocies"] = []
    return render_template("index.html" , grocies=session["grocies"])

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        name = request.form.get("name")
        session["grocies"].append(name)
        return redirect("/")