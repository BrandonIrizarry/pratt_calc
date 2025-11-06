import enum


class Precedence(enum.IntEnum):
    EOF = enum.auto()
    LITERAL = enum.auto()
    PLUS_MINUS = enum.auto()
    TIMES_DIVIDE = enum.auto()
    POWER = enum.auto()
    UNARY = enum.auto()


type Token = int | str


def precedence(token: Token) -> Precedence:
    # It looks like only potential led-tokens need to appear in this
    # match statement ("potential", meaning that they get checked in
    # the 'expression' while-loop condition.)
    match token:
        case ")":
            return Precedence.LITERAL

        case "+":
            return Precedence.PLUS_MINUS

        case "*":
            return Precedence.TIMES_DIVIDE

        case "^":
            return Precedence.POWER

        case "eof":
            return Precedence.EOF

        case _:
            raise ValueError(f"Invalid token: '{token}'")


def expression(tokens: list[Token], i: int, acc: int, level: int) -> tuple[int, int]:
    # NUD
    match tokens[i]:
        case int() as num:
            acc = num
            i += 1

        case "-":
            value, i = expression(tokens, i + 1, acc, Precedence.UNARY)
            acc = -value

        case "(":
            value, i = expression(tokens, i + 1, acc, Precedence.LITERAL)
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
                value, i = expression(tokens, i + 1, acc, Precedence.PLUS_MINUS)
                acc += value

            case "*":
                value, i = expression(tokens, i + 1, acc, Precedence.TIMES_DIVIDE)
                acc *= value

            case "^":
                # Enforce right-association.
                value, i = expression(tokens, i + 1, acc, Precedence.POWER - 1)

                prod = 1

                for _ in range(value):
                    prod *= acc

                acc = prod

            case _ as token:
                raise ValueError(f"led: {token}")

    return acc, i


t2: list[Token] = [2, "^", 3, "^", 2, "eof"]

value = expression(t2, 0, 0, Precedence.EOF)

print(value)
