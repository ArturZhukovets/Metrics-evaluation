from database import db
from flask import Blueprint, flash, render_template, url_for, request
from forms.translations import CreateDatasetForm, CreateLanguageForm
from models.translation import Language, MonoDataSet
from services.create_file import create_file
from sqlalchemy.orm import joinedload

from services.file_paginator import FilePaginator
from validations.exceptions import ValidationError
from werkzeug.utils import redirect
from services.file_service import FileService


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

        try:
            file = form_dt.file.data
            language = Language.query.filter(Language.lang_title == form_dt.language.data).first()
            file_path = create_file(file=file, lang=language)
        except ValidationError as error:
            flash(str(error), category="danger")
            return redirect(url_for("translations.create_dataset"))

        try:
            dataset = MonoDataSet(
                title=form_dt.title.data,
                description=form_dt.description.data,
                file=file_path,
                language=language
            )
            db.session.add(dataset)
            db.session.commit()
        except Exception as error:
            flash(str(error), category="danger")
            return redirect(url_for("translations.create_dataset"))

        else:
            flash("Dataset was successfully created", category="success")
            return redirect(url_for("translations.index"))

    return render_template("translations/create.html", form_dt=form_dt)


@translations.route("/detail-dataset/<int:dataset_id>", methods=["GET"])
def detail_dataset(dataset_id: int):
    dataset = MonoDataSet.query.get(dataset_id)
    file = FileService(dataset.file)
    page = request.args.get('page', 1)
    paginator = FilePaginator(20, request, file, page)

    return render_template(
        "translations/detail_dataset.html",
        dataset=dataset,
        page_obj=paginator.get_page_obj(),
        paginator=paginator

    )


def delete_dataset():
    pass


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





