from expressions import Visitor, Expr, Binary, Grouping, Literal, Unary


class AstPrinter(Visitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        res = "(" + name + " "
        res += " ".join([expr.accept(self) for expr in exprs])
        res += ")"
        return res

    def visit_binary(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr: Literal) -> str:
        return "nil" if expr.value is None else str(expr.value)

    def visit_unary(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)


if __name__ == "__main__":
    from tokens import Token, TokenType

    # there's no parser yet, so we'll make do and hack-parse an example ourselves
    # an over-explained example but I figured this will be easier to get back to in a month or so

    expression = Binary(
        left=Unary(
            operator=Token(TokenType.MINUS, lexeme="-", literal=None, line=1),
            right=Literal(123)
        ),
        operator=Token(TokenType.STAR, lexeme="*", literal=None, line=1),
        right=Grouping(
            expression=Binary(
                left=Literal(value=45.67),
                operator=Token(TokenType.PLUS, lexeme="+", literal=None, line=1),
                right=Literal(value=8.901)
            )
        )
    )

    res = AstPrinter().print(expression)
    assert res == "(* (- 123) (group (+ 45.67 8.901)))"
    print(res)
