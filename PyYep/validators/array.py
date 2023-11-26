import collections
from typing import TypeVar
from collections.abc import Iterable
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validatorMethod


IterableValueT = TypeVar("IterableValueT")
ValidatorT = TypeVar("ValidatorT", bound=Validator)


class ArrayValidator(Validator):
    """
    A class to represent a Array validator, children of Validator.

    ...

    Methods
    -------
    len(size, value):
            verify if the size of the received list is equal to size

    min(min, value):
            Verify if the size of the received list is equal
            or higher than the min

    max(max, value):
            Verify if the size of the received list is equal
            or lower than the max

    verify():
            Get the validator's input value.
            If the value is not None converts it to a string
            and pass it to the input verify method
    """

    @validatorMethod
    def of(
        self, validator: ValidatorT, value: Iterable[IterableValueT]
    ) -> "ArrayValidator":
        """
        Validate the items of a list

        Parameters
        ----------
        value : (Iterable[IterableValueT])
                the list that will be checked
        validator : (Validator)
                the validation used to check the list items

        Raises
        ----------
        ValidationError:
                if any of the items fails validation

        Returns
        ________
        validator (ArrayValidator):
                the validator being used
        """

        for index, item in enumerate(value):
            validator.input_._input.set_value(item)
            validator.verify()

    @validatorMethod
    def len(
        self, size: int, value: Iterable[IterableValueT]
    ) -> "ArrayValidator":
        """
        Verify if size of the received list

        Parameters
        ----------
        value : (Iterable[IterableValueT])
                the list that will be checked
        size : (int)
                the expected size of the list

        Raises
        ----------
        ValidationError:
                if the size of the list is not equal to the expected

        Returns
        ________
        validator (ArrayValidator):
                the validator being used
        """

        if len(value) != size:
            raise ValidationError(
                self.name,
                f"Invalid size, expected the list to have {size} items",
            )

    @validatorMethod
    def min(
        self, min: int, value: Iterable[IterableValueT]
    ) -> "ArrayValidator":
        """
        Verify if size of the received list is equal or higher than the min

        Parameters
        ----------
        value : (Iterable[IterableValueT])
                the list that will be checked
        min : (int)
                the minimun length allowed

        Raises
        ----------
        ValidationError:
                if the length is smaller than the min

        Returns
        ________
        validator (ArrayValidator):
                the validator being used
        """

        if len(value) < min:
            raise ValidationError(
                self.name,
                "received list is to small, expected a minimum of"
                f" {min} items",
            )

    @validatorMethod
    def max(
        self, max: int, value: Iterable[IterableValueT]
    ) -> "ArrayValidator":
        """
        Verify if the size of the received list is equal or lower than the max

        Parameters
        ----------
        value : (Iterable[IterableValueT])
                the list that will be checked
        max : (int)
                the maximun length allowed

        Raises
        ----------
        ValidationError:
                if the length is larger than the max

        Returns
        ________
        validator (ArrayValidator):
                the validator being used
        """

        if len(value) > max:
            raise ValidationError(self.name, "Value too large received")

    def verify(self) -> dict:
        """
        Get the validator's input value, verify if its a list
        and pass it to the input verify method

        Raises
        ----------
        ValidationError:
                if the received value is not a list

        Returns
        -------
        result (list): The value returned by the input verify method
        """

        result = self.getInputValue()

        if not isinstance(result, collections.abc.Sequence):
            raise ValidationError(
                self.name, "Invalid value received, expected an iterable"
            )

        return self.input_.verify(result)
