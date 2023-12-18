import re
from typing import TypeVar, cast
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validator_method


T = TypeVar("T", bound=str)


class StringValidator(Validator[T]):
    """
    A class to represent a string validator, children of Validator.

    ...

    Methods
    -------
    email(value):
            Verify if the received value is a valid email address

    min(min, value):
            Verify if the length of the received value is equal
            or higher than the min

    max(max, value):
            Verify if the length of the received value is equal
            or lower than the max

    verify():
            Get the validator's input value.
            If the value is not None converts it to a string
            and pass it to the input verify method
    """

    @validator_method
    def email(self, value: str) -> None:
        """
        Verify if the received value is a valid email address

        Parameters
        ----------
        value : (str)
                the value that will be checked

        Raises
        ----------
        ValidationError:
                if the value is not a valid email address

        Returns
        ________
        validator (StringValidator):
                the validator being used
        """

        if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", value) is None:
            raise ValidationError(
                self.name, "Value for email type does not match a valid format"
            )

    @validator_method
    def min(self, min: int, value: T) -> None:
        """
        Verify if the length of the received value is equal
        or higher than the min

        Parameters
        ----------
        value : (str)
                the value that will be checked
        min : (int)
                the minimun length allowed

        Raises
        ----------
        ValidationError:
                if the value length is smaller than the min

        Returns
        ________
        validator (StringValidator):
                the validator being used
        """

        if len(value) < min:
            raise ValidationError(self.name, "Value too short received")

    @validator_method
    def max(self, max: int, value: T) -> None:
        """
        Verify if the length of the received value is equal
        or lower than the max

        Parameters
        ----------
        value : (str)
                the value that will be checked
        max : (int)
                the maximun length allowed

        Raises
        ----------
        ValidationError:
                if the value length is larger than the max

        Returns
        ________
        validator (StringValidator):
                the validator being used
        """

        if len(value) > max:
            raise ValidationError(self.name, "Value too long received")

    def verify(self) -> T | None:
        """
        Get the validator's input value.
        If the value is not None converts it to a string
        and pass it to the input verify method

        Returns
        -------
        result (str): The value returned by the input verify method
        """

        result = self.get_input_item_value()

        if result is not None:
            result = cast(T, str(result))

        if self.input_item is None:
            raise AttributeError(
                "It's not possible to use validation on a Validator "
                "without an input item."
            )

        result = self.input_item.verify(result)

        return result
