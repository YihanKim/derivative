
class Expression(object):
    # template
    def __init__(self, value):
        self.type = "expression"

    def __repr__(self):
        return ""

    def evaluate(self, env: dict):
        return 0

    def gradient(self, var: str):
        return Number(0)

    def reduce(self):
        return self

class Number(Expression):
    # 0, 1, 2.5, ...
    def __init__(self, n: float):
        self.n = n
        self.type = "number"

    def __repr__(self):
        return "{} {}".format(self.type, self.n)

    def evaluate(self, env: dict):
        return n

    def gradient(self, var: str):
        return Number(0)

    def reduce(self):
        return self

class Variable(Expression):
    # x, y, z, ...
    def __init__(self, x: str):
        self.var = x
        self.type = "variable"

    def __repr__(self):
        return "{} {}".format(self.type, self.var)

    def evaluate(self, env: dict):
        return env[x]

    def gradient(self, var: str):
        if self.var == var:
            return Number(1)
        return Number(0)

    def reduce(self):
        return self

class Negation(Expression):
    # - e
    def __init__(self, e:Expression):
        self.e = e
        self.type = "negation"

    def __repr__(self):
        return "-{}".format(self.e.__repr__())

    def evaluate(self, env: dict):
        return self.e.evaluate(env)

    def gradient(self, var: str):
        return Negation(self.e.gradient(var))

    def reduce(self):
        if self.e.type == "negation":
            return self.e.e.reduce()
        return self

class Addition(Expression):
    # e1 + e2
    def __init__(self, a: Expression, b: Expression):
        self.a = a
        self.b = b
        self.type = "addition"

    def __repr__(self):
        return "({})+({})".format(self.a.__repr__(), self.b.__repr__())

    def evaluate(self, env: dict):
        return self.a.evaluate(env) + self.b.evaluate(env)

    def gradient(self, var: str):
        return Addition(self.a.gradient(var), self.b.gradient(var))

    def reduce(self):
        self.a = self.a.reduce()
        self.b = self.b.reduce()

        if self.a.type == "number" and self.a.n == 0:
            return self.b

        if self.b.type == "number" and self.b.n == 0:
            return self.a

        return Addition(self.a, self.b)

class Subtraction(Expression):
    # e1 - e2
    def __init__(self, a: Expression, b: Expression):
        self.a = a
        self.b = b
        self.type = "subtraction"

    def __repr__(self):
        return "({})-({})".format(self.a.__repr__(), self.b.__repr__())

    def evaluate(self, env: dict):
        return self.a.evaluate(env) - self.b.evaluate(env)

    def gradient(self, var: str):
        return Subtraction(self.a.gradient(var), self.b.gradient(var))

    def reduce(self):
        self.a = self.a.reduce()
        self.b = self.b.reduce()

        if self.a.type == "number" and self.a.n == 0:
            return Negate(self.b).reduce()

        if self.b.type == "number" and self.b.n == 0:
            return self.a

        return Subtraction(self.a, self.b)


class Multiplication(Expression):
    # e1 * e2
    def __init__(self, a: Expression, b: Expression):
        self.a = a
        self.b = b
        self.type = "multiplication"

    def __repr__(self):
        return "({})*({})".format(self.a.__repr__(), self.b.__repr__())

    def evaluate(self, env: dict):
        return self.a.evaluate(env) * self.b.evaluate(env)

    def gradient(self, var: str):

        return Addition(
                Multiplication(self.a.gradient(var), self.b),
                Multiplication(self.a, self.b.gradient(var))
            )

    def reduce(self):
        self.a = self.a.reduce()
        self.b = self.b.reduce()

        if self.a.type == "number" and self.a.n == 0:
            return Number(0)

        if self.b.type == "number" and self.b.n == 0:
            return Number(0)

        if self.a.type == "number" and self.a.n == 1:
            return self.b

        if self.b.type == "number" and self.b.n == 1:
            return self.a

        if self.a.type == "number" and self.b.type == "number":
            return Number(self.a.n * self.b.n)

        return Multiplication(self.a, self.b)

class Division(Expression):
    # e1 / e2
    def __init__(self, a: Expression, b: Expression):
        self.a = a
        self.b = b
        self.type = "division"

    def __repr__(self):
        return "({})/({})".format(self.a.__repr__(), self.b.__repr__())

    def evaluate(self, env: dict):
        return self.a.evaluate(env) / self.b.evaluate(env)

    def gradient(self, var: str):
        return Division(
                Subtraction(
                    Multiplication(self.a.gradient(var), self.b),
                    Multiplication(self.a, self.b.gradient(var))
                ),
                Multiplication(self.b, self.b)
            )

    def reduce(self):
        self.a = self.a.reduce()
        self.b = self.b.reduce()

        if self.a.type == "number" and self.a.n == 0:
            return Number(0)

        if self.b.type == "number" and self.b.n == 0:
            raise ZeroDivisionError

        if self.b.type == "number" and self.b.n == 1:
            return self.a

        if self.a.type == "number" and self.b.type == "number":
            return Number(self.a.n / self.b.n)

        return Division(self.a, self.b)


class ConstantExponentiation(Expression):
    # e ** k
    def __init__(self, e: Expression, k: Expression):
        assert k.type == "number"
        self.e = e
        self.k = k
        self.type = "exponentiation"

    def __repr__(self):
        return self.e.__repr__() + "+" + self.k.__repr__()

    def evaluate(self, env: dict):
        return self.e.evaluate(env) ** self.k

    def gradient(self, var: str):
        return Multiplication(
                self.e.gradient(var),
                ConstantExponentiation(self.e, self.k - 1)
            )

    def reduce(self):
        self.e = self.e.reduce()
        return self

class Logarithm(Expression):
    # log_b e
    def __init__(self, e: Expression, b: Expression):
        assert self.b.type == "number"
        self.e = e
        self.b = b
        self.type = "logarithm"

    def evaluate(self, env: dict):
        import math
        return math.log(self.e.evaluate(env), b)

    def gradient(self, var: str):
        return Division(
                self.e.gradient(var),
                Multiplication(Logarithm(self.b), self.e)
            )

    def reduce(self):
        self.e = self.e.reduce()
        return self

fifteen = Number(15)
x = Variable('x')
x2 = Multiplication(x, x)
x4 = Multiplication(x2, x2)
x4plus15x = Addition(x4, Multiplication(x, fifteen))

print(x4plus15x)
print(x4plus15x.gradient('x'))
print(x4plus15x.gradient('x').reduce())
