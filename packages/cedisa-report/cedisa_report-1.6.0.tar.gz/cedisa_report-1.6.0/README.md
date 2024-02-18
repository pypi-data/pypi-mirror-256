## Functions

```python
def make_title(self, title: str, merge_range: str) -> None

def make_report_creation_date(self) -> None

def make_simple_header(self, title: str, merge_range: str, line_number: int, column_number: int, width: int = 30) -> None

def make_text_data(self, line_number: int, column_number: int, data) -> None

def make_number_data(self, line_number: int, column_number: int, data) -> None
```

## Initialize
```python
from cedisa_report import Report

wb = Workbook()
ws = wb.active

report = Report(ws, img_path='./path/to/title/image')
# OR
report = Report(ws)

```

## Dependencies
```sh
pip install pillow openpyxl
```