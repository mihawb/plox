from typing import Any
from tokens import TokenType as TT, Token
from expressions import Visitor, Expr, Binary, Grouping, Literal, Unary


class LoxRuntimeError(RuntimeError):
    def __init__(self, message: str, token: Token) -> None:
        super().__init__(message)
        self.token = token


class Interpreter(Visitor):
    """Tree-walker interpreter with post-order node traversal"""
    def interpret(self, expression: Expr) -> None:
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except LoxRuntimeError as lre:
            from lox import Lox as LoxImpl
            LoxImpl.runtime_error(lre)
        except AttributeError as ae:
            # this behaviour (parser returning None for interpreter to evaluate) is replicated in og source
            # so im just mitigating it till statements are coded in
            from lox import Lox as LoxImpl
            lre = LoxRuntimeError("Parser error occurred resulting in None expression", Token(TT.NIL, "nil", None, -1))
            LoxImpl.runtime_error(lre)

    @staticmethod
    def stringify(obj: Any) -> str:
        if obj is None:
            return "nil"

        if isinstance(obj, float):
            text = str(obj)
            if text[-2:] == ".0":  # bc Lox int values are represented by Python floats at runtime
                text = text[:-2]
            return text

        if isinstance(obj, bool):
            return str(obj).lower()

        return str(obj)

    def visit_literal(self, expr: Literal) -> Any:
        return expr.value

    def visit_grouping(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expression)

    def visit_unary(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        match expr.operator.token_type:
            case TT.BANG:
                return not self.make_truthy(right)
            case TT.MINUS:
                self.assert_number_operands(expr.operator, right)
                return -1 * float(right)

    def visit_binary(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.token_type:
            case TT.MINUS:
                self.assert_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TT.SLASH:
                self.assert_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TT.STAR:
                self.assert_number_operands(expr.operator, left, right)
                return float(left) * float(right)

            case TT.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise LoxRuntimeError("Operands must be two numbers or two strings.", expr.operator)

            case TT.GREATER:
                self.assert_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TT.GREATER_EQUAL:
                self.assert_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TT.LESS:
                self.assert_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TT.LESS_EQUAL:
                self.assert_number_operands(expr.operator, left, right)
                return float(left) <= float(right)

            case TT.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TT.EQUAL_EQUAL:
                return self.is_equal(left, right)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    @staticmethod
    def assert_number_operands(operator: Token, *operands: Any) -> None:
        """I MIGHT HAVE FUCKED UP THE ALL HERE"""
        if not all([isinstance(op, float) for op in operands]):
            raise LoxRuntimeError("Operand must be a number.", operator)

    @staticmethod
    def make_truthy(obj: Any) -> bool:
        """Ruby-style truthfulness: false and nil only coerce to false"""
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    @staticmethod
    def is_equal(a: Any, b: Any) -> bool:
        return a == b
