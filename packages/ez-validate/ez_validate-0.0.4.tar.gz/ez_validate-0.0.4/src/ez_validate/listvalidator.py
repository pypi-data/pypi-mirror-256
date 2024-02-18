from .validatethat import ValidateThat
from .intvalidator import IntValidator
from .validationerror import ValidationError


class ListValidator:
    def __init__(self, var, name='"Untitled var"'):
        # type: (ListValidator, int, str) -> None
        if not isinstance(name, str):
            raise TypeError('Name must be an instance of {} but is {}'.format(str, type(name)))
        if not isinstance(var, list):
            raise TypeError('Variable must be an instance of {} but is {}'.format(list, type(var)))
        self.__var__ = var
        self.__var_name__ = name

    def of_types(self, _type):
        # type: (ListValidator, type) -> ListValidator
        for i, item in enumerate(self.__var__):
            ValidateThat(item, name='item {} of {}'.format(i, self.__var_name__)).is_of_type(_type)
        return self

    def of_length(self, length=None):
        # type: (ListValidator, int) -> IntValidator
        if length is None:
            return IntValidator(len(self.__var__), name='length of {}'.format(self.__var_name__))

        if not isinstance(length, int):
            raise TypeError('length must be an instance of {} but is {}'.format(int, type(length)))
        if length < 0:
            raise ValueError('length must be greater than or equal to 0 but is {}'.format(length))

        if len(self.__var__) != length:
            raise ValidationError('{} must be equal to {} but is {}'
                                  .format(self.__var_name__, length, self.__var__))
        return self
