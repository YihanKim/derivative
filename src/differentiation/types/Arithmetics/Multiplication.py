from BinaryExpression import BinaryExpression

class Multiplication(BinaryExpression):
    # e1 * e2
    def __init__(self, a: Expression, b: Expression):
        self.left = a
        self.right = b
        self.op = "*"
        self.type = "multiplication"

    def evaluate(self, env: dict):
        return self.left.evaluate(env) * self.right.evaluate(env)

    def gradient(self, var: str):

        return Addition(
                Multiplication(self.left.gradient(var), self.right),
                Multiplication(self.left, self.right.gradient(var))
            )

    def reduce(self):
        self.left = self.left.reduce()
        self.right = self.right.reduce()

        if self.left.type == "number" and self.left.n == 0:
            return Number(0)

        if self.right.type == "number" and self.right.n == 0:
            return Number(0)

        if self.left.type == "number" and self.left.n == 1:
            return self.right

        if self.right.type == "number" and self.right.n == 1:
            return self.left

        if self.left.type == "number" and self.right.type == "number":
            return Number(self.left.n * self.right.n)

        return Multiplication(self.left, self.right)

