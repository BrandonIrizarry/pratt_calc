import sys

from minimal_pratt.parser import Parser
from minimal_pratt.tokenizer import tokenize


def main():
    raw_expression = sys.argv[1]

    stream = tokenize(raw_expression)
    parser = Parser(stream)

    value = parser.expression()

    print(value)
