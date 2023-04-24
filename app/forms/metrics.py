import wtforms
from flask_wtf import FlaskForm
from wtforms import validators

from models.translation import Language


# ====================================================== Simple Metric Test |
class StartEvaluateMetricForm(FlaskForm):
    SAVE_TO_CHOICES = [
        ("db", "Database"),
        ("csv", "CSV"),
        ("table", "Display in html table")
    ]
    title = wtforms.StringField(
        "Title:",
        validators=[
            validators.DataRequired(), validators.Length(min=1, max=40)
        ]
    )
    file_prediction = wtforms.FileField("File prediction:", validators=[validators.DataRequired()])
    file_reference = wtforms.FileField("File reference:", validators=[validators.DataRequired()])
    language_from = wtforms.SelectField(
        "Language from:",
        choices=[],
        coerce=int,
    )
    save_to = wtforms.RadioField(
        "Save to: ",
        choices=SAVE_TO_CHOICES,
        default="table",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        languages = Language.query.all()
        self.language_from.choices = [(language.id, language.lang_title) for language in languages]


# ======================================================== Metrics config |
class SelectMetricsForm(FlaskForm):
    bleu = wtforms.BooleanField(label="bleu:")
    bert = wtforms.BooleanField(label="bert:")
    comet = wtforms.BooleanField(label="comet:")
    ter = wtforms.BooleanField(label="ter:")
    chrf = wtforms.BooleanField(label="chrf:")
