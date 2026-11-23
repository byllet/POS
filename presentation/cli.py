import argparse
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from . import criteria, evaluations, reports, students


@dataclass
class ConsoleApp:
    students: students.StudentsCommands
    criteria: criteria.CriteriaCommands
    evaluations: evaluations.EvaluationsCommands
    reports: reports.ReportsCommands

    def execute(self, args: argparse.Namespace) -> str:
        return args.action(self, args)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ПОС · Преподавательская оценка студентов")
    parser.add_argument("--data-dir", type=Path, default=Path("data"), metavar="КАТАЛОГ",
                        help="Каталог рабочих CSV-файлов (по умолчанию data)")
    groups = parser.add_subparsers(required=True)
    students.register(groups.add_parser("student", help="Студенты"))
    criteria.register(groups.add_parser("criterion", help="Рубрикатор"))
    evaluations.register(groups.add_parser("grade", help="Оценки"))
    reports.register(groups.add_parser("report", help="Итоги и экспорт"))
    return parser.parse_args(argv)
