from __future__ import annotations
from typing import Dict, Any, TypeGuard, TypeVar, TypedDict
import PyYep
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validator_method, ProxyContainer


ShapeValidatorT = TypeVar("ShapeValidatorT", bound=Validator)
T = TypeVar("T", bound=TypedDict)


class DictValidator(Validator[T]):
    @validator_method
    def shape(self, schema: Dict[Any, ShapeValidatorT], value: T) -> None:
        """
        Validate the items of a dict

        Parameters
        ----------
        value : (Dict[Any, Any])
                the dict that will be checked
        schema : (Dict[Any, Validator])
                the validators used to check the dict items

        Raises
        ----------
        ValidationError:
                if any of the items fails validation

        Returns
        ________
        validator (DictValidator):
                the validator being used
        """

        errors = []

        for key in schema:
            validator = schema[key]

            if validator.input_item is None:
                raise AttributeError(
                    "It's not possible to set a schema of a validator "
                    "before setting an input_item."
                )

            if not is_valid_data_container(
                validator.input_item.data_container
            ):
                raise TypeError(
                    "Inplicit schemas require the usage of ProxyContainer "
                    "as data_container"
                )

            validator.input_item.data_container.set_value(value.get(key))

            try:
                validator.verify()
            except ValidationError as error:
                format_error_path(self.name, key, error)

                if not error.inner:
                    errors.append(error)
                else:
                    errors.extend(error.inner)

        if errors:
            raise ValidationError("", "Internal validation errors", errors)

    def verify(self, data: T | None = None) -> T:
        """
        Get the validator's input value, verify if its a dict
        and pass it to the input verify method

        Parameters
        ----------
        value(Optional) : (Dict[Any, Any])
                the dict that will be checked, this parameter must only be
                passed when not using the Schema and InputItem objects

        Raises
        ----------
        ValidationError:
                if the received value is not a dict

        Returns
        -------
        result (dict): The value returned by the input verify method
        """

        if self.input_item is None:
            proxy_container = ProxyContainer()
            proxy_container.set_value(data)
            self.set_input_item(
                PyYep.InputItem("", proxy_container, "get_value")
            )
        elif data is not None:
            proxy_container = ProxyContainer()
            proxy_container.set_value(data)
            self.input_item.set_data_container(
                "", proxy_container, "get_value"
            )

        result = self.get_input_item_value()

        if not isinstance(result, dict):
            raise ValidationError(
                self.name, "Invalid value received, expected a dictionary"
            )

        if self.input_item is None:
            raise AttributeError(
                "It's not possible to set a schema of a validator "
                "before setting an input_item."
            )

        return self.input_item.verify(result)


def is_valid_data_container(x: object) -> TypeGuard[ProxyContainer]:
    return hasattr(x, "set_value")


def format_error_path(base: str, key: str, error: ValidationError) -> None:
    message = ""

    if base:
        message += base + "."

    message += key

    if not error.inner:
        error.path = message
        return

    for e in error.inner:
        e.path = f"{message}.{e.path}"
