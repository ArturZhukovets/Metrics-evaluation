import os
from pathlib import Path

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER, ABSOLUTE_PATH, API_STORAGE
from database import db
from forms.metrics import SelectMetricsForm, StartEvaluateMetricForm
from models.metric import TestmetricsConfig
from services.file_service import FileService
from services.metrics_utils.evaluate_metrics import MetricEvaluator, SentenceMetric, TextMetric, \
    count_average_text_metric
from services.metrics_utils.manual_metrics import InMemoryFileProcessor
from services.metrics_utils.metric_configuration_utils import get_current_metrics, get_new_metrics_values

metrics = Blueprint("metrics", __name__, template_folder="templates")


@metrics.route("/", methods=["GET"])
def index():
    form = StartEvaluateMetricForm()
    return render_template("metrics/index.html", form=form)


@metrics.route('/start-manual-test', methods=["POST"])
def start_manual_test():
    form = StartEvaluateMetricForm()
    if form.validate_on_submit():
        file_pred = request.files['file_prediction']
        file_ref = request.files['file_reference']

        try:
            file_processor = InMemoryFileProcessor(file_pred, file_ref)
            total_text: list[TextMetric] = []
            total_sentences: list[SentenceMetric] = []
            for chunk_pred, chunk_ref in file_processor.split_files_by_chunks():
                metrics_evaluator = MetricEvaluator(chunk_pred, chunk_ref)
                total_text.append(metrics_evaluator.run_evaluating_text())
                total_sentences += metrics_evaluator.run_evaluating_sentence_new_dt()
            average_text_metrics: TextMetric = count_average_text_metric(total_text)

            if form.data['save_to'] == 'table':
                # TODO Create pagination
                table = file_processor.readline_result_table(scores=total_sentences)
                return render_template('metrics/metrics_result.html', table=table, total_text=average_text_metrics)

            if form.data['save_to'] == 'csv':
                csv_file = file_processor.save_to_csv(
                    sent_scores=total_sentences,
                    total_score=average_text_metrics,
                    title=form.data['title']
                )
                return send_file(csv_file, as_attachment=True, download_name=csv_file.name)

        except Exception as ex:
            error_massage = {
                "message": "error while processing files",
                "info": str(ex)
            }
            return jsonify(error_massage), 500

    else:
        flash(f"Error. Form is invalid {form.errors}", category='error')
        return redirect(url_for("metrics.index"))


@metrics.route("/metrics-config", methods=["GET", "POST"])
def metrics_config():
    config = TestmetricsConfig.get()
    form = SelectMetricsForm(**get_current_metrics(config))
    return render_template("metrics/metrics_config.html", config=config, form=form)


@metrics.route("/metrics-update", methods=["POST"])
def metrics_config_update():
    config = TestmetricsConfig.get()
    form = SelectMetricsForm()
    if form.validate_on_submit():
        selected_metrics = get_new_metrics_values(form.data)
        config.evaluate_metrics = selected_metrics
        db.session.commit()
        flash("Metrics config were updated", category="success")
    return redirect(url_for('metrics.metrics_config'))


@metrics.route("/api-get-string-metrics", methods=["GET"])
def api_string_metrics():
    prediction: str = request.args.get("pred")
    reference: list[str] = request.args.getlist("ref")
    all_metrics: list[str] = request.args.getlist('metric')
    lowercase = request.args.get('lower')
    if lowercase and lowercase.isdigit():
        lowercase = bool(int(lowercase))
    else:
        lowercase = True

    evaluator = MetricEvaluator(
        prediction=[prediction],
        reference=reference,
        lowercase=lowercase,
    )
    try:
        res = evaluator.run_evaluating_api_sent_metrics(all_metrics)
    except Exception as e:
        res = {"err": str(e)}

    return jsonify(res)


@metrics.route("/api-get-text-metrics", methods=["POST"])
def api_text_metrics():
    prediction_file = request.files['pred']
    reference_file = request.files['ref']
    all_metrics = request.form.getlist('metrics')
    lowercase = request.form.get('lower')
    if lowercase and lowercase.isdigit():
        lowercase = bool(int(lowercase))
    else:
        lowercase = True

    pred_file_name = secure_filename(prediction_file.filename + "(pred)")
    ref_file_name = secure_filename(reference_file.filename + "(ref)")

    _storage_dir = os.path.join(ABSOLUTE_PATH, API_STORAGE, "txt_files")
    if not os.path.exists(_storage_dir):
        Path(_storage_dir).mkdir(parents=True, exist_ok=True)

    prediction_file.save(os.path.join(_storage_dir, pred_file_name))
    reference_file.save(os.path.join(_storage_dir, ref_file_name))

    _pred_service = FileService(os.path.join(_storage_dir, pred_file_name))
    _pred_lines = [line for line in _pred_service.readline()]
    _ref_service = FileService(os.path.join(_storage_dir, ref_file_name))
    _ref_lines = [line for line in _ref_service.readline()]

    evaluator = MetricEvaluator(
        prediction=_pred_lines,
        reference=_ref_lines,
        lowercase=lowercase,
    )
    res = evaluator.run_evaluating_api_text_metrics(all_metrics)
    return jsonify(res)



