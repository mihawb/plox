import pytest
from lox.lox import Lox as LoxImpl
from lox.scanner import Scanner
from lox.tokens import TokenType as TT


def test_inline_c_comment() -> None:
	source = "var x /* float */ = 3 + 2"
	expected = [TT.VAR, TT.IDENTIFIER, TT.EQUAL, TT.NUMBER, TT.PLUS, TT.NUMBER, TT.EOF]
	
	scanner = Scanner(source)
	tokens = scanner.scan_tokens()

	assert all(t.line == 1 for t in tokens), "Inline C-comment mustn't change line number"
	assert [t.token_type for t in tokens] == expected, "Inline C-comment scanned incorrectly"


def test_multiline_c_comment() -> None:
	source = f"idef /* {'\n' * 3} */ idef"

	scanner = Scanner(source)
	ts = scanner.scan_tokens()

	assert ts[0].line == 1 and ts[-1].line == 4, "Scanner counted lines incorrectly in multiline C-comment"
	

def test_unterminated_c_comment() -> None:
	source = "idef /* lorem ipsum"
	expected = [TT.IDENTIFIER, TT.EOF]

	scanner = Scanner(source)
	ts = scanner.scan_tokens()

	assert LoxImpl.had_error, "Scanner error went unreported to LoxImpl"
	assert [t.token_type for t in ts] == expected, "Unterminated C-comment didn't terminate scanning"

def test_unterminated_string() -> None:
	source = "idef \"lorem ipsum"
	expected = [TT.IDENTIFIER, TT.EOF]

	scanner = Scanner(source)
	ts = scanner.scan_tokens()

	assert LoxImpl.had_error, "Scanner error went unreported to LoxImpl"
	assert [t.token_type for t in ts] == expected, "Unterminated string literal didn't terminate scanning"
