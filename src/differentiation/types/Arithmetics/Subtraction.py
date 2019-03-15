from BinaryExpression import BinaryExpressiosn

class Subtraction(BinaryExpression):
    # e1 - e2
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
        self.op = "-"
        self.type = "subtraction"

    def evaluate(self, env: dict):
        return self.left.evaluate(env) - self.right.evaluate(env)

    def gradient(self, var: str):
        return Subtraction(self.left.gradient(var), self.right.gradient(var))

    def reduce(self):
        self.left = self.left.reduce()
        self.right = self.right.reduce()

        if self.left.type == "number" and self.left.n == 0:
            return Negate(self.right).reduce()

        if self.right.type == "number" and self.right.n == 0:
            return self.left

        return Subtraction(self.left, self.right)

