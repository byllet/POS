from argparse import ArgumentParser
from dataclasses import dataclass

from use_cases.export_results import ExportResultsRequest, IExportResultsRequestHandler
from use_cases.get_student_result import GetStudentResultRequest, IGetStudentResultRequestHandler

from .console import nonempty_text


@dataclass
class ReportsCommands:
    get_result: IGetStudentResultRequestHandler
    export_results: IExportResultsRequestHandler

    def show(self, student_id: int) -> str:
        request = GetStudentResultRequest(student_id=student_id)
        result = self.get_result.handle(request).result
        percent = "—" if result.percent is None else f"{result.percent:.2f}%"
        return (
            f"{result.student.name} (ID {result.student.id}) · итог {percent}\n"
            f"Оценено критериев: {result.evaluated_count} из {result.criterion_count}."
        )

    def export(self, destination: str) -> str:
        request = ExportResultsRequest(destination=destination)
        response = self.export_results.handle(request)
        return f"Ведомость сохранена: {response.destination}. Студентов: {response.student_count}."


def register(parser: ArgumentParser) -> None:
    commands = parser.add_subparsers(required=True)
    result = commands.add_parser("result", help="Рассчитать итог студента")
    result.add_argument("student_id", type=int, help="ID студента")
    result.set_defaults(action=lambda app, args: app.reports.show(args.student_id))
    export = commands.add_parser("export", help="Выгрузить ведомость в CSV")
    export.add_argument("destination", type=nonempty_text, help="Путь к новому файлу CSV")
    export.set_defaults(action=lambda app, args: app.reports.export(args.destination))
