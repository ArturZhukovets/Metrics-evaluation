import os

from werkzeug.utils import secure_filename, redirect

from config import UPLOAD_FOLDER, ABSOLUTE_PATH
from flask import Blueprint, render_template, flash, url_for
from forms.translations import CreateDatasetForm
from models.translation import Language, MonoDataSet
from database import db


translations = Blueprint("translations", __name__, template_folder="templates")


@translations.route("/")
def index():
    obj_list = MonoDataSet.query.all()  # todo select related with languages
    langs_list = Language.query.all()
    return render_template("translations/index.html", obj_list=obj_list, langs_list=langs_list)


@translations.route("/create-dataset", methods=["GET", "POST"])
def create_dataset():
    form = CreateDatasetForm()
    form.language.choices = [lang for lang in Language.query.all()]
    if form.validate_on_submit():
        file = form.file.data
        file_path = os.path.join(
            ABSOLUTE_PATH, UPLOAD_FOLDER, secure_filename(file.filename)
        )
        file.save(file_path)

        dataset = MonoDataSet(
            title=form.title.data,
            description=form.description.data,
            file=file_path,
            language=Language.query.filter(Language.lang_title == form.language.data).first()
        )
        db.session.add(dataset)
        db.session.commit()
        flash("Dataset was successfully created")
        return redirect(url_for("translations.index"))

    return render_template("translations/create.html", form=form)

