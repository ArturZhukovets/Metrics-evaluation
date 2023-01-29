from database import db
from datetime import datetime


class MonoDataSet(db.Model):
    __tablename__ = 'mono_data_set'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=True,)
    creation_date = db.Column(db.DateTime, default=datetime.now())
    file = db.Column(db.String(250), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'), nullable=False)

    def __repr__(self) -> str:
        return str(self.title)


class Language(db.Model):
    # todo create validation on the locale field
    __tablename__ = "language"
    id = db.Column(db.Integer, primary_key=True)
    lang_title = db.Column(db.String(30), nullable=False)
    lang_locale = db.Column(db.String(5), nullable=False)
    datasets = db.relationship('MonoDataSet', backref="language")

    def get_all_languages(self):
        return db.session.query(Language).all()

    def __repr__(self) -> str:
        return str(self.lang_title)
