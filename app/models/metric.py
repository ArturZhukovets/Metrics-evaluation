from database import db
from datetime import datetime

METRICS = ["bleu", 'bert', 'comet', 'ter', 'chrf']


def initialize_default_metrics() -> str:
    return ','.join(METRICS)


class SingletonModel(db.Model):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        if self.__class__.query.count() > 0:
            raise Exception("Singleton instance already exists")
        super().__init__(*args, **kwargs)

    @classmethod
    def get(cls):
        obj = cls.query.first()
        if obj is None:
            obj = cls()
            db.session.add(obj)
            db.session.commit()
        return obj


class TestmetricsConfig(SingletonModel):
    __tablename__ = "testmetrics_config"

    id = db.Column(db.Integer, primary_key=True)
    evaluate_metrics = db.Column(db.String(150), default=initialize_default_metrics())

    def __repr__(self) -> str:
        return "[TestmetricsConfig instance]"
