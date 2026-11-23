from dataclasses import dataclass
from typing import Protocol

from domain.rubricator import Rubricator

from .dto import CriterionDTO
from .mappers import to_criterion_dto


@dataclass(frozen=True)
class ListCriteriaRequest:
    pass


@dataclass(frozen=True)
class ListCriteriaResponse:
    criteria: list[CriterionDTO]


class IListCriteriaRepository(Protocol):
    def load(self) -> Rubricator: ...


class IListCriteriaRequestHandler(Protocol):
    def handle(self, request: ListCriteriaRequest) -> ListCriteriaResponse: ...


class ListCriteriaRequestHandler:
    def __init__(self, repository: IListCriteriaRepository):
        self._repository = repository

    def handle(self, request: ListCriteriaRequest) -> ListCriteriaResponse:
        rubricator = self._repository.load()
        return ListCriteriaResponse(list(map(to_criterion_dto, rubricator)))
