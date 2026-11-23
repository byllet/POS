from argparse import ArgumentTypeError
from collections.abc import Iterable


def nonempty_text(value: str) -> str:
    text = value.strip()
    if not text:
        raise ArgumentTypeError("Ожидается непустой текст.")
    return text


def format_table(headers: tuple[str, ...], rows: Iterable[tuple], empty: str) -> str:
    data = [tuple(map(str, row)) for row in rows]
    if not data:
        return empty
    widths = [max(map(len, column)) for column in zip(headers, *data)]
    return "\n".join(
        "  ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip()
        for row in [headers, *data]
    )
