from __future__ import annotations
from numbers import Number
from typing import TypeVar, cast
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validator_method


T = TypeVar("T", bound=float)


class NumericValidator(Validator[T]):
    """
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
            If the value is not None converts it to a string
            and pass it to the input verify method
    """

    @validator_method
    def min(self, min: int, value: T) -> None:
        """
        Verify if the received value is equal or higher than the min

        Parameters
        ----------
        value : (Decimal)
                the value that will be checked
        min : (int)
                the minimun value allowed

        Raises
        ----------
        ValidationError:
                if the value smaller than the min

        Returns
        ________
        validator (NumericValidator[T]):
                the validator being used
        """

        if value < min:
            raise ValidationError(self.name, "Value too small received")

    @validator_method
    def max(self, max: int, value: T) -> None:
        """
        Verify if the the received value is equal or lower than the max

        Parameters
        ----------
        value : (Decimal)
                the value that will be checked
        max : (int)
                the maximun length allowed

        Raises
        ----------
        ValidationError:
                if the value is larger than the max

        Returns
        ________
        validator (NumericValidator[T]):
                the validator being used
        """

        if value > max:
            raise ValidationError(self.name, "Value too large received")

    def verify(self) -> T | None:
        """
        Get the validator's input value, converts it to a Decimal
        and pass it to the input verify method

        Raises
        ----------
        ValidationError:
                if the conversion operation to Decimal is invalid

        Returns
        -------
        result (Decimal): The value returned by the input verify method
        """

        result = self.get_input_item_value()

        if not isinstance(result, Number):
            try:
                result = float(result)
                result = cast(T, result)
            except (TypeError, ValueError):
                raise ValidationError(
                    self.name, "Non-numeric value received in a numeric input"
                )

        if self.input_item is None:
            raise AttributeError(
                "It's not possible to use validation on a Validator "
                "without an input item."
            )

        return self.input_item.verify(result)
