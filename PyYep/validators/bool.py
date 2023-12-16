from typing import TypeVar, cast
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validator_method


T = TypeVar("T", bound=bool)


class BooleanValidator(Validator[T]):
    """
    A class to represent a Boolean validator, children of Validator.

    ...

    Methods
    -------
    to_be(expected_value, value):
        Verify if the received value is equal or higher than the min

    verify():
        Get the validator's input value.
        If the value is not None converts it to a string
        and pass it to the input verify method
    """

    def __init__(self, strict: bool = False, *args):
        """
        Constructs a BooleanValidator object.

        Parameters
        ----------
            strict (bool): difines if the validator must raise erros
            if the received values is not a boolean
        """
        super().__init__(*args)
        self.strict = strict

    @validator_method
    def to_be(self, expected_value: bool, value: bool) -> None:
        """
        Verify if the received value is equal to expected

        Parameters
        ----------
        value : (bool)
            the value that will be checked
        expected_value : (bool)
            the expected value

        Raises
        ----------
        ValidationError:
            if the value does not equal to expected

        Returns
        ----------
        None
        """

        if value is not expected_value:
            raise ValidationError(
                self.name,
                f"{value} received on a boolean validator expecting"
                f" {expected_value}",
            )

    def verify(self) -> T | None:
        """
        Get the validator's input value, converts it to a boolean
        and pass it to the input verify method

        Raises
        ----------
        ValidationError:
            if the conversion operation to boolean is invalid

        Returns
        ----------
        result (bool): The value returned by the input verify method
        """

        result = self.get_input_item_value()

        if self.strict and not isinstance(result, bool):
            raise ValidationError(
                self.name,
                "Non-boolean value received in a strict boolean input",
            )

        if self.input_item is None:
            raise AttributeError(
                "It's not possible to set a schema of a validator "
                "before setting an input_item."
            )

        result = bool(result)
        result = cast(T, result)

        return self.input_item.verify(result)
