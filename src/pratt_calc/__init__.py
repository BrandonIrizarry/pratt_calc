import pathlib
from typing import Annotated

import typer

from pratt_calc.main import evaluate
from pratt_calc.repl import Repl


def app():
    """Entry-point for project script."""

    # Note that the name of this particular function is insigificant,
    # as the function only serves to wrap the logic used by
    # 'typer.run'
    def cli(
        interactive: Annotated[
            bool, typer.Option("--interactive", "-i", help="Launch the REPL.")
        ] = False,
        exp: Annotated[
            str, typer.Option("--exp", "-e", help="Evaluate the given expression.")
        ] = "",
        filename: Annotated[str, typer.Argument(help="Path to source file")] = "",
    ):
        """Pratt Calc application."""

        if exp != "":
            print(evaluate(exp))

        if filename != "":
            path = pathlib.Path(filename)

            if not path.exists():
                print(f"Fatal: '{path}' doesn't exist")
                raise typer.Abort()

            if path.is_dir():
                print(f"Fatal: '{path}' is a directory")
                raise typer.Abort()

            with path.open(encoding="utf-8") as f:
                code = f.read()

                print(evaluate(code))

        launch_repl = interactive or (filename == "" and exp == "")

        if launch_repl:
            Repl().cmdloop()

    typer.run(cli)
