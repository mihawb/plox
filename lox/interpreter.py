from typing import Any
from .tokens import Token, TokenType as TT
from .expressions import Expr, Literal, Grouping, Unary, Binary, Conditional
from .errors import LoxRuntimeError


def test_truthiness(obj: Any) -> bool:
	# Ruby's definition of truthiness: ONLY `false` and `nil` are falsey
	if obj is None or isinstance(obj, bool) and not obj:
		return False
	return True


def __test_equlity(a: Any, b: Any) -> bool:
	# Lox's equality is identical to Python's
	if a is None and b is None:
		return True
	elif a is None:
		return False
	else:
		return a == b
	

def stringify(value: Any) -> str:
	if value is None:
		return "nil"
	
	if isinstance(value, float):
		res = str(value)
		res = res[:-2] if res[-2:] == ".0" else res
		return res
	
	return str(value)
	

def assert_numeric_operands(operator: Token, *operands: Any) -> None:
	ops = "Operand" + "s" if len(operands) > 1 else ""

	assertion = all(isinstance(op, float) for op in operands)
	if not assertion:
		raise LoxRuntimeError(operator, f"{ops} must be numeric")



def evaluate_binary_expr(bin_expr: Binary) -> Any:
	left = evaluate(bin_expr.left)
	right = evaluate(bin_expr.right)

	match tt := bin_expr.operator.token_type:
		case TT.MINUS:
			assert_numeric_operands(tt, left, right)
			return float(left) - float(right)
		case TT.PLUS:
			if isinstance(left, float) and isinstance(right, float):
				return float(left) + float(right)
			if isinstance(left, str) and isinstance(right, str):
				return str(left) + str(right)
			
			raise LoxRuntimeError(bin_expr.operator, "Operands must be two numbers or two strings.")


		case TT.SLASH:
			assert_numeric_operands(tt, left, right)
			return float(left) / float(right)
		case TT.STAR:
			assert_numeric_operands(tt, left, right)
			return float(left) * float(right)
		
		case TT.GREATER:
			assert_numeric_operands(tt, left, right)
			return float(left) > float(right)
		case TT.GREATER_EQUAL:
			assert_numeric_operands(tt, left, right)
			return float(left) >= float(right)
		case TT.LESS:
			assert_numeric_operands(tt, left, right)
			return float(left) < float(right)
		case TT.LESS_EQUAL:
			assert_numeric_operands(tt, left, right)
			return float(left) <= float(right)
		
		case TT.EQUAL_EQUAL:
			return left == right
		case TT.BANG_EQUAL:
			return left != right
		
		case _:
			raise NotImplementedError(f"Invalid operator for Binary expression: {tt}")



def evaluate(expr: Expr) -> Any:
	match expr:

		case Literal() as l:
			return l.value
		
		case Grouping() as g:
			return evaluate(g.expression)
		
		case Unary(operator=Token(token_type=TT.MINUS)) as u:
			right = evaluate(u.right)
			assert_numeric_operands(u.operator, right)
			return -float(right)
		
		case Unary(operator=Token(token_type=TT.BANG)) as u:
			right = evaluate(u.right)
			return not test_truthiness(right)
		
		case Binary() as b:
			return evaluate_binary_expr(b)
		
		case Conditional() as c:
			cond = test_truthiness(evaluate(c.condition))

			res_branch = c.then_branch if cond else c.else_branch
			return evaluate(res_branch)
		
		case _:
			raise NotImplementedError(f"No evaluation for this type of expression: {type(expr)}")


def interpret(expr: Expr) -> None:
	try:
		value = evaluate(expr)
		print(stringify(value))
	except LoxRuntimeError as lre:
		from .lox import LoxImpl
		LoxImpl.runtime_error(lre)
