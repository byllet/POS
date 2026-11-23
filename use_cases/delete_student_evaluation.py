from dataclasses import dataclass
from typing import Protocol

from domain.student import Student


@dataclass(frozen=True)
class DeleteStudentEvaluationRequest:
    student_id: int
    criterion_id: int


@dataclass(frozen=True)
class DeleteStudentEvaluationResponse:
    student_id: int
    criterion_id: int


class IDeleteStudentEvaluationRepository(Protocol):
    def get(self, student_id: int) -> Student:
        """Возвращает студента с его оценками или сообщает, что ID не найден."""
        ...

    def save(self, student: Student) -> None:
        """Сохраняет текущие оценки студента."""
        ...


class IDeleteStudentEvaluationRequestHandler(Protocol):
    def handle(self, request: DeleteStudentEvaluationRequest) -> DeleteStudentEvaluationResponse: ...


class DeleteStudentEvaluationRequestHandler:
    def __init__(self, repository: IDeleteStudentEvaluationRepository):
        self._repository = repository

    def handle(self, request: DeleteStudentEvaluationRequest) -> DeleteStudentEvaluationResponse:
        student = self._repository.get(request.student_id)
        student.remove_evaluation(request.criterion_id)
        self._repository.save(student)
        return DeleteStudentEvaluationResponse(request.student_id, request.criterion_id)
