from typing import Dict, Any, Optional, TypeVar
import PyYep
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validatorMethod, ProxyContainer


ShapeValidatorT = TypeVar("ShapeValidatorT", bound=Validator)


class DictValidator(Validator):
    @validatorMethod
    def shape(
        self, schema: Dict[Any, ShapeValidatorT], value: Dict[Any, Any]
    ) -> "DictValidator":
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

        erros = []

        for key in schema:
            validator = schema[key]
            validator.input_item.data_container.set_value(value.get(key))

            try:
                validator.verify()
            except ValidationError as error:
                erros.append(error)

        if erros:
            raise ValidationError(
                f"{self.name}.{key}", "Internal validation erros", erros
            )

    def verify(self, data: Optional[Dict[Any, Any]] = None) -> dict:
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

        return self.input_item.verify(result)
