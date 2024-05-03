import sys
from tokens import Token, TokenType
from scanner import Scanner


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
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, f"at '{token.lexeme}'", message)

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        Lox.had_error = True

    @staticmethod
    def run(source: str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

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


def main() -> None:
    match len(sys.argv):
        case 1:
            Lox.run_prompt()
        case 2:
            Lox.run_file(sys.argv[1])
        case _:
            print("Usage: plox [script]")
            sys.exit(64)


if __name__ == "__main__":
    main()
