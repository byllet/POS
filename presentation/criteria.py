from argparse import ArgumentParser
from dataclasses import dataclass

from use_cases.add_criterion import AddCriterionRequest, IAddCriterionRequestHandler
from use_cases.list_criterions import IListCriteriaRequestHandler, ListCriteriaRequest

from .console import nonempty_text, format_table


@dataclass
class CriteriaCommands:
    add_criterion: IAddCriterionRequestHandler
    list_criteria: IListCriteriaRequestHandler

    def add(self, name: str, max_score: int, weight: int) -> str:
        request = AddCriterionRequest(
            name=name,
            max_score=max_score,
            weight=weight,
        )
        criterion = self.add_criterion.handle(request).criterion
        return f"Критерий добавлен: {criterion.name} (ID {criterion.id})."

    def show(self) -> str:
        criteria = self.list_criteria.handle(ListCriteriaRequest()).criteria
        return format_table(
            ("ID", "Критерий", "Максимум", "Вес"),
            ((c.id, c.name, c.max_score, c.weight) for c in criteria),
            "Рубрикатор пуст.",
        )


def register(parser: ArgumentParser) -> None:
    commands = parser.add_subparsers(required=True)
    add = commands.add_parser("add", help="Добавить критерий")
    add.add_argument("name", type=nonempty_text, help="Название критерия")
    add.add_argument("max_score", type=int, help="Максимальный балл")
    add.add_argument("weight", type=int, help="Относительный вес")
    add.set_defaults(action=lambda app, args: app.criteria.add(args.name, args.max_score, args.weight))
    commands.add_parser("list", help="Список критериев").set_defaults(action=lambda app, args: app.criteria.show())
