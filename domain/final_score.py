from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class FinalScore:
    percent: Fraction | None
    evaluated_count: int
    criterion_count: int
