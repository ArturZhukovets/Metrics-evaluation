import math

from flask import request as rqst

from services.file_service import FileService


class FilePaginator:
    def __init__(self, lines_per_page: int, request: rqst, file: FileService, page):
        self.lines_per_page = lines_per_page
        self.request = request
        self.file = file
        self.all_lines = self.file.count_lines()
        self.page = self.current_page(page)

    def current_page(self, page) -> int:
        """
        Return the current page
        If page number more than max possible page ValueError raise
        """
        try:
            page = int(page)
        except ValueError:
            page = 1
        if page <= self.all_pages():
            page = int(page)
        else:
            raise ValueError(f"page number {page} does not exist")
        return page

    def all_pages(self):
        if not self.all_lines <= self.lines_per_page:
            return math.ceil(self.all_lines / self.lines_per_page)
        return 1

    def get_page_obj(self) -> list[tuple[int, str]]:
        """
        get chunk based on self.lines_per_page and on self.current_page
        :return: list of lines
        """
        start = self.lines_per_page * self.page - self.lines_per_page
        stop = self.lines_per_page * self.page
        return self.file.get_chunk(start=start, stop=stop)

    def next_page(self):
        return self.page + 1

    def is_has_next(self):
        return self.page < self.all_pages()

    def prev_page(self):
        if self.page > 1:
            return self.page - 1
        return self.page

    def is_has_prev(self):
        return self.page > 1
