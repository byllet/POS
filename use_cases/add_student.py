from dataclasses import dataclass
from typing import Protocol

from domain.student import Student, StudentName

from .dto import StudentDTO
from .mappers import to_student_dto


@dataclass(frozen=True)
class AddStudentRequest:
    name: str


@dataclass(frozen=True)
class AddStudentResponse:
    student: StudentDTO


class IAddStudentRepository(Protocol):
    def create(self, name: StudentName) -> Student:
        """Сохраняет нового студента и возвращает его с назначенным ID."""
        ...


class IAddStudentRequestHandler(Protocol):
    def handle(self, request: AddStudentRequest) -> AddStudentResponse: ...


class AddStudentRequestHandler:
    def __init__(self, repository: IAddStudentRepository):
        self._repository = repository

    def handle(self, request: AddStudentRequest) -> AddStudentResponse:
        student = self._repository.create(StudentName(request.name))
        return AddStudentResponse(to_student_dto(student))
