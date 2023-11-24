import decimal
from typing import Callable
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validatorMethod


class NumericValidator(Validator):
	'''
	A class to represent a Numeric validator, children of Validator.

	...

	Methods
	-------
	min(min, value):
		Verify if the received value is equal or higher than the min

	max(max, value):
		Verify if the received value is equal or lower than the max

	verify():
		Get the validator's input value.
		If the value is not None converts it to a string and pass it to the input verify method
	'''

	@validatorMethod
	def min(self, min: int, value: decimal.Decimal) -> None:
		'''
		Verify if the received value is equal or higher than the min

		Parameters
		----------
		value : (any)
			the value that will be checked
		min : (int)
			the minimun value allowed

		Raises
		----------
		ValidationError:
			if the value smaller than the min

		Returns
		________
		None
		'''

		if value < min:
			raise ValidationError(self.name, 'Value too small received')

	@validatorMethod
	def max(self, max: int, value: decimal.Decimal) -> None:
		'''
		Verify if the the received value is equal or lower than the max

		Parameters
		----------
		value : (any)
			the value that will be checked
		max : (int)
			the maximun length allowed

		Raises
		----------
		ValidationError:
			if the value is larger than the max

		Returns
		________
		None
		'''

		if value > max:
			raise ValidationError(self.name, 'Value too large received')

	def verify(self) -> dict:
		'''
		Get the validator's input value, converts it to a Decimal and pass it to the input verify method

		Raises
		----------
		ValidationError:
			if the conversion operation to Decimal is invalid

		Returns
		-------
		result (Decimal): The value returned by the input verify method
		'''

		result = getattr(self.input_._input, self.input_._path)

		if callable(result):
			result = result()

		try:
			value = decimal.Decimal(result)
		except decimal.InvalidOperation:
			raise ValidationError(self.name, 'Non-numeric value received in a numeric input')

		return self.input_.verify(value)