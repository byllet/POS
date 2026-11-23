from fractions import Fraction

from .final_score import FinalScore
from .rubricator import Rubricator
from .student import Student


class FinalScoreService:
    def calculate(self, student: Student, rubricator: Rubricator) -> FinalScore:
        weighted_sum = Fraction()
        total_weight = 0
        criterion_count = 0
        evaluations = student.evaluations

        for criterion in rubricator:
            criterion_count += 1
            evaluation = evaluations.get(criterion.id)
            if evaluation is not None:
                total_weight += criterion.weight.value
                fraction = Fraction(evaluation.score.value, criterion.max_score.value)
                weighted_sum += fraction * criterion.weight.value

        percent = 100 * weighted_sum / total_weight if total_weight else None
        return FinalScore(percent, len(evaluations), criterion_count)
