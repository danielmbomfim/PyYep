from abc import ABC, abstractmethod
from typing import Any, Optional, TYPE_CHECKING
from collections.abc import Iterable
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validatorMethod


if TYPE_CHECKING:
    from .__init__ import InputItem, Schema


class Validator(ABC):
    """
    A class to represent a base validator.

    ...

    Attributes
    ----------
    input_ : any
            the input that will be validated
    name : str
            the name of the input that will be validated

    Methods
    -------
    _set_parent_form(form):
            Set the parent schema

    condition(condition):
            Set a condition for the execution of the previous validator

    modifier(modifier):
            Set a modifier to allow changes in the value after validation

    required(value):
            Verify if the received value is empty

    in_(data_structure, value):
            verifies the presence of a value into a data structure
    """

    def __init__(self, input_: Optional["InputItem"] = None) -> None:
        """
        Constructs all the necessary attributes for the base validator object.

        Parameters
        ----------
                input_ (InputItem): the input that will be validated
        """

        if input_ is not None:
            self.input_ = input_
            self.name = input_.name

    def setInput(self, input_: "InputItem"):
        """
        Sets the input_ property

        Parameters
        ----------
                input_ (InputItem): the input that will be validated
        """

        self.input_ = input_
        self.name = input_.name

    def getInputValue(self) -> Any:
        """
        Get the value of the input

        Returns
        -------
        Any
        """

        result = getattr(self.input_._input, self.input_._path)

        if callable(result):
            result = result()

        return result

    def _set_parent_form(self, form: "Schema") -> None:
        """
        Set the parent schema of the validator's input

        Parameters
        ----------
        form : Schema
                the validator's input parent schema

        Returns
        -------
        None
        """

        self.input_.form = form

    @validatorMethod
    def required(self, value: Any) -> None:
        """
        Verify if the received value is empty

        Parameters
        ----------
        value : (Any)
                the value that will be checked

        Raises
        ----------
        ValidationError:
                if the value is empty or None

        Returns
        ________
        None
        """

        if value is None or (not value and value != 0):
            raise ValidationError(
                self.name, "Empty value passed to a required input"
            )

    @validatorMethod
    def in_(self, data_structure: Iterable, value: Any):
        """
        Verify if the received value is present in the received data structure

        Parameters
        ----------
        value : (Any)
                the value that will be checked
        data_structure : (Iterable)
                a iterable in wich the received value is supposed to be present

        Raises
        ----------
        ValidationError:
                if the value is not present in the data structure

        Returns
        ________
        None
        """

        if value not in data_structure:
            raise ValidationError(
                self.name, "Value not present in the received data structure"
            )

    @abstractmethod
    def verify(self):
        raise NotImplementedError
