from Expression import Expression

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

