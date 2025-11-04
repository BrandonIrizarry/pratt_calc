import re
from collections.abc import Callable, Generator
from typing import TypedDict

token_pat = re.compile(r"\s*(?:(\d+)|(.))")


class Action(TypedDict):
    """A Pratt-parser augmented token.

    NUD (null denotation) refers to a token's action as a prefix.
    LED (left denotation) refers to a token's action as a suffix.

    """

    nud: Callable[[], float]
    led: Callable[[float], float]


table: dict[str, Action] = {
    "+": {
        "nud": lambda: 0,
        "led": lambda left: left + 0,
    },
    "-": {
        "nud": lambda: 0,
        "led": lambda left: left - 0,
    },
    "*": {
        "nud": lambda: 0,
        "led": lambda left: left * 1,
    },
    "//": {
        "nud": lambda: 0,
        "led": lambda left: left / 1,
    },
    "^": {
        "nud": lambda: 0,
        "led": lambda left: left**1,
    },
    "(": {
        "nud": lambda: 0,
        "led": lambda left: 0,
    },
    ")": {
        "nud": lambda: 0,
        "led": lambda left: 0,
    },
}


def tokenize(program: str) -> Generator[Action]:
    for number, operator in token_pat.findall(program):
        if number:
            yield {"nud": lambda: float(number), "led": lambda left: 0}

        elif operator in table:
            yield table[operator]

        else:
            raise SyntaxError(f"Unknown: {operator}")

    # The end token.
    yield {"nud": lambda: 0, "led": lambda left: 0}


def match(tok=None):
    global token

    if tok and tok != type(token):
        raise SyntaxError("Expected %s" % tok)

    token = next(gen)


def parse(program):
    global token, gen
    gen = tokenize(program)
    token = next(gen)

    return expression()


def expression(rbp=0):
    global token
    t = token
    token = next(gen)
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next(gen)
        left = t.led(left)
    return left


class literal_token:
    def __init__(self, value):
        self.value = int(value)

    def nud(self):
        return self.value


class operator_add_token:
    lbp = 10

    def nud(self):
        return expression(100)

    def led(self, left):
        right = expression(10)
        return left + right


class operator_sub_token:
    lbp = 10

    def nud(self):
        return -expression(100)

    def led(self, left):
        return left - expression(10)


class operator_mul_token:
    lbp = 20

    def led(self, left):
        return left * expression(20)


class operator_div_token:
    lbp = 20

    def led(self, left):
        return left / expression(20)


class operator_pow_token:
    lbp = 30

    def led(self, left):
        return left ** expression(30 - 1)


class operator_lparen_token:
    lbp = 0

    def nud(self):
        expr = expression()
        match(operator_rparen_token)
        return expr


class operator_rparen_token:
    lbp = 0


class end_token:
    lbp = 0
