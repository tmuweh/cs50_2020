import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd, get_int

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    current_stock = {}
    stocks = db.execute("SELECT * FROM stocks WHERE user_id=:user_id", user_id=session["user_id"])
    for stock in stocks:
        current_stock[stock['symbol']] = lookup(stock['symbol'])
    cash = db.execute("SELECT cash from Users WHERE id =:user_id", user_id=session["user_id"])

    # total value of stock
    total = 0.0
    for stock in stocks:
        # each stock current price
        current_price = lookup(stock["symbol"])
        total += stock["shares"] * current_price["price"]

    return render_template("index.html", stocks=stocks, current_stock=current_stock, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # save symbols as uppercase string
        symbol = symbol.upper()
        shares = request.form.get("shares")
        shares = get_int(shares)
        if not shares or not symbol:
            return apology("Must provide stock symbol and shares", 403)
        shares = int(shares)
        # check for valid symbol and valid shares
        request_data = lookup(symbol)
        if not request_data:
            return apology("Enter a valid Symbol", 403)
        if shares <= 0:
            return apology("Shares can not be be zero or less", 403)

        # check user fund and check if they can purchase stocks
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        user_fund = rows[0]["cash"]
        stock_fund = float(request_data["price"]) * shares
        if user_fund < stock_fund:
            return apology("Inadequate funds to acquire stocks")
        else:
            # check if stock already exist... update
            shares_present = db.execute("SELECT * FROM stocks, users WHERE users.id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol)
            if len(shares_present) == 1:
                update = db.execute("UPDATE stocks SET shares = :shares, date = :date WHERE user_id = :user_id AND symbol = :symbol", shares=shares_present[0]["shares"] + shares, date=datetime.timestamp(datetime.now()), user_id=session["user_id"], symbol=symbol)

                # update user's cash
                cash_update = db.execute("Update users SET cash = :cash WHERE id=:user_id", cash=user_fund-stock_fund, user_id=session["user_id"])
                history = db.execute("INSERT INTO history(user_id,symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)", user_id=session["user_id"], symbol=symbol, shares=shares, price=float(request_data["price"]))
                if not update or not history or not cash_update:
                    return apology("Some error buying these shares", 403)

                return redirect("/")

            # else insert new stock
            else:
                insert = db.execute("INSERT INTO stocks(symbol, shares, user_id) VALUES(:symbol, :shares, :user_id)", symbol=symbol, shares=shares, user_id=session["user_id"])
                history = db.execute("INSERT INTO history(user_id,symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)", user_id=session["user_id"], symbol=symbol, shares=shares, price=request_data["price"])
                cash_update = db.execute("Update users SET cash = :cash WHERE id=:user_id", cash=user_fund-stock_fund, user_id=session["user_id"])
                if not insert or not history or not cash_update:
                    return apology("Some error occur why buying stock", 403)
                return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    histories = db.execute("SELECT * FROM history WHERE user_id=:user_id", user_id=session['user_id'])

    return render_template("history.html", histories=histories)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("You must provide a symbol", 403)
        symbol = symbol.upper()
        request_data = lookup(symbol)
        if not request_data:
            return apology("Must enter a valid Stock Symbol", 403)
        stock_cost = request_data["price"]
        stock_name = request_data["name"]
        stock_symbol = request_data["symbol"]
        return render_template("quoted.html", stock_name=stock_name, stock_cost=stock_cost, stock_symbol=stock_symbol )

    else:
        return render_template("quote.html")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure passwords were submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif not request.form.get("confirm_password"):
            return apology("must provide password", 403)
        else:
            username = request.form.get("username")
            password = request.form.get("password")

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

            # make sure username doesn't exist
            print(rows)
            if len(rows) != 0:
                return apology("User Already exits", 403)
            else:
                # create user
                successful = db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)", username=username, hash=generate_password_hash(password))
                if successful:
                    return redirect("login")
                else:
                    return render_template("register.html", message = "Something went wrong!")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # get all stock names
    symbols = db.execute("SELECT symbol FROM stocks WHERE user_id = :user_id", user_id=session["user_id"])
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        shares = get_int(shares)

        stocks = db.execute("SELECT * from stocks WHERE symbol=:symbol AND user_id=:user_id", symbol=symbol.upper(), user_id=session["user_id"])

        # check for valid input
        if not symbol or not shares or int(shares) <= 0:
            return apology("Select a valid symbol and/or shares", 403)

        elif int(shares) > stocks[0]["shares"]:
            return apology("Unsufficient shares to sell", 403)
        else:
            "sell stock and update affected dbs"

            # user money and shares
            current_stock = lookup(stocks[0]["symbol"])
            user_data = db.execute("SELECT * FROM users WHERE id=:user_id", user_id=session["user_id"])
            cash = user_data[0]["cash"] + (int(shares) * current_stock["price"])
            update_user_details = db.execute("UPDATE users SET cash = :cash WHERE id = :user_id",cash=cash, user_id=session["user_id"])

            # stock
            if int(shares) == stocks[0]["shares"]:
                #delete stock if all shares are sold
                update_stocks = db.execute("DELETE FROM stocks WHERE symbol=:symbol", symbol=symbol.upper())
            else:
                update_stocks = db.execute("UPDATE stocks SET shares=:shares WHERE user_id=:user_id", shares=stocks[0]["shares"]-int(shares), user_id=session["user_id"])

            # history
            add_history = db.execute("INSERT INTO history(user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)", user_id=session["user_id"], symbol=symbol, shares= 0-int(shares), price=current_stock["price"])

            if not update_user_details or not update_stocks or not add_history:
                return apology("Failed to sell. Sorry!")
            else:
                return redirect("/")
    else:
        return render_template("sell.html", symbols=symbols)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
