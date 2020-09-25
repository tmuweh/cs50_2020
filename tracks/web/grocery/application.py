from flask import Flask, request, redirect, render_template

app = Flask(__name__)

#list of grocies
grocies = []

@app.route("/")
def index():
    return render_template("index.html" , grocies=grocies)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        name = request.form.get("name")
        grocies.append(name)
        return redirect("/")