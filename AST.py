from dataclasses import dataclass
from typing import List, Optional


# base

class Node:
    """Tutaj dodawaj swoje"""
    pass


#  program / instructions

@dataclass(frozen=True)
class Program(Node):
    instructions: List["Instruction"]


class Instruction(Node):
    pass


@dataclass(frozen=True)
class Block(Instruction):
    instructions: List["Instruction"]


# control flow

@dataclass(frozen=True)
class If(Instruction):
    condition: "Condition"
    then_instr: "Instruction"


@dataclass(frozen=True)
class IfElse(Instruction):
    condition: "Condition"
    then_instr: "Instruction"
    else_instr: "Instruction"


@dataclass(frozen=True)
class While(Instruction):
    condition: "Condition"
    body: "Instruction"


@dataclass(frozen=True)
class For(Instruction):
    var: "Variable"
    range_: "Range"
    body: "Instruction"


#  assignments / statements

@dataclass(frozen=True)
class Assignment(Instruction):
    target: "Variable"
    value: "Expression"


@dataclass(frozen=True)
class CompoundAssignment(Instruction):
    op: str
    target: "Variable"
    value: "Expression"


@dataclass(frozen=True)
class Print(Instruction):
    args: List["Expression"]


@dataclass(frozen=True)
class Return(Instruction):
    value: "Expression"


@dataclass(frozen=True)
class Break(Instruction):
    pass


@dataclass(frozen=True)
class Continue(Instruction):
    pass


#  expressions

class Expression(Node):
    pass


@dataclass(frozen=True)
class IntNum(Expression):
    value: int


@dataclass(frozen=True)
class FloatNum(Expression):
    value: float


@dataclass(frozen=True)
class StringLit(Expression):
    value: str


@dataclass(frozen=True)
class Id(Expression):
    name: str


@dataclass(frozen=True)
class Variable(Expression):

    name: str
    index_vector: Optional["Vector"] = None
    index_matrix: Optional["Vector"] = None


@dataclass(frozen=True)
class BinOp(Expression):
    op: str
    left: "Expression"
    right: "Expression"


@dataclass(frozen=True)
class UnaryMinus(Expression):
    expr: "Expression"


@dataclass(frozen=True)
class Transpose(Expression):
    expr: "Expression"


@dataclass(frozen=True)
class Range(Node):
    start: "Expression"
    end: "Expression"


#  conditions

@dataclass(frozen=True)
class Condition(Node):
    op: str
    left: "Expression"
    right: "Expression"


#  vectors / matrices

@dataclass(frozen=True)
class Vector(Expression):
    items: List["Expression"]


@dataclass(frozen=True)
class Matrix(Expression):
    rows: List["Vector"]


@dataclass(frozen=True)
class Zeros(Expression):
    n: int


@dataclass(frozen=True)
class Ones(Expression):
    n: int


@dataclass(frozen=True)
class Eye(Expression):
    n: int
