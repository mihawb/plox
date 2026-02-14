import sys
import argparse
from enum import Enum
from pathlib import Path

from .ast_generator import generate_ast_module


class __Mode(Enum):
	AST_GEN = "ast_gen"


def __parse_params() -> argparse.Namespace:
	parser = argparse.ArgumentParser()

	parser.add_argument("mode", type=__Mode, )

	# AST_GEN mode params
	# TODO (1): AST generator operating on assets/lox.gram
	# parser.add_argument("--gram", type=Path, help="Grammar definition file")
	parser.add_argument("--lox_root", type=Path, help="Lox root directory to insert with expressions module", default=Path("lox"))

	params = parser.parse_args()
	return params


def main() -> None:
	p = __parse_params()

	match p.mode:
		case __Mode.AST_GEN:
			# TODO (1): grammar def file as `gram` parameter here
			generate_ast_module(lox_root=p.lox_root)
		case _:
			print(f"No implemetation for mode {p.mode}")


if __name__ == "__main__":
	main()
