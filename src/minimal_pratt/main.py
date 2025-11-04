import re

token_pat = re.compile(r"\s*(?:(\d+)|(.))")


def tokenize(program):
    for number, operator in token_pat.findall(program):
        if number:
            yield literal_token(number)
        elif operator == "+":
            yield operator_add_token()
        elif operator == "-":
            yield operator_sub_token()
        elif operator == "*":
            yield operator_mul_token()
        elif operator == "/":
            yield operator_div_token()
        elif operator == "^":
            yield operator_pow_token()
        elif operator == "(":
            yield operator_lparen_token()
        elif operator == ")":
            yield operator_rparen_token()
        else:
            raise SyntaxError("unknown operator: %s", operator)
    yield end_token()


def match(tok=None):
    global token

    if tok and tok != type(token):
        raise SyntaxError("Expected %s" % tok)

    token = next(gen)


def parse(program):
    global token, gen
    gen = tokenize(program)
    token = next(gen)

    return expression()


def expression(rbp=0):
    global token
    t = token
    token = next(gen)
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next(gen)
        left = t.led(left)
    return left


class literal_token:
    def __init__(self, value):
        self.value = int(value)

    def nud(self):
        return self.value


class operator_add_token:
    lbp = 10

    def nud(self):
        return expression(100)

    def led(self, left):
        right = expression(10)
        return left + right


class operator_sub_token:
    lbp = 10

    def nud(self):
        return -expression(100)

    def led(self, left):
        return left - expression(10)


class operator_mul_token:
    lbp = 20

    def led(self, left):
        return left * expression(20)


class operator_div_token:
    lbp = 20

    def led(self, left):
        return left / expression(20)


class operator_pow_token:
    lbp = 30

    def led(self, left):
        return left ** expression(30 - 1)


class operator_lparen_token:
    lbp = 0

    def nud(self):
        expr = expression()
        match(operator_rparen_token)
        return expr


class operator_rparen_token:
    lbp = 0


class end_token:
    lbp = 0
