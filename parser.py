from sly import Parser
from scanner import Scanner
import AST

class Mparser(Parser):
    tokens = Scanner.tokens

    debugfile = 'parser.out'

    start = 'program'


    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),

        ('left', '+', '-'),
        ("left", 'DOTADD', 'DOTSUB'),
        ('left', '*', '/'),
        ("left", 'DOTMUL', 'DOTDIV'),

        ('right', 'UNEG'),
        ("left", "'"),
    )

    def error(self, p):
        if p:
            print(f"sly: Syntax error at line {p.lineno}, token={p.type}, value={p.value!r}")
            self.errok()
        else:
            print("sly: Syntax error at EOF")

    # start

    @_('instructions_opt')
    def program(self, p):
        return AST.Program(p.instructions_opt)

    # is instructions_opt

    @_('instructions')
    def instructions_opt(self, p):
        return p.instructions

    @_('')
    def instructions_opt(self, p):
        return []

    # is instructions

    @_('instructions instruction')
    def instructions(self, p):
        return p.instructions + [p.instruction]

    @_('instruction')
    def instructions(self, p):
        return [p.instruction]

    # is instruction

    @_('"{" instructions "}"')
    def instruction(self, p):
        return AST.Block(p.instructions)

    @_('assignment ";"')
    def instruction(self, p):
        return p.assignment

    @_('statement ";"')
    def instruction(self, p):
        return p.statement

    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.If(p.condition, p.instruction)

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.IfElse(p.condition, p.instruction0, p.instruction1)

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return AST.While(p.condition, p.instruction)

    @_('FOR variable "=" range_expr instruction')
    def instruction(self, p):
        return AST.For(p.variable, p.range_expr, p.instruction)

    # is assignment

    @_('variable "=" expression')
    def assignment(self, p):
        return AST.Assignment(p.variable, p.expression)

    @_('variable ADDASSIGN expression')
    def assignment(self, p):
        return AST.CompoundAssignment('+=', p.variable, p.expression)

    @_('variable SUBASSIGN expression')
    def assignment(self, p):
        return AST.CompoundAssignment('-=', p.variable, p.expression)

    @_('variable MULASSIGN expression')
    def assignment(self, p):
        return AST.CompoundAssignment('*=', p.variable, p.expression)

    @_('variable DIVASSIGN expression')
    def assignment(self, p):
        return AST.CompoundAssignment('/=', p.variable, p.expression)


    # statements

    @_('BREAK')
    def statement(self, p):
        return AST.Break()

    @_('CONTINUE')
    def statement(self, p):
        return AST.Continue()

    @_('RETURN expression')
    def statement(self, p):
        return AST.Return(p.expression)

    @_('PRINT expressions')
    def statement(self, p):
        return AST.Print(p.expressions)

    # is expressions

    @_('expressions "," expression')
    def expressions(self, p):
        return p.expressions + [p.expression]

    @_('expression')
    def expressions(self, p):
        return [p.expression]

    # is condition

    @_('expression ">" expression')
    def condition(self, p):
        return AST.Condition(">", p.expression0, p.expression1)

    @_('expression "<" expression')
    def condition(self, p):
        return AST.Condition("<", p.expression0, p.expression1)

    @_('expression LESSEQ expression')
    def condition(self, p):
        return AST.Condition("<=", p.expression0, p.expression1)

    @_('expression MOREEQ expression')
    def condition(self, p):
        return AST.Condition(">=", p.expression0, p.expression1)

    @_('expression EQUALS expression')
    def condition(self, p):
        return AST.Condition("==", p.expression0, p.expression1)

    @_('expression NOTEQ expression')
    def condition(self, p):
        return AST.Condition("!=", p.expression0, p.expression1)

    # is variable

    @_('ID vector')
    def variable(self, p):
        return AST.Variable(p.ID, p.vector)

    @_('ID')
    def variable(self, p):
        return AST.Variable(p.ID)

    # is expression

    @_('STRING')
    def expression(self, p):
        return AST.StringLit(p.STRING)

    @_('number')
    def expression(self, p):
        return p.number

    @_('ID')
    def expression(self, p):
        return AST.Id(p.ID)

    @_('expression "+" expression')
    def expression(self, p):
        return AST.BinOp("+", p.expression0, p.expression1)

    @_('expression "-" expression')
    def expression(self, p):
        return AST.BinOp("-", p.expression0, p.expression1)

    @_('expression "*" expression')
    def expression(self, p):
        return AST.BinOp("*", p.expression0, p.expression1)

    @_('expression "/" expression')
    def expression(self, p):
        return AST.BinOp("/", p.expression0, p.expression1)

    @_('expression DOTADD expression')
    def expression(self, p):
        return AST.BinOp(".+", p.expression0, p.expression1)

    @_('expression DOTSUB expression')
    def expression(self, p):
        return AST.BinOp(".-", p.expression0, p.expression1)

    @_('expression DOTMUL expression')
    def expression(self, p):
        return AST.BinOp(".*", p.expression0, p.expression1)

    @_('expression DOTDIV expression')
    def expression(self, p):
        return AST.BinOp("./", p.expression0, p.expression1)

    @_('"-" expression %prec UNEG')
    def expression(self, p):
        return AST.UnaryMinus(p.expression)

    @_('expression "\'"')
    def expression(self, p):
        return AST.Transpose(p.expression)

    @_('"(" expression ")"')
    def expression(self, p):
        return p.expression

    @_('matrix')
    def expression(self, p):
        return p.matrix

    @_('vector')
    def expression(self, p):
        return p.vector

    # is numbers

    @_('INTNUM')
    def number(self, p):
        return AST.IntNum(int(p.INTNUM))

    @_('FLOATNUM')
    def number(self, p):
        return AST.FloatNum(float(p.FLOATNUM))

    # is vector

    @_('"[" numbers "]"')
    def vector(self, p):
        return AST.Vector(p.numbers)

    @_('numbers "," number')
    def numbers(self, p):
        return p.numbers + [p.number]

    @_('number')
    def numbers(self, p):
        return [p.number]

    # is matrix

    @_('"[" vectors "]"')
    def matrix(self, p):
        return AST.Matrix(p.vectors)

    @_('vectors "," vector')
    def vectors(self, p):
        return p.vectors + [p.vector]

    @_('vector')
    def vectors(self, p):
        return [p.vector]

    @_('ZEROS "(" INTNUM ")"')
    def matrix(self, p):
        return AST.Zeros(int(p.INTNUM))

    @_('ONES "(" INTNUM ")"')
    def matrix(self, p):
        return AST.Ones(int(p.INTNUM))

    @_('EYE "(" INTNUM ")"')
    def matrix(self, p):
        return AST.Eye(int(p.INTNUM))

    # -------- range --------

    @_('range_value ":" range_value')
    def range_expr(self, p):
        return AST.Range(p.range_value0, p.range_value1)

    @_('INTNUM')
    def range_value(self, p):
        return AST.IntNum(int(p.INTNUM))

    @_('variable')
    def range_value(self, p):
        return p.variable

