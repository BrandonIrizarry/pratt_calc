# Introduction

An arithmetic expression calculator in Python, demoing the Pratt
parsing algorithm.

This takes inspiration from [this excellent 2010 blog post](https://eli.thegreenplace.net/2010/01/02/top-down-operator-precedence-parsing), as
well as a few other sources:

1. [Simple but Powerful Pratt Parsing](https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html)
2. [Pratt Parsers: Expression Parsing Made Easy](https://journal.stuffwithstuff.com/2011/03/19/pratt-parsers-expression-parsing-made-easy/)
3. [Compiling Expressions (Chapter 17 of Crafting Interpreters)](https://craftinginterpreters.com/compiling-expressions.html)

I also have [some notes](#the-pratt-parsing-algorithm) at the end of this document which go into
some detail over how the Pratt parsing machinery works.

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

Pratt Calc supports three modes of usage:

1. Evaluating expressions from inside a REPL;
2. evaluating the contents of a source file, and
3. evaluating an expression given at the command line.

Also see

`pratt-calc --help`


## REPL

To launch the REPL:

`pratt-calc`

Use the `exit` command (or `Ctrl+D`) to quit the REPL.

## Loading a file

To execute the contents of a file:

`pratt-calc FILENAME`

## Evaluating an expression on the fly

To evaluate a one-off expression:

`pratt-calc -e EXPRESSION`

Single quotes surrounding the expression are recommended, to prevent
the shell from expanding `*` and so on. Example:

`pratt-calc -e '3-4*5'`

This should print `-17` at the console.

## Combining switches (the `-i` flag)

If neither a filename argument nor `-e` are provided, the REPL will
launch. Conversely, if either one is present, the REPL will not
launch. However, you can use `-i` to force the REPL to launch in such
a case.

# Basic Arithmetic

Pratt Calc is at its most basic level an arithmetic expression
calculator over integers and floats. It currently supports `+`, `-`,
`*`, and `\` with their usual meanings of addition, subtraction,
multiplication, and division respectively. In addition, unary negation
(e.g. `-2.5`), as well as exponentiation (`^`) and factorial (`!`) are
supported.

Note that an expression like `3.2!` is first truncated to an integer
before evaluation, that is, `3.2!` would evaluate to `6`.

Parentheses are used to enforce precedence, viz.,

`pratt-calc -e '(3 + 5) * 2'` => `16`

## Semicolons

Semicolons enable side-effect-based programming, which currently are a
work in progress. For now, semicolons discard the result of whatever
is to the left of them:

`pratt-calc -e '3 + 3 ; 3 * 3; 3 ^ 3'` => `27.0`

That is, the result of the above expression is simply the value of the
last subexpression, namely, `3 ^ 3`.

Note: for now, semicolons can't *terminate* an expression, since
they're technically infix operators, and thus require a right-hand
argument! I have some ideas for workarounds, but I'm not focused on
that right now.

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

# A Note on Libraries Used

Pratt Calc, as a command-line app, is built using
[Typer](https://typer.tiangolo.com/).

It also uses the
[more-itertools](https://more-itertools.readthedocs.io/en/stable/)
library to implement the token stream used to drive expression
evaluation.

# The Pratt Parsing Algorithm

I'm including these notes in case they may be of help to anyone trying
to learn about Pratt parsing (and to help me remember for future
projects!) The algorithm is ultimately simple, but tricky. To be
honest, I don't think I have a 100% perfect mental model of it, but I
still want to present and possibly refine my understanding.

The Pratt parsing algorithm can be summarized as follows. Note that I
may occasionally make the assumption here that the "parsed" expression
is also simultaneously being *evaluated*, though it should be very
easy to adjust the following explanation to do whatever you want, for
example, construct an abstract syntax tree instead of accumulate a
literal result.

```
parse(level):
    t ← next(stream)
    acc ← nud_dispatch(t)                           # Calls 'parse' recursively.

    while level < precedence(peek(stream)):
        t ← next(stream)
        acc ← led_dispatch(t, acc)                  # Calls 'parse' recursively.

    return acc

main():
    parse(0)
```

1. `parse` is the top-level function. It accepts an
   operator-precedence level as an argument.

2. `nud_dispatch`, which may or may not be a separate function,
   represents the logic that processes the next token as a prefix
   operator, or `nud`.

   The `nud_dispatch` logic serves to initialize `acc`, which
   represents the *accumulated* result of the computation. It can
   either recursively call `parse` with a `level` arugment equal to
   the unary-operator precedence of `t`, or else assign `t` directly
   to `acc` in the case where `t` is a constant value (a number, for
   example).

   There is also an implicit assumption that the stream of tokens is
   structured properly, that is, a valid `nud` *will* be met with at
   this point in the code. For example, a stray infix operator will be
   caught as an error.

   `nud` is short for **null denotation**.

3. `precedence` is a function (or else some logic) that returns the
   precedence of a given token *as an infix operator*, or `led`. If
   said precedence is higher than the current `level`, the next token
   is fetched, and determines the current action of `led_dispatch`
   (which is logic that, by construction, should involve `acc`). For
   example, if `t` is `+`, `led_dispatch` should assign `acc +
   parse(ADDITION_PRECEDENCE)` to `acc`.

   `precedence`, in this formulation, also checks whether
   `peek(stream)` is a valid `led` token in the first place.

   The literature aptly notes that a `led` technically can be any
   non-prefix operator, for example, factorial (`52!`), or ternary
   conditional expressions (`foo ? bar : baz`). The only relevant
   characteristic of a `led` is that it utilizes `acc` in reassigning
   its computation back to `acc`.

   `led` is short for **left denotation**.

4. If the precedence of the next would-be token is lesser or equal,
   we're done for this `level`: return `acc`.

In general, it helps to think of the algorithm as traversing an
expression along fluctuating "gradients" of operator precedence, such
that the algorithm "ramps up" or "ramps down", depending on the
operator seen.

There is also a "ramp-even" which is functionally equivalent to a
ramp-down. This fact is important in understanding how the algorithm
enforces associativity.

Example: evaluate `3 + 5 * 2 - 1`.

Assume we have the following precedence levels:

```
NONE = 0
PLUS_MINUS = 1
TIMES_DIVIDE = 2
```

I'll now trace through what the above algorithm would do in this
case.

I've deliberately kept this example simple to demonstrate the most
salient aspects of the algorithm, but there are certain bespoke tricks
that become manifest in more complex expressions involving, for
example, parentheses and right-associative operators. Ideally,
adequately explaining Pratt parsing would take at least several
examples of varied complexity.

To differentiate the different [stack
frames](https://en.wikipedia.org/wiki/Call_stack) associated with
recursive calls to `parse`, I'll subscript each mention of the `acc`
variable according to the stack frame it belongs to, e.g., `acc₀`,
`acc₁`, etc.

Without further ado:

- `parse` is called as `parse(NONE)`. It's a good idea to have a
  `NONE` precedence which bootstraps the precedence gradient.

- `3` is a valid `nud`, because it's a constant. So perform

  `acc₀  ←  3`

- `+`, as **peeked** from the stream, is a `led`, and would ramp up
  the precedence to `PLUS_MINUS`: so we consume it and enter the while
  loop body. We dispatch `+` as a `led`, such that

  `acc₀ ← acc₀ + parse(PLUS_MINUS)`

  We now enter the recursive call to `parse`.

  The fact that we don't unconditionally consume tokens is important:
  this lets lower-precedence tokens function as sentinels that force
  the evaluation of more-tightly-bound expressions, something which
  we'll see in a bit.

- We're now one frame deep in recursion, with a `level` of
  `PLUS_MINUS`. We find that `5` is a constant `nud`, so we assign it
  to the `acc` of our current stack frame:

  `acc₁ ← 5`

- `*` is a `led`, and would ramp up the precedence to `TIMES_DIVIDE`,
  so consume it and enter the while loop body.  We dispatch `*` as a `led`,
  such that

  `acc₁ ← acc₁ * parse(TIMES_DIVIDE)`

  We now enter the recursive call to `parse`.

- We're now two frames deep in recursion, with a `level` of
  `TIMES_DIVIDE`. We find that `2` is a valid `nud`, so perform

  `acc₂  ← 2`

- Here it gets interesting. We peek the stream and find the `led`
  token `-`, binary subtraction, waiting for us. However, the current
  level is `TIMES_DIVIDE`, while `precedence(`-`)` is
  `PLUS_MINUS`. We've just hit our first ramp-down! So we don't
  consume the `-`: we return `acc₂`, which is `2`, from the current
  frame.

- We're now back at stack frame #1, with a `level` of `PLUS_MINUS`. We
  had just executed the call

  `acc₁ ← acc₁ * parse(TIMES_DIVIDE)`.

  Well, the recursive call evaluated to `2`, so we're now left with

  `acc₁ ← acc₁ * 2`

  In this frame, `acc₁` is 5, and so perform `acc₁ ← 10`.

- We continue looping within the current stack frame. We again peek
  the stream and find the unconsumed `-` from before: since this would
  be a ramp-even, we exit the loop and return `10` from the current
  frame.

- We're now back at stack frame #0, with a `level` of `NONE`. The
  `led_dispatch` portion reduces as follows:

 `acc₀ ← acc₀ + parse(PLUS_MINUS)`
 `acc₀ ← acc₀ + 10`
 `acc₀ ← 3 + 10`
 `acc₀ ← 13`

 - We continue looping within the current stack frame. We again peek
   the stream and once again find the unconsumed `-` from
   before. However, this time, it would ramp the precedence up to
   `PLUS_MINUS`, and so we enter the while loop body, finally
   consuming the `-`, and entering another stack frame to compute

   `acc₀ ← acc₀ - parse(PLUS_MINUS)`

- In the current frame (`level` == `PLUS_MINUS`), we perform

  `acc₁ ← 1`

  Next, something interesting happens. When we peek the stream, it
  looks like there are no more tokens; it looks like we've "fallen off
  the edge of the earth." To accomodate this necessary edge case, we
  always provide `EOF` as the last token of any expression. We parse
  `EOF` as a `led` such that `precedence(EOF) == NONE`. Thus, `EOF` is
  a kind of sentinel value that forces an unconditional ramp-down/even
  at the end of every expression, triggering the evaluation of
  everything prior.

  In this case, that means that the while loop exits without consuming
  `EOF` (a good thing, since `EOF` can't really be *dispatched* as a
  `led`), and we return `1` from the current frame.

- Back at frame #0, we continue with

 `acc₀ ← acc₀ - parse(PLUS_MINUS)`
 `acc₀ ← acc₀ - 1`
 `acc₀ ← 13 - 1`
 `acc₀ ← 12`

- Continuing the loop within frame #0, we peek the stream and find
  `EOF` still sitting there (which it will always do.) Since `EOF` by
  construction never has higher precedence than any other token, we
  exit the loop and return `12` as our final answer.

## More Thoughts

Writing the above trace-through example actually made me realize a few
more things about how Pratt parsing works! More complex examples are
possible, maybe at another time though.

As a whole, the algorithm allows for a great deal of artistic
license.

For example, in some cases it may be desirable to consume `EOF` as a
`nud` equal, say, to `0`.

Also, the "dispatch functions" may not even be functions; for example,
in this project, these are represented by Python `match` statements
that assign to `acc` accordingly.
