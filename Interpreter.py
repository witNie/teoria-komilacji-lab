
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

import operator

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self):
        global_mem = Memory('global')
        self.memStack = MemoryStack()
        self.memStack.push(global_mem)

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)



    @when(AST.BinOp)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        operations = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            ".+": lambda A, B: [[a + b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)],
            ".-": lambda A, B: [[a - b for a, b in zip(rowA, rowB)] for rowA, rowB in zip(A, B)],

        }
        # print(node.left, node.right)
        # for m in self.memStack.stack:
        #     print(m.data)
        return operations[node.op](r1, r2)
        # try sth smarter than:
        # if(node.op=='+') return r1+r2
        # elsif(node.op=='-') ...
        # but do not use python eval

    @when(AST.Assignment)
    def visit(self, node):
        var = node.target.accept(self)
        value = node.value.accept(self)
        x = self.memStack.get(node.target.name)
        if self.memStack.get(node.target.name):
            if len(x) > 1:
                if len(x[0]) > 1:
                    x[node.target.index.items[0].accept(self)][node.target.index.items[1].accept(self)] = value
                    self.memStack.set(node.target.name, x)
                else:
                    x[node.target.index.accept(self)] = value
                    self.memStack.set(node.target.name, x)
            else:
                self.memStack.set(node.target.name, value)
        else:
            self.memStack.insert(node.target.name, value)

        # print("DEBUG")
        # for r in self.memStack.stack:
        #     print(r.data)
        # print("END DEBUG")
        return
    #

    #
    @when(AST.CompoundAssignment)
    def visit(self, node):
        # print(self.memStack.stack[0].data, self.memStack.stack[1].data)
        var = node.target.accept(self)
        value = node.value.accept(self)
        # print(type(var), type(value))
        operations = {
            "+=": operator.iadd,
            "-=": operator.isub,
            "*=": operator.imul,
            "/=": operator.itruediv,
        }
        # print(type(var))
        self.memStack.set(node.target.name, operations[node.op](var, value))
        # print(self.memStack.stack[0].data)
        return


    @when(AST.IntNum)
    def visit(self, node):
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.StringLit)
    def visit(self, node):
        return node.value

    @when(AST.Id)
    def visit(self, node):
        return node.name

    @when(AST.Variable)
    def visit(self, node):
        # print("OK", node.name)
        value = self.memStack.get(node.name)
        if node.index:
            if len(node.index.items) == 1:
                return value[node.index.accept(self)]
            elif len(node.index.items) == 2:
                # print(node.index.items[0].accept(self))
                return value[node.index.items[0].accept(self)][node.index.items[1].accept(self)]
        return value

    @when(AST.Vector)
    def visit(self, node):
        return node.items

    @when(AST.Matrix)
    def visit(self, node):
        return [node.rows[i].accept(self) for i in range(len(node.rows))]

    @when(AST.Zeros)
    def visit(self, node):
        return [0 for _ in range(node.n)]

    @when(AST.Ones)
    def visit(self, node):
        return [1 for _ in range(node.n)]

    @when(AST.Eye)
    def visit(self, node):
        return [[int(i==j) for j in range(node.n)] for i in range(node.n)]

    @when(AST.Condition)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        operations = {
            "<": operator.lt,
            ">": operator.gt,
            "<=": operator.le,
            ">=": operator.ge,
            "==": operator.eq,
            "!=": operator.ne,
        }
        return operations[node.op](r1, r2)

    @when(AST.IfElse)
    def visit(self, node):
        if node.condition.accept(self):
            node.then_instr.accept(self)
        elif node.else_instr:
            node.else_instr.accept(self)

    # chyba niepotrzebne
    @when(AST.Instruction)
    def visit(self, node):
        return None

    @when(AST.Range)
    def visit(self, node):
        return range(node.start.accept(self), node.end.accept(self)+1)

    @when(AST.For)
    def visit(self, node):
        mem = Memory('for')
        self.memStack.push(mem)
        # var = node.var.accept(self)
        range_ = node.range_.accept(self)
        # print(f'Debug {node.var.name}')
        self.memStack.insert(node.var.name, 0)
        for v in range_:
            self.memStack.set(node.var.name, v)
            # for m in self.memStack.stack:
            #     print(m.data)
            node.body.accept(self)
        self.memStack.pop()
        # print("OK FOR")


    @when(AST.If)
    def visit(self, node):
        if node.condition.accept(self):
            node.then_instr.accept(self)

    @when(AST.While)
    def visit(self, node):
        mem = Memory('while')
        self.memStack.push(mem)
        while node.condition.accept(self):
            node.body.accept(self)
        self.memStack.pop()

# simplistic while loop interpretation
    # @when(AST.WhileInstr)
    # def visit(self, node):
    #     r = None
    #     while node.cond.accept(self):
    #         r = node.body.accept(self)
    #     return r

    @when(AST.Print)
    def visit(self, node):
        val = [node.args[i].accept(self) for i in range(len(node.args))]
        # print(val)
        print(*(arg.accept(self) for arg in node.args))
        # print("OK PRINT")
        return None

    @when(AST.Return)
    def visit(self, node):
        value = node.expr.accept(self)
        raise ReturnValueException(value)


    @when(AST.Break)
    def visit(self, node):
        if len(self.memStack.stack) < 2:
            raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        if len(self.memStack.stack) < 2:
            raise ContinueException()

    @when(AST.Block)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

