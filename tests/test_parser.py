import pytest

from lox.parser import Parser, ParseError
from lox.tokens import Token, TokenType as TT
from lox.expressions import Conditional, Literal
from lox.lox import Lox as LoxImpl


def mk_ts(tts: list[TT]) -> list[Token]:
	return [Token(tt, tt.value, "", 1) for tt in tts] + [Token(TT.EOF, "", "", 1)]


def test_conditional() -> None:
	ts = mk_ts([TT.TRUE, TT.QUESTION, TT.STRING, TT.COLON, TT.STRING])
	parser = Parser(ts)
	parsed_expr = parser.parse()

	expected_expr = Conditional(
		condition=Literal(True),
		then_branch=Literal(""),
		else_branch=Literal(""),
	)

	assert parsed_expr == expected_expr, "Parsing conditional expression failed"

def test_conditional_missing_colon() -> None:
	ts = mk_ts([TT.TRUE, TT.QUESTION, TT.STRING, TT.STRING])
	
	parser = Parser(ts)
	with pytest.raises(ParseError) as exc_info:
		_cond_parser_pass = parser.conditional()

	parser = Parser(ts)
	full_parser_pass = parser.parse()

	assert LoxImpl.had_error, "Missing colon in conditional should report an error"
	assert exc_info.type is ParseError, "On missing colon Conditional should panic and raise ParseError"
	assert full_parser_pass is None, "Parser.parse() should return None after encountering ParseError"
