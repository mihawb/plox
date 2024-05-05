import sys

# istg I need to learn macros in Rust


NLNL = "\n\n"
TAB = "    "  # 4 spaces in lieu of \t

IMPORTS = [
    "from dataclasses import dataclass",
    "from typing import Any",
    "from tokens import Token",
]

EXPRS = [
    "Binary -> left: Expr, operator: Token, right: Expr",
    "Grouping -> expression: Expr",
    "Literal -> value: Any",
    "Unary -> operator: Token, right: Expr",
    "Conditional -> conditional: Expr, then_branch: Expr, else_branch: Expr"
]


def generate_expr_meta_dataclass(expr_def: str) -> str:
    class_name, fields = expr_def.split("->")
    class_name, fields = [s.strip() for s in [class_name, fields]]
    fields = [f.strip() for f in fields.split(",")]

    meta_class_def = "@dataclass\n" + f"class {class_name}(Expr):\n"
    for field in fields:
        meta_class_def += f"{TAB}{field}\n"

    return meta_class_def


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_ast.py <AST file path>")
        sys.exit(64)

    with open(sys.argv[1], "w") as ast_file:

        ast_file.writelines(map(lambda i: i + "\n", IMPORTS))
        ast_file.write(NLNL)
        ast_file.write(f"class Expr:\n{TAB}pass\n")

        for expr in EXPRS:
            ast_file.write(NLNL)
            meta_class_def = generate_expr_meta_dataclass(expr)
            ast_file.write(meta_class_def)
