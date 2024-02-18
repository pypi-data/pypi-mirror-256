
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Statement,
    Expression,
)


class Rule(Statement):
    def eval(self, environment: Environment):
        res = ''
        res += self.property.literal
        res += ':'
        res += str(self.value.eval(environment))
        res += ';'
        return res

    def __init__(self):
        self.property: Token | None = None
        self.value: Expression | None = None

    def stmt_node(self):
        pass

