import os

from .validationerror import ValidationError
from .intvalidator import IntValidator
from .floatvalidator import FloatValidator
from .strvalidator import StrValidator
from .pathvalidator import PathValidator
from .listvalidator import ListValidator
from .functions import either


class ValidateThat:
    def __init__(self, var, name='"Untitled var"'):
        # type: (ValidateThat, ..., str) -> None
        if not isinstance(name, str):
            raise TypeError('Name must be an instance of {} but is {}'.format(str, type(name)))
        self.__var__ = var
        self.__var_name__ = name

    def is_float(self):
        # type: (ValidateThat) -> FloatValidator
        either(
            lambda: self.is_of_type(float),
            lambda: self.is_of_type(int)
        )
        return FloatValidator(float(self.__var__), name=self.__var_name__)

    def is_int(self):
        # type: (ValidateThat) -> IntValidator
        self.is_of_type(int)
        return IntValidator(self.__var__, name=self.__var_name__)

    def is_str(self):
        # type: (ValidateThat) -> StrValidator
        self.is_of_type(str)
        return StrValidator(self.__var__, name=self.__var_name__)

    def is_existing_path(self):
        # type: (ValidateThat) -> PathValidator
        if (not isinstance(self.__var__, str)) or (not os.path.exists(self.__var__)):
            raise ValidationError('{} must be an existing path but is {}'
                                  .format(self.__var_name__, self.__var__))
        return PathValidator(self.__var__, name=self.__var_name__)

    def is_none(self):
        # type: (ValidateThat) -> None
        if self.__var__ is not None:
            raise ValidationError('{} must be None but is {}'.format(self.__var_name__, self.__var__))

    def is_of_type(self, _type):
        # type: (ValidateThat, type) -> None
        if not isinstance(self.__var__, _type):
            raise ValidationError('{} must be an instance of {} but is {}'
                                  .format(self.__var_name__, _type, type(self.__var__)))

    def is_list(self):
        # type: (ValidateThat)->ListValidator
        self.is_of_type(list)
        return ListValidator(self.__var__, name=self.__var_name__)

    def casts_to_int(self):
        # type: (ValidateThat)->IntValidator
        try:
            int_var = int(self.__var__)
            return IntValidator(int_var, self.__var_name__)
        except ValueError:
            raise ValidationError('{} must be castable to int but is not: {}'.format(self.__var_name__, self.__var__))

    def casts_to_float(self):
        # type: (ValidateThat)->FloatValidator
        try:
            float_var = float(self.__var__)
            return FloatValidator(float_var, self.__var_name__)
        except ValueError:
            raise ValidationError('{} must be castable to float but is not: {}'.format(self.__var_name__, self.__var__))
