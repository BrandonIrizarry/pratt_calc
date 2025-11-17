import math

import pytest

from pratt_calc import main

# The original set of examples, before floats were introduced.
examples = [
    ("3", 3),
    ("3 + 4", 7),
    ("3 + 4 * 5 + 6", 29),
    ("3 + -4 * 5 + 6", -11),
    ("-3 + 4", 1),
    ("(3 + -4) * 5 + 6", 1),
    ("2^3^2", 512),
    ("2^3*3", 24),
    ("2^(3*2)", 64),
    ("2-3*2", -4),
    ("-(3 + 1)!", -24),
    ("(3)", 3),
    ("- 3", -3),
]


@pytest.mark.parametrize("raw_expression, value", examples)
def test_examples(raw_expression: str, value: int):
    result = main(raw_expression)

    assert result == value


float_examples = [
    ("3.3", 3.3),
    ("3.3+4.4", 7.7),
    ("5/2", 2.5),
    ("1+5/2", 3.5),
    ("100*(100 + 1)/2", 5050),
    ("pi", math.pi),
    ("sin (pi/2)", 1),
    ("sin(pi/2)^2 + cos(pi/2)^2", 1),
    ("tan(pi/4)", 1),
    ("1 + 0.5", 1.5),
    ("1 + tan(pi/4)", 1 / math.pow(math.cos(math.pi / 4), 2)),
    ("sin(1)^2", 0.7080734182735712),
]


@pytest.mark.parametrize("raw_expression, value", float_examples)
def test_float_examples(raw_expression: str, value: int | float):
    result = main(raw_expression)

    assert math.isclose(result, value)


bad_examples = [
    "?",
    "(3",
    "()",
    "3/0",
]


@pytest.mark.parametrize("raw_expression", bad_examples)
def test_bad_examples(raw_expression: str):
    with pytest.raises((ValueError, AssertionError, ZeroDivisionError)):
        _ = main(raw_expression)
