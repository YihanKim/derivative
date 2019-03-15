from BinaryExpression import BinaryExpression

class Addition(BinaryExpression):
    # e1 + e2
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
        self.op = "+"
        self.type = "addition"

    def evaluate(self, env: dict):
        return self.left.evaluate(env) + self.right.evaluate(env)

    def gradient(self, var: str):
        return Addition(self.left.gradient(var), self.right.gradient(var))

    def reduce(self):
        self.left = self.left.reduce()
        self.right = self.right.reduce()

        if self.left.type == "number" and self.left.n == 0:
            return self.right

        if self.right.type == "number" and self.right.n == 0:
            return self.left

        return Addition(self.left, self.right)

