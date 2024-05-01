from typing import Any
from lox import Lox as LoxImpl
from tokens import TokenType, Token, KEYWORDS


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens: list[Token] = []

        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
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
                elif self.match_next("*"):
                    self.c_comment()
                else:
                    self.add_token(TokenType.SLASH)

            # whitespaces
            case " ": pass
            case "\r": pass
            case "\t": pass
            case "\n": self.line += 1

            case "\"": self.string_literal()

            case _:
                if c.isdigit():
                    self.number_literal()
                elif c.isalpha():
                    self.identifier()
                else:
                    print(f'"{c}"')
                    LoxImpl.error(self.line, "Unexpected character.")

    def add_token(self, token_type: TokenType, literal: Any = None) -> None:
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def advance(self) -> str:
        consumed_char = self.source[self.current]
        self.current += 1
        return consumed_char

    def peek(self, lookahead: int = 0) -> str:
        # performs *lookahead*, lookahead is actually greater by 1 since current points to next unconsumed character
        # Lox's scanner looks ahead at most 2 characters
        if self.current + lookahead >= len(self.source):
            return "\0"
        return self.source[self.current + lookahead]

    def match_next(self, expected: str) -> bool:
        # combines peek with advance
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def c_comment(self):
        while not ((p := self.peek()) == "*" and self.peek(lookahead=1) == "/") and not self.is_at_end():
            if p == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            LoxImpl.error(self.line, "Unterminated C-style comment.")
            return

        self.advance()
        self.advance()  # closing */

    def string_literal(self) -> None:
        while (p := self.peek()) != "\"" and not self.is_at_end():
            if p == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            LoxImpl.error(self.line, "Unterminated string.")
            return

        self.advance()  # closing quote

        literal = self.source[self.start + 1:self.current - 1]  # trimming quotes
        self.add_token(TokenType.STRING, literal)

    def number_literal(self) -> None:
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek(lookahead=1).isdigit():
            self.advance()  # consume the dot

        while self.peek().isdigit():
            self.advance()

        literal = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, literal)

    def identifier(self) -> None:
        while self.peek().isalnum():
            self.advance()

        identifier = self.source[self.start:self.current]
        token_type = KEYWORDS.get(identifier, TokenType.IDENTIFIER)
        self.add_token(token_type, identifier)
