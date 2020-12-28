from cs50 import SQL
from flask import g, Flask, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from functools import wraps
from flask_mail import Mail, Message

import os
from werkzeug.utils import secure_filename
import time


ticks = time.time()

IMAGE_UPLOADS = 'static/images/products/'

app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["IMAGE_FOLDER"] = IMAGE_UPLOADS


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
app.debug = True
Session(app)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nagprisapp@gmail.com'  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'nagprisapp@gmail.com' # enter your email here
app.config['MAIL_PASSWORD'] = 'alpha1002' # enter your password here

# mailing
mail = Mail(app)

db = SQL("sqlite:///data.db")

categories = db.execute("SELECT * FROM category WHERE 1")

""" lOGIN REQUIRED DECORATOR """
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


@app.route("/")
def index():

    # setup filter for displayed products
    f = request.args
    if f:
        if 'search' in f:
            # search each word in entered search string
            for item in splitter(f['search'], " "):
                products = db.execute("SELECT * FROM products JOIN images WHERE products.product_id = images.product_id AND product_name LIKE :name UNION SELECT * FROM products JOIN images WHERE products.product_id = images.product_id AND product_name LIKE :item ", name="%" + splitter(f['search'], " ")[0] + "%", item="%" + item + "%")
        else:
            cat_id = db.execute("SELECT cat_id FROM category WHERE name = :name", name=f['f'].capitalize())
            if cat_id:
                products = db.execute("SELECT * FROM products JOIN images WHERE products.product_id = images.product_id AND cat_id = :cat_id", cat_id=cat_id[0]["cat_id"])
    else:
        products = db.execute("SELECT * FROM products JOIN images WHERE products.product_id = images.product_id")

    categories = db.execute("SELECT * FROM category WHERE 1")
    images = db.execute("SELECT img_url FROM images")


    return render_template("index.html", products=products, categories=categories, images=images)


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
            session["first_name"] = rows[0]["first_name"]

            # Redirect user to home page
            return redirect("/")
    else:
        return render_template("login.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        unit_price = request.form.get("unit_price")
        quantity = request.form.get("quantity")
        category = request.form.get("category")
        cat_id = db.execute("SELECT cat_id FROM category WHERE name = :name",
                                    name=category)[0]["cat_id"]
        image = request.files["image"]
        description = request.form.get("description")

        # if no file was submitted
        if image.filename == "":
            return render_template("sell.html", message="Please upload a clear image of the product")
        else:
            # rename image file
            image.filename = splitter(image.filename, ".")[0] + "_" + str(int(ticks)) + "." + splitter(image.filename, '.')[1]

            # secure name of image
            filename = secure_filename(image.filename)

            # get image absolute path
            image_path = os.path.join(app.config['IMAGE_FOLDER'], filename)

            # Add product to db
            success = db.execute("INSERT INTO products(product_name, unit_price, quantity, cat_id, user_id, description) VALUES(:product_name, :unit_price, :quantity, :cat_id, :user_id, :description)",
                                                        product_name=product_name, unit_price=unit_price, quantity=quantity, cat_id=cat_id, user_id=session['user_id'], description=description)
            if True:
                # save image
                product_id=db.execute("SELECT product_id FROM products WHERE product_name=:product_name",
                                                       product_name=product_name)[0]["product_id"]
                stored = db.execute("INSERT INTO images(img_url, product_id) VALUES(:img_url, :product_id)",
                                    img_url=image_path, product_id=product_id)
                if stored:
                    image.save(image_path)
                    return render_template("index.html", message="Product added!")
                else:
                    return render_template("index.html", message="Couldn't save image")
            else:
                return render_template("index.html", message="Error adding product.")
    else:

        categories = db.execute("SELECT * FROM category WHERE 1")
        return render_template("sell.html", categories=categories)


@app.route("/product")
def product_info():
    product_id = request.args
    if product_id:
        product_info = db.execute("SELECT * FROM products JOIN images WHERE images.product_id = products.product_id AND products.product_id = :product_id", product_id=product_id["n"])
        if product_info:
            return render_template("product.html", product_info=product_info)
    else:
        return redirect("/")


@app.route("/message", methods=["POST", "GET"])
@login_required
def message():

    product_id = request.args
    if request.method == "POST":
        email = request.form.get("email")
        message = request.form.get("message")
        seller_id = request.form.get("user_id")
        print(seller_id)
        seller_email  = db.execute("SELECT email FROM users WHERE user_id = :user_id", user_id=int(seller_id))
        print(seller_email[0]["email"])
        name = request.form.get("name")
        msg = Message("Purchase Request", recipients=[seller_email[0]["email"]])
        msg.body = "{} from {}<{}>.".format(message, name, email)
        mail.send(msg)
        print("\nData received. Now redirecting ...")
        return redirect("/")
    elif product_id:
        product_info = db.execute("SELECT * FROM products JOIN users WHERE users.user_id = products.user_id AND products.product_id = :product_id", product_id=product_id["pid"])
        return render_template("message.html", product_info=product_info)
    else:
        return redirect("/")


""" separate strings according to supplied delimiter"""
def splitter(name, delimiter):
    # returns a list of two strings... [0] name and [1] extension
    list = name.split(delimiter)
    return list
