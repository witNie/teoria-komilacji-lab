from _ast import arguments

from sly import Parser
from scanner import Scanner


class Mparser(Parser):
    # from scanner import Scanner
    tokens = Scanner.tokens

    debugfile = 'parser.out'

    start = 'program'


    precedence = (
        ('left', '+', '-'),
        ("left", 'DOTADD', 'DOTSUB'),
        ('left', '*', '/'),
        ("left", 'DOTMUL', 'DOTDIV'),
        ('right', 'UNEG'),
        ("left", "'"),


        # ('right', 'UMINUS'),
    )



    @_('instructions_opt')
    def program(self, p):
        ast = p.instructions_opt
        print(ast)
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


    # to finish the grammar
    # ....


    # instruction

    @_('assignment ";"')
    def instruction(self, p):
        return p.assignment

    # @_('expression ";"')
    # def instruction(self, p):
    #     return p.expression

    @_('statement ";"')
    def instruction(self, p):
        return p.statement

    @_('"{" instructions_opt "}"')
    def block_body(self, p):
        return p.instructions_opt

    @_('instructions')
    def block_body(self, p):
        return p.instructions

    @_('IF "(" condition ")" block_body')
    def instruction(self, p):
        return (p[0], p.condition, p.block_body)

    @_('IF "(" condition ")" block_body ELSE block_body')
    def instruction(self, p):
        return (p[0], p.condition, p.block_body0, p.ELSE, p.block_body1)

    @_('WHILE "(" condition ")" block_body')
    def instruction(self, p):
        return (p[0], p.condition, p.block_body)

    @_('FOR variable "=" range block_body')
    def instruction(self, p):

        return (p[0], p.range, p.block_body)


    # statements

    @_('BREAK', 'CONTINUE')
    def statement(self, p):
        return p[0]

    @_('RETURN expression')
    def statement(self, p):
        return (p[0], p.expression)

    # @_('PRINT expression')
    # def statement(self, p):
    #     return (p[0], p.expression)

    @_('PRINT expressions')
    def statement(self, p):
        return (p[0], p.expressions)

    @_('expressions "," expression')
    def expressions(self, p):
        return p.expressions + [p.expression]

    @_('expression')
    def expressions(self, p):
        return [p.expression]


    @_('STRING')
    def expression(self, p):
        return p.STRING

    # @_('STRING "(" STRING_LITERAL ")"')
    # def string(self, p):
    #     return ('string', p.STRING_LITERAL)




    # assignment

    @_('variable "=" expression')
    def assignment(self, p):
        return ('assign', p.variable, p.expression)

    @_('variable "=" expression_list')
    def assignment(self, p):
        return ('assign', p.variable, p.expression_list)

    @_('variable ADDASSIGN expression', 'variable SUBASSIGN expression', 'variable MULASSIGN expression', 'variable DIVASSIGN expression')
    def assignment(self, p):
        return (p[1], p.variable, p.expression)

    @_('ID')
    def variable(self, p):
        return p.ID

    @_('matrix')
    def variable(self, p):
        return p.matrix

    # expression

    @_('function_call')
    def expression(self, p):
        return p.function_call

    @_('number')
    def expression(self, p):
        return p.number

    @_('ID')
    def expression(self, p):
        return p.ID

    @_('expression "+" expression', 'expression "-" expression', 'expression "/" expression', 'expression "*" expression')
    def expression(self, p):
        return (p[1], p.expression0, p.expression1)

    @_('FLOATNUM')
    def number(self, p):
        return float(p.FLOATNUM)

    @_('INTNUM')
    def number(self, p):
        return int(p.INTNUM)

    # matrix creation funtions

    @_('matrix_function argument_par')
    def function_call(self, p):
        return (p.matrix_function, p.argument_par)

    @_('"(" arguments ")"')
    def argument_par(self, p):
        return p.arguments

    @_('')
    def arguments(self, p):
        return []

    @_('arguments "," expression')
    def arguments(self, p):
        return p.arguments + [p.expression]

    @_('EYE','ZEROS','ONES')
    def matrix_function(self, p):
        return p[0]

    @_('matrix "\'" ')
    def expression(self, p):
        return ('transpose', p.matrix)

    @_('"[" expression_list "]"')
    def indexing(self, p):
        return ('index', p.expression_list)

    @_('matrix indexing')
    def matrix(self, p):
        return (p.matrix, p.indexing)

    @_('ID')
    def matrix(self, p):
        return p.ID

    @_('function_call')
    def matrix(self, p):
        return p.function_call

    @_('"(" expression ")"')
    def matrix(self, p):
        return p.expression

    @_('expression DOTADD expression', 'expression DOTSUB expression', 'expression DOTMUL expression', 'expression DOTDIV expression')
    def expression(self, p):
        return (p[1], p.expression0, p.expression1)

    @_('expression ">" expression', 'expression "<" expression', 'expression LESSEQ expression', 'expression MOREEQ expression',
       'expression EQUALS expression', 'expression NOTEQ expression' )
    def condition(self, p):
        return (p[1], p.expression0, p.expression1)

    @_('"-" expression %prec UNEG')
    def uneg(self, p):
        return ('-', p.expression)

    @_('uneg')
    def expression(self, p):
        return p.uneg

    @_('')
    def expression_list(self, p):
        return []

    @_('"[" expression_list "]"')
    def expression_list(self, p):
        return ('matrix', p.expression_list)

    @_('expression_list "," expression_list ')
    def expression_list(self, p):
        return p.expression_list0 + p.expression_list1



    @_('expression')
    def expression_list(self, p):
        return [p.expression]

    @_('expression ":" expression')
    def range(self, p):
        return ('range', p.expression0, p.expression1)

    @_('range')
    def expression(self, p):
        return p.range


    @_('"{" instructions "}"')
    def instruction(self, p):
        return ('block', p.instructions)

    def error(self, token):
        if token:
            print(f"Syntax error at token {token.type}, value {token.value!r}, line {token.lineno}")
            self.errok()
        else:
            print("Syntax error at EOF")