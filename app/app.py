from flask import Flask
from database import db

from controllers.metrics import metrics
from controllers.translations import translations

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)

app.register_blueprint(metrics, url_prefix="/metrics")
app.register_blueprint(translations, url_prefix="/translations")
