import sys
from .tokens import Token, TokenType
from .scanner import Scanner
from .parser import Parser
from .interpreter import LoxRuntimeError, interpret
from .ast_printer import pprint_expr


class LoxImpl:
    # shamelessly using shared metaclass fields to store state without instance initialization
    # yes I do know what I'm doing, ask me about it in the interview
    had_error = False
    had_runtime_error = False

    # TODO: move errors and reporting to separate module
    # @classmethod
    # def lexer_error(cls, line: int, message: str) -> None:
    #     cls.report(line, "", message)

    @staticmethod
    def parser_error(token: Token, message: str) -> None:
        if token.token_type == TokenType.EOF:
            LoxImpl.report(token.line, "at end", message)
        else:
            LoxImpl.report(token.line, f"at '{token.lexeme}'", message)

    @staticmethod
    def runtime_error(lre: LoxRuntimeError) -> None:
        print(f"LoxRuntimeError [line {lre.token.line}]: {lre.message}")
        LoxImpl.had_runtime_error = True

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        LoxImpl.had_error = True

    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if LoxImpl.had_error:
            return

        interpret(expression)


    @staticmethod
    def run_file(file_path: str) -> None:
        with open(file_path, "r") as file:
            LoxImpl.run(file.read())

        if LoxImpl.had_error:
            sys.exit(65)

        if LoxImpl.had_runtime_error:
            sys.exit(70)

    @staticmethod
    def run_prompt() -> None:
        while True:
            line = input("> ")
            if not line:
                break
            LoxImpl.run(line)
            LoxImpl.had_error = False
