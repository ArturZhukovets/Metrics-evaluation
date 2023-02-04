from wtforms import ValidationError
import re


class FileLengthValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u'File name should contain only latin characters and "_-"'
        self.message = message

    def __call__(self, form, field):
        file = field.data
        if not file.content_type == "text/plain" or not self.validate_filename(file.filename):
            raise ValidationError(message=self.message)
        if len(file.filename) > 50:
            raise ValidationError(message="filename should be less than 50 characters")

    @staticmethod
    def validate_filename(filename: str) -> bool:
        return bool(re.match(pattern=r'^[a-zA-Z0-9-_\.]*$', string=filename))
