import wtforms
from flask_wtf import FlaskForm


class SelectMetricsForm(FlaskForm):
    bleu = wtforms.BooleanField(label="bleu:")
    bert = wtforms.BooleanField(label="bert:")
    comet = wtforms.BooleanField(label="comet:")
    ter = wtforms.BooleanField(label="ter:")
    chrf = wtforms.BooleanField(label="chrf:")
