from flask_wtf import FlaskForm
from wtforms import FileField, StringField, TextAreaField, validators, SelectField
from validations.form_validators import FileLengthValidator


class CreateDatasetForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[validators.Length(min=1, max=50)]
    )
    description = TextAreaField("Description", validators=[validators.DataRequired()])
    language = SelectField("Language", validators=[validators.DataRequired()])
    file = FileField("File", validators=[validators.DataRequired(), FileLengthValidator()])



