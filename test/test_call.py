import pytest

from pratt_calc.evaluator import Evaluator

examples = [
    ("x <- {2} ; @x", 0),
    ("x <- {2 + 3}; y <- {3}; @y", 5),
    ("x <- {2 + 3} ; y <- {foo <- 12 ; 10}; call @y; @foo", 12),
]


@pytest.mark.parametrize("raw_expression, value", examples)
def test_examples(raw_expression: str, value: int | float):
    ev = Evaluator()
    result = ev.evaluate(raw_expression)

    assert result == value
