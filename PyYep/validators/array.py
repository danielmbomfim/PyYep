from typing import Any, TypeVar, TypeGuard
from collections.abc import Sequence
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import ProxyContainer, validator_method


T = TypeVar("T", bound=Sequence)


class ArrayValidator(Validator[T]):
    """
    A class to represent a Array validator, children of Validator.

    ...

    Methods
    ----------
    len(size, value):
        verify if the size of the received list is equal to size

    min(min, value):
        Verify if the size of the received list is equal or higher than the min

    max(max, value):
        Verify if the size of the received list is equal or lower than the max

    verify():
        Get the validator's input value. If the value is not None converts
        it to a string and pass it to the input verify method
    """

    @validator_method
    def of(self, validator: Validator, value: Sequence) -> None:
        """
        Validate the items of a list

        Parameters
        ----------
        value : (Sequence)
            the list that will be checked
        validator : (Validator)
            the validation used to check the list items

        Raises
        ----------
        ValidationError:
            if any of the items fails validation

        Returns
        ----------
        None
        """

        if validator.input_item is None:
            raise AttributeError(
                "It's not possible to set a schema of a validator "
                "before setting an input_item."
            )

        errors = []

        for index, item in enumerate(value):
            if not is_valid_data_container(
                validator.input_item.data_container
            ):
                raise TypeError(
                    "Inplicit schemas require the usage "
                    "of ProxyContainer as data_container"
                )

            validator.input_item.data_container.set_value(item)

            try:
                validator.verify()
            except ValidationError as error:
                format_error_path(self.name, index, error)

                if not error.inner:
                    errors.append(error)
                else:
                    errors.extend(error.inner)

        if errors:
            raise ValidationError("", "Internal validation erros", errors)

    @validator_method
    def len(self, size: int, value: Sequence) -> None:
        """
        Verify if size of the received list

        Parameters
        ----------
        value : (Sequence)
            the list that will be checked
        size : (int)
            the expected size of the list

        Raises
        ----------
        ValidationError:
            if the size of the list is not equal to the expected

        Returns
        ----------
        None
        """

        if len(value) != size:
            raise ValidationError(
                self.name,
                f"Invalid size, expected the list to have {size} items",
            )

    @validator_method
    def min(self, min: int, value: Sequence) -> None:
        """
        Verify if size of the received list is equal or higher than the min

        Parameters
        ----------
        value : Sequence
            the list that will be checked
        min : (int)
            the minimun length allowed

        Raises
        ----------
        ValidationError:
            if the length is smaller than the min

        Returns
        ----------
        None
        """

        if len(value) < min:
            raise ValidationError(
                self.name,
                "received list is to small, expected a minimum of"
                f" {min} items",
            )

    @validator_method
    def max(self, max: int, value: Sequence) -> None:
        """
        Verify if the size of the received list is equal or lower than the max

        Parameters
        ----------
        value : (Sequence)
            the list that will be checked
        max : (int)
            the maximun length allowed

        Raises
        ----------
        ValidationError:
            if the length is larger than the max

        Returns
        ----------
        None
        """

        if len(value) > max:
            raise ValidationError(self.name, "Value too large received")

    @validator_method
    def includes(self, item: Any, value: Sequence) -> None:
        """
        Verify if iterable contains a given item

        Parameters
        ----------
        value : (Sequence)
            the list that will be checked
        item : (int)
            the value expected to be found on the iterable

        Raises
        ----------
        ValidationError:
            if the item is not contained on the value

        Returns
        ----------
        None
        """

        if item not in value:
            raise ValidationError(
                self.name, f"Value '{item}' not included on iterable"
            )

    def verify(self) -> Sequence | None:
        """
        Get the validator's input value, verify if its a sequence and pass
        it to the input verify method

        Raises
        ----------
        ValidationError:
            if the received value is not a list

        Returns
        ----------
        result (Sequence):
            the value returned by the input
        """

        result = self.get_input_item_value()

        if not isinstance(result, Sequence):
            raise ValidationError(
                self.name, "Invalid value received, expected an iterable"
            )

        if self.input_item is None:
            raise AttributeError(
                "It's not possible to set a schema of a validator "
                "before setting an input_item."
            )

        return self.input_item.verify(result)


def is_valid_data_container(x: object) -> TypeGuard[ProxyContainer]:
    return hasattr(x, "set_value")


def format_error_path(base: str, index: int, error: ValidationError) -> None:
    message = ""

    if base:
        message += base
    else:
        message += "_PyYepBlank"

    message += f"[{index}]"

    if not error.inner:
        error.path = message
        return

    for e in error.inner:
        e.path = f"{message}.{e.path}"
