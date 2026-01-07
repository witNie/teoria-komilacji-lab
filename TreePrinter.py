import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


def _line(indent: int, text: str) -> None:
    print("|  " * indent + str(text))


#  program / blocks

@addToClass(AST.Program)
def printTree(self, indent=0):
    for instr in self.instructions:
        instr.printTree(indent)


@addToClass(AST.Block)
def printTree(self, indent=0):
    for instr in self.instructions:
        instr.printTree(indent)


#  instructions

@addToClass(AST.Assignment)
def printTree(self, indent=0):
    _line(indent, "=")
    self.target.printTree(indent + 1)
    self.value.printTree(indent + 1)


@addToClass(AST.CompoundAssignment)
def printTree(self, indent=0):
    _line(indent, self.op)
    self.target.printTree(indent + 1)
    self.value.printTree(indent + 1)


@addToClass(AST.Print)
def printTree(self, indent=0):
    _line(indent, "PRINT")
    for e in self.args:
        e.printTree(indent + 1)


@addToClass(AST.Return)
def printTree(self, indent=0):
    _line(indent, "RETURN")
    self.value.printTree(indent + 1)


@addToClass(AST.Break)
def printTree(self, indent=0):
    _line(indent, "BREAK")


@addToClass(AST.Continue)
def printTree(self, indent=0):
    _line(indent, "CONTINUE")


@addToClass(AST.If)
def printTree(self, indent=0):
    _line(indent, "IF")
    self.condition.printTree(indent + 1)
    _line(indent, "THEN")
    self.then_instr.printTree(indent + 1)


@addToClass(AST.IfElse)
def printTree(self, indent=0):
    _line(indent, "IF")
    self.condition.printTree(indent + 1)
    _line(indent, "THEN")
    self.then_instr.printTree(indent + 1)
    _line(indent, "ELSE")
    self.else_instr.printTree(indent + 1)


@addToClass(AST.While)
def printTree(self, indent=0):
    _line(indent, "WHILE")
    self.condition.printTree(indent + 1)
    self.body.printTree(indent + 1)


@addToClass(AST.For)
def printTree(self, indent=0):
    _line(indent, "FOR")
    self.var.printTree(indent + 1)
    self.range_.printTree(indent + 1)
    self.body.printTree(indent + 1)


#  condition / range

@addToClass(AST.Condition)
def printTree(self, indent=0):
    _line(indent, self.op)
    self.left.printTree(indent + 1)
    self.right.printTree(indent + 1)


@addToClass(AST.Range)
def printTree(self, indent=0):
    _line(indent, "RANGE")
    self.start.printTree(indent + 1)
    self.end.printTree(indent + 1)


#  expressions

@addToClass(AST.BinOp)
def printTree(self, indent=0):
    _line(indent, self.op)
    self.left.printTree(indent + 1)
    self.right.printTree(indent + 1)


@addToClass(AST.UnaryMinus)
def printTree(self, indent=0):
    _line(indent, "-")
    self.expr.printTree(indent + 1)


@addToClass(AST.Transpose)
def printTree(self, indent=0):
    _line(indent, "TRANSPOSE")
    self.expr.printTree(indent + 1)


@addToClass(AST.Variable)
def printTree(self, indent=0):
    if self.index_vector is not None:
        _line(indent, "REF")
        _line(indent+1, self.name)
        self.index_vector.printTree(indent + 1)
        if self.index_matrix is not None:
            self.index_matrix.printTree(indent + 1)
    else:
        _line(indent, self.name)


@addToClass(AST.Id)
def printTree(self, indent=0):
    _line(indent, self.name)


@addToClass(AST.IntNum)
def printTree(self, indent=0):
    _line(indent, self.value)


@addToClass(AST.FloatNum)
def printTree(self, indent=0):
    _line(indent, self.value)


@addToClass(AST.StringLit)
def printTree(self, indent=0):
    _line(indent, self.value)


#  vectors / matrices / constructors

@addToClass(AST.Vector)
def printTree(self, indent=0):
    # If you prefer not to print "VECTOR", remove this line.
    _line(indent, "VECTOR")
    for item in self.items:
        item.printTree(indent + 1)


@addToClass(AST.Matrix)
def printTree(self, indent=0):
    # If you prefer not to print "MATRIX", remove this line.
    _line(indent, "MATRIX")
    for row in self.rows:
        row.printTree(indent + 1)


@addToClass(AST.Zeros)
def printTree(self, indent=0):
    _line(indent, "zeros")
    _line(indent + 1, self.n)


@addToClass(AST.Ones)
def printTree(self, indent=0):
    _line(indent, "ones")
    _line(indent + 1, self.n)


@addToClass(AST.Eye)
def printTree(self, indent=0):
    _line(indent, "eye")
    _line(indent + 1, self.n)
