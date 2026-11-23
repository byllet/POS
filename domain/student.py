from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from .evaluation import Evaluation


@dataclass(frozen=True)
class StudentName:
    name: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Имя студента не может быть пустым.")

    def __str__(self):
        return self.name


@dataclass
class Student:
    id: int
    name: StudentName = field(compare=False)
    _evaluations: dict[int, Evaluation] = field(default_factory=dict, init=False, compare=False)

    @property
    def evaluations(self) -> Mapping[int, Evaluation]:
        return MappingProxyType(self._evaluations)

    def add_evaluation(self, evaluation: Evaluation) -> None:
        if evaluation.criterion_id in self._evaluations:
            raise ValueError(f"У студента {self.id} уже есть оценка по критерию {evaluation.criterion_id}.")
        self._evaluations[evaluation.criterion_id] = evaluation

    def change_evaluation(self, evaluation: Evaluation) -> None:
        self._require_grade(evaluation.criterion_id)
        self._evaluations[evaluation.criterion_id] = evaluation

    def remove_evaluation(self, criterion_id: int) -> None:
        self._require_grade(criterion_id)
        del self._evaluations[criterion_id]

    def _require_grade(self, criterion_id: int) -> None:
        if criterion_id not in self._evaluations:
            raise ValueError(f"У студента {self.id} ещё нет оценки по критерию {criterion_id}.")
