import csv
import sys
from collections.abc import Sequence

from container import Container
from infrastructure.csv_store import CsvStore
from presentation.cli import parse_args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        store = CsvStore(args.data_dir)
        with store.command():
            app = Container(store=store).app()
            message = app.execute(args)
    except (ValueError, OSError, csv.Error) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
