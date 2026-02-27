from .tokens import Token
from abc import abstractmethod


class LoxError(Exception):
	@abstractmethod
	def report(self) -> None:
		pass


class LoxScannerError(LoxError):
	def __init__(self, line: int, message: str) -> None:
		super().__init__(message)
		self.line = line
		self.message = message

	def report(self) -> None:
		print(f"[Line {self.line}] {self.__class__.__name__}: {self.message}")
		from .lox import LoxImpl
		LoxImpl.had_error = True


class LoxParseError(Exception):
    pass


class LoxRuntimeError(Exception):
	def __init__(self, token: Token, message: str) -> None:
		super().__init__(message)
		self.token = token
		self.message = message
