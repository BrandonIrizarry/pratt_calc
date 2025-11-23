import typer

from pratt_calc.main import evaluate


def app():
    """Entry-point for project script."""

    # Note that the name of this particular function is insigificant,
    # as the function only serves to wrap the logic used by
    # 'typer.run'
    def cli(exp: str):
        """Evaluate EXP as an arithmetic expression."""

        print(evaluate(exp))

    typer.run(cli)
