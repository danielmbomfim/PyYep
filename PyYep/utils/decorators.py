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

        if validator.input_item is None:
            proxy_container = ProxyContainer()
            validator.set_input_item(
                PyYep.InputItem("", proxy_container, "get_value")
            )

        validator.input_item = validator.input_item.validate(
            lambda v: func(validator, *args, v)
        )

        return validator

    return wrapper


class ProxyContainer:
    def __init__(self):
        self.value = None

    def get_value(self) -> Union["InputValueT", None]:
        return self.value

    def set_value(self, value: "InputValueT") -> "InputValueT":
        self.value = value
