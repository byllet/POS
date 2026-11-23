from dataclasses import dataclass


@dataclass(frozen=True)
class StudentDTO:
    id: int
    name: str


@dataclass(frozen=True)
class CriterionDTO:
    id: int
    name: str
    max_score: int
    weight: int


@dataclass(frozen=True)
class EvaluationDTO:
    criterion_id: int
    score: int


@dataclass(frozen=True)
class StudentResultDTO:
    student: StudentDTO
    percent: float | None
    evaluated_count: int
    criterion_count: int
