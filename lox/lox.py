import sys
from .tokens import Token, TokenType
from .scanner import Scanner
from .parser import Parser
from .ast_printer import pprint_expr


class Lox:
    # shamelessly using shared metaclass fields to store state without instance initialization
    # yes I do know what I'm doing, ask me about it in the interview
    had_error = False

    @staticmethod
    def lexer_error(line: int, message: str) -> None:
        Lox.report(line, "", message)

    @staticmethod
    def parser_error(token: Token, message: str) -> None:
        if token.token_type == TokenType.EOF:
            Lox.report(token.line, "at end", message)
        else:
            Lox.report(token.line, f"at '{token.lexeme}'", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        Lox.had_error = True

    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if Lox.had_error:
            return

        print(pprint_expr(expression))
        # REPL input: -123 * (45.67 + 8.901)
        # REPL output: (* (- 123.0) (group (+ 45.67 8.901)))

        # REPL input: 1 == 2 ? 45 : -123 * (45.67 + 8.901)
        # REPL output: (if (== 1.0 2.0) then 45.0 else (* (- 123.0) (group (+ 45.67 8.901))))

    @staticmethod
    def run_file(file_path: str) -> None:
        with open(file_path, "r") as file:
            Lox.run(file.read())

        if Lox.had_error:
            sys.exit(65)

    @staticmethod
    def run_prompt() -> None:
        while True:
            line = input("> ")
            if not line:
                break
            Lox.run(line)
            Lox.had_error = False
