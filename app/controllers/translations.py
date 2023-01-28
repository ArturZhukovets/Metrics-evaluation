from flask import Blueprint, render_template

translations = Blueprint("translations", __name__, template_folder="templates")


@translations.route("/")
def index():
    return render_template("translations/index.html")
