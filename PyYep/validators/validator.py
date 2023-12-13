from abc import ABCMeta, abstractmethod
from typing import Optional, TYPE_CHECKING
from collections.abc import Iterable
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validatorMethod


if TYPE_CHECKING:
    from PyYep import InputItem, Schema, InputValueT


class Validator(metaclass=ABCMeta):
    """
    A class to represent a base validator.

    ...

    Attributes
    ----------
    input_item : InputItem
            the input that will be validated
    name : str
            the name of the input that will be validated

    Methods
    -------
    set_schema(form):
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

    def __init__(self, input_item: Optional["InputItem"] = None) -> None:
        """
        Constructs all the necessary attributes for the base validator object.

        Parameters
        ----------
                input_ (InputItem): the input that will be validated
        """

        self.input_item = None
        self.name = None

        if input_item is not None:
            self.input_item = input_item
            self.name = input_item.name

    def set_input_item(self, input_item: "InputItem"):
        """
        Sets the input_ property

        Parameters
        ----------
                input_ (InputItem): the input that will be validated
        """

        self.input_item = input_item
        self.name = input_item.name

    def get_input_item_value(self) -> "InputValueT":
        """
        Get the value of the input

        Returns
        -------
        InputValueT
        """

        result = getattr(self.input_item.data_container, self.input_item._path)

        if callable(result):
            result = result()

        return result

    def set_schema(self, form: "Schema") -> None:
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

        self.input_item.form = form

    @validatorMethod
    def required(self, value: "InputValueT") -> "Validator":
        """
        Verify if the received value is empty

        Parameters
        ----------
        value : (InputValueT)
                the value that will be checked

        Raises
        ----------
        ValidationError:
                if the value is empty or None

        Returns
        ________
        validator (Validator):
                the validator being used
        """

        if value is None or (not value and value != 0):
            raise ValidationError(
                self.name, "Empty value passed to a required input"
            )

    @validatorMethod
    def in_(
        self, data_structure: Iterable, value: "InputValueT"
    ) -> "Validator":
        """
        Verify if the received value is present in the received data structure

        Parameters
        ----------
        value : (InputValueT)
                the value that will be checked
        data_structure : (Iterable)
                a iterable in wich the received value is supposed to be present

        Raises
        ----------
        ValidationError:
                if the value is not present in the data structure

        Returns
        ________
        validator (Validator):
                the validator being used
        """

        if value not in data_structure:
            raise ValidationError(
                self.name, "Value not present in the received data structure"
            )

    @abstractmethod
    def verify(self):
        raise NotImplementedError
