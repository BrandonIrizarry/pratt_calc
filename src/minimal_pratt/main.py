from __future__ import annotations

import enum

from more_itertools import peekable


class Precedence(enum.IntEnum):
    EOF = enum.auto()
    PARENS = enum.auto()
    PLUS_MINUS = enum.auto()
    TIMES_DIVIDE = enum.auto()
    POWER = enum.auto()
    UNARY = enum.auto()
    FACTORIAL = enum.auto()


# Since this definition has been known to change periodically, it's
# better to keep a fixed alias for this.
type Token = int | str

# Mostly to keep line lengths shorter.
type Stream = peekable[Token]


def precedence(token: Token) -> Precedence:
    # It looks like only potential led-tokens need to appear in this
    # match statement ("potential", meaning that they get checked in
    # the while-loop condition.)
    match token:
        case ")":
            return Precedence.PARENS

        case "+":
            return Precedence.PLUS_MINUS

        case "-":
            return Precedence.PLUS_MINUS

        case "*":
            return Precedence.TIMES_DIVIDE

        case "^":
            return Precedence.POWER

        case "!":
            return Precedence.FACTORIAL

        case "eof":
            return Precedence.EOF

        case _:
            raise ValueError(f"Invalid token: '{token}'")


def expression(stream: Stream, level: int) -> tuple[int, Stream]:
    # NUD
    current = stream.peek()
    _ = next(stream)

    match current:
        case int() as num:
            acc = num

        case "-":
            value, stream = expression(stream, Precedence.UNARY)
            acc = -value

        case "(":
            value, stream = expression(stream, Precedence.PARENS)
            assert stream.peek() == ")"
            acc = value

            # We don't drive parsing/evaluation with right-paren, so
            # skip it.
            _ = next(stream)

        case _ as token:
            raise ValueError(f"nud: {token}")

    while level < precedence(stream.peek()):
        current = stream.peek()
        _ = next(stream)

        # LED
        match current:
            case "+":
                value, stream = expression(stream, Precedence.PLUS_MINUS)
                acc += value

            case "-":
                value, stream = expression(stream, Precedence.PLUS_MINUS)
                acc -= value

            case "*":
                value, stream = expression(stream, Precedence.TIMES_DIVIDE)
                acc *= value

            case "^":
                # Enforce right-association.
                value, stream = expression(stream, Precedence.POWER - 1)

                prod = 1

                for _ in range(value):
                    prod *= acc

                acc = prod

            case "!":
                prod = 1

                for j in range(1, acc + 1):
                    prod *= j

                acc = prod

            case _ as token:
                raise ValueError(f"led: {token}")

    return acc, stream


def expression_top(tokens: list[Token]) -> int:
    stream = peekable(tokens)

    value, _ = expression(stream, Precedence.EOF)

    return value
