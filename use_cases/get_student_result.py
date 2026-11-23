from dataclasses import dataclass
from typing import Protocol

from domain.final_score_service import FinalScoreService
from domain.rubricator import Rubricator
from domain.student import Student

from .dto import StudentResultDTO
from .mappers import to_student_result_dto


@dataclass(frozen=True)
class GetStudentResultRequest:
    student_id: int


@dataclass(frozen=True)
class GetStudentResultResponse:
    result: StudentResultDTO


class IGetStudentResultRepository(Protocol):
    def get_with_rubricator(self, student_id: int) -> tuple[Student, Rubricator]:
        """Возвращает студента и рубрикатор из одного снимка данных."""
        ...


class IGetStudentResultRequestHandler(Protocol):
    def handle(self, request: GetStudentResultRequest) -> GetStudentResultResponse: ...


class GetStudentResultRequestHandler:
    def __init__(self, repository: IGetStudentResultRepository, calculator: FinalScoreService):
        self._repository = repository
        self._calculator = calculator

    def handle(self, request: GetStudentResultRequest) -> GetStudentResultResponse:
        student, rubricator = self._repository.get_with_rubricator(request.student_id)
        result = self._calculator.calculate(student, rubricator)
        return GetStudentResultResponse(to_student_result_dto(student, result))
