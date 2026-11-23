import csv
import fcntl
import os
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile


def write_csv(path: Path, header: tuple[str, ...], rows: Iterable[tuple], *, replace: bool) -> None:
    temp = NamedTemporaryFile(mode="w", encoding="utf-8-sig", newline="", dir=path.parent, delete=False)
    try:
        with temp:
            writer = csv.writer(temp, delimiter=";")
            writer.writerow(header)
            writer.writerows(rows)
        if replace:
            os.replace(temp.name, path)
        else:
            try:
                os.link(temp.name, path)
            except FileExistsError:
                raise FileExistsError(f"Файл «{path}» уже существует. Укажите новое имя.") from None
    finally:
        Path(temp.name).unlink(missing_ok=True)


class CsvTable:
    def __init__(self, path: Path, header: tuple[str, ...]):
        self.path = path
        self.header = header

    def read(self) -> list[tuple[str, ...]]:
        with self.path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, delimiter=";", strict=True)
            if tuple(next(reader, ())) != self.header:
                raise ValueError(f"Некорректный заголовок в {self.path}.")
            rows = []
            for row in reader:
                if len(row) != len(self.header):
                    raise ValueError(f"Некорректное число полей в {self.path}, строка {reader.line_num}.")
                rows.append(tuple(row))
            return rows

    def write(self, rows: Iterable[tuple]) -> None:
        write_csv(self.path, self.header, rows, replace=True)


class CsvStore:
    def __init__(self, directory: Path):
        self.directory = directory
        self.students = CsvTable(directory / "students.csv", ("id", "name"))
        self.criteria = CsvTable(directory / "criteria.csv", ("id", "name", "max_score", "weight"))
        self.evaluations = CsvTable(directory / "evaluations.csv", ("student_id", "criterion_id", "score"))

    @contextmanager
    def command(self) -> Iterator[None]:
        self.directory.mkdir(parents=True, exist_ok=True)
        # Один процесс выполняет всю последовательность загрузки, изменения и сохранения.
        with (self.directory / ".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            for table in (self.students, self.criteria, self.evaluations):
                if not table.path.exists():
                    table.write(())
            yield
