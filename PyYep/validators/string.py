import re
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validatorMethod


class StringValidator(Validator):
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

    @validatorMethod
    def email(self, value: str) -> "StringValidator":
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

    @validatorMethod
    def min(self, min: int, value: str) -> "StringValidator":
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

    @validatorMethod
    def max(self, max: int, value: str) -> "StringValidator":
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

    def verify(self) -> dict:
        """
        Get the validator's input value.
        If the value is not None converts it to a string
        and pass it to the input verify method

        Returns
        -------
        result (str): The value returned by the input verify method
        """

        result = self.get_input_value()

        if result is not None:
            result = str(result)

        result = self.input_.verify(result)
        return result
