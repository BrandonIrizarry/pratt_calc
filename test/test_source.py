import pytest

from pratt_calc.evaluator import Evaluator

examples = [
    ("test/source.txt", ["20"]),
    ("test/source_comments.txt", ["11", "15"]),
]


@pytest.mark.parametrize("filename, lines", examples)
def test_examples(filename: str, lines: list[str], capsys: pytest.CaptureFixture[str]):
    ev = Evaluator()
    _ = ev.evaluate_file(filename)

    output = capsys.readouterr().out.splitlines()
    errors = capsys.readouterr().err

    assert output == lines
    assert errors == ""
