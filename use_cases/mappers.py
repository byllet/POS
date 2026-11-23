from domain.criterion import Criterion
from domain.evaluation import Evaluation
from domain.final_score import FinalScore
from domain.student import Student

from .dto import CriterionDTO, EvaluationDTO, StudentDTO, StudentResultDTO


def to_student_dto(student: Student) -> StudentDTO:
    return StudentDTO(id=student.id, name=str(student.name))


def to_criterion_dto(criterion: Criterion) -> CriterionDTO:
    return CriterionDTO(criterion.id, str(criterion.name), int(criterion.max_score), criterion.weight.value)


def to_evaluation_dto(evaluation: Evaluation) -> EvaluationDTO:
    return EvaluationDTO(evaluation.criterion_id, int(evaluation.score))


def to_student_result_dto(student: Student, result: FinalScore) -> StudentResultDTO:
    percent = None if result.percent is None else float(round(result.percent, 2))
    return StudentResultDTO(to_student_dto(student), percent, result.evaluated_count, result.criterion_count)
