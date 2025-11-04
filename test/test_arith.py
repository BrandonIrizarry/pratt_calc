import pytest

from minimal_pratt.main import parse

examples = [
    ("3 * (2 + -4) ^ 4", 48),
    ("3", 3),
]


@pytest.mark.parametrize("expr, value", examples)
def test_examples(expr: str, value: int):
    result = parse(expr)

    assert result == value
