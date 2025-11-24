from __future__ import annotations

import enum
import math
from collections import UserDict
from typing import final, override

from pratt_calc.tokenizer import Stream, Token


class Precedence(enum.IntEnum):
    """Establish the various precedence levels.

    Rather than being associated directly with a token, a given
    precedence level gets passed in as an argument whenever a given
    token is dispatched.

    For example, subtraction is dispatched using PLUS_MINUS, while
    negation is dispatched using UNARY, even though both are
    associated with the '-' token.

    """

    NONE = enum.auto()
    SEMICOLON = enum.auto()
    PLUS_MINUS = enum.auto()
    TIMES_DIVIDE = enum.auto()
    POWER = enum.auto()
    UNARY = enum.auto()
    FACTORIAL = enum.auto()


class LedPrecedenceTable(UserDict[Token, Precedence]):
    """Specify precedence of LED-position tokens.

    Not all LED-position tokens are actual LEDs, since, for example,
    'eof' serves no other function than to report a precedence level
    of NONE. In most cases though, a LED-position token and a LED
    token are the same thing.

    """

    @override
    def __getitem__(self, token: Token):
        try:
            return self.data[token]
        except KeyError:
            raise ValueError(f"Invalid token: '{token}'")


@final
class Parser:
    """Pratt-parse a list of tokens.

    The tokens are converted internally into a more_itertools
    'peekable' object, basically a generator.

    This class enables us to encapsulate the stream as global state
    usable across recursive calls to 'expression', freeing us from
    having to return the stream (or any kind of placeholder state, for
    that matter) after each such recursive call.

    """

    led_precedence = LedPrecedenceTable(
        {
            "eof": Precedence.NONE,
            ")": Precedence.NONE,
            "+": Precedence.PLUS_MINUS,
            "-": Precedence.PLUS_MINUS,
            "*": Precedence.TIMES_DIVIDE,
            "/": Precedence.TIMES_DIVIDE,
            "^": Precedence.POWER,
            "!": Precedence.FACTORIAL,
            ";": Precedence.SEMICOLON,
        }
    )

    def __init__(self, stream: Stream):
        self.stream = stream

    def expression(self, level: int = Precedence.NONE) -> int | float:
        """Pratt-parse an arithmetic expression, evaluating it."""

        # NUD
        current = next(self.stream)

        match current:
            case int() | float() as num:
                acc = num

            case "pi":
                acc = math.pi

            case "sin":
                acc = math.sin(self.expression(Precedence.UNARY))

            case "cos":
                acc = math.cos(self.expression(Precedence.UNARY))

            case "tan":
                acc = math.tan(self.expression(Precedence.UNARY))

            case "sec":
                acc = 1 / math.cos(self.expression(Precedence.UNARY))

            case "csc":
                acc = 1 / math.sin(self.expression(Precedence.UNARY))

            case "cot":
                acc = 1 / math.tan(self.expression(Precedence.UNARY))

            case "-":
                acc = -self.expression(Precedence.UNARY)

            case "(":
                acc = self.expression(Precedence.NONE)

                # We don't drive parsing/evaluation with right-paren,
                # so we skip it as we read it.
                assert next(self.stream) == ")"

            case "print":
                acc = self.expression(Precedence.UNARY)
                print(acc)

            case _ as token:
                raise ValueError(f"Invalid nud: {token}")

        while level < self.led_precedence[self.stream.peek()]:
            current = next(self.stream)

            # LED
            match current:
                case "+":
                    acc += self.expression(Precedence.PLUS_MINUS)

                case "-":
                    acc -= self.expression(Precedence.PLUS_MINUS)

                case "*":
                    acc *= self.expression(Precedence.TIMES_DIVIDE)

                case "/":
                    acc /= self.expression(Precedence.TIMES_DIVIDE)

                case "^":
                    # Enforce right-association by subtracting 1 from
                    # the precedence argument.
                    acc = math.pow(acc, self.expression(Precedence.POWER - 1))

                case "!":
                    # Compute factorial by hand.
                    #
                    # If ACC is a float, truncate it first to an int.
                    prod = 1

                    acc = int(acc)

                    for j in range(1, acc + 1):
                        prod *= j

                    acc = prod

                case ";":
                    # Discard the left-hand side, keeping only the
                    # right-hand side. This will hopefully be useful
                    # for side-effects later.
                    acc = self.expression(Precedence.SEMICOLON)

                case _ as token:
                    raise ValueError(f"Invalid led: {token}")

        return acc
