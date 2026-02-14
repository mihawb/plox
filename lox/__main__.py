import sys
from .lox import Lox


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
    try:
        main()
    except KeyboardInterrupt:
        print("", end="\r")
