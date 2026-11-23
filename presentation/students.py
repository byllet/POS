from argparse import ArgumentParser
from dataclasses import dataclass

from use_cases.add_student import AddStudentRequest, IAddStudentRequestHandler
from use_cases.list_sudents import IListStudentsRequestHandler, ListStudentsRequest

from .console import nonempty_text, format_table


@dataclass
class StudentsCommands:
    add_student: IAddStudentRequestHandler
    list_students: IListStudentsRequestHandler

    def add(self, name: str) -> str:
        request = AddStudentRequest(name=name)
        student = self.add_student.handle(request).student
        return f"Студент добавлен: {student.name} (ID {student.id})."

    def show(self) -> str:
        students = self.list_students.handle(ListStudentsRequest()).students
        return format_table(("ID", "Студент"), ((s.id, s.name) for s in students), "Список студентов пуст.")


def register(parser: ArgumentParser) -> None:
    commands = parser.add_subparsers(required=True)
    add = commands.add_parser("add", help="Зарегистрировать студента")
    add.add_argument("name", type=nonempty_text, help="Имя студента")
    add.set_defaults(action=lambda app, args: app.students.add(args.name))
    commands.add_parser("list", help="Список студентов").set_defaults(action=lambda app, args: app.students.show())
