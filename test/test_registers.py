import math

import pytest

from pratt_calc.evaluator import Evaluator

examples = [
    ("alice <- 100 ; bob <- 200; alice + bob", 300),
    ("alice <- bob <- charlie <- 1000; alice + bob + charlie", 3000),
    ("alice <- 10; alice!", 3628800),
]


@pytest.mark.parametrize("raw_expression, value", examples)
def test_examples(raw_expression: str, value: int | float):
    ev = Evaluator()
    result = ev.evaluate(raw_expression)

    assert math.isclose(result, value, abs_tol=1e-10)
