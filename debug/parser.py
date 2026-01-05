from sly import Parser
from scanner import Scanner

class Mparser(Parser):
    tokens = Scanner.tokens

    debugfile = 'parser.out'

    start = 'program'

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        # ('right', 'UMINUS'),
        )

    @_('instructions_opt')
    def program(self, p):
        return p.instructions_opt

    @_('instructions')
    def instructions_opt(self, p):
        return p.instructions

    @_('')
    def instructions_opt(self, p):
        return []

    @_('instructions instruction')
    def instructions(self, p):
        return p.instructions + [p.instruction]

    @_('instruction')
    def instructions(self, p):
        return [p.instruction]

    @_('expr')
    def instruction(self, p):
        return p.expr

    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1
