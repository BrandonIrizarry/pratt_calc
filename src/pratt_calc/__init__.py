import sys

from pratt_calc.main import evaluate


def run():
    print(evaluate(sys.argv[1]))


if __name__ == "__main__":
    run()
