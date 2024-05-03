from typing import Iterable
from tokens import Token, TokenType
from expressions import Expr, Binary, Unary, Literal, Grouping


class Parser:
    """Top-down predictive parser based on recursive descent algorithm"""

    def __init__(self, tokens: Iterable[Token]) -> None:
        self.tokens = list(tokens)
        self.current = 0

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        """Matches an equality operator or anything of higher precedence, is left-associative"""
        # TODO: (1) helper method for all left-associative series
        #  with swappable kernels for ttypes to match and higher prec. expressions
        expr = self.comparison()

        while self.match_types(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):  # while=>()* rule for equality in lox.gram
            operator = self.previous()
            right_most = self.comparison()
            expr = Binary(expr, operator, right_most)

        return expr

    def comparison(self) -> Expr:
        """Matches a comparison operator or anything of higher precedence, is left-associative"""
        # TODO: (1)
        expr = self.term()

        while self.match_types(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right_most = self.term()
            expr = Binary(expr, operator, right_most)

        return expr

    def term(self) -> Expr:
        """Matches a subtraction or addition operator or anything of higher precedence, is left-associative"""
        # TODO: (1)
        expr = self.factor()

        while self.match_types(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right_most = self.factor()
            expr = Binary(expr, operator, right_most)

        return expr

    def factor(self) -> Expr:
        """Matches a factorization operator or anything of higher precedence, is left-associative"""
        # TODO: (1)
        expr = self.unary()

        while self.match_types(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right_most = self.unary()
            expr = Binary(expr, operator, right_most)

        return expr

    def unary(self) -> Expr:
        """Matches a unary operator or anything of higher precedence"""
        if self.match_types(TokenType.BANG, TokenType.MINUS):  # if==()?
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        """Matches a singular literal or a grouping of expressions"""
        # these if blocks are HORRIBLE, but since match_types has some consuming logic
        # so it will be fixed only on main branch alongside TODO (2)
        if self.match_types(TokenType.FALSE):
            return Literal(False)
        if self.match_types(TokenType.TRUE):
            return Literal(True)
        if self.match_types(TokenType.NIL):
            return Literal(None)

        if self.match_types(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match_types(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expr)

    def consume(self, expected_type: TokenType, message: str) -> Token:
        """Consumes a token if it's of expected type, enters error recovery mode otherwise"""
        # TODO (2)
        if self.check_type(expected_type):
            return self.advance()
        # raise panic mode otherwise! but I will finish that tomorrow

    def match_types(self, *types: TokenType) -> bool:
        """Tries to match next token to supplied list of types, consumes it on match"""
        # TODO: (2) big contender for substitution for pattern matching on main branch
        # as this branch is a carbon copy of the original Java code only to verify correctness
        for t in types:
            if self.check_type(t):
                self.advance()
                return True
        return False

    def check_type(self, t: TokenType) -> bool:
        # TODO: (2)
        if self.is_at_end():
            return False
        return self.peek().token_type == t  # what does .type refer to?

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().token_type == TokenType.EOF


if __name__ == "__main__":
    x = TokenType.BANG_EQUAL
    match x:
        case TokenType.BANG:
            print("boo")
        case TokenType.BANG_EQUAL:
            print("yay")
        case _:
            print('default boo')
