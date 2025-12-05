import enum
import re
from collections.abc import Callable, Generator
from functools import wraps
from types import SimpleNamespace
from typing import NamedTuple, final

from more_itertools import peekable


class Type(enum.Enum):
    NUMBER = enum.auto()
    OPERATOR = enum.auto()
    IDENTIFIER = enum.auto()
    EOF = enum.auto()


class Token(NamedTuple):
    tag: Type
    what: str | int | float


@final
class Operator(SimpleNamespace):
    eof = Token(Type.EOF, "eof")
    lparen = Token(Type.OPERATOR, "(")
    rparen = Token(Type.OPERATOR, ")")
    prt = Token(Type.OPERATOR, "print")
    at = Token(Type.OPERATOR, "@")
    plus = Token(Type.OPERATOR, "+")
    minus = Token(Type.OPERATOR, "-")
    times = Token(Type.OPERATOR, "*")
    divide = Token(Type.OPERATOR, "/")
    power = Token(Type.OPERATOR, "^")
    factorial = Token(Type.OPERATOR, "!")
    semicolon = Token(Type.OPERATOR, ";")
    assign = Token(Type.OPERATOR, "<-")
    pi = Token(Type.OPERATOR, "pi")
    sin = Token(Type.OPERATOR, "sin")
    cos = Token(Type.OPERATOR, "cos")
    tan = Token(Type.OPERATOR, "tan")
    sec = Token(Type.OPERATOR, "sec")
    csc = Token(Type.OPERATOR, "csc")
    cot = Token(Type.OPERATOR, "cot")


# See docstring for 'tokenize'.
type Stream = peekable[Token]
type tokenizer = Callable[[str], Generator[Token]]


def _stream(fn: tokenizer) -> Callable[[str], Stream]:
    """Convert the tokenizer's generator into a peekable."""

    @wraps(fn)
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
        ("OPERATOR", r"pi|sin|cos|tan|sec|csc|cot|print|<-|[-+*/!()^;@]"),
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
                yield Token(Type.NUMBER, float(value) if "." in value else int(value))
            case "OPERATOR":
                yield Token(Type.OPERATOR, value)
            case "IDENTIFIER":
                yield Token(Type.IDENTIFIER, value)
            case "SKIP":
                continue
            case "ERROR":
                raise ValueError(f"Fatal: invalid token '{value}'")
            case _:
                raise ValueError(f"Fatal: unknown category '{what}:{value}'")

    yield Token(Type.EOF, "eof")
