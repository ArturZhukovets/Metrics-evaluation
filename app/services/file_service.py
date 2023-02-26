import os
from typing import Generator


class FileService:

    def __init__(self, filepath: str, encoding: str = 'utf-8'):
        self.encoding = encoding
        self.filepath = filepath

    def readline(self) -> Generator:
        with open(self.filepath, 'r', encoding=self.encoding) as f_o:
            for line in f_o:
                yield line.strip()

    def count_lines(self) -> int:
        counter = 0
        for _ in self.readline():
            counter += 1
        return counter

    def get_chunk(self, start: int, stop: int) -> list[tuple[int, str]]:
        chunk = []
        for index, line in enumerate(self.readline(), 1):
            if index >= start + 1:
                chunk.append((index, line))
            if len(chunk) == stop - start:
                break
        return chunk


