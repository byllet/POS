from dataclasses import dataclass
from typing import Protocol

from domain.evaluation import Evaluation
from domain.rubricator import Rubricator
from domain.score import Score
from domain.student import Student

from .dto import EvaluationDTO
from .mappers import to_evaluation_dto


@dataclass(frozen=True)
class EvaluateStudentRequest:
    student_id: int
    criterion_id: int
    score: int


@dataclass(frozen=True)
class EvaluateStudentResponse:
    student_id: int
    evaluation: EvaluationDTO


class IEvaluateStudentRepository(Protocol):
    def get(self, student_id: int) -> Student:
        """Возвращает студента с его оценками или сообщает, что ID не найден."""
        ...

    def save(self, student: Student) -> None:
        """Сохраняет текущие оценки студента."""
        ...


class IEvaluateStudentRubricatorRepository(Protocol):
    def load(self) -> Rubricator: ...


class IEvaluateStudentRequestHandler(Protocol):
    def handle(self, request: EvaluateStudentRequest) -> EvaluateStudentResponse: ...


class EvaluateStudentRequestHandler:
    def __init__(
        self,
        repository: IEvaluateStudentRepository,
        rubricator_repository: IEvaluateStudentRubricatorRepository,
    ):
        self._repository = repository
        self._rubricator_repository = rubricator_repository

    def handle(self, request: EvaluateStudentRequest) -> EvaluateStudentResponse:
        student = self._repository.get(request.student_id)
        rubricator = self._rubricator_repository.load()
        evaluation = Evaluation(rubricator, request.criterion_id, Score(request.score))
        student.add_evaluation(evaluation)
        self._repository.save(student)
        return EvaluateStudentResponse(request.student_id, to_evaluation_dto(evaluation))
