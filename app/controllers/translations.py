import os

from sqlalchemy.orm import joinedload

from config import ABSOLUTE_PATH, UPLOAD_FOLDER
from database import db
from flask import Blueprint, flash, render_template, url_for
from forms.translations import CreateDatasetForm, CreateLanguageForm
from models.translation import Language, MonoDataSet
from werkzeug.utils import redirect, secure_filename

translations = Blueprint("translations", __name__, template_folder="templates")


@translations.route("/")
def index():
    obj_list = MonoDataSet.query.options(joinedload(MonoDataSet.language))
    langs_list = Language.query.all()
    return render_template("translations/index.html", obj_list=obj_list, langs_list=langs_list)


# ============================================================ Dataset |
@translations.route("/create-dataset/", methods=["GET", "POST"])
def create_dataset():
    form_dt = CreateDatasetForm()
    form_dt.language.choices = [lang for lang in Language.query.all()]
    if form_dt.validate_on_submit():
        file = form_dt.file.data
        file_path = os.path.join(
            ABSOLUTE_PATH,
            UPLOAD_FOLDER,
            secure_filename(file.filename)
        )
        file.save(file_path)

        dataset = MonoDataSet(
            title=form_dt.title.data,
            description=form_dt.description.data,
            file=file_path,
            language=Language.query.filter(Language.lang_title == form_dt.language.data).first()
        )
        db.session.add(dataset)
        db.session.commit()
        flash("Dataset was successfully created", category="success")
        return redirect(url_for("translations.index"))

    return render_template("translations/create.html", form_dt=form_dt)


# ============================================================ LANGUAGE |
@translations.route("/create-language/", methods=["GET", "POST"])
def create_language():
    form_lang = CreateLanguageForm()
    if form_lang.validate_on_submit():
        language = Language(lang_title=form_lang.title.data, lang_locale=form_lang.locale.data)
        db.session.add(language)
        db.session.commit()
        flash("Language was successfully created", category="success")
        return redirect(url_for("translations.index"))

    return render_template("translations/create_language.html", form_lang=form_lang)





