from typing import Any, List, Optional, Callable
from .validators import StringValidator, NumericValidator
from .exceptions import ValidationError


class Schema():
	'''
	Object responsable for storing the schema of a form
	'''
	def __init__(self, inputs: List['InputItem'],
		on_fail: Optional[Callable[[], None]] = None, abort_early: Optional[int] = True) -> None:
		for item in inputs:
			item._set_parent_form(self)

		self._inputs = inputs
		self.on_fail = on_fail
		self.abort_early = abort_early

	def validate(self) -> dict:
		result = {}
		errors = []

		for item in self._inputs:
			try:
				result[item.name] = item.verify()
			except ValidationError as error:
				if self.abort_early:
					raise error

				errors.append(error)

		if not self.abort_early and errors:
			raise ValidationError('', 'One or more inputs failed during validation', inner=errors)

		return result
	

class InputItem():
	def __init__(self, name: str, input_: Any, path: str,
		on_fail: Optional[Callable[[], None]] = None):
		self.name = name
		self._form = None
		self._input = input_
		self._path = path

		self._validators = []
		self.on_fail = on_fail

	def _set_parent_form(self, form: Schema) -> None:
		self.form = form

	def verify(self, result: Optional[Any] = None) -> None:
		if result is None:
			result = getattr(self._input, self._path)

		if callable(result):
			result = result()

		for validator in self._validators:
			try:
				validator(result)
			except ValidationError as error:
				if self.on_fail is not None:
					self.on_fail()
				elif self.form.on_fail is not None:
					self.form.on_fail()

				raise error

		return result

	def validate(self, validator: Callable[[Any], None]) -> 'InputItem':
		self._validators.append(validator)
		return self

	def string(self) -> StringValidator:
		return StringValidator(self)

	def number(self) -> NumericValidator:
		return NumericValidator(self)
