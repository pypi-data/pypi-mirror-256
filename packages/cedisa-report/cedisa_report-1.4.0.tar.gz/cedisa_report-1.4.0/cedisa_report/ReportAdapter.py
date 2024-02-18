from typing import Protocol

class ReportAdapter(Protocol):

    def make_title(self, title: str, merge_range: str) -> None:
        pass

    def make_report_creation_date(self) -> None:
        pass

    def make_simple_header(self, title: str, merge_range: str, line_number: int, column_number: int, width: int = 30) -> None:
        pass

    def make_text_data(self, line_number: int, column_number: int, data) -> None:
        pass

    def make_number_data(self, line_number: int, column_number: int, data) -> None:
        pass

