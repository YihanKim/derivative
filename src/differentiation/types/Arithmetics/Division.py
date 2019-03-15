from BinaryExpression import BinaryExpression

class Division(BinaryExpression):
    # e1 / e2
    def __init__(self, a: Expression, b: Expression):
        self.left = a
        self.right = b
        self.op = "/"
        self.type = "division"

    def __repr__(self):
        return "({})/({})".format(self.left.__repr__(), self.right.__repr__())

    def evaluate(self, env: dict):
        return self.left.evaluate(env) / self.right.evaluate(env)

    def gradient(self, var: str):
        return Division(
                Subtraction(
                    Multiplication(self.left.gradient(var), self.right),
                    Multiplication(self.left, self.right.gradient(var))
                ),
                Multiplication(self.right, self.right)
            )

    def reduce(self):
        self.left = self.left.reduce()
        self.right = self.right.reduce()

        if self.left.type == "number" and self.left.n == 0:
            return Number(0)

        if self.right.type == "number" and self.right.n == 0:
            raise ZeroDivisionError

        if self.right.type == "number" and self.right.n == 1:
            return self.left

        if self.left.type == "number" and self.right.type == "number":
            return Number(self.left.n / self.right.n)

        return Division(self.left, self.right)

