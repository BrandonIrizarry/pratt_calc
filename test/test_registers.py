import math

import pytest

from pratt_calc.main import evaluate

examples = [
    ("0 <- 100 ; 1 <- 200; @0 + @1", 300),
    ("0 <- 1 <- 2 <- 1000; @0 + @1 + @2", 3000),
    ("0 <- 10; @0!", 3628800),
]


@pytest.mark.parametrize("raw_expression, value", examples)
def test_float_examples(raw_expression: str, value: int | float):
    result = evaluate(raw_expression)

    assert math.isclose(result, value, abs_tol=1e-10)
