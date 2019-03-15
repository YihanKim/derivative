from Expression import Expression
from abc import *

class BinaryExpression(Expression):

    @abstractmethod
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
        self.op = "op"
        self.type = "binary operations"

    def __repr__(self):
        return "({}){}({})".format(
                self.left.__repr__(),
                self.op,
                self.right.__repr__()
                )

    @abstractmethod
    def evaluate(self, env: dict):
        pass

    @abstractmethod
    def gradient(self, var: str):
        pass

    @abstractmethod
    def reduce(self):
        pass

