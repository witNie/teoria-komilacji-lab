import sys
from sly import Lexer



class Scanner(Lexer):
    # tokens = { PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN }
    tokens = { ZEROS, INTNUM, DOTADD, DOTSUB, DOTMUL, DOTDIV, LESSEQ, MOREEQ, EQUALS, NOTEQ, ADDASSIGN,
               SUBASSIGN, MULASSIGN, DIVASSIGN, IF, ELSE, WHILE, FOR, BREAK, RETURN, CONTINUE, PRINT,
               EYE, ONES, FLOATNUM, ID, STRING  }

    # literals = "+-()/;=:[]{},'<>"

    literals = {'=', '+', '-', '/', '(', ')', ';', ':', '[', ']', '{', '}', ',', "'", '<', '>'}

    ignore = " \t"
    ignore_comment = r'#.'


    FLOATNUM = r'(0?|[1-9]\d).\d((E|e)(-|+)?\d+)?'
    INTNUM = r'([1-9]\d)|(0)'

    DOTADD = r'.+'
    DOTSUB = r'.-'
    DOTMUL = r'.*'
    DOTDIV = r'./'
    LESSEQ = r'<='
    MOREEQ = r'>='
    NOTEQ = r'!='
    EQUALS = r'=='
    ADDASSIGN = r'+='
    SUBASSIGN = r'-='
    MULASSIGN = r'*='
    DIVASSIGN = r'/='
    ID = r'[a-zA-Z][a-zA-Z0-9]'
    ID['if'] = 'IF'
    ID['else'] = 'ELSE'
    ID['for'] = 'FOR'
    ID['while'] = 'WHILE'
    ID['break'] = 'BREAK'
    ID['continue'] = 'CONTINUE'
    ID['return'] = 'RETURN'
    ID['print'] = 'PRINT'
    ID['eye'] = 'EYE'
    ID['ones'] = 'ONES'


    ID['zeros'] = 'ZEROS'

    STRING = r'".?"'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1





if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example4.m"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"{tok.lineno}: {tok.type}({tok.value})")