"""
Development config
"""
import os
from dotenv import load_dotenv

load_dotenv()


TESTING = True
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
SECRET_KEY = os.getenv("SECRET_KEY")
UPLOAD_FOLDER = "static/files"
ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
