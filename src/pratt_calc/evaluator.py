from __future__ import annotations

import enum
import math
import pathlib
from collections import UserDict
from dataclasses import dataclass
from typing import final, override

from pratt_calc.tokenizer import Op, Token, Type, tokenize


@dataclass
class Register:
    alias: str
    value: int | float


class Precedence(enum.IntEnum):
    """Establish the various precedence levels.

    Rather than being associated directly with a token, a given
    precedence level gets passed in as an argument whenever a given
    token is dispatched.

    For example, subtraction is dispatched using PLUS_MINUS, while
    negation is dispatched using UNARY, even though both are
    associated with the '-' token.

    """

    NONE = enum.auto()
    SEMICOLON = enum.auto()
    ASSIGNMENT = enum.auto()
    PLUS_MINUS = enum.auto()
    TIMES_DIVIDE = enum.auto()
    POWER = enum.auto()
    UNARY = enum.auto()
    FACTORIAL = enum.auto()
    DEREFERENCE = enum.auto()


class LedPrecedenceTable(UserDict[Token, Precedence]):
    """Specify precedence of LED-position tokens.

    Not all LED-position tokens are actual LEDs, since, for example,
    'eof' serves no other function than to report a precedence level
    of NONE. In most cases though, a LED-position token and a LED
    token are the same thing.

    """

    @override
    def __getitem__(self, token: Token):
        try:
            return self.data[token]
        except KeyError:
            raise ValueError(f"Invalid led: '{token}'")


