from flask import Blueprint, render_template

metrics = Blueprint("metrics", __name__, template_folder="templates")


@metrics.route("/")
def index():
    return render_template("metrics/index.html")
