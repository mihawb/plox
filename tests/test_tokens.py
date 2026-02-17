from lox.tokens import Token, TokenType


def test_str_repr() -> None:
	token = Token(TokenType.NUMBER, "123.456", 123.456, 67)

	t_str = str(token)
	t_repr = repr(token)

	expected = "Token(TokenType.NUMBER, lexeme='123.456', literal=123.456, line=67)"

	assert t_str == expected, "Invalid Token.__str__ method"
	assert t_repr == expected, "Invalid Token.__repr__ method"
