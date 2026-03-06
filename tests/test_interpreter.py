import pytest
from lox.interpreter import evaluate
from lox.expressions import Unary, Literal
from lox.tokens import Token, TokenType as TT


def test_interpret_unary() -> None:
	neg_number = Unary(Token.empty(TT.MINUS), Literal(6.7))
	eval_res = evaluate(neg_number)
	assert eval_res == -6.7, "Numeric Unary interpreted incorrectly"

	neg_truth = Unary(Token.empty(TT.BANG), Literal(True))
	eval_res = evaluate(neg_truth)
	assert not eval_res, "Boolean Unary interpreted incorrectly"

	error_prod = Unary(Token.empty(TT.PLUS), Literal(6.7))
	with pytest.raises(NotImplementedError) as exc_info:
		eval_res = evaluate(error_prod)
	assert exc_info.type is NotImplementedError, "Error productions for Unary should throw on Parser step"
