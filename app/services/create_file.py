import os

from config import ABSOLUTE_PATH, UPLOAD_FOLDER
from models.translation import Language
from validations.exceptions import ValidationError
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def create_file(file: FileStorage, lang: Language) -> str:
    """
    Create name for file, validate this file and save it in local storage.
    :param lang: Language object
    :param file: file object
    :return: path of created file
    """
    filename = file_name_preprocessing(file.filename, lang)
    file_path = os.path.join(
            ABSOLUTE_PATH,
            UPLOAD_FOLDER,
            secure_filename(filename)
        )
    file.save(file_path)

    return file_path


def file_name_preprocessing(file_name: str, lang: Language):
    while "." in file_name:
        file_name = os.path.splitext(file_name)[0]

    file_name += ".from"
    file_name += "." + lang.lang_locale[:2] + ".txt"

    if _file_already_exists(file_name):
        raise ValidationError(
            "Such file already exists. Please rename your file or delete existing dataset"
        )
    return file_name


def _file_already_exists(filename: str) -> bool:
    """
    Validate creating file. If such file is in local file storage
    ValidationError will raise
    """
    if filename in os.listdir(os.path.join(ABSOLUTE_PATH, UPLOAD_FOLDER)):
        return True

