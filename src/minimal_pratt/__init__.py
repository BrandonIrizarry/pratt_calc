import sys
from collections.abc import Callable

from minimal_pratt.parser import Parser
from minimal_pratt.tokenizer import tokenize


def _display(fn: Callable[[], int]):
    def wrapper():
        value = fn()

        print(value)

    return wrapper


@_display
def main() -> int:
    raw_expression = sys.argv[1]

    stream = tokenize(raw_expression)
    parser = Parser(stream)

    value = parser.expression()

    return value
