
from SymbolTable import SymbolTable, Symbol

import AST


class TypeChecker:
    def __init__(self):
        self.symbol_table = SymbolTable(None, "root")
        self.loop_level = 0

        self.INT = 'int'
        self.FLOAT = 'float'
        self.STR = 'string'
        self.MATRIX = 'matrix'
        self.VECTOR = 'vector'
        self.BOOL = 'boolean'

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # print(f"Generic : {node.__class__.__name__, node}")
        if isinstance(node, list):
            for item in node:
                self.visit(item)
        else:
            for field, value in vars(node).items():
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(value, AST.Node):
                    self.visit(value)

    # --- Program i Bloki ---

    def visit_Program(self, node):
        self.visit(node.instructions)

    def visit_Block(self, node):
        self.symbol_table = self.symbol_table.pushScope("block")
        self.visit(node.instructions)
        self.symbol_table = self.symbol_table.popScope()

    # --- Typy ---

    def visit_IntNum(self, node):
        return self.INT, None

    def visit_FloatNum(self, node):
        return self.FLOAT, None

    def visit_StringLit(self, node):
        return self.STR, len(node.value)

    def visit_Variable(self, node):
        symbol = self.symbol_table.get(node.name)
        if symbol is None:
            print(f"Error: Variable '{node.name}' undefined at line {getattr(node, 'lineno', '?')}")
            return None, None
        if symbol.type == self.MATRIX:
            if node.index:
                if len(node.index.items) == 2:
                    if node.index.items[0].value < symbol.size[0] and node.index.items[0].value < symbol.size[0]:
                        return self.INT , None
                    else:
                        print(f"Error: Index out of range")
                        return None, None
                else:
                    print(f"Error: Index matrix should be len 2")
            return self.MATRIX, symbol.size
        if symbol.type == self.VECTOR:
            if node.index:
                if len(node.index.items) == 1:
                    if node.inex < symbol.size:
                        return self.FLOAT , None
                    else:
                        print(f"Error: Index out of range")
                        return None, None
                else:
                    print(f"Error: Index vector should be len 1")


        if node.index is not None:
            self.visit(node.index)
            return self.FLOAT, None
        return symbol.type, None

    def visit_Id(self, node):
        name = node.name
        symbol = self.symbol_table.get(name)
        return symbol.type, symbol.size

    # --- Operacje ---

    def visit_UnaryMinus(self, node):
        type, size = self.visit(node.expr)
        return type, size

    def visit_BinOp(self, node):
        # print(f'Debug : {self.visit(node.left)}')
        left_type, left_size = self.visit(node.left)
        right_type, right_size = self.visit(node.right)


        # print(f'Bin OP : left: {left_type}, right: {right_type}')
        op = node.op

        # Operatory macierzowe (.+, .-, .*, ./)
        if op in ['.+', '.-', '.*', './']:
            if left_type != self.MATRIX or right_type != self.MATRIX:
                print(f"Error: Operator {op} requires matrix operands")
                return None, None
            if op in ['.+', '.-']:
                if left_size != right_size:
                    print(f"Error: Operator {op} matrix size mismatch")
                    return None, None
                return self.MATRIX, left_size
            else:
                if left_size[1] != right_size[0]:
                    print(f"Error: Operator {op} matrix size mismatch")
                    return None, None
                return self.MATRIX, (left_size[1], right_size[0])

        # Standardowe operatory (+, -, *, /)
        if left_type == self.STR and op == '+' and right_type == self.STR:
            return self.STR, left_size + right_size

        if left_type in [self.INT, self.FLOAT] and right_type in [self.INT, self.FLOAT]:
            # print("---------- Ok")
            # print(left_type, right_type)

            return (self.FLOAT, None) if (left_type == self.FLOAT or right_type == self.FLOAT) else (self.INT, None)

        # Mnożenie macierzy przez skalar
        if op == '*':
            # if left_type == self.MATRIX and right_type == self.MATRIX: return self.MATRIX,
            if left_type == self.MATRIX and right_type in [self.INT, self.FLOAT]:
                symbol = self.symbol_table.get(node.left.name)
                return self.MATRIX, symbol.size
        if left_type == right_type:
            if left_size == right_size:
                return left_type, left_size
            else:
                print(f"Error: Matrix size mismatch {left_size} vs {right_size}")
                return None, None

        print(f"Error: Type mismatch for {op}: {left_type} and {right_type}")
        return None, None

    def visit_Transpose(self, node):
        type, size = self.visit(node.expr)
        if type != self.MATRIX:
            print("Error: Transpose can only be applied to a matrix")
        return self.MATRIX, (size[1], size[0])

    # --- Przypisanie ---

    def visit_Assignment(self, node):
        # print(f'Debug : {self.visit(node.value)}')
        rhs_type, rhs_size = self.visit(node.value)

        if node.target.index is None:
            self.symbol_table.put(node.target.name, Symbol(node.target.name, rhs_type, rhs_size))
        else:
            self.visit(node.target)

        return rhs_type, rhs_size

    # --- Pętle i Sterowanie ---

    def visit_While(self, node):
        self.visit(node.condition)
        self.loop_level += 1
        self.symbol_table = SymbolTable(self.symbol_table, 'while')
        self.visit(node.body)
        self.loop_level -= 1
        self.symbol_table = self.symbol_table.parent

        return None, None

    def visit_For(self, node):
        self.visit(node.range_)
        self.symbol_table.put(node.var.name, Symbol(node.var.name, 'int', None))

        self.symbol_table = SymbolTable(self.symbol_table,'for')
        self.loop_level += 1
        self.visit(node.body)
        self.loop_level -= 1
        self.symbol_table = self.symbol_table.parent

        return None, None

    def visit_Break(self, node):
        if self.loop_level == 0:
            print("Error: 'break' used outside of loop")

        return None, None

    def visit_Continue(self, node):
        if self.loop_level == 0:
            print("Error: 'continue' used outside of loop")

        return None, None

    # --- Macierze i Wektory ---

    def visit_Zeros(self, node):
        return self.VECTOR, node.n

    def visit_Ones(self, node):
        return self.VECTOR, node.n

    def visit_Eye(self, node):
        return self.MATRIX, (node.n, node.n)

    def visit_Vector(self, node):
        for item in node.items:
            self.visit(item)
        return self.VECTOR, len(node.items)

    def visit_Matrix(self, node):
        for row in node.rows:
            self.visit(row)
        return self.MATRIX, (len(node.rows), len(node.rows[0].items))

    def visit_Condition(self, node):
        left_type, left_size = self.visit(node.left)
        right_type, right_size = self.visit(node.right)
        if left_type != right_type:
            print(f"Error: cond type mismatch : {left_type} and {right_type}")
            return None, None
        return None, None