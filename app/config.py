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
