import re
import decimal
from typing import Any
from .exceptions import ValidationError


class Validator():
	def __init__(self, input_: 'InputItem') -> None:
		self.input_ = input_
		self.name = input_.name

	def _set_parent_form(self, form: 'Schema') -> None:
		self.input_.form = form

	def required(self) -> 'Validator':
		self.input_ = self.input_.validate(self._required)
		return self

	def _required(self, value: Any):
		if value is None or (not value and value != 0):
			raise ValidationError(self.name, 'Empty value passed to a required input')


class StringValidator(Validator):
	def email(self) -> 'StringValidator':
		self.input_ = self.input_.validate(self._email)
		return self

	def _email(self, value: str) -> 'StringValidator':
		if re.fullmatch(r'[^@]+@[^@]+\.[^@]+', value) is None:
			raise ValidationError(self.name, 'Value for email type does not match a valid format')

	def min(self, value: int) -> 'StringValidator':
		self.input_ = self.input_.validate(lambda v: self._min(value, v))
		return self

	def _min(self, min: int, value: str) -> 'StringValidator':
		if len(value) < min:
			raise ValidationError(self.name, 'Value too short received')

	def max(self, value: int) -> 'StringValidator':
		self.input_ = self.input_.validate(lambda v: self._max(value, v))
		return self

	def _max(self, max: int, value: str) -> 'StringValidator':
		if len(value) > max:
			raise ValidationError(self.name, 'Value too long received')

	def verify(self) -> dict:
		result = getattr(self.input_._input, self.input_._path)

		if callable(result):
			result = result()

		if result is not None:
			result = str(result)

		return self.input_.verify(result)


class NumericValidator(Validator):
	def min(self, value: int) -> 'NumericValidator':
		self.input_ = self.input_.validate(lambda v: self._min(value, v))
		return self

	def _min(self, min: int, value: str) -> 'NumericValidator':
		if value < min:
			raise ValidationError(self.name, 'Value too small received')

	def max(self, value: int) -> 'NumericValidator':
		self.input_ = self.input_.validate(lambda v: self._max(value, v))
		return self

	def _max(self, max: int, value: str) -> 'NumericValidator':
		if value > max:
			raise ValidationError(self.name, 'Value too large received')

	def verify(self) -> dict:
		result = getattr(self.input_._input, self.input_._path)

		if callable(result):
			result = result()

		try:
			value = decimal.Decimal(result)
		except decimal.InvalidOperation:
			raise ValidationError(self.name, 'Non-numeric value received in a numeric input')

		return self.input_.verify(value)
