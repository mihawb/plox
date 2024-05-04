from typing import Iterable
from tokens import Token, TokenType as TT
from expressions import Expr, Binary, Unary, Literal, Grouping


class ParseError(RuntimeError):
    pass


class Parser:
    """Top-down predictive parser based on recursive descent algorithm"""

    def __init__(self, tokens: Iterable[Token]) -> None:
        self.tokens = list(tokens)
        self.current = 0

    def parse(self) -> Expr | None:
        try:
            return self.expression()
        except ParseError as err:
            return None

    def binary_left_assoc(self, higher_precedence_rule: callable, *expected_token_types: TT) -> Expr:
        expr = higher_precedence_rule()

        while self.peek().token_type in expected_token_types:  # while=>()* regex rule in lox.gram
            operator = self.advance()
            right_most = higher_precedence_rule()
            expr = Binary(expr, operator, right_most)

        return expr

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        """Matches an equality operator or anything of higher precedence, is left-associative"""
        return self.binary_left_assoc(self.comparison, TT.BANG_EQUAL, TT.EQUAL_EQUAL)

    def comparison(self) -> Expr:
        """Matches a comparison operator or anything of higher precedence, is left-associative"""
        return self.binary_left_assoc(self.term,
                                      TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL)

    def term(self) -> Expr:
        """Matches a subtraction or addition operator or anything of higher precedence, is left-associative"""
        return self.binary_left_assoc(self.factor, TT.MINUS, TT.PLUS)

    def factor(self) -> Expr:
        """Matches a factorization operator or anything of higher precedence, is left-associative"""
        return self.binary_left_assoc(self.unary, TT.SLASH, TT.STAR)

    def unary(self) -> Expr:
        """Matches a unary operator or anything of higher precedence"""
        if self.peek().token_type in [TT.BANG, TT.MINUS]:  # if==()?
            operator = self.advance()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        """Matches a singular literal or a grouping of expressions"""
        if self.is_at_end():
            raise Parser.error(self.peek(), "Expect expression.")

        match self.peek().token_type:
            case TT.FALSE:
                self.advance()
                return Literal(False)
            case TT.TRUE:
                self.advance()
                return Literal(True)
            case TT.NIL:
                self.advance()
                return Literal(None)

            case TT.NUMBER | TT.STRING:
                token = self.advance()
                return Literal(token.literal)

            case TT.LEFT_PAREN:
                self.advance()
                expr = self.expression()
                self.consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
                return Grouping(expr)

        raise Parser.error(self.peek(), "Expect expression.")  # IDK if still necessary

    def consume(self, expected_type: TT, message: str) -> Token:
        """Consumes a token if it's of expected type, enters error recovery mode otherwise"""
        if not self.is_at_end() and self.peek().token_type == expected_type:
            return self.advance()
        raise Parser.error(self.peek(), message)

    def __match_types(self, *types: TT) -> bool:
        """DEPRECATED! Tries to match next token (by lookahead) to supplied list of types, consumes it on match"""
        # 1. if is_at_end => False
        # 2. check if peek().token_type in list of expected types
        if self.is_at_end():
            return False

        if self.peek().token_type in types:
            self.advance()
            return True

        return False

    def __check_type(self, t: TT) -> bool:
        """DEPRECATED! Checks type of next unconsumed token"""
        # 1. if is_at_end => False
        # 2. compare peek().token_type with expected type
        if self.is_at_end():
            return False
        return self.peek().token_type == t

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().token_type == TT.EOF

    @staticmethod
    def error(token: Token, message: str) -> ParseError:
        from lox import Lox as LoxImpl
        LoxImpl.parser_error(token, message)
        return ParseError()

    def synchronize(self) -> None:
        """Synchronizes parser state to statement boundary after encountering syntax error
           i.e. discards tokens up until one signifying a statement appears."""
        self.advance()

        while not self.is_at_end():
            if self.previous().token_type == TT.SEMICOLON:
                return

            match self.peek().token_type:
                case TT.CLASS | TT.FUN | TT.VAR \
                     | TT.FOR | TT.IF | TT.WHILE \
                     | TT.PRINT | TT.RETURN:
                    return

            self.advance()


if __name__ == "__main__":
    x = TT.EQUAL
    match x:
        case TT.BANG:
            print("boo")
        case TT.BANG_EQUAL | TT.EQUAL:
            print("yay")
        case _:
            print('default boo')

    tt = TT.MINUS
    if tt in (TT.FOR, TT.MINUS, TT.CLASS):
        print(f"{TT.MINUS} matched")
