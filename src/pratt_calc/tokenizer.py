import re
from collections.abc import Callable, Generator
from typing import Literal

from more_itertools import peekable

# See docstring for 'tokenize'.
type Token = int | float | str | tuple[Literal["IDENTIFIER"], str]
type Stream = peekable[Token]
type tokenizer = Callable[[str], Generator[Token]]


def _stream(fn: tokenizer) -> Callable[[str], Stream]:
    """Convert the tokenizer's generator into a peekable."""

    def wrapper(raw_expression: str) -> Stream:
        gen = fn(raw_expression)

        return peekable(gen)

    return wrapper


@_stream
def tokenize(raw_expression: str) -> Generator[Token]:
    """Tokenize RAW_EXPRESSION.

    Integers are yielded as Python ints; everything else is yielded as
    its original string representation.

    Inspiration taken from

    https://docs.python.org/3/library/re.html

    """

    token_specification = [
        ("NUMBER", r"\d+(\.\d*)?"),
        ("BUILTIN", r"pi|sin|cos|tan|sec|csc|cot|print|<-"),
        ("TOKEN", r"[-+*/!()^;@]"),
        ("IDENTIFIER", r"[a-zA-Z_][\w]*"),
        ("SKIP", r"[ \t]+"),
        ("ERROR", r"."),
    ]

    token_regex = "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification)
    pattern = re.compile(token_regex)

    for mo in re.finditer(pattern, raw_expression):
        what = mo.lastgroup
        value = mo.group()

        match what:
            case "NUMBER":
                yield float(value) if "." in value else int(value)
            case "BUILTIN" | "TOKEN":
                yield value
            case "IDENTIFIER":
                yield ("IDENTIFIER", value)
            case "SKIP":
                continue
            case "ERROR":
                raise ValueError(f"Fatal: invalid token '{value}'")
            case _:
                raise ValueError(f"Fatal: unknown category '{what}:{value}'")

    yield "eof"
