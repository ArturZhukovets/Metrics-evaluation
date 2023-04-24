# TODO RENAME MODULE
import csv
import itertools
import subprocess
import logging
from pathlib import Path
from typing import Generator

from werkzeug.datastructures import FileStorage

from config import ABSOLUTE_PATH
from services.metrics_utils.evaluate_metrics import SentenceMetric, TextMetric

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)


class InMemoryFileProcessor:

    CHUNK_SIZE = 50

    def __init__(self, file_prediction: FileStorage, file_reference: FileStorage):
        self.file_pred = file_prediction
        self.file_ref = file_reference
        self.validate_count_lines()

    def validate_count_lines(self):
        """
        Validate both files by length. If files have different length
        - raise an Exception.
        """
        try:
            output_pred = int(subprocess.run(
                ['wc', '-l'],
                input=self.file_pred.read().decode(encoding='utf-8'),
                capture_output=True, text=True
            ).stdout.strip().split()[0])
            output_ref = int(subprocess.run(
                ['wc', '-l'],
                input=self.file_ref.read().decode(encoding='utf-8'),
                capture_output=True, text=True
            ).stdout.strip().split()[0])
        except MemoryError as m_ex:
            logger.exception("Files is too big for manual testing. {}".format(m_ex))
            raise m_ex
        except Exception as ex:
            logger.exception(ex)
            raise ex
        else:
            if output_pred != output_ref:
                logger.error("Files have different length")
                raise ValueError("Files have different length")
        finally:
            self.file_pred.seek(0)
            self.file_ref.seek(0)

    def split_files_by_chunks(self):
        while True:
            chunk_pred = list(
                map(lambda line: line.decode(encoding='utf-8'), itertools.islice(self.file_pred, self.CHUNK_SIZE))
            )
            chunk_ref = list(
                map(lambda line: line.decode(encoding='utf-8'), itertools.islice(self.file_ref, self.CHUNK_SIZE))
                )
            if not all((chunk_pred, chunk_ref)):
                break
            yield chunk_pred, chunk_ref

    def readline_result_table(self, scores: list[SentenceMetric]) -> Generator[tuple[str, str, str], None, None]:
        self._reset_pointer()
        for line_pred, line_reference, score in zip(self.file_pred, self.file_ref, scores):
            yield line_pred.decode(encoding='utf-8').strip(), line_reference.decode(encoding='utf-8').strip(), score

    def save_to_csv(self, sent_scores: list[SentenceMetric], total_score: TextMetric, title: str) -> Path:
        self._reset_pointer()

        csv_dir = Path(ABSOLUTE_PATH, "media", "csv")
        csv_dir.mkdir(parents=True, exist_ok=True)
        # file_name = self.file_pred.name + "_" + self.file_ref.name + ".csv"
        file_name = title + ".csv"
        with open(Path(csv_dir / file_name), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Line prediction",
                "Line reference",
                "BLEU",
                "CHR-F",
                "TER",
            ])
            for line_pred, line_reference, score in zip(self.file_pred, self.file_ref, sent_scores):
                writer.writerow([
                    line_pred.decode(encoding='utf-8').strip(),
                    line_reference.decode(encoding='utf-8').strip(),
                    score.bleu,
                    score.chrf,
                    score.ter
                ])
        return Path(csv_dir / file_name)

    def _reset_pointer(self) -> None:
        position_pred = self.file_pred.tell()
        position_ref = self.file_ref.tell()
        if not all([position_pred == 0, position_ref == 0]):
            self.file_pred.seek(0)
            self.file_ref.seek(0)
