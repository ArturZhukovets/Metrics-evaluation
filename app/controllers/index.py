from app import app
from flask import render_template


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/not-found-404/")
def not_found():
    return render_template("not_found_404.html")
