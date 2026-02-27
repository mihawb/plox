import sys
from .tokens import Token, TokenType
from .scanner import Scanner
from .parser import Parser
from .interpreter import interpret
from .ast_printer import pprint_expr


class LoxImpl:
    # shamelessly using shared metaclass fields to store state without instance initialization
    # yes I do know what I'm doing, ask me about it in the interview
    had_error = False
    had_runtime_error = False        

    @classmethod
    def run(cls, source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if cls.had_error:
            return

        interpret(expression)


    @classmethod
    def run_file(cls, file_path: str) -> None:
        with open(file_path, "r") as file:
            LoxImpl.run(file.read())

        if cls.had_error:
            sys.exit(65)

        if cls.had_runtime_error:
            sys.exit(70)

    @classmethod
    def run_prompt(cls) -> None:
        while True:
            line = input("> ")
            if not line:
                break
            cls.run(line)
            cls.had_error = False
