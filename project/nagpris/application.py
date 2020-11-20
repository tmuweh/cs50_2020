from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

db = SQL("sqlite:///data.db")

@app.route("/")
def index():
  
    return render_template("index.html")