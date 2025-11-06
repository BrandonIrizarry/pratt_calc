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


class Parser:
    def __init__(self, tokens: list[Token]):
        self.stream: peekable[Token] = peekable(tokens)

    def expression(self, level: int = Precedence.EOF) -> int:
        # NUD
        current = next(self.stream)

        match current:
            case int() as num:
                acc = num

            case "-":
                acc = -self.expression(Precedence.UNARY)

            case "(":
                acc = self.expression(Precedence.PARENS)

                # We don't drive parsing/evaluation with right-paren,
                # so we skip it as we read it.
                assert next(self.stream) == ")"

            case _ as token:
                raise ValueError(f"nud: {token}")

        while level < precedence(self.stream.peek()):
            current = next(self.stream)

            # LED
            match current:
                case "+":
                    acc += self.expression(Precedence.PLUS_MINUS)

                case "-":
                    acc -= self.expression(Precedence.PLUS_MINUS)

                case "*":
                    acc *= self.expression(Precedence.TIMES_DIVIDE)

                case "^":
                    # Enforce right-association.
                    value = self.expression(Precedence.POWER - 1)

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

        return acc
