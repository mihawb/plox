from dataclasses import dataclass
from typing import Any
from tokens import Token


class Visitor:
    def visit_binary(self, expr): pass
    def visit_grouping(self, expr): pass
    def visit_literal(self, expr): pass
    def visit_unary(self, expr): pass


class Expr:
    def accept(self, visitor: Visitor):
        pass


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_binary(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping(self)


@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: Visitor):
        return visitor.visit_literal(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_unary(self)
