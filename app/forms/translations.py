from flask_wtf import FlaskForm
from wtforms import FileField, StringField, TextAreaField, validators, SelectField


class CreateDatasetForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[validators.Length(min=1, max=120)]
    )
    description = TextAreaField("Description", validators=[validators.DataRequired()])
    language = SelectField("Language")
    file = FileField("File")


