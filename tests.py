import unittest
from unittest.mock import Mock
from PyYep import Schema, InputItem, ValidationError


class TestInputItem(unittest.TestCase):
	def test_validate(self):
		input_ = SimpleInput('test')

		def custom_validator(value):
			if value == 'test':
				return

			raise ValidationError('test', 'test')

		form = Schema([
			InputItem('test', input_, 'value').validate(custom_validator)
		])

		self.assertEqual(form.validate()['test'], 'test')

		input_.value = 'a'
		with self.assertRaises(ValidationError): form.validate()

	def test_hooks(self):
		local_success_hook = Mock(return_value='success')
		global_error_hook = Mock(return_value='global_error')
		local_error_hook = Mock(return_value='local_error')

		def custom_validator(_):
			raise ValidationError('test', '')

		form = Schema([
			InputItem('test', SimpleInput(''), 'value').validate(custom_validator),
			InputItem('test1', SimpleInput(''), 'value', on_fail=local_error_hook).validate(custom_validator),
			InputItem('test2', SimpleInput(''), 'value', on_success=local_success_hook)
		], global_error_hook, False)

		try:
			form.validate()
		except ValidationError:
			pass

		local_success_hook.assert_called_once()
		global_error_hook.assert_called_once()
		local_error_hook.assert_called_once()

	def test_not_aborting_early(self):
		def custom_validator(value):
			if value == 'test':
				return

			raise ValidationError('test', 'test')

		form = Schema([
			InputItem('a', SimpleInput(''), 'value').validate(custom_validator),
			InputItem('b', SimpleInput(''), 'value').validate(custom_validator)
		], abort_early=False)

		with self.assertRaises(ValidationError): form.validate()

		try:
			form.validate()
		except ValidationError as error:
			self.assertTrue(error.inner)

class TestStringValidator(unittest.TestCase):
	def test_required(self):
		input_ = SimpleInput('')
		form = Schema([
			InputItem('test', input_, 'value').string().required()
		])

		with self.assertRaises(ValidationError): form.validate()

		input_.value = None
		with self.assertRaises(ValidationError): form.validate()

	def test_email(self):
		input_ = SimpleInput('test@test.com')
		form = Schema([
			InputItem('email', input_, 'value').string().email()
		])
		self.assertEqual(form.validate()['email'], 'test@test.com')

		input_.value = 10
		with self.assertRaises(ValidationError): form.validate()

		input_.value = 'test'
		with self.assertRaises(ValidationError): form.validate()

		input_.value = 'test@test'
		with self.assertRaises(ValidationError): form.validate()

	def test_min_and_max(self):
		input_ = SimpleInput('12345')
		form = Schema([
			InputItem('test', input_, 'value').string().min(5).max(10)
		])

		self.assertEqual(form.validate()['test'], '12345')
		input_.value = '1234567890'
		self.assertEqual(form.validate()['test'], '1234567890')

		input_.value = '1234'
		with self.assertRaises(ValidationError): form.validate()

		input_.value = '1234567890+'
		with self.assertRaises(ValidationError): form.validate()


class TestNumberValidator(unittest.TestCase):
	def test_min_and_max(self):
		input_ = SimpleInput(5)
		form = Schema([
			InputItem('test', input_, 'value').number().min(5).max(10)
		])

		self.assertEqual(form.validate()['test'], 5)
		input_.value = 10
		self.assertEqual(form.validate()['test'], 10)

		input_.value = 4
		with self.assertRaises(ValidationError): form.validate()

		input_.value = 11
		with self.assertRaises(ValidationError): form.validate()


class SimpleInput():
	def __init__(self, value):
		self.value = value


if __name__ == '__main__':
    unittest.main()