# Introduction

An arithmetic expression calculator in Python, demoing the Pratt
parsing algorithm.

This takes inspiration from [this 2010 blog
post](https://eli.thegreenplace.net/2010/01/02/top-down-operator-precedence-parsing)
by Eli Bendersky, as well as a few other sources, which I'll touch on
in a future blog post.

# Installation

## Using `uv`

First, [make
sure](https://docs.astral.sh/uv/getting-started/installation/) `uv` is
installed in your system.

Then,

`git clone https://github.com/BrandonIrizarry/pratt_calc && cd !$`

`uv sync`

# Usage

`uv run pratt_calc $EXPRESSION`

Example: 

`uv run pratt_calc '3-4*5'`

This should print -17 at the console.





