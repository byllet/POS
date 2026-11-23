from argparse import ArgumentParser
from dataclasses import dataclass

from use_cases.change_student_evaluation import (
    ChangeStudentEvaluationRequest,
    IChangeStudentEvaluationRequestHandler,
)
from use_cases.delete_student_evaluation import (
    DeleteStudentEvaluationRequest,
    IDeleteStudentEvaluationRequestHandler,
)
from use_cases.evaluate_sudent import EvaluateStudentRequest, IEvaluateStudentRequestHandler
from use_cases.list_criterions import IListCriteriaRequestHandler, ListCriteriaRequest
from use_cases.list_student_evaluations import (
    IListStudentEvaluationsRequestHandler,
    ListStudentEvaluationsRequest,
)

from .console import format_table


@dataclass
class EvaluationsCommands:
    evaluate_student: IEvaluateStudentRequestHandler
    change_evaluation: IChangeStudentEvaluationRequestHandler
    delete_evaluation: IDeleteStudentEvaluationRequestHandler
    list_evaluations: IListStudentEvaluationsRequestHandler

    def assign(self, student_id: int, criterion_id: int, score: int) -> str:
        request = EvaluateStudentRequest(
            student_id=student_id,
            criterion_id=criterion_id,
            score=score,
        )
        response = self.evaluate_student.handle(request)
        grade = response.evaluation
        return f"Студент {response.student_id}, критерий {grade.criterion_id}: выставлено {grade.score} б."

    def change(self, student_id: int, criterion_id: int, score: int) -> str:
        request = ChangeStudentEvaluationRequest(
            student_id=student_id,
            criterion_id=criterion_id,
            score=score,
        )
        response = self.change_evaluation.handle(request)
        grade = response.evaluation
        return f"Студент {response.student_id}, критерий {grade.criterion_id}: теперь {grade.score} б."

    def delete(self, student_id: int, criterion_id: int) -> str:
        request = DeleteStudentEvaluationRequest(
            student_id=student_id,
            criterion_id=criterion_id,
        )
        response = self.delete_evaluation.handle(request)
        return f"Оценка студента {response.student_id} по критерию {response.criterion_id} отменена."

    def show(self, student_id: int, list_criteria: IListCriteriaRequestHandler) -> str:
        request = ListStudentEvaluationsRequest(student_id=student_id)
        response = self.list_evaluations.handle(request)
        criteria = {c.id: c for c in list_criteria.handle(ListCriteriaRequest()).criteria}
        rows = []
        for grade in response.evaluations:
            criterion = criteria[grade.criterion_id]
            rows.append((criterion.id, criterion.name, f"{grade.score}/{criterion.max_score}"))
        table = format_table(
            ("ID критерия", "Название критерия", "Балл/макс."),
            rows,
            "У студента пока нет оценок.",
        )
        return f"Оценки студента {response.student_id}\n{table}"


def register(parser: ArgumentParser) -> None:
    commands = parser.add_subparsers(required=True)
    add = commands.add_parser("add", help="Выставить оценку")
    change = commands.add_parser("change", help="Исправить оценку")
    delete = commands.add_parser("delete", help="Отменить оценку")
    show = commands.add_parser("list", help="Показать оценки студента")
    for command in (add, change, delete, show):
        command.add_argument("student_id", type=int, help="ID студента")
    for command in (add, change, delete):
        command.add_argument("criterion_id", type=int, help="ID критерия")
    for command in (add, change):
        command.add_argument("score", type=int, help="Балл")
    add.set_defaults(action=lambda app, a: app.evaluations.assign(a.student_id, a.criterion_id, a.score))
    change.set_defaults(action=lambda app, a: app.evaluations.change(a.student_id, a.criterion_id, a.score))
    delete.set_defaults(action=lambda app, a: app.evaluations.delete(a.student_id, a.criterion_id))
    show.set_defaults(action=lambda app, a: app.evaluations.show(a.student_id, app.criteria.list_criteria))
