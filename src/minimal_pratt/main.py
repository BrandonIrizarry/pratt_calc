import enum


class Precedence(enum.IntEnum):
    EOF = enum.auto()
    PARENS = enum.auto()
    PLUS_MINUS = enum.auto()
    TIMES_DIVIDE = enum.auto()
    POWER = enum.auto()
    UNARY = enum.auto()
    FACTORIAL = enum.auto()


type Token = int | str


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


def expression(tokens: list[Token], i: int, level: int) -> tuple[int, int]:
    # NUD
    match tokens[i]:
        case int() as num:
            acc = num
            i += 1

        case "-":
            value, i = expression(tokens, i + 1, Precedence.UNARY)
            acc = -value

        case "(":
            value, i = expression(tokens, i + 1, Precedence.PARENS)
            assert tokens[i] == ")"
            acc = value

            # We don't drive parsing/evaluation with right-paren, so
            # skip it.
            i += 1

        case _ as token:
            raise ValueError(f"nud: {token}")

    while level < precedence(tokens[i]):
        # LED
        match tokens[i]:
            case "+":
                value, i = expression(tokens, i + 1, Precedence.PLUS_MINUS)
                acc += value

            case "-":
                value, i = expression(tokens, i + 1, Precedence.PLUS_MINUS)
                acc -= value

            case "*":
                value, i = expression(tokens, i + 1, Precedence.TIMES_DIVIDE)
                acc *= value

            case "^":
                # Enforce right-association.
                value, i = expression(tokens, i + 1, Precedence.POWER - 1)

                prod = 1

                for _ in range(value):
                    prod *= acc

                acc = prod

            case "!":
                prod = 1

                for j in range(1, acc + 1):
                    prod *= j

                acc = prod
                i += 1

            case _ as token:
                raise ValueError(f"led: {token}")

    return acc, i
