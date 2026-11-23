from dataclasses import dataclass

from .rubricator import Rubricator
from .score import Score


@dataclass(frozen=True, init=False)
class Evaluation:
    criterion_id: int
    score: Score

    def __init__(self, rubricator: Rubricator, criterion_id: int, score: Score):
        rubricator.require(criterion_id).check(score)
        object.__setattr__(self, "criterion_id", criterion_id)
        object.__setattr__(self, "score", score)
