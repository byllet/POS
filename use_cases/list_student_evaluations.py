from dataclasses import dataclass
from typing import Protocol

from domain.student import Student

from .dto import EvaluationDTO
from .mappers import to_evaluation_dto


@dataclass(frozen=True)
class ListStudentEvaluationsRequest:
    student_id: int


@dataclass(frozen=True)
class ListStudentEvaluationsResponse:
    student_id: int
    evaluations: list[EvaluationDTO]


class IListStudentEvaluationsRepository(Protocol):
    def get(self, student_id: int) -> Student:
        """Возвращает студента с его оценками или сообщает, что ID не найден."""
        ...


class IListStudentEvaluationsRequestHandler(Protocol):
    def handle(self, request: ListStudentEvaluationsRequest) -> ListStudentEvaluationsResponse: ...


class ListStudentEvaluationsRequestHandler:
    def __init__(self, repository: IListStudentEvaluationsRepository):
        self._repository = repository

    def handle(self, request: ListStudentEvaluationsRequest) -> ListStudentEvaluationsResponse:
        student = self._repository.get(request.student_id)
        evaluations = list(map(to_evaluation_dto, student.evaluations.values()))
        return ListStudentEvaluationsResponse(student.id, evaluations)
