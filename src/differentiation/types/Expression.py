from abc import *

class Expression(object):

    @abstractmethod
    def __init__(self, value):
        self.type = "expression"

    @abstractmethod
    def __repr__(self):
        return ""

    @abstractmethod
    def evaluate(self, env: dict):
        return 0

    @abstractmethod
    def gradient(self, var: str):
        return Number(0)

    @abstractmethod
    def reduce(self):
        return self

