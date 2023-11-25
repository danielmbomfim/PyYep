import functools
from typing import Union, TYPE_CHECKING
import PyYep

if TYPE_CHECKING:
    from PyYep import InputValueT


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
    def wrapper(*args):
        """A wrapper function that appends a validator
        in the input's validators list

        Parameters
        ----------
        *args
            the positional orguments received by the wrapped method

        Returns
        -------
        args[0] (Type[Validator]): the self argument passed
        to the method being wrapped
        """

        if args[0].input_ is None:
            dummyInput = DummyInput()
            args[0].setInput(
                PyYep.InputItem("dummyInput", dummyInput, "get_value")
            )

        args[0].input_ = args[0].input_.validate(lambda v: func(*args, v))

        return args[0]

    return wrapper


class DummyInput:
    def __init__(self):
        self.value = None

    def get_value(self) -> Union["InputValueT", None]:
        return self.value

    def set_value(self, value: "InputValueT") -> "InputValueT":
        self.value = value
