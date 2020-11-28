from cs50 import SQL
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from functools import wraps

import os
from werkzeug.utils import secure_filename

IMAGE_UPLOADS = '/static/images/products/'

app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["IMAGE_UPLOADS"] = IMAGE_UPLOADS


#Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


db = SQL("sqlite:///data.db")

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/logout")
def logout():

    # forget user_id
    session.clear()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        # register to db
        rows = db.execute("INSERT INTO users(username, first_name, last_name, hash, email) VALUES(:username, :first_name,:last_name, :hash, :email)",
                                        username=username, first_name=first_name, last_name=last_name, hash=generate_password_hash("password"), email=email)
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    if request.method == "POST":
        username = request.form.get("username")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        # Ensure username exists and password is correct
        print(len(rows))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):

            return render_template("login.html", message="Invalid username/password")

        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["user_id"]
            session["username"] = rows[0]["username"]

            # Redirect user to home page
            return redirect("/")
    else:
        return render_template("login.html")


@app.route("/sell", methods=["GET", "POST"])
def sell():

    if request.method == "POST":
        image = request.files["image"]
        if image.filename == "":
            pass
        else:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            print(image_path)
            filename = secure_filename(image.filename)
            image.save(image_path)
        pass
    else:
        rows = db.execute("SELECT * FROM category WHERE 1")

        return render_template("sell.html", rows=rows)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
