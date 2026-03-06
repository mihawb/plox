import sys
from .scanner import Scanner
from .parser import Parser
from .interpreter import interpret
from .ast_printer import pprint_expr
from .errors import LoxWatchdog


class LoxImpl:
    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if LoxWatchdog.had_static_error:
            return

        interpret(expression)


    @staticmethod
    def run_file(file_path: str) -> None:
        with open(file_path, "r") as file:
            LoxImpl.run(file.read())

        if LoxWatchdog.had_static_error:
            sys.exit(65)

        if LoxWatchdog.had_runtime_error:
            sys.exit(70)

    @classmethod
    def run_prompt(cls) -> None:
        while True:
            line = input("> ")
            if not line:
                break
            cls.run(line)
            LoxWatchdog.had_static_error = False
