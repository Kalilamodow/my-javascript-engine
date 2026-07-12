from dataclasses import dataclass
from enum import Enum


class Operator(Enum):
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIVIDE = "/"

    EQEQ = "=="
    NEQ = "!="

    GT = ">"
    LT = "<"
    GREQ = ">="
    LEEQ = "<="

    OR = "||"
    AND = "&&"
    NOT = "!"

    INC = "++"
    DEC = "--"


class Expression:
    pass


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Operator
    right: Expression


@dataclass
class NumberExpression(Expression):
    num: float


@dataclass
class StringExpression(Expression):
    value: str


@dataclass
class IdentifierExpression(Expression):
    name: str


@dataclass
class AssignmentExpression(Expression):
    name: Expression
    value: Expression


@dataclass
class MemberExpression(Expression):
    object: Expression
    property: IdentifierExpression


@dataclass
class FunctionCallExpression(Expression):
    fn: Expression
    arguments: list[Expression]


@dataclass
class PostfixExpression(Expression):
    operator: Operator
    expression: Expression


@dataclass
class PrefixExpression(Expression):
    operator: Operator
    expression: Expression


class Statement:
    pass


@dataclass
class Block:
    statements: list[Statement | Expression]


@dataclass
class VarDeclarationStatement(Statement):
    name: str
    value: Expression


@dataclass
class IfStatement(Statement):
    condition: Expression
    body: Block


@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: Block
