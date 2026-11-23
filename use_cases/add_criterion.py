from dataclasses import dataclass
from typing import Protocol

from domain.criterion import Criterion, CriterionName, Weight
from domain.score import Score

from .dto import CriterionDTO
from .mappers import to_criterion_dto


@dataclass(frozen=True)
class AddCriterionRequest:
    name: str
    max_score: int
    weight: int


@dataclass(frozen=True)
class AddCriterionResponse:
    criterion: CriterionDTO


class IAddCriterionRepository(Protocol):
    def add_criterion(self, name: CriterionName, max_score: Score, weight: Weight) -> Criterion:
        """Создаёт критерий с новым ID и атомарно добавляет его в рубрикатор."""
        ...


class IAddCriterionRequestHandler(Protocol):
    def handle(self, request: AddCriterionRequest) -> AddCriterionResponse: ...


class AddCriterionRequestHandler:
    def __init__(self, repository: IAddCriterionRepository):
        self._repository = repository

    def handle(self, request: AddCriterionRequest) -> AddCriterionResponse:
        criterion = self._repository.add_criterion(CriterionName(request.name), Score(request.max_score), Weight(request.weight))
        return AddCriterionResponse(to_criterion_dto(criterion))
