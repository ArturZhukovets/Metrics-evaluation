

def get_current_metrics(config) -> dict[str: bool]:
    current_metrics = config.evaluate_metrics.split(',')
    return {metric: metric for metric in current_metrics}


def get_new_metrics_values(form_data: dict[str: str]) -> str:
    form_data.pop('csrf_token')
    included_metrics = []
    for key, value in form_data.items():
        if value:
            included_metrics.append(key)
    return ','.join(included_metrics)
