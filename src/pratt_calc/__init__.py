import typer

from pratt_calc.main import evaluate


def app():
    """Entry-point for project script."""

    def cli(exp: str):
        """Evaluate EXP as an arithmetic expression."""

        print(evaluate(exp))

    typer.run(cli)
