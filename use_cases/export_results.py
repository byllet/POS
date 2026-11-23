from dataclasses import dataclass
from typing import Protocol

from domain.final_score_service import FinalScoreService
from domain.rubricator import Rubricator
from domain.student import Student

from .dto import StudentResultDTO
from .mappers import to_student_result_dto


@dataclass(frozen=True)
class ExportResultsRequest:
    destination: str


@dataclass(frozen=True)
class ExportResultsResponse:
    destination: str
    student_count: int


class IExportResultsRepository(Protocol):
    def get_all_with_rubricator(self) -> tuple[list[Student], Rubricator]:
        """Возвращает студентов и общий рубрикатор из одного снимка данных."""
        ...


class IResultsWriter(Protocol):
    def write(self, destination: str, rows: list[StudentResultDTO]) -> None:
        """Записывает всю ведомость или сообщает об ошибке."""
        ...


class IExportResultsRequestHandler(Protocol):
    def handle(self, request: ExportResultsRequest) -> ExportResultsResponse: ...


class ExportResultsRequestHandler:
    def __init__(
        self,
        repository: IExportResultsRepository,
        calculator: FinalScoreService,
        writer: IResultsWriter,
    ):
        self._repository = repository
        self._calculator = calculator
        self._writer = writer

    def handle(self, request: ExportResultsRequest) -> ExportResultsResponse:
        students, rubricator = self._repository.get_all_with_rubricator()
        rows = [
            to_student_result_dto(student, self._calculator.calculate(student, rubricator))
            for student in students
        ]
        self._writer.write(request.destination, rows)
        return ExportResultsResponse(request.destination, len(rows))
