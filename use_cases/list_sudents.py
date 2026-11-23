from dataclasses import dataclass
from typing import Protocol

from domain.student import Student

from .dto import StudentDTO
from .mappers import to_student_dto


@dataclass(frozen=True)
class ListStudentsRequest:
    pass


@dataclass(frozen=True)
class ListStudentsResponse:
    students: list[StudentDTO]


class IListStudentsRepository(Protocol):
    def get_all(self) -> list[Student]: ...


class IListStudentsRequestHandler(Protocol):
    def handle(self, request: ListStudentsRequest = ListStudentsRequest()) -> ListStudentsResponse: ...


class ListStudentsRequestHandler:
    def __init__(self, repository: IListStudentsRepository):
        self._repository = repository

    def handle(self, request: ListStudentsRequest = ListStudentsRequest()) -> ListStudentsResponse:
        students = self._repository.get_all()
        return ListStudentsResponse(list(map(to_student_dto, students)))
