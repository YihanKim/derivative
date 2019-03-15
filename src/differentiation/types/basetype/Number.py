from Expression import Expression

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
