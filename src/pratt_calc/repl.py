import atexit
import cmd
import os
import readline
from typing import final, override

from pratt_calc.evaluator import Evaluator


def _save(prev_hlen: int, histfile: str):
    """Helper function to append lines to history."""

    new_hlen = readline.get_current_history_length()
    readline.set_history_length(1000)
    readline.append_history_file(new_hlen - prev_hlen, histfile)


@final
class Repl(cmd.Cmd):
    # FIXME: we should let the user customize where this is stored, as
    # well as the capacity of the file itself.
    histfile = os.path.join(os.path.expanduser("~"), ".pratt_calc_history")

    intro = """Welcome to the Pratt Calc REPL.

Use Ctrl+D (or the 'exit' command) to exit.

Type 'help' or '?' to list all commands."""

    prompt = "(calc) "

    def __init__(self, ev: Evaluator):
        super().__init__()

        try:
            readline.read_history_file(self.histfile)
            history_length = readline.get_current_history_length()
        except FileNotFoundError:
            # Create the file for the first time.
            open(self.histfile, "wb").close()
            history_length = 0

        _ = atexit.register(_save, history_length, self.histfile)

        # Initialize the evaluator to be shared across prompts.
        self.ev = ev

    @override
    def default(self, line: str):
        """Read, evaluate and print the provided expression."""

        print(self.ev.evaluate(line))

    @override
    def precmd(self, line: str):
        """Intercept EOF before it mangles the application."""

        if line == "EOF":
            return "exit"

        return line

    def do_exit(self, _):
        """Exit the REPL."""

        print()
        return True

    def do_heap(self, _):
        """Print the current heap."""

        print([str(t) for t in self.ev.heap])

    def do_locals(self, _):
        """Print all locals."""

        print([str(r) for r in self.ev.registers])
