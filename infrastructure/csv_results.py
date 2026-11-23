from pathlib import Path

from use_cases.dto import StudentResultDTO

from .csv_store import write_csv


class CsvResultsWriter:
    def write(self, destination: str, rows: list[StudentResultDTO]) -> None:
        header = ("ID студента", "Студент", "Оценено", "Всего критериев", "Итог (%)")
        records = (
            (r.student.id, r.student.name, r.evaluated_count, r.criterion_count,
             "" if r.percent is None else f"{r.percent:.2f}")
            for r in rows
        )
        write_csv(Path(destination), header, records, replace=False)