@final
class Evaluator:
    """An environment for evaluating expressions.

    Encapsulates a stream of Token objects as global state usable
    across recursive calls to 'expression', freeing us from having to
    return the stream (or any kind of placeholder state, for that
    matter) after each such recursive call.

    """

    led_precedence = LedPrecedenceTable(
        {
            Op.eof: Precedence.NONE,
            Op.rparen: Precedence.NONE,
            Op.plus: Precedence.PLUS_MINUS,
            Op.minus: Precedence.PLUS_MINUS,
            Op.times: Precedence.TIMES_DIVIDE,
            Op.divide: Precedence.TIMES_DIVIDE,
            Op.power: Precedence.POWER,
            Op.factorial: Precedence.FACTORIAL,
            Op.semicolon: Precedence.SEMICOLON,
            Op.assign: Precedence.ASSIGNMENT,
        }
    )

    def __init__(self):
        """Initialize the evaluator object.

        In particular initialize an empty token stream, to which
        EVALUATE will later append tokens comprising the expression to
        be evaluated.

        """

        # Initialize an empty token stream.
        self.stream = tokenize("")

        self.registers: list[Register] = []
        self.heap: list[Token] = []

    def evaluate(self, raw_expression: str) -> int | float:
        """Evaluate RAW_EXPRESSION.

        Note that each call to EVALUATE per object will peristently
        grow both the registers and the heap.

        """

        tokens = tokenize(raw_expression)
        self.stream.prepend(*tokens)

        return self.expression()

    def evaluate_file(self, filename: str) -> int | float:
        """Execute code in FILENAME."""

        path = pathlib.Path(filename)

        if not path.exists():
            raise FileNotFoundError(f"Fatal: '{path}' doesn't exist")

        if path.is_dir():
            raise IsADirectoryError(f"Fatal: '{path}' is a directory")

        with path.open(encoding="utf-8") as f:
            code = f.read()

            return self.evaluate(code)

    def dealias(self, alias: str) -> int:
        """Return address associated with locals alias.

        If alias doesn't exist yet, create it.

        """

        for i, register in enumerate(self.registers):
            if register.alias == alias:
                return i

        self.registers.append(Register(alias, 0))

        return len(self.registers) - 1

    def expression(self, level: int = Precedence.NONE) -> int | float:
        """Pratt-parse an arithmetic expression, evaluating it."""

        # NUD
        current = next(self.stream)

        match current.tag:
            case Type.INT:
                acc = int(current.what)

            case Type.FLOAT:
                acc = float(current.what)

            case Type.IDENTIFIER:
                acc = self.dealias(current.what)

            case Type.EOF:
                raise ValueError("Invalid eof")

            case Type.ERROR:
                raise ValueError(f"Invalid token: '{current}'")

            case Type.OPERATOR:
                match current:
                    case Op.pi:
                        acc = math.pi

                    case Op.sin:
                        acc = math.sin(self.expression(Precedence.UNARY))

                    case Op.cos:
                        acc = math.cos(self.expression(Precedence.UNARY))

                    case Op.tan:
                        acc = math.tan(self.expression(Precedence.UNARY))

                    case Op.sec:
                        acc = 1 / math.cos(self.expression(Precedence.UNARY))

                    case Op.csc:
                        acc = 1 / math.sin(self.expression(Precedence.UNARY))

                    case Op.cot:
                        acc = 1 / math.tan(self.expression(Precedence.UNARY))

                    case Op.minus:
                        acc = -self.expression(Precedence.UNARY)

                    case Op.lparen:
                        acc = self.expression(Precedence.NONE)

                        # We don't drive parsing/evaluation with right-paren,
                        # so we skip it as we read it.
                        assert next(self.stream) == Op.rparen

                    case Op.prt:
                        acc = self.expression(Precedence.UNARY)
                        print(acc)

                    case Op.at:
                        # Use 'index' as an index into the registers.
                        #
                        # Note that '@' should be right-associative, in case
                        # we'd like to do some double (or higher)
                        # dereferencing, for example, '@@alice'.
                        index = int(self.expression(Precedence.DEREFERENCE - 1))

                        # Retrieve the programmer-stored value.
                        acc = self.registers[index].value

                    case Op.quote:
                        # Note that this case doesn't call
                        # 'expression': it flatly consumes the next
                        # series of tokens until '}' is seen.
                        start = len(self.heap)
                        expr: list[Token] = []

                        while (t := next(self.stream)) != Op.endquote:
                            expr.append(t)

                        self.heap.append(Token(Type.INT, str(len(expr))))
                        self.heap.extend(expr)

                        acc = start

                    case Op.call:
                        # First evaluate the corresponding register
                        # address, then dereference it.
                        register_addr = int(self.expression(Precedence.UNARY))
                        len_addr = int(self.registers[register_addr].value)

                        expr_len_t = self.heap[len_addr]

                        if expr_len_t.tag != Type.INT:
                            raise ValueError(f"Non-int tag at heap address {len_addr}")

                        expr_len = int(expr_len_t.what)

                        # Get the address of the code itself.
                        addr = len_addr + 1
                        code = self.heap[addr : addr + expr_len]
                        self.stream.prepend(*code)

                        acc = self.expression(Precedence.NONE)

                    case _ as nonexistent:
                        raise ValueError(f"Invalid nud: '{nonexistent}'")

        while level < self.led_precedence[self.stream.peek()]:
            current = next(self.stream)

            # LED
            match current:
                case Op.plus:
                    acc += self.expression(Precedence.PLUS_MINUS)

                case Op.minus:
                    acc -= self.expression(Precedence.PLUS_MINUS)

                case Op.times:
                    acc *= self.expression(Precedence.TIMES_DIVIDE)

                case Op.divide:
                    acc /= self.expression(Precedence.TIMES_DIVIDE)

                case Op.power:
                    # Enforce right-association by subtracting 1 from
                    # the precedence argument.
                    acc = math.pow(acc, self.expression(Precedence.POWER - 1))

                case Op.factorial:
                    # Compute factorial by hand.
                    #
                    # If ACC is a float, truncate it first to an int.
                    prod = 1

                    acc = int(acc)

                    for j in range(1, acc + 1):
                        prod *= j

                        acc = prod

                case Op.semicolon:
                    # Discard the left-hand side, keeping only the
                    # right-hand side. This will hopefully be useful
                    # for side-effects later.
                    acc = self.expression(Precedence.SEMICOLON)

                case Op.assign:
                    # Assignment is right-associative.
                    right_hand_side = self.expression(Precedence.ASSIGNMENT - 1)

                    # Truncate 'acc' so that we can use it as an index
                    # into our registers.
                    self.registers[int(acc)].value = right_hand_side

                    # Set the current result to 'right_hand_side',
                    # like with Lisp's 'setq'.
                    acc = right_hand_side

                case _ as token:
                    raise ValueError(f"Invalid led: {token}")

        return acc
