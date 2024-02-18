
from pqss.env import Environment
from pqss.lex import Token
from .ast import (
    Statement,
    Expression,
)
from .selector import Selector
from .rule import Rule


class Ruleset(Statement):
    def eval(self, environment: Environment):
        res = ''
        selectors = ''
        for selector in self.selector_list:
            selectors += ' ' + selector.eval(environment)
        res += selectors
        res += '{'
        for rule in self.rule_list:
            res += rule.eval(environment)
        res += '}'

        def eval_child(sec, children):
            res = ''
            s = ''
            for se in sec:
                s += ' ' + se.eval(environment)
            s = s.replace(' ', '')
            for child_ruleset in children:
                val = child_ruleset.eval(environment)

                if val.find('&') != -1:
                    val = val.replace('&', s.split(' ')[-1])
                    val = val.replace(' ', '')
                    s = s.split(s.split(' ')[-1])[0]
                    res += s + val
                else:
                    res += s + ' '
                    res += val

            return res

        child_rules = eval_child(self.selector_list, self.child_ruleset)

        res += child_rules
        return res

    def __init__(self):
        self.selector_list: list[Selector] | None = []
        self.rule_list: list[Rule] = []
        self.child_ruleset: list[Ruleset] = []

    def stmt_node(self):
        pass
