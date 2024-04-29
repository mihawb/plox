from typing import Any
from lox import Lox
from tokens import TokenType, Token


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []

        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c = self.advance()
        match c:
            # single character lexemes
            case "(": self.add_token(TokenType.LEFT_PAREN)
            case ")": self.add_token(TokenType.RIGHT_PAREN)
            case "{": self.add_token(TokenType.LEFT_BRACE)
            case "}": self.add_token(TokenType.RIGHT_BRACE)
            case ",": self.add_token(TokenType.COMMA)
            case ".": self.add_token(TokenType.DOT)
            case "-": self.add_token(TokenType.MINUS)
            case "+": self.add_token(TokenType.PLUS)
            case ";": self.add_token(TokenType.SEMICOLON)
            case "*": self.add_token(TokenType.STAR)

            # operators
            case "!": self.add_token(TokenType.BANG_EQUAL if self.match_next("=") else TokenType.BANG)
            case "=": self.add_token(TokenType.EQUAL_EQUAL if self.match_next("=") else TokenType.EQUAL)
            case "<": self.add_token(TokenType.LESS_EQUAL if self.match_next("=") else TokenType.LESS)
            case ">": self.add_token(TokenType.GREATER_EQUAL if self.match_next("=") else TokenType.GREATER)

            # comment or division?
            case "/":
                if self.match_next("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)

            # whitespaces
            case " ": pass
            case "\r": pass
            case "\t": pass
            case "\n": self.line += 1

            case _: Lox.error(self.line, "Unexpected character.")

    def add_token(self, token_type: TokenType, literal: Any = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self) -> chr:
        self.current += 1
        return self.source[self.current]

    def peek(self) -> chr:
        # performs *lookahead*
        if not self.is_at_end():
            return "\0"
        return self.source[self.current]

    def match_next(self, expected: chr) -> bool:
        # combines peek with advance
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

