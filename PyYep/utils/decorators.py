import functools
from typing import Union, TypeVar, TYPE_CHECKING
import PyYep

if TYPE_CHECKING:
    from PyYep import InputValueT
    from PyYep.validators.validator import Validator


T = TypeVar("T", bound="Validator")


def validatorMethod(func):
    """Wraps a Validator method to be used as a validator function

    Parameters
    ----------
    func : Callable
        the function that will be used as validator

    Returns
    -------
    wrapper (Callable)
        the wrapper function of the decorator
    """

    @functools.wraps(func)
    def wrapper(validator: T, *args):
        """A wrapper function that appends a validator
        in the input's validators list

        Parameters
        ----------
        validator
            the instance of validator using the decorator
        *args
            the positional arguments received by the wrapped method

        Returns
        -------
        validator Validator:
            the instance of validator using the decorator
        """

        if validator.input_ is None:
            dummyInput = DummyInput()
            validator.setInput(
                PyYep.InputItem("dummyInput", dummyInput, "get_value")
            )

        validator.input_ = validator.input_.validate(
            lambda v: func(validator, *args, v)
        )

        return validator

    return wrapper


class DummyInput:
    def __init__(self):
        self.value = None

    def get_value(self) -> Union["InputValueT", None]:
        return self.value

    def set_value(self, value: "InputValueT") -> "InputValueT":
        self.value = value
