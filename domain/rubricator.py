from .criterion import Criterion


class Rubricator:
    def __init__(self):
        self._index: dict[int, Criterion] = {}

    def require(self, criterion_id: int) -> Criterion:
        if criterion_id not in self._index:
            raise ValueError(f"В рубрикаторе нет критерия с ID {criterion_id}.")

        return self._index[criterion_id]

    def add(self, criterion: Criterion) -> None:
        if criterion.id in self._index:
            raise ValueError(f"Критерий с ID {criterion.id} уже есть в рубрикаторе.")
        
        self._index[criterion.id] = criterion

    def __iter__(self):
        return iter(self._index.values())
