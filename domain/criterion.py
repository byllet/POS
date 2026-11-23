from dataclasses import dataclass, field

from .score import Score


@dataclass(frozen=True)
class CriterionName:
    name: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Название критерия не может быть пустым.")

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Weight:
    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("Вес должен быть целым числом")

        if self.value <= 0:
            raise ValueError("Вес должен быть положительным")


@dataclass(frozen=True)
class Criterion:
    id: int
    name: CriterionName = field(compare=False)
    max_score: Score = field(compare=False)
    weight: Weight = field(compare=False)

    def __post_init__(self) -> None:
        if self.max_score.value == 0:
            raise ValueError("Максимальный балл критерия должен быть положительным.")

    def check(self, score: Score) -> None:
        if score > self.max_score:
            raise ValueError(f"Критерий «{self.name}» допускает от 0 до {self.max_score.value} баллов.")
