from lox.tokens import Token, TokenType


def test_str_repr() -> None:
	token = Token(TokenType.NUMBER, "123.456", 123.456, 67)

	t_repr = repr(token)

	expected = "Token(TokenType.NUMBER, lexeme='123.456', literal=123.456, line=67)"

	assert expected == t_repr, "Invalid Token.__repr__ method"
	assert token == eval(t_repr), "Eval of repr should create the token"
	