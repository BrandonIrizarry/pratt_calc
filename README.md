# Introduction

An arithmetic expression calculator in Python, demoing the Pratt
parsing algorithm.

This takes inspiration from [this 2010 blog
post](https://eli.thegreenplace.net/2010/01/02/top-down-operator-precedence-parsing)
by Eli Bendersky, as well as a few other sources:

1. [Simple but Powerful Pratt Parsing](https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html)
2. [Pratt Parsers: Expression Parsing Made Easy](https://journal.stuffwithstuff.com/2011/03/19/pratt-parsers-expression-parsing-made-easy/)
3. [Compiling Expressions (Chapter 17 of Crafting Interpreters)](https://craftinginterpreters.com/compiling-expressions.html)

# Requirements

Requires Python 3.13 or greater.

# Installation

## pip

Set up and activate a virtual environment, then:

`pip install pratt-calc`

## pipx (recommended)

Using `pipx` enables you to globally install the application without
worrying about virtual environments.

`pipx install pratt-calc`

In some cases it may be necessary to specify the Python version
manually:

`PIPX_DEFAULT_PYTHON=python3.13 pipx install pratt-calc`

Or, if you have `uv` installed:

`uvx pipx install pratt-calc`

# Contributing

Install `uv`, then run:

```bash
git clone https://github.com/BrandonIrizarry/pratt-calc
cd pratt-calc
uv sync --locked
```

# Usage

Pratt Calc, as a command-line app, is built using
[Typer](https://typer.tiangolo.com/). Built-in help is accessible via
the `--help` switch:

`pratt-calc --help`

Pratt Calc supports three modes of usage:

1. Evaluating expressions from inside a REPL;
2. evaluating the contents of a source file, and
3. evaluating an expression given at the command line.

These are described below.

## REPL

To launch the REPL:

`pratt-calc`

To exit the REPL, `Ctrl+D` or issuing the `exit` command suffice.

## Loading a file

To execute the contents of a file:

`pratt-calc FILENAME`

## Evaluating an expression on the fly

To evaluate a one-off expression:

`pratt-calc -e EXPRESSION`

Single quotes surrounding the expression are recommended, to prevent
shell expansion. Example:

`pratt-calc '3-4*5'`

This should print `-17` at the console.

## Combining switches (the `-i` flag)

If neither a filename argument nor `-e` are provided, the REPL will
launch. Conversely, if either one is present, the REPL will not
launch. However, you can use `-i` to force the REPL to launch in such
a case.


# Trigonometric Functions

`pratt-calc` supports the following trigonometric functions:

1. sin
2. cos
3. tan
4. csc
5. sec
6. cot

The constant 𝝿 is also available as `pi`. Examples:

`pratt-calc -e 'pi'` => `3.141592653589793`

`pratt-calc -e 'cos(pi)'` => `-1.0`

`pratt-calc -e 'sin(1)^2 + cos(1)^2'` => `1.0`

## A Note on the Implementation of Trig Functions

Trig functions are implemented as unary operators, as opposed to
function calls. Hence the parentheses used by `sin` and so forth are
merely there to enforce precedence, even though they conveniently
evoke the intuition of a function call.

Hence `sin²(1) + cos²(1)` can be written (somewhat misleadingly) as
follows:

`sin 1^2 + cos 1^2`

This evaluates to `1.0`.

For this reason, parentheses in this case are always recommended.

As an aside, to evaluate `[sin(1)]² + [cos(1)]²`, write:

`sin (1^2) + cos (1^2)`

This evaluates to `1.3817732906760363`.
