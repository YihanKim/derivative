from Expression import Expression

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

