from .expressions import Expr, Binary, Grouping, Literal, Unary, Conditional


def parenthesize(name: str, *exprs: Expr) -> str:
    res = "(" + name + " "
    res += " ".join([pprint_expr(expr) for expr in exprs])
    res += ")"
    return res


def pprint_expr(expr: Expr) -> str:
    match expr:
        case Binary(left, operator, right):
            return parenthesize(operator.lexeme, left, right)
        case Grouping(expression):
            return parenthesize("group", expression)
        case Literal(value):
            return "nil" if value is None else str(value)
        case Unary(operator, right):
            return parenthesize(operator.lexeme, right)
        case Conditional(conditional, then_branch, else_branch):
            return "(if " + pprint_expr(conditional) + " then " + pprint_expr(then_branch) + " else " + pprint_expr(else_branch) + ")"
        case None:
            return "[SYNTAX ERROR]"
        case _:
            raise NotImplementedError(f"Non-exhaustive match in AST Pretty Printer failed on expression: {type(expr)}")


if __name__ == "__main__":
    from tokens import Token, TokenType

    # there's no parser yet, so we'll make do and hack-parse an example ourselves
    # an over-explained example, but I figured this will be easier to get back to in a month or so

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

    res = pprint_expr(expression)
    assert res == "(* (- 123) (group (+ 45.67 8.901)))"
    print(res)
