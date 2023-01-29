from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from controllers.metrics import metrics
from controllers.translations import translations

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

app.register_blueprint(metrics, url_prefix="/metrics")
app.register_blueprint(translations, url_prefix="/translations")
