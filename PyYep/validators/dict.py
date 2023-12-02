from typing import Dict, Any, TypeVar
from PyYep.validators.validator import Validator
from PyYep.exceptions import ValidationError
from PyYep.utils.decorators import validatorMethod


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
            validator.input_._input.set_value(value.get(key))

            try:
                validator.verify()
            except ValidationError as error:
                erros.append(error)

        if erros:
            raise ValidationError(
                f"{self.name}.{key}", "Internal validation erros", erros
            )

    def verify(self) -> dict:
        """
        Get the validator's input value, verify if its a dict
        and pass it to the input verify method

        Raises
        ----------
        ValidationError:
                if the received value is not a dict

        Returns
        -------
        result (dict): The value returned by the input verify method
        """

        result = self.getInputValue()

        if not isinstance(result, dict):
            raise ValidationError(
                self.name, "Invalid value received, expected a dictionary"
            )

        return self.input_.verify(result)
