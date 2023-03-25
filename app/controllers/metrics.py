from flask import Blueprint, render_template, request, flash, redirect, url_for
from database import db
from forms.metrics import SelectMetricsForm
from models.metric import TestmetricsConfig
from services.metrics_utils.metric_configuration_utils import get_current_metrics, get_new_metrics_values

metrics = Blueprint("metrics", __name__, template_folder="templates")


@metrics.route("/")
def index():
    return render_template("metrics/index.html")


@metrics.route("/metrics-config", methods=["GET", "POST"])
def metrics_config():
    config = TestmetricsConfig.get()
    form = SelectMetricsForm(**get_current_metrics(config))
    return render_template("metrics/metrics_config.html", config=config, form=form)


@metrics.post("/metrics-update")
def metrics_config_update():
    config = TestmetricsConfig.get()
    form = SelectMetricsForm()
    if form.validate_on_submit():
        selected_metrics = get_new_metrics_values(form.data)
        config.evaluate_metrics = selected_metrics
        db.session.commit()
        flash("Metrics config was successfully", category="success")
    return redirect(url_for('metrics.metrics_config'))
