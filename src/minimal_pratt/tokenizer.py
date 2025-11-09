import re
from collections.abc import Callable, Generator

from more_itertools import peekable

# Since this definition has been known to change periodically, it's
# better to keep a fixed alias for this.
type Token = int | str

type Stream = peekable[Token]
type tokenizer = Callable[[str], Generator[Token]]


def _stream(fn: tokenizer) -> Callable[[str], Stream]:
    def wrapper(raw_expression: str) -> Stream:
        gen = fn(raw_expression)

        return peekable(gen)

    return wrapper


@_stream
def tokenize(raw_expression: str) -> Generator[Token]:
    pattern = re.compile(r"\s*((\d+)|(.))")

    for mo in re.finditer(pattern, raw_expression):
        token = mo.group(1)

        if token.isdigit():
            yield int(token)
        else:
            yield token

    yield "eof"
