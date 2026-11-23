from domain.criterion import Criterion, CriterionName, Weight
from domain.rubricator import Rubricator
from domain.score import Score

from .csv_store import CsvStore


class CsvRubricatorRepository:
    def __init__(self, store: CsvStore):
        self._criteria = store.criteria

    def add_criterion(self, name: CriterionName, max_score: Score, weight: Weight) -> Criterion:
        rubricator = self.load()
        new_id = 1 + max((c.id for c in rubricator), default=0)
        criterion = Criterion(new_id, name, max_score, weight)
        rubricator.add(criterion)
        self._criteria.write(
            (c.id, str(c.name), int(c.max_score), c.weight.value) for c in rubricator
        )
        return criterion

    def load(self) -> Rubricator:
        rubricator = Rubricator()
        for key, name, maximum, weight in self._criteria.read():
            rubricator.add(Criterion(int(key), CriterionName(name), Score(int(maximum)), Weight(int(weight))))
        return rubricator
