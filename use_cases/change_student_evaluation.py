from dataclasses import dataclass
from typing import Protocol

from domain.evaluation import Evaluation
from domain.rubricator import Rubricator
from domain.score import Score
from domain.student import Student

from .dto import EvaluationDTO
from .mappers import to_evaluation_dto


@dataclass(frozen=True)
class ChangeStudentEvaluationRequest:
    student_id: int
    criterion_id: int
    score: int


@dataclass(frozen=True)
class ChangeStudentEvaluationResponse:
    student_id: int
    evaluation: EvaluationDTO


class IChangeStudentEvaluationRepository(Protocol):
    def get(self, student_id: int) -> Student:
        """Возвращает студента с его оценками или сообщает, что ID не найден."""
        ...

    def save(self, student: Student) -> None:
        """Сохраняет текущие оценки студента."""
        ...


class IChangeStudentEvaluationRubricatorRepository(Protocol):
    def load(self) -> Rubricator: ...


class IChangeStudentEvaluationRequestHandler(Protocol):
    def handle(self, request: ChangeStudentEvaluationRequest) -> ChangeStudentEvaluationResponse: ...


class ChangeStudentEvaluationRequestHandler:
    def __init__(
        self,
        repository: IChangeStudentEvaluationRepository,
        rubricator_repository: IChangeStudentEvaluationRubricatorRepository,
    ):
        self._repository = repository
        self._rubricator_repository = rubricator_repository

    def handle(self, request: ChangeStudentEvaluationRequest) -> ChangeStudentEvaluationResponse:
        student = self._repository.get(request.student_id)
        rubricator = self._rubricator_repository.load()
        evaluation = Evaluation(rubricator, request.criterion_id, Score(request.score))
        student.change_evaluation(evaluation)
        self._repository.save(student)
        return ChangeStudentEvaluationResponse(request.student_id, to_evaluation_dto(evaluation))
