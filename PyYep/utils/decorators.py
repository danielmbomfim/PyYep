from typing import Callable, Generic, TypeVar, TypeVarTuple, TYPE_CHECKING
import PyYep

if TYPE_CHECKING:
    from PyYep.validators.validator import Validator


ArgsT = TypeVarTuple("ArgsT")
T = TypeVar("T", bound="Validator")
V = TypeVar("V")


def validator_method(
    func: Callable[[T, *ArgsT, V], None]
) -> Callable[[T, *ArgsT], T]:
    """Wraps a Validator method to be used as a validator function

    Parameters
    ----------
    func : Callable
        the function that will be used as validator

    Returns
    ----------
    wrapper (Callable)
        the wrapper function of the decorator
    """

    def wrapper(validator: T, *args: *ArgsT) -> T:
        """A wrapper function that appends a validator
        in the input's validators list

        Parameters
        ----------
        validator
            the instance of validator using the decorator
        *args
            the positional arguments received by the wrapped method

        Returns
        ----------
        Validator:
            the instance of validator using the decorator
        """

        if validator.input_item is None:
            proxy_container = ProxyContainer()
            validator.set_input_item(
                PyYep.InputItem("", proxy_container, "get_value")
            )

        if validator.input_item is None:
            raise AttributeError(
                "It's not possible to use validation on a Validator "
                "without an input item."
            )

        validation_method: Callable[[V], None] = lambda v: func(
            validator, *args, v
        )
        validator.input_item = validator.input_item.validate(validation_method)

        return validator

    return wrapper


class ProxyContainer(Generic[V]):
    def __init__(self):
        self.value = None

    def get_value(self) -> V | None:
        return self.value

    def set_value(self, value: V) -> None:
        self.value = value
