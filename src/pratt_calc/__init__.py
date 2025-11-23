from typing import Annotated

import typer

from pratt_calc.main import evaluate


def app():
    """Entry-point for project script."""

    # Note that the name of this particular function is insigificant,
    # as the function only serves to wrap the logic used by
    # 'typer.run'
    def cli(filename: Annotated[str, typer.Argument(help="Path to source file")]):
        """Pratt Calc application."""
        with open(filename, encoding="utf-8") as f:
            code = f.read()

            print(evaluate(code))

    typer.run(cli)
