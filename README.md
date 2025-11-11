# Introduction

An arithmetic expression calculator in Python, demoing the Pratt
parsing algorithm.

This takes inspiration from [this 2010 blog
post](https://eli.thegreenplace.net/2010/01/02/top-down-operator-precedence-parsing)
by Eli Bendersky, as well as a few other sources:

1. [Simple but Powerful Pratt Parsing](https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html)
2. [Pratt Parsers: Expression Parsing Made Easy](https://journal.stuffwithstuff.com/2011/03/19/pratt-parsers-expression-parsing-made-easy/)
3. [Compiling Expressions (Chapter 17 of Crafting Interpreters](https://craftinginterpreters.com/compiling-expressions.html)

# Installation

Requires Python 3.13 or greater.

To install,

`pipx install pratt-calc`

In some cases it may be necessary to specify the Python version
manually, for example, in cases where your system Python is less than
the required version, but you have a more recent Python accessible
under a different binary:

`PIPX_DEFAULT_PYTHON=python3.13 pipx install pratt-calc`

Hopefully this becomes less necessary in the future, as Linux
distributions upgrade their default Python installations.

## Using `uvx`

If you're missing the required Python version but have `uv` installed,
you can get away with this nice trick:

`uvx pipx install pratt-calc`

This should automatically acquire the correct Python version for you.

# Contributing

If you'd like to work on this project, I recommend installing `uv`, then:

```bash
git clone https://github.com/BrandonIrizarry/pratt-calc
cd pratt-calc
uv sync --locked
```

# Usage

`pratt-calc $EXPRESSION`

Example: 

`pratt-calc 3-4*5`

This should print -17 at the console.



