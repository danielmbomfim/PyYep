import re
from PyYep.exceptions import ValidationError


class DocumentsValidators:
    """
    A class to represent group document validators methods.

    ...

    Methods
    -------
    cnpj(value):
            Verify if the received value is a valid cnpj

    cpf(value):
            Verify if the received value is a valid cpf
    """

    def cnpj(self, value: str) -> None:
        """
        Verify if the received value is a valid cnpj

        Parameters
        ----------
        value : (str)
                the value that will be checked

        Raises
        ----------
        ValidationError:
                if the value is not a valid cnpj

        Returns
        ________
        None
        """

        if re.fullmatch(r"(^\d{2}.\d{3}.\d{3}/\d{4}-\d{2}$)", value) is None:
            raise ValidationError(
                "", "Value for CNPJ type does not match a valid format"
            )

        value = re.sub(r"[^0-9]", "", value)

        if len(set([*value])) == 1:
            raise ValidationError("", "Invalid CNPJ received")

        bases = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        f_result = 0
        s_result = 0

        for index, element in enumerate(value):
            if index == 12:
                break

            f_result += int(element) * bases[index + 1]

        if f_result % 11 < 2 and int(value[-2]) != 0:
            raise ValidationError("", "CNPJ value does not pass validation")
        elif 11 - (f_result % 11) != int(value[-2]):
            raise ValidationError("", "CNPJ value does not pass validation")

        for index, element in enumerate(value):
            if index == 13:
                break

            s_result += int(element) * bases[index]

        if s_result % 11 < 2 and int(value[-1]) != 0:
            raise ValidationError("", "CNPJ value does not pass validation")
        elif 11 - (s_result % 11) != int(value[-1]):
            raise ValidationError("", "CNPJ value does not pass validation")

    def cpf(self, value: str) -> None:
        """
        Verify if the received value is a valid cpf

        Parameters
        ----------
        value : (str)
                the value that will be checked

        Raises
        ----------
        ValidationError:
                if the value is not a valid cpf

        Returns
        ________
        None
        """

        if re.fullmatch(r"(^\d{3}\x2E\d{3}\x2E\d{3}\x2D\d{2}$)", value) is None:
            raise ValidationError(
                "", "Value for CPF type does not match a valid format"
            )

        value = re.sub(r"[^0-9]", "", value)

        if len(set([*value])) == 1:
            raise ValidationError("", "Invalid CPF received")

        f_result = 0
        s_result = 0

        for index, element in enumerate(value):
            if 10 - index == 1:
                break

            f_result += int(element) * (10 - index)

        if (f_result * 10) % 11 != int(value[-2]):
            raise ValidationError("", "CPF value does not pass validation")

        for index, element in enumerate(value):
            if 11 - index == 1:
                break

            s_result += int(element) * (11 - index)

        if (s_result * 10) % 11 != int(value[-1]):
            raise ValidationError("", "CPF value does not pass validation")
