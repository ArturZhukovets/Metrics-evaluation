import logging
import string
from torchmetrics.functional.text import chrf_score, translation_edit_rate
from dataclasses import dataclass
from itertools import zip_longest

import sacrebleu
from typing import Final, Sequence

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

PUNCTUATION = string.punctuation.translate(str.maketrans('', '', '-><'))


@dataclass
class TextMetric:
    bleu: float = 0

    def __add__(self, other):
        if not isinstance(other, TextMetric):
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'"
                .format(type(self).__name__, type(other).__name__)
            )
        return TextMetric(self.bleu + other.bleu)

    def __truediv__(self, other: float | int):
        return TextMetric(self.bleu / other)

@dataclass
class SentenceMetric:
    bleu: float = 0
    chrf: float = 0
    ter: float = 0

class MetricEvaluator:
    def __init__(
            self,
            prediction: Sequence[str], reference: Sequence[str],
            with_punctuation: bool = False, lowercase: bool = True
    ):
        self.prediction = prediction
        self.reference = reference
        self.with_punctuation = with_punctuation
        self.lowercase = lowercase

    def chrf_text(self) -> float:
        logger.debug("Evaluating `chrf` for whole text...")
        metric = chrf_score(
            preds=self.prediction,
            target=self.reference,
            lowercase=self.lowercase
        )
        return round(float(metric) * 100, 2)

    def chrf_sentence(self, prediction: str, reference: str) -> float:
        metric = chrf_score(
            preds=prediction,
            target=[reference],
            lowercase=self.lowercase
        )
        return round(float(metric) * 100, 2)

    def ter_text(self) -> float:
        logger.debug("Evaluating `ter` for whole text...")
        metric = translation_edit_rate(
            preds=self.prediction,
            target=self.reference,
            lowercase=self.lowercase,
        )
        return round(float(metric) * 100, 2)

    def ter_sentence(self, prediction: str, reference: str) -> float:
        metric = translation_edit_rate(
            preds=prediction,
            target=reference,
            lowercase=self.lowercase,
        )
        return round(float(metric) * 100, 2)

    def bleu_text(self) -> float:
        logger.debug("Evaluating `bleu` for whole text...")
        metric = sacrebleu.corpus_bleu(
            self.prediction,
            [self.reference],
            lowercase=self.lowercase,
            use_effective_order=True
        )
        metric_score = round(metric.score, 2)
        return metric_score

    def bleu_sentence(self, prediction: str, reference: str) -> float:
        if not self.with_punctuation:
            prediction = prediction.translate(str.maketrans('', '', PUNCTUATION))
            reference = reference.translate(str.maketrans('', '', PUNCTUATION))

        metric = sacrebleu.sentence_bleu(
            prediction,
            [reference],
            use_effective_order=True,
            lowercase=self.lowercase,
        )
        return round(metric.score, 2)

    # ======================================= Run funcs |

    def run_evaluating_text(self) -> TextMetric:
        total_metrics = TextMetric()
        total_metrics.bleu = self.bleu_text()
        return total_metrics

    def run_evaluating_sentence_new_dt(self) -> list[SentenceMetric]:
        results = []
        for line_pred, line_ref in zip(self.prediction, self.reference):
            metric = SentenceMetric()
            metric.bleu = self.bleu_sentence(line_pred, line_ref)
            results.append(metric)
        return results

    def run_evaluating_api_sent_metrics(self, metrics: list[str]) -> dict[str: float]:
        pred = self.prediction[0]
        ref = self.reference[0]
        result = {}
        for metric in metrics:
            try:
                func = getattr(self, metric + "_sentence")
                result[metric] = func(pred, ref)
                print(f"{metric} calculated. Result: {result[metric]}")
            except AttributeError:
                logger.error(f"There is no attribute `{metric + '_sentence'}`.")
        return result

    def run_evaluating_api_text_metrics(self, metrics: list[str]) -> dict[str: float]:
        # todo realize evaluation whole text + tuple[each sentence].
        # todo rewrote TER using sacreBleu lib.
        result = {}
        for metric in metrics:
            try:
                func = getattr(self, metric + "_text")
                result[metric] = func()
            except AttributeError:
                logger.error(f"There is no attribute `{metric + '_sentence'}`.")
        return result

    # ======================================= Utils |

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Delete all punctuation from text/string.
        """
        cleaned_text: Final = text.translate(str.maketrans("", "", string.punctuation))
        return cleaned_text


def count_average_text_metric(chunks_metrics: list[TextMetric]) -> TextMetric:
    result = TextMetric()
    for value in chunks_metrics:
        result += value
    return result / len(chunks_metrics)
